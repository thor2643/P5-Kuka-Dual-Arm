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

# ROS 2 libraries and Node structure
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

# ROS 2 messages
from project_interfaces.action import JointValues
from project_interfaces.srv import GetObjectInfo
from project_interfaces.srv import MoveCommand

class LLMNode(Node):
    def __init__(self):
        super().__init__('minimal_client_async')

        # Action Client setup
        self._action_client = ActionClient(self, JointValues, 'JointValues')
        self.jointvalues = [0, 0, 0, 0, 0, 0, 0]

        #Object detector service client
        self.detector_client = self.create_client(GetObjectInfo, 'get_object_info')
        self.detector_req = GetObjectInfo.Request()

        # Robot service client
        self.robot_client = self.create_client(MoveCommand, 'move_command')
        self.robot_req = MoveCommand.Request()

        # Specify a specific microphone if needed
        self.microphone_index = 8
        self.microphone_timeout = 10

        # Decide whether to use Ollama API or OpenAI API
        self.use_ollama = False

        # Define all function available to models
        self.tools = [ 
                    {
                        "type": "function",
                        "function": {
                            'name': 'get_joint_values_from_location',
                            'description': 'Used only to retrieve the robot joint angles based on the user-specified location. It does not move the robot',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'location': {
                                        'type': 'string',
                                        'description': 'The name of the target location, e.g., "home", "cooling", or "painting".',
                                    }
                                },
                                'required': ['location'],
                            },
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "send_goal",
                            "description": "Sends joint angles to move the robot to the specified joint positions, which in turn moves the robot.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "joint_values": {
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "description": "A list of 7 floating-point numbers representing joint angles for the robot arm."
                                    }
                                },
                                "required": ["joint_values"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            'name': 'move_to_location',
                            'description': 'Retrieves the robot joint angles based on the user-specified location and sends them to the robot to make it move to said location.',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'location': {
                                        'type': 'string',
                                        'description': 'The name of the target location, e.g., "home", "cooling", or "painting".',
                                    }
                                },
                                'required': ['location'],
                            },
                        }
                    },
                    {
                        'type': 'function',
                        'function': {
                            'name': 'find_object',
                            'description': 'Find the object in the environment using the object detector service. The object name should be provided as an argument to this function. The object detector service will return the number of objects found as well as the Cartesian center point, width, height and orientation of each object.',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'object_name': {
                                        'type': 'string',
                                        'description': 'The name of the object that must be found. Only one name can be provided. Must use _ (underscore) instead of spaces.',
                                    }
                                },
                                'required': ['object_name'],
                            },
                        },
                    },
                    {
                        'type': 'function',
                        'function': {
                            'name': 'move_robot_to_pose',
                            'description': 'Move the robot to a specific pose in the environment. The pose should be provided as an argument to this function. The robot will move to the specified pose.',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'pose': {
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "description": "A list of 6 floating-point numbers representing the pose of the robot arm e.g. the first 3 numbers representing the x,y,z position and the last 3 numbers representing the roll, pitch and yaw in degrees."
                                    }
                                },
                                'required': ['pose'],
                            },
                        },
                    }
                ]

        # Initialize OpenAI client with API key and optional project ID
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
    

    #########################################################################################
    # -------------------------- ROS2 COMMUNICATION AND FEEDBACK -------------------------- #
    #########################################################################################
    

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.success))
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.progress))


    ########################################################################################
    # -------------------------- FUNCTIONS AVAILABLE TO THE LLM -------------------------- #
    ########################################################################################


    async def get_joint_values_from_location(self, location: str) -> list:
        coordinates = { # Predefined joint angles for different locations
            'HOME-STATION': {'joint_1': '0.0', 'joint_2': '0.0', 'joint_3': '0.0', 'joint_4': '0.0', 'joint_5': '0.0', 'joint_6': '0.0', 'joint_7': '0.0'},
            'START-STATION': {'joint_1': '0.1745', 'joint_2': '0.2618', 'joint_3': '0.3491', 'joint_4': '0.4363', 'joint_5': '0.5236', 'joint_6': '0.5236', 'joint_7': '0.5236'},
            'WELDING-STATION': {'joint_1': '0.0873', 'joint_2': '0.1745', 'joint_3': '0.2618', 'joint_4': '0.3491', 'joint_5': '0.4363', 'joint_6': '0.5236', 'joint_7': '0.5236'},
            'COOLING-STATION': {'joint_1': '0.0524', 'joint_2': '0.1047', 'joint_3': '0.1571', 'joint_4': '0.2094', 'joint_5': '0.2618', 'joint_6': '0.3142', 'joint_7': '0.3665'},
            'PAINTING-STATION': {'joint_1': '0.3491', 'joint_2': '0.4363', 'joint_3': '0.5236', 'joint_4': '0.5236', 'joint_5': '0.5236', 'joint_6': '0.5236', 'joint_7': '0.5236'},
            'END-STATION': {'joint_1': '0.0698', 'joint_2': '0.1396', 'joint_3': '0.2094', 'joint_4': '0.2793', 'joint_5': '0.3491', 'joint_6': '0.4189', 'joint_7': '0.4887'},
        }
        self.get_logger().info(f"Received location to find joint angles for: location={location}")

        joint_dict = coordinates.get(location.upper() + '-STATION', {})
    
        # Convert dictionary values to a list of floats
        joint_values = [float(value) for value in joint_dict.values()]

        return joint_values
    
    def send_goal(self, jointvalues: list) -> str:
        print("\nsend_goal started with jointvalues:", jointvalues)

        # Convert the string to a list of floats
        if type(jointvalues) == str:
            jointvalues = json.loads(jointvalues)

        try:
            if len(jointvalues) != 7:
                raise ValueError("Incorrect number of joint angles. Expected 7 values.")

            print("Correct number of joint angles received")
            joint_values = JointValues.Goal()
            joint_values.joint_1, joint_values.joint_2, joint_values.joint_3, joint_values.joint_4, \
            joint_values.joint_5, joint_values.joint_6, joint_values.joint_7 = jointvalues

            self.get_logger().info(f"Sending joint values: {joint_values}")

            if not self._action_client.wait_for_server(timeout_sec=5.0):
                self.get_logger().error("Action server not available after waiting.")
                return "Action server unavailable"

            print("Action server available. Sending goal now...")
            self._send_goal_future = self._action_client.send_goal_async(
                joint_values, feedback_callback=self.feedback_callback)
            self._send_goal_future.add_done_callback(self.goal_response_callback)

        except Exception as e:
            print(f"Exception in send_goal: {e}")
            return f"Error sending joint angles: {e}"

    async def move_to_location(self, location):
        # Get joint values asynchronously
        joint_values = await self.get_joint_values_from_location(location)
        self.send_goal(joint_values)
        return f"Moving to {location} station with joint values: {joint_values}"

    def find_object(self, object: str) -> GetObjectInfo.Response:
        print(f"\nRequesting the detector service to find {object}")  # Debugging
        self.get_logger().info(f"\nLooking for object: {object}\n")
        self.detector_req.object_name = object
 
        self.future = self.detector_client.call_async(self.detector_req)
        rclpy.spin_until_future_complete(self, self.future)

        if self.future.result() is not None:
            response = self.future.result()
            self.get_logger().info(f"\nObjects found: {response.object_count}")
            self.get_logger().info(f"Center points: {response.centers}")
            self.get_logger().info(f"Object orientations: {response.orientations}")
            self.get_logger().info(f"Grasping widths: {response.grasp_widths}\n")

            # Define the transformation matrix from camera coordinates to world coordinates
            T_cam_world = np.array([
                [-1, 0, 0, -0.487],  # Example values, replace with actual transformation values
                [0, 1, 0, 0.336],
                [0, 0, -1, 1.011],
                [0, 0, 0, 1]
            ])

            return response
        else:
            self.get_logger().error('Service call failed')
            return GetObjectInfo.Response()
        
    def move_robot_to_pose(self, pose):
        # Define the transformation matrix from camera coordinates to world coordinates
        # Found by CAD model and modified to using print_cartesian in detect_objects.py
        angle_around_x = 180-33
        T_world_cam = np.array([
                        [1, 0, 0, 0.487],  # Example values, replace with actual transformation values
                        [0, np.cos(np.pi/180*angle_around_x), -np.sin(np.pi/180*angle_around_x), 0.77],
                        [0, np.sin(np.pi/180*angle_around_x), np.cos(np.pi/180*angle_around_x), 0.62],
                        [0, 0, 0, 1]
                    ])
        
        # Found in CAD model
        T_world_moveit = np.array([
                        [1, 0, 0, -0.35],  # Example values, replace with actual transformation values
                        [0, 1, 0, -0.34],
                        [0, 0, 1, 0.809],
                        [0, 0, 0, 1]
                    ])
        
        # Extract the position from the pose and append 1 to make it a 4D vector
        pos_cam = pose[:3].append(1)

        # Transform the position from camera to world coordinates
        #pos_world = np.dot(T_world_cam, pos_cam)
        #pos_moveit = np.dot(T_world_moveit, pos_world)

        #TODO: Add orientation transformation
        #0.14205068 -0.08728484  0.75022754 

        #target_pose.position.x = 0;
        #target_pose.position.y = 0.5;
        #target_pose.position.z = 1.8;

        print(f"\nMoving robot to pose: {pose}\n")
        self.robot_req.position.x = 0.527    #float(pos_moveit[0])
        self.robot_req.position.y = 0.286     #0.286 #float(pos_moveit[1])
        self.robot_req.position.z = 1.0     #float(pos_moveit[2])
        self.robot_req.orientation.x = float(0.707) # float(0) # Example values, replace with actual orientation values
        self.robot_req.orientation.y = float(0.707) #float(0.8)
        self.robot_req.orientation.z = float(0)     #float(0.5)
        self.robot_req.orientation.w = float(0)     #float(0.2)
 
        self.future = self.robot_client.call_async(self.robot_req)
        try:
            rclpy.spin_until_future_complete(self, self.future, timeout_sec=15.0)
            if self.future.result() is not None:
                return self.future.result()
            else:
                self.get_logger().error('Service call timed out')
                return None
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
            return None

    ################################################################################################
    # -------------------------- INTERACTION WITH LARGE LANGUAGE MODELS -------------------------- #
    ################################################################################################


    async def send_openai_request(self, model: str = 'gpt-4o', use_speech: bool = False):
        messages = [{"role": "system", "content": """
                    Your name is Janise. You are an AI robotic arm assistant using the LLM gpt-4o for task reasoning and manipulation tasks. You are to assume the persona of a butler and address me with 'sir.'

                    When the user asks for the gripper or robot to be moved to a certain location use your functions to do so. 
                                
                    The user must always be replied to, and it should follow a style similar to the following examples, but only make this type of reply if the send_goal() function is called:
                    Yes, sir. Moving the gripper to cooling station.
                    Right away, sir. The gripper will be moved to home position.

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
                print("The model didn't use a function.")
                self.text_to_speech(response_text)
                continue

            # Process functions calls from the model
            available_functions = {
                'get_joint_values_from_location': self.get_joint_values_from_location,
                'send_goal': self.send_goal,
                'move_to_location': self.move_to_location,
                'find_object': self.find_object,
                'move_robot_to_pose': self.move_robot_to_pose
            }

            # Iterate through every function in tool_calls list
            print("Tool calls: ", tool_calls)
            for tool_call in tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                # Debugging information
                print(f"\nFunction called by model: {func_name}")
                print(f"Arguments received: {func_args}")

                # Call a fitting function and add the result to message history
                if func_name == 'get_joint_values_from_location':
                    # Call function and verify if joint angles are valid
                    function_response = await available_functions[func_name](func_args['location'])
                    print("The function response for get_joint_values_from_location: ", function_response)
                    if not function_response:  
                        messages.append({'role': 'assistant', 'content': 'No valid joint angles found for this location.'})
                        self.text_to_speech("No valid joint angles found for the specified location, sir.")
                        break  
                    
                    # Add found joint angles to message history
                    messages.append({
                        'role': 'function',
                        'name': func_name,
                        'content': json.dumps(function_response)
                    })
                    
                    break

                elif func_name == 'send_goal':
                    # Call send_goal function with joint values
                    function_response = available_functions[func_name](func_args['joint_values'])
                    print("The function response for send_goal:", function_response)

                    # Add send_goal response to message history
                    messages.append({
                        'role': 'function',
                        'name': func_name,
                        'content': function_response
                    })

                    break

                elif func_name == 'move_to_location':
                    # Call move_to_location function asynchronously
                    function_response = await available_functions[func_name](func_args['location'])
                    print("Function response for move_to_location:", function_response)

                    # Add move_to_location response to message history
                    messages.append({
                        'role': 'function',
                        'name': func_name,
                        'content': function_response
                    })

                    break
                
                elif func_name == 'find_object':
                    print("Arguments sent to find_object: ", func_args['object_name'])
                    # Call the find_object function
                    function_response = available_functions[func_name](func_args['object_name'])
                    print("function response for find_object: ", function_response)

                    # Add the object detection response to the conversation
                    messages.append({
                        'role': 'function',
                        'name': func_name, 
                        'content': f"Found {function_response.object_count} objects."
                    })

                    break

                elif func_name == 'move_robot_to_pose':
                    print("Arguments sent to move_robot_to_pose: ", func_args['pose'])
                    # Call the find_object function
                    function_response = available_functions[func_name](func_args['pose'])
                    print("function response for move_robot_to_pose: ", function_response)

                    # Add the object detection response to the conversation
                    messages.append({
                        'role': 'function',
                        'name': func_name, 
                        'content': f"Found {function_response.result}."
                    })

                    break

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
                available_functions = {
                    'get_joint_values_from_location': self.get_joint_values_from_location,
                    'send_goal': self.send_goal,
                    'find_object': self.find_object,
                }
                print("\nTool calls received from model: ", response['message']['tool_calls'])  # Debugging
                print("Clean response from model: ", response) # Debugging

                for tool in response['message']['tool_calls']:
                    print("\nFunction name called by model: ", tool['function']['name'])  # Debugging
                    function_to_call = available_functions[tool['function']['name']]

                    if tool['function']['name'] == 'get_joint_values_from_location':
                        # Call get_joint_values_from_location and check if joint angles are valid
                        function_response = function_to_call(tool['function']['arguments']['location']) 
                        
                        if not function_response:  # If no valid joint angles were found
                            messages.append({'role': 'tool', 'content': 'No valid joint angles found for this location.'})
                            break  # Stop the process here, do not call send_goal

                        # Add the joint angles to the conversation history
                        messages.append({'role': 'tool', 'content': f"Retrieved joint angles: {function_response}"})
                        print(function_response)
                        print("1: Joint values: ", function_response)
                    
                    elif tool['function']['name'] == 'send_goal': 
                        print("Arguments sent to send_goal: ", tool['function']['arguments'])  # Debugging
                        # Only proceed if the previous call returned valid joint angles
                        function_response = function_to_call(tool['function']['arguments']['joint_values']) 
                        print("function response for send_goal: ", function_response)
                        # Add the robot movement response to the conversation
                        messages.append({'role': 'tool', 'content': function_response})

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
