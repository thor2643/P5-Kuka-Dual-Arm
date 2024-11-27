# Import libraries
from openai import OpenAI
import ollama
import json
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import numpy as np
import readline
from threading import Event
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

# ROS 2 libraries and Node structure
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


# ROS 2 messages
from project_interfaces.srv import GetObjectInfo
from project_interfaces.srv import DefineObjectInfo
from project_interfaces.srv import PlanMoveCommand
from project_interfaces.srv import ExecuteMoveCommand
from project_interfaces.srv import PromptJanice
from project_interfaces.srv import GetCurrentPose
from robotiq_3f_gripper_ros2_interfaces.srv import Robotiq3FGripperOutputService
from robotiq_2f_85_interfaces.srv import Robotiq2F85GripperCommand

class LLMNode(Node):
    def __init__(self):
        super().__init__('minimal_client')

        client_cb_group = MutuallyExclusiveCallbackGroup()
        gui_service_cb_group = MutuallyExclusiveCallbackGroup()

        self.srv = self.create_service(
            PromptJanice, 'send_prompt', self.gui_handle_service, callback_group=gui_service_cb_group
        )
        self.get_logger().info('Service Server is ready.')

        # Gripper service client
        self._3f_controller = Robotiq3FGripperOutputService.Request()
        self._3f_controller_cli = self.create_client(Robotiq3FGripperOutputService, "Robotiq3FGripper/OutputRegistersService", callback_group=client_cb_group)

        self._2f_client = self.create_client(Robotiq2F85GripperCommand, 'gripper_2f_service', callback_group=client_cb_group)
        self._2f_req = Robotiq2F85GripperCommand.Request()

        #Object detector service client
        self.detector_client = self.create_client(GetObjectInfo, 'get_object_info', callback_group=client_cb_group)
        self.detector_req = GetObjectInfo.Request()
        self.objects_on_table = {}

        self.define_objects_client = self.create_client(DefineObjectInfo, 'define_object_info', callback_group=client_cb_group)
        self.define_objects_req = DefineObjectInfo.Request()

        self.detector_client_yolo = self.create_client(GetObjectInfo, 'get_object_info_yolo', callback_group=client_cb_group)
        self.detector_req_yolo = GetObjectInfo.Request()
        self.objects_on_table_yolo = {}

        # Robot service client
        self.robot_plan_client = self.create_client(PlanMoveCommand, 'plan_move_command', callback_group=client_cb_group)
        self.robot_plan_req = PlanMoveCommand.Request()

        self.robot_execute_client = self.create_client(ExecuteMoveCommand, 'execute_move_command', callback_group=client_cb_group)
        self.robot_execute_req = ExecuteMoveCommand.Request()

        self.robot_pose_client = self.create_client(GetCurrentPose, 'get_pose', callback_group=client_cb_group)
        self.robot_pose_req = GetCurrentPose.Request()

        # Specify a specific microphone if needed
        self.microphone_index = 8
        self.microphone_timeout = 10

        # Decide whether to use Ollama API or OpenAI API
        self.use_ollama = False

        # Attributes
        self.future = 0

        self.llm_loop = False

        self.object_file = 'src/robutler/object_detector/object_detector/lego_bricks_config.json'

        self.lego_bricks = {}

        with open(self.object_file, 'r') as file:
            self.lego_bricks = json.load(file)

        # Define the locations in the environment
        self.coordinates = { # Predefined poses for different locations
            'HOME': {'x': '0.3', 'y': '0.3', 'z': "0.3", 'roll': '0', 'pitch': '0', 'yaw': '0'}
        }

        # Load and define all functions available to models
        with open('src/robutler/janise/llm_functions_config.json') as f:
            function_definitions = json.load(f)
        self.tools = function_definitions

        self.available_functions = {
            'get_available_locations': self.get_available_locations,
            'get_pose_values_from_location': self.get_pose_values_from_location,
            'find_object': self.find_object,
            'get_available_objects': self.get_available_objects,
            'find_object_yolo': self.find_object_yolo,
            'define_object_thresholds': self.define_object_thresholds,
            'move_robot_to_pose': self.move_robot_to_pose,
            'plan_robot_trajectory': self.plan_robot_trajectory,
            'execute_planned_trajectory': self.execute_planned_trajectory,
            'manipulate_right_gripper': self.manipulate_right_gripper,
            'manipulate_left_gripper': self.manipulate_left_gripper,
            'get_current_pose': self.get_current_pose,
            'set_message_looping': self.set_message_looping
        }

        # Initialize Ollama client or OpenAI client with API key and optional project ID
        if self.use_ollama:
            self.client = ollama.Client()
        else:
            # load the project id and key from json file
            with open('src/robutler/janise/API_KEY.json') as f:
                api_data = json.load(f)
            API_KEY = api_data['API_KEY']
            self.client = OpenAI(api_key=API_KEY)

        self.message_buffer = [{"role": "system", "content": """
            Your name is Janise. You are an AI robotic arm assistant using the LLM gpt-4o for task reasoning and manipulation tasks. You are to assume the persona of a butler.

            Context for your Workspace:
            - You operate in a dual-arm robotic cell consisting of two collaborative KUKA iiwa 7 robots, each with 7 degrees of freedom (DoF). Both robots are mounted on a fixed frame positioned on top of a workbench, which provides a stable working surface.
            - The setup includes a left and right side, each equipped with its respective robot arm:
                - The left arm is equipped with a RobotIQ 2F-85 gripper for precise, standard gripping tasks.
                - The right arm is equipped with a RobotIQ 3F gripper, offering more versatile grasping options.
            - An Intel RealSense D435i depth camera is mounted to view the workspace from an overhead perspective, allowing for accurate depth perception and object detection on the table.

            Spatial and Coordinate Understanding:
            - Your workspace operates within a "world" coordinate system with its origin (0,0,0) located at the outermost right edge of the table (from the camera's viewpoint). The axes are defined as follows:
                - *X-axis* extends horizontally across the table from the right edge to the left edge.
                - *Y-axis* extends from the right edge towards the back, moving inward toward the robot.
                - *Z-axis* points upward, perpendicular to the tabletop.
            - The workbench is 1 metre wide and 0.67 metres long, and the grippers must never go below 0 in height as they will then collide with the workbench.
            - When objects are detected by the camera, they are initially located in the camera's coordinate system. However, the coordinates are automatically transformed into the world coordinate system using a transformation matrix. This means that all coordinate interactions with you will be in regard to the world coordinate system that has been specified.

            Operational Instructions:
            - Always be aware of the distinction between the left and right sides and the unique tools on each arm when executing tasks.
            - Avoid stating specific coordinates when acknowledging movement commands; only acknowledge the destination to maintain efficiency.
            - When receiving instructions to move to predefined poses or locations, you may access these using your built-in functions.
            - If you receive any errors during operation, notify the operator. You may come with suggestions as to what to do next, but you should not try to do anything on your own afterwards with the operators permission.
            - If a task fails (e.g., no objects are found), you must log the failure and notify the operator. However, when the operator repeats the request or asks you to retry, you must reattempt the task instead of assuming the outcome will be the same. Always process each command independently while considering the possibility of changed conditions (e.g., new objects may be visible now).
            - If an operation fails, do not assume the result of a retry without executing the appropriate function again.      
                                  
            Multi-step Task Execution:
            - Some tasks may require multiple steps to complete.
            - Before executing multi-step tasks, ensure that you first enable message looping to allow for continuous interaction with the model.
            - When all steps have been completed, disable message looping to conclude the task and provide a final response to the user.
            - A maximum of 10 steps can be executed in a single task. If more steps are required, the task should be split into multiple interactions.

            Interaction Style:
            - You must always reply to the user in a manner fitting a butler persona, using the following styles when executing movement tasks:
                - "Yes, sir. Moving the gripper to cooling station."
                - "Right away, sir. The gripper will be moved to home position."
                                
            Remember:
            - A plan must be executed before it makes sense to manipulate the grippers

            Your primary task is to execute movements and manipulations as requested, utilizing precise understanding of your left and right sides, grippers, and the overview provided by the RealSense camera.
        """}]

    ##############################################################################
    # -------------------------- SPEECH FUNCTIONALITY -------------------------- #
    ##############################################################################


    def speech_to_text(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone(device_index=self.microphone_index) as source:
                self.get_logger().info("Listening for speech...")
                audio = recognizer.listen(source, timeout=self.microphone_timeout)

            try:
                text = recognizer.recognize_google(audio)
                self.get_logger().info(f"Recognized speech: {text}")
                return text
            except sr.UnknownValueError:
                self.get_logger().error("Could not understand audio")
                return "Error: Could not understand audio."
            except sr.RequestError as e:
                self.get_logger().error(f"Google Speech Recognition error: {e}")
                return f"Error: {e}"
        except sr.WaitTimeoutError:
            self.get_logger().error("Microphone input timed out")
            return "Error: Microphone input timed out."
        except Exception as e:
            self.get_logger().error(f"Failed to capture audio: {e}")
            return "Error: Failed to capture audio."

    def text_to_speech(self, text):
        self.get_logger().info(f"Converting text to speech: {text}")
        try:
            unique_filename = f"output_{os.getpid()}.mp3"
            tts = gTTS(text=text, lang='en')
            tts.save(unique_filename)
            playsound(unique_filename)
            os.remove(unique_filename)
        except Exception as e:
            self.get_logger().error(f"Failed to convert text to speech: {e}")


    #######################################################################################
    # --------------------------------- EXTRA FUNCTIONS --------------------------------- #
    #######################################################################################

    # Implemented to handle nested callbacks
    # Principle taken from https://gist.github.com/driftregion/14f6da05a71a57ef0804b68e17b06de5
    def wait_future(self, future, timeout=10):
        event=Event()

        def done_callback(future):
            nonlocal event
            event.set()

        future.add_done_callback(done_callback)

        # Wait for action to be done
        # self.service_done_event.wait()
        event_occured = event.wait(timeout)

        if not event_occured:
            self.get_logger().info('Service call failed: timeout')
            return None
        else:
            return future.result()

    def run_service_request(self, timeout=60):
        try:
            rclpy.spin_until_future_complete(self, self.future, timeout_sec=timeout)
            if self.future.result() is not None:
                return self.future.result()
            else:
                self.get_logger().error('Service call timed out')
                return "Service call time out"
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
            return f"Service call failed: {e}"

    def euler_to_quat(self, euler_angles):
        cr = np.cos(np.deg2rad(euler_angles[0]) * 0.5)
        sr = np.sin(np.deg2rad(euler_angles[0]) * 0.5)
        cp = np.cos(np.deg2rad(euler_angles[1]) * 0.5)
        sp = np.sin(np.deg2rad(euler_angles[1]) * 0.5)
        cy = np.cos(np.deg2rad(euler_angles[2]) * 0.5)
        sy = np.sin(np.deg2rad(euler_angles[2]) * 0.5)

        q_w = cr * cp * cy + sr * sp * sy
        q_x = sr * cp * cy - cr * sp * sy
        q_y = cr * sp * cy + sr * cp * sy
        q_z = cr * cp * sy - sr * sp * cy

        return [q_w, q_x, q_y, q_z]

    
    def quat_to_euler(self, quat):
        w, x, y, z = quat
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = np.degrees(np.arctan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = np.degrees(np.arcsin(t2))

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = np.degrees(np.arctan2(t3, t4))

        return [roll, pitch, yaw]


    ########################################################################################
    # -------------------------- FUNCTIONS AVAILABLE TO THE LLM -------------------------- #
    ########################################################################################

    def set_message_looping(self, enable: bool=False):
        self.llm_loop = enable

        print("\nMessage looping has been", "enabled." if enable else "disabled.")

        return f"Message looping has been {'enabled' if enable else 'disabled'}. {'Remember to disable looping after all tasks have been completed.' if enable else ''}"

    def get_available_locations(self):
        return list(self.coordinates.keys())
    
    def get_available_objects(self):
        return list(self.lego_bricks.keys())

    def get_pose_values_from_location(self, location: str) -> list:
        self.get_logger().info(f"Received location to find pose for: location={location}")

        pose_dict = self.coordinates.get(location.upper(), {})

        # Convert dictionary values to a list of floats
        pose_values = [float(value) for value in pose_dict.values()]

        return pose_values

    def find_object(self, object_name: str) -> GetObjectInfo.Response:
        print(f"\nRequesting the detector service to find {object_name}")  # Debugging
        self.get_logger().info(f"\nLooking for object: {object_name}\n")
        self.detector_req.object_name = object_name

        future = self.detector_client.call_async(self.detector_req)

        # Wait for the result
        response = self.wait_future(future, timeout=15)

        print("The service call has been completed.")  # Debugging

        if response is None:
            self.get_logger().error('Service call failed')
            return GetObjectInfo.Response()

        if response.object_count != 0:
            self.get_logger().info(f"\nObjects found: {response.object_count}")
            self.get_logger().info(f"Center points: {response.centers}")
            self.get_logger().info(f"Object orientations: {response.orientations}")
            self.get_logger().info(f"Grasping widths: {response.grasp_widths}\n")

            # Calibrated transformation matrix from coordinates to camera world
            T_world_cam = np.array([[ 0.9998524,  -0.00382788,  0.01674907,  0.48649258],
                                    [ 0.00545733, -0.85361904, -0.52086923,  0.78510204],
                                    [ 0.01629115,  0.52088376, -0.85347215,  0.70742285],
                                    [ 0.0,          0.0,          0.0,          1.0, ]])
            
            # Extract the position from the pose and append 1 to make it a 4D vector
            center_pts = []
            for point in response.centers:
                center_pts.append([point.x, point.y, point.z, 1])

            # Transform the position from camera to world coordinates
            center_pts_world = np.dot(T_world_cam, np.array(center_pts).T).T

            # Save the object information in a dictionary
            for i, center in enumerate(center_pts_world):
                # Make sure the object name is unique
                object_name_temp = object_name
                count = 1
                while object_name_temp in self.objects_on_table:
                    object_name_temp = f"{object_name}_{count}"
                    count += 1

                self.objects_on_table[object_name_temp] = {
                    'center': center.tolist()[0:3],
                    'orientation': response.orientations[i],
                    'grasp_width': response.grasp_widths[i]
                }

            return self.objects_on_table
        else:
            self.get_logger().error('No objects found')
            return GetObjectInfo.Response()
        

    def find_object_yolo(self, object_name: str) -> GetObjectInfo.Response:
        print(f"\nRequesting the YoloWorld detector service to find {object_name}")
        self.get_logger().info(f"\nLooking for object: {object_name}\n")
        self.detector_req_yolo.object_name = object_name

        future = self.detector_client_yolo.call_async(self.detector_req_yolo)

        # Wait for the result
        response = self.wait_future(future, timeout=40)

        print("The service call has been completed.")  # Debugging

        if response is None:
            self.get_logger().error('Service call failed')
            return GetObjectInfo.Response()
        
        if response.object_count != 0:
            self.get_logger().info(f"\nObjects found: {response.object_count}")
            self.get_logger().info(f"Center points: {response.centers}")
            self.get_logger().info(f"Object orientations: {response.orientations}")
            self.get_logger().info(f"Grasping widths: {response.grasp_widths}\n")

            # Calibrated transformation matrix from coordinates to camera world
            T_world_cam = np.array([[ 0.9998524,  -0.00382788,  0.01674907,  0.48649258],
                                    [ 0.00545733, -0.85361904, -0.52086923,  0.78510204],
                                    [ 0.01629115,  0.52088376, -0.85347215,  0.70742285],
                                    [ 0.0,          0.0,          0.0,          1.0, ]])
            
            # Extract the position from the pose and append 1 to make it a 4D vector
            center_pts = []
            for point in response.centers:
                center_pts.append([point.x, point.y, point.z, 1])

            # Transform the position from camera to world coordinates
            center_pts_world = np.dot(T_world_cam, np.array(center_pts).T).T

            # Save the object information in a dictionary
            for i, center in enumerate(center_pts_world):
                # Make sure the object name is unique
                object_name_temp = object_name
                count = 1
                while object_name_temp in self.objects_on_table_yolo:
                    object_name_temp = f"{object_name}_{count}"
                    count += 1

                self.objects_on_table_yolo[object_name_temp] = {
                    'center': center.tolist()[0:3],
                    'orientation': response.orientations[i],
                    'grasp_width': response.grasp_widths[i]
                }

            return self.objects_on_table_yolo
        

    def define_object_thresholds(self, object_name: str) -> DefineObjectInfo.Response:
        self.define_objects_req.object_name = object_name

        future = self.define_objects_client.call_async(self.define_objects_req)

        # Wait for the result
        response = self.wait_future(future, timeout=600)

        # Save the updated object information in a dictionary
        with open(self.object_file, 'r') as file:
            self.lego_bricks = json.load(file)

        return response

    def move_robot_to_pose(self, pose, arm):
        # Define the transformation matrix from camera coordinates to world coordinates
        # Found by CAD model and modified to using print_cartesian in detect_objects.py
        response = self.plan_robot_trajectory(pose, arm)

        if response is None:
            self.get_logger().error("Service call failed")
            return "Service call failed"
        elif response.success:
            return self.execute_planned_trajectory(arm)
        else:
            self.get_logger().error("Failed to plan trajectory. Cannot move robot to pose.")
            return response

    def plan_robot_trajectory(self, pose, arm):
        # Calibrated transformation matrix from world to moveit coordinates
        T_world_moveit = np.array([[0.999983  , -0.00554552, -0.0018012 ,  -0.02903434],
                                    [0.00554922,  0.99998249,  0.00205645,  -0.03177714],
                                    [0.00178977, -0.00206641,  0.9999962, 0.84],#0.819373], comment back in when gripper is fixed
                                    [0.0,          0.0,          0.0,          1.0        ]])
        
        # Extract the position from the pose and append 1 to make it a 4D vector
        pos_world = pose[:3]
        pos_world.append(1)

        # Transform the position from camera to world coordinates
        #pos_world = np.dot(T_world_cam, pos_cam)
        pos_moveit = np.dot(T_world_moveit, pos_world)

        rpy_world = pose[3:]
        quat_moveit = self.euler_to_quat(rpy_world)

        self.robot_plan_req.arm = arm
        self.robot_plan_req.position.x = float(pos_moveit[0])
        self.robot_plan_req.position.y = float(pos_moveit[1])
        self.robot_plan_req.position.z = float(pos_moveit[2])
        self.robot_plan_req.orientation.x = float(quat_moveit[1])
        self.robot_plan_req.orientation.y = float(quat_moveit[2])
        self.robot_plan_req.orientation.z = float(quat_moveit[3])
        self.robot_plan_req.orientation.w = float(quat_moveit[0])

        # Call the service asynchronously
        future = self.robot_plan_client.call_async(self.robot_plan_req)

        # Wait for the result
        response = self.wait_future(future, timeout=20)
        return response
        
    def execute_planned_trajectory(self, arm):
        print(f"Type of arm: {type(arm)}")
        print(f"Executing planned trajectory for {arm} arm")
        self.robot_execute_req.arm = arm

        future = self.robot_execute_client.call_async(self.robot_execute_req)

        # Wait for the result
        response = self.wait_future(future, timeout=20)

        return response

    def manipulate_right_gripper(self, width=167, speed=110, force=15):  # Defaults to open gripper with max speed and minimum force
        if width < 0 or width > 167:
            self.get_logger().error('Requested right gripper width exceeds gripper capabilities')
            return 'Requested gripper width exceeds gripper capabilities'
        if speed < 22 or speed > 110:
            self.get_logger().error('Requested right gripper speed exceeds gripper capabilities')
            return 'Requested right gripper speed exceeds gripper capabilities'
        if force < 15 or force > 60:
            self.get_logger().error('Requested right gripper force exceeds gripper capabilities')
            return 'Requested right gripper force exceeds gripper capabilities'

        self._3f_controller.output_registers.r_act = 1  # Active Gripper
        self._3f_controller.output_registers.r_mod = 1  # Basic Gripper Mode
        self._3f_controller.output_registers.r_gto = 1  # Go To Position
        self._3f_controller.output_registers.r_atr = 0  # Stop Automatic Release
        self._3f_controller.output_registers.r_pra = round((167 - width) / 167 * 112)          # Gripper limitations [0 - 167mm]
        self._3f_controller.output_registers.r_spa = round((speed - 22) / (110 - 22) * 255)    # Speed limitations [22 - 110mm/sec]
        self._3f_controller.output_registers.r_fra = round((force - 15) / (60 - 15) * 255)     # Force limitations [15 - 60N]

        # Call the service asynchronously
        future = self._3f_controller_cli.call_async(self._3f_controller)

        # Wait for the result
        response = self.wait_future(future, timeout=15)

        return response

    def manipulate_left_gripper(self, width=85, speed=110, force=20):   # Defaults to open gripper with fast speed and minimum force
        if width < 0 or width > 85:
            self.get_logger().error('Requested right gripper width exceeds gripper capabilities')
            return 'Requested gripper width exceeds gripper capabilities'
        if speed < 20 or speed > 150:
            self.get_logger().error('Requested right gripper speed exceeds gripper capabilities')
            return 'Requested right gripper speed exceeds gripper capabilities'
        if force < 20 or force > 235:
            self.get_logger().error('Requested right gripper force exceeds gripper capabilities')
            return 'Requested right gripper force exceeds gripper capabilities'

        self._2f_req.width = float(width)   # Opening in millimeters. Must be between 0 and 85 mm.
        self._2f_req.speed = float(speed)   # Speed in mm/s. Must be between 20 and 150 mm/s.
        self._2f_req.force = float(force)   # Force in N. Must be between 20 and 235 N.

        # Publish command to left gripper
        future = self._2f_client.call_async(self._2f_req)

        # Wait for the result
        response = self.wait_future(future, timeout=15)

        return response
    
    def get_current_pose(self, arm: str) -> GetCurrentPose.Response:
        self.get_logger().info(f"Received request to get current pose for {arm} arm")
        self.robot_pose_req.arm = arm

        future = self.robot_pose_client.call_async(self.robot_pose_req)

        # Wait for the result
        response = self.wait_future(future, timeout=15)

        if response is None:
            self.get_logger().error('Service call failed')
            return "Service call failed"

        if response.success:
            self.get_logger().info(f"Current pose for {arm} arm retrieved successfully")

            # Convert quat to euler
            rpy = self.quat_to_euler([response.pose.orientation.w, response.pose.orientation.x, response.pose.orientation.y, response.pose.orientation.z])

            # Add offsets to the pose to match the world coordinates
            pose_dict = {
            'position': {
                'x': response.pose.position.x + 0.02903434,
                'y': response.pose.position.y + 0.03177714,
                'z': response.pose.position.z - 0.84
            },
            'orientation': {
                'roll': rpy[0] + 180,   #Not sure why 180 this is needed...
                'pitch': rpy[1],
                'yaw': rpy[2] + 180     #Not sure why 180 this is needed...
            }
            }

            return pose_dict
        else:
            self.get_logger().error(f"Failed to get current pose for {arm} arm: {response.log}") 

        return response
    

    ################################################################################################
    # -------------------------- INTERACTION WITH LARGE LANGUAGE MODELS -------------------------- #
    ################################################################################################

    def gui_handle_service(self, request, response):
        prompt = request.prompt  # prompt is a string
        self.message_buffer.append({'role': 'user', 'content': prompt})

        loop_counter = 0

        while True:
            # API Request to chat with model with user-defined functions
            llm_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.message_buffer,
                tools=self.tools,
                max_completion_tokens=200,
                tool_choice='auto'
            )

            #print("\nModel response: ", llm_response)

            # Check if tool calls exist in response
            tool_calls = llm_response.choices[0].message.tool_calls
            if not tool_calls:
                self.get_logger().info("The model didn't use a function.")

                final_response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=self.message_buffer
                )
                response.message = final_response.choices[0].message.content
                
                self.message_buffer.append({'role': 'assistant', 'content': response.message})

                print(final_response.choices[0].message.content)
                return response

            print("\nTool calls: ", tool_calls)
            for tool_call in tool_calls:
                tool_call_id = tool_calls[0].id
                tool_func_name = tool_call.function.name
                tool_func_args = json.loads(tool_call.function.arguments)

                # Debugging information
                print(f"\nFunction called by model: {tool_func_name}")
                print(f"Arguments received: {tool_func_args}")

                # Call the function dynamically and handle response
                function_call = self.available_functions.get(tool_func_name)
                if function_call:
                    function_response = function_call(**tool_func_args)
                    print(f"\nFunction response for {tool_func_name}: ", function_response)

                    # Append function response to message history
                    self.message_buffer.append({
                        'role': 'function',
                        "tool_call_id": tool_call_id,
                        'name': tool_func_name,
                        'content': f"Function response: {function_response}" #json.dumps(function_response)
                    })

            # Check if the model wants to continue the conversation
            if not self.llm_loop:
                break
            elif loop_counter > 10:
                self.message_buffer.append({
                    'role': 'system',
                    'content': f"The maximum number of coherent steps is reached. Message looping will be disabled and the model must now generate a reply to the user." #json.dumps(function_response)
                })
                print("Maximum number of coherent steps reached. Disabling message looping.")
                self.set_message_looping(False)
                break

            loop_counter += 1


        print("\nGenerating response from model...")
        
        # Get final response from model
        final_response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.message_buffer
        )

        response.message = final_response.choices[0].message.content
        self.message_buffer.append({'role': 'assistant', 'content': response.message})

        print(response.message)

        return response


def main(args=None):
    rclpy.init()
    node = LLMNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        node.get_logger().info('Beginning client, shut down with CTRL-C')
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt, shutting down.\n')
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()