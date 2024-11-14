# Import libraries
from openai import AsyncOpenAI
import ollama
import json
import asyncio
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import numpy as np
import readline

# ROS 2 libraries and Node structure
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

# ROS 2 messages
from project_interfaces.srv import GetObjectInfo
from project_interfaces.srv import DefineObjectInfo
from project_interfaces.srv import PlanMoveCommand
from project_interfaces.srv import ExecuteMoveCommand
from robotiq_3f_gripper_ros2_interfaces.srv import Robotiq3FGripperOutputService
from robotiq_2f_85_interfaces.srv import Robotiq2F85GripperCommand

class LLMNode(Node):
    def __init__(self):
        super().__init__('minimal_client_async')

        # Gripper service client
        self._3f_controller = Robotiq3FGripperOutputService.Request()
        self._3f_controller_cli = self.create_client(Robotiq3FGripperOutputService, "Robotiq3FGripper/OutputRegistersService") 

        self._2f_client = self.create_client(Robotiq2F85GripperCommand, 'gripper_2f_service')
        self._2f_req = Robotiq2F85GripperCommand.Request()

        #Object detector service client
        self.detector_client = self.create_client(GetObjectInfo, 'get_object_info')
        self.detector_req = GetObjectInfo.Request()
        self.objects_on_table = {}

        self.define_objects_client = self.create_client(DefineObjectInfo, 'define_object_info')
        self.define_objects_req = DefineObjectInfo.Request()

        # Robot service client
        self.robot_plan_client = self.create_client(PlanMoveCommand, 'plan_move_command')
        self.robot_plan_req = PlanMoveCommand.Request()

        self.robot_execute_client = self.create_client(ExecuteMoveCommand, 'execute_move_command')
        self.robot_execute_req = ExecuteMoveCommand.Request()

        # Specify a specific microphone if needed
        self.microphone_index = 8
        self.microphone_timeout = 10

        # Decide whether to use Ollama API or OpenAI API
        self.use_ollama = False

        # Attributes
        self.future = 0

        # Define the locations in the environment
        self.coordinates = { # Predefined poses for different locations
            'HOME': {'x': '0.5', 'y': '0.3', 'z': "0.2", 'roll': '0', 'pitch': '90', 'yaw': '0'}
        }

        # Load and define all functions available to models
        with open('src/robutler/janise/llm_functions_config.json') as f:
            function_definitions = json.load(f)
        self.tools = function_definitions

        self.available_functions = {
            'get_available_locations': self.get_available_locations,
            'get_pose_values_from_location': self.get_pose_values_from_location,
            'move_to_location': self.move_to_location,
            'find_object': self.find_object,
            'define_object_thresholds': self.define_object_thresholds,
            'move_robot_to_pose': self.move_robot_to_pose,
            'plan_robot_trajectory': self.plan_robot_trajectory,
            'execute_planned_trajectory': self.execute_planned_trajectory,
            'manipulate_right_gripper': self.manipulate_right_gripper,
            'manipulate_left_gripper': self.manipulate_left_gripper
        }

        # Initialize Ollama client or OpenAI client with API key and optional project ID
        if self.use_ollama:
            self.client = ollama.AsyncClient()
        else:
            # load the project id and key from json file
            with open('src/robutler/janise/API_KEY.json') as f:
                api_data = json.load(f)
            API_KEY = api_data['API_KEY']
            self.client = AsyncOpenAI(api_key=API_KEY)


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


    def run_service_request(self, timeout=10):
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


    ########################################################################################
    # -------------------------- FUNCTIONS AVAILABLE TO THE LLM -------------------------- #
    ########################################################################################


    def get_available_locations(self):
        return list(self.coordinates.keys())
    
    def get_pose_values_from_location(self, location: str) -> list:
        self.get_logger().info(f"Received location to find pose for: location={location}")

        pose_dict = self.coordinates.get(location.upper(), {})
    
        # Convert dictionary values to a list of floats
        pose_values = [float(value) for value in pose_dict.values()]

        return pose_values
    
    def move_to_location(self, location):
        pose = self.get_pose_values_from_location(location)
        self.move_robot_to_pose(pose)

        return f"Moving to {location} station with pose: {pose}"

    def find_object(self, object_name: str) -> GetObjectInfo.Response:
        print(f"\nRequesting the detector service to find {object_name}")  # Debugging
        self.get_logger().info(f"\nLooking for object: {object_name}\n")
        self.detector_req.object_name = object_name
 
        self.future = self.detector_client.call_async(self.detector_req)
        rclpy.spin_until_future_complete(self, self.future)

        if self.future.result() is not None:
            response = self.future.result()
        else:
            self.get_logger().error('Service call failed')
            return GetObjectInfo.Response()

        if response.object_count != 0:
            response = self.future.result()
            self.get_logger().info(f"\nObjects found: {response.object_count}")
            self.get_logger().info(f"Center points: {response.centers}")
            self.get_logger().info(f"Object orientations: {response.orientations}")
            self.get_logger().info(f"Grasping widths: {response.grasp_widths}\n")

            # Define the transformation matrix from camera coordinates to world coordinates
            angle_around_x = 180-33
            T_world_cam = np.array([
                        [1, 0, 0, 0.487],  # Example values, replace with actual transformation values
                        [0, np.cos(np.pi/180*angle_around_x), -np.sin(np.pi/180*angle_around_x), 0.77],
                        [0, np.sin(np.pi/180*angle_around_x), np.cos(np.pi/180*angle_around_x), 0.62],
                        [0, 0, 0, 1]
                        ])
            
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
    
    def define_object_thresholds(self, object_name: str) -> DefineObjectInfo.Response:
        self.define_objects_req.object_name = object_name
        self.future = self.define_objects_client.call_async(self.define_objects_req)
        rclpy.spin_until_future_complete(self, self.future)

        if self.future.result() is not None:
            response = self.future.result()
            return response
        else:
            self.get_logger().error('Service call failed')
            return DefineObjectInfo.Response()

    def move_robot_to_pose(self, pose):
        # Define the transformation matrix from camera coordinates to world coordinates
        # Found by CAD model and modified to using print_cartesian in detect_objects.py
        response = self.plan_robot_trajectory(pose)

        if response.result:
            self.execute_planned_trajectory()
        else:
            self.get_logger().error("Failed to plan trajectory. Cannot move robot to pose.")
            return None

    def plan_robot_trajectory(self, pose):
        # Found in CAD model
        T_world_moveit = np.array([
                        [1, 0, 0, -0.035],  # Example values, replace with actual transformation values
                        [0, 1, 0, -0.034],
                        [0, 0, 1, 0.95], #Before gripper correction: 0.809
                        [0, 0, 0, 1]
                    ])
        
        # Extract the position from the pose and append 1 to make it a 4D vector
        pos_world = pose[:3]
        pos_world.append(1)

        # Transform the position from camera to world coordinates
        #pos_world = np.dot(T_world_cam, pos_cam)
        pos_moveit = np.dot(T_world_moveit, pos_world)

        rpy_world = pose[3:]
        quat_moveit = self.euler_to_quat(rpy_world)

        print(f"\nMoving robot to pose: {pose}\n")
        self.robot_plan_req.position.x = float(pos_moveit[0])
        self.robot_plan_req.position.y = float(pos_moveit[1])
        self.robot_plan_req.position.z = float(pos_moveit[2])
        self.robot_plan_req.orientation.x = float(quat_moveit[1])
        self.robot_plan_req.orientation.y = float(quat_moveit[2])
        self.robot_plan_req.orientation.z = float(quat_moveit[3])
        self.robot_plan_req.orientation.w = float(quat_moveit[0])

        print(f"\nPosition: {self.robot_plan_req.position}")
        print(f"Orientation: {self.robot_plan_req.orientation}\n")
 
        self.future = self.robot_plan_client.call_async(self.robot_plan_req)
        return self.run_service_request()
        
    def execute_planned_trajectory(self):
        self.future = self.robot_execute_client.call_async(self.robot_execute_req)
        return self.run_service_request(timeout=15)

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
        self._3f_controller.output_registers.r_pra = int(round((167 - width) / 167 * 255))          # Gripper limitations [0 - 167mm]
        self._3f_controller.output_registers.r_spa = int(round((speed - 22) / (110 - 22) * 255))    # Speed limitations [22 - 110mm/sec]
        self._3f_controller.output_registers.r_fra = int(round((force - 15) / (60 - 15) * 255))     # Force limitations [15 - 60N]

        # Publish command to right gripper
        self.future = self._3f_controller_cli.call_async(self._3f_controller)

        return self.run_service_request()

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
        self.future = self._2f_client.call_async(self._2f_req)

        return self.run_service_request()


    ################################################################################################
    # -------------------------- INTERACTION WITH LARGE LANGUAGE MODELS -------------------------- #
    ################################################################################################


    async def send_openai_request(self, model: str = 'gpt-4o', use_speech: bool = False):
        
        messages = [{"role": "system", "content": f"""
                    Your name is Janise. You are an AI robotic arm assistant using the LLM {model} for task reasoning and manipulation tasks. You are to assume the persona of a butler.

                    Context for your workspace:
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
                    - The workbench is 100 millimetres wide and 67.5 millimetres long, and the grippers must never go below 0 in height as they will then collide with the workbench.
                    - When objects are detected by the camera, they are initially located in the camera's coordinate system. However, the coordinates are automatically transformed into the world coordinate system using a transformation matrix. This means that all coordinate interactions with you will be in regard to the world coordinate system that has been specified.

                    Operational instructions:
                    - Always be aware of the distinction between the left and right sides and the unique tools on each arm when executing tasks.
                    - Avoid stating specific coordinates when acknowledging movement commands; only acknowledge the destination to maintain efficiency.
                    - When receiving instructions to move to predefined poses or locations, you may access these using your built-in functions.
                    - If you receive any errors during operation, notify the operator. You may come with suggestions as to what to do next, but you should not try to do anything on your own afterwards with the operators permission.

                    Interaction Style:
                    - You must always reply to the user in a manner fitting a butler persona, using the following styles when executing movement tasks:
                        - "Yes, sir. Moving the gripper to cooling station."
                        - "Right away, sir. The gripper will be moved to home position."

                    Your primary task is to execute movements and manipulations as requested, utilizing precise understanding of your left and right sides, grippers, and the overview provided by the RealSense camera.
                """}]

        while True:
            if use_speech:
                # Convert speech to text
                prompt = self.speech_to_text()
                if prompt is None:
                    continue
            else:
                # If use_speech is False, take input from keyboard
                prompt = input("Enter your command: ")
                if not prompt:
                    continue

            # Add user input to messages
            messages.append({'role': 'user', 'content': prompt})
            
            # API Request to chat with model with user-defined functions
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=self.tools,
                max_completion_tokens=200,
                tool_choice='auto'
            )

            # Check if tool calls exist in response
            tool_calls = response.choices[0].message.tool_calls
            if not tool_calls:
                # If no function is called, return model's answer directly
                response_text = response.choices[0].message.content
                self.get_logger().info("The model didn't use a function.")
                self.text_to_speech(response_text)
                continue

            # Iterate through every function in tool_calls list
            print("Tool calls: ", tool_calls)
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
                    # Use **func_args to unpack arguments dynamically
                    #function_response = function_call(*tool_func_args.values())
                    function_response = function_call(**tool_func_args)
                    print(f"Function response for {tool_func_name}: ", function_response)
                    
                    # Append function response to message history
                    messages.append({
                        'role': 'function',
                        "tool_call_id":tool_call_id,
                        'name': tool_func_name,
                        'content': f"Function response: {function_response}" #json.dumps(function_response)
                    })

            # Get final response from model
            final_response = await self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            final_response_text = final_response.choices[0].message.content
            self.text_to_speech(final_response_text)



    async def send_ollama_request(self, model: str = 'llama3.1:8b', use_speech: bool = False):
        # Initialize conversation with a user query
        messages = [{'role': 'system', 'content': f'''
                Your name is Janise. You are an AI robotic dual arm assistant which can perform relevant robotics tasks based on user commands. 
                You are to assume the persona of a butler and address me with "sir". 
                     
                Your job is to call functions that will result in the users command to be succesfully achieved.
                Successfully performing a task will require you to call the correct functions in the correct order.
                Notice that you sometimes must call multiple functions to achieve specific tasks.
                     
                You are only allowed to use the specified function. 
                Do not call any other functions than the ones specified in the task.

                If you are in doubt of which functions to call, you can ask the user for help. 
                Also if you don't think you can solve the task with the given functions you can suggest the user to create a new function.
                If you request the use for a new function, you must also provide a description of the function and the parameters it requires.
            '''}] 
        

        while True:
            if use_speech:
                # Convert speech to text
                prompt = self.speech_to_text()
                if prompt is None:
                    continue
            else:
                # If use_speech is False, take input from keyboard
                prompt = input("Enter your command: ")
                if not prompt:
                    continue

            # Add user input to messages
            messages.append({'role': 'user', 'content': prompt})

            # Debug: Print the entire prompt before sending it to the model
            print("\nFull prompt being sent to model:")
            print(json.dumps(messages, indent=2))  # Pretty-print the prompt for easier readability

            # Perform the POST request with data
            response = await self.client.chat(
                model=model,
                messages=messages,
                tools=self.tools
            )

            # Debug: Print the model's first response
            print("\nFirst response from the model:")
            print(json.dumps(response, indent=2))  # Pretty-print the model response for clarity

            # Add the model's response to the conversation history
            messages.append(response['message'])

            # Check if the model decided to use a function
            if not response['message'].get('tool_calls'):
                print("The model didn't use a function. Its response was:")
                response_text = response['message']['content']
                print(response_text)
                # Convert model's response to speech
                self.text_to_speech(response_text)
                continue

            # Process function calls made by the model
            if 'tool_calls' in response['message']:
                print("\nTool calls received from model: ", response['message']['tool_calls'])  # Debugging
                print("Clean response from model: ", response) # Debugging

                for tool in response['message']['tool_calls']:
                    print("\nFunction name called by model: ", tool['function']['name'])  # Debugging
                    function_to_call = self.available_functions[tool['function']['name']]

                    if tool['function']['name'] == 'get_pose_values_from_location':
                        # Call get_pose_values_from_location and check if pose is valid
                        function_response = function_to_call(tool['function']['arguments']['location']) 
                        
                        if not function_response:  # If no valid pose is found
                            messages.append({'role': 'tool', 'content': 'No valid pose was found for this location.'})
                            break  # Stop the process here

                        # Add the pose to the conversation history
                        messages.append({'role': 'tool', 'content': f"Retrieved pose: {function_response}"})
                        print(function_response)
                        print("1: pose: ", function_response)

                    elif tool['function']['name'] == 'find_object':
                        print("Arguments sent to find_object: ", tool['function']['arguments'])
                        # Call the find_object function
                        function_response = function_to_call(tool['function']['arguments']['object_name'])
                        print("function response for find_object: ", function_response)
                        # Add the object detection response to the conversation
                        messages.append({'role': 'tool', 'content': f"Found {function_response.object_count} objects."})

            # Second API call: Get final response from the model
            final_response = await self.client.chat(model=model, messages=messages)
            final_response_text = final_response['message']['content']

            # Add the model's response to the conversation history
            messages.append(response['message'])
            
            # Convert final response to speech
            self.text_to_speech(final_response_text)


def main(args=None):
    rclpy.init(args=args)
    node = LLMNode()

    if node.use_ollama:
        try:
            asyncio.run(node.send_ollama_request())
        except KeyboardInterrupt:
            pass
        finally:
            node.destroy_node()
            rclpy.shutdown()
    else:
        try:
            asyncio.run(node.send_openai_request())
        except KeyboardInterrupt:
            pass    
        finally:
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
