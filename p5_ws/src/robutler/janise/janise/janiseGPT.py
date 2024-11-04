# Import libraries
from openai import AsyncOpenAI
import json
import asyncio
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

# ROS 2 libraries and Node structure
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

# ROS 2 messages
from project_interfaces.action import JointValues
from project_interfaces.srv import GetObjectInfo

class LLMNode(Node):
    def __init__(self):
        super().__init__('minimal_client_async')

        # Action Client setup
        self._action_client = ActionClient(self, JointValues, 'JointValues')
        self.jointvalues = [0, 0, 0, 0, 0, 0, 0]

        #Object detector service client
        self.detector_client = self.create_client(GetObjectInfo, 'get_object_info')
        self.detector_req = GetObjectInfo.Request()

        # Specify a specific microphone if needed
        self.microphone_index = 8
        self.microphone_timeout = 10

        # Initialize OpenAI client with API key and optional project ID
        self.client = AsyncOpenAI(api_key="API_KEY", project="PROJECT_ID")


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
            tts = gTTS(text=text, lang='en', tld='com.au')
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
            
            return response
        else:
            self.get_logger().error('Service call failed')
            return GetObjectInfo.Response()


    ###############################################################################################
    # -------------------------- INTERACTION WITH LARGE LANGUAGE MODEL -------------------------- #
    ###############################################################################################


    async def run(self, model: str = 'gpt-4o', use_speech: bool = False):
        messages = [{"role": "system", 
                     "content": """Your name is Janise. You are an AI robotic arm assistant using the LLM gpt-4o for task reasoning and manipulation tasks. You are to assume the persona of a butler and address me with 'sir.'

                                When the user asks for the gripper or robot to be moved to a certain location. 
                                
                                The user must always be replied to, and it should follow a style similar to the following examples, but only make this type of reply if the send_goal() function is called:
                                Yes, sir. Moving the gripper to cooling station.
                                Right away, sir. The gripper will be moved to home position."""}
                    ]

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
                tools=[ 
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
                    }
                ],
                max_completion_tokens=200,
                tool_choice='auto'
            )

            # Check if tool calls exist in response
            tool_calls = response.choices[0].message.tool_calls
            if not tool_calls:
                # If no function is called, return model's answer directly
                response_text = response.choices[0].message.content
                print("The model didn't use a function. Its response was:")
                print(response_text)
                self.text_to_speech(response_text)
                break

            # Process functions calls from the model
            available_functions = {
                'get_joint_values_from_location': self.get_joint_values_from_location,
                'send_goal': self.send_goal,
                'move_to_location': self.move_to_location,
                'find_object': self.find_object
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

            # Get final response from model
            final_response = await self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            final_response_text = final_response.choices[0].message.content
            self.text_to_speech(final_response_text)

def main(args=None):
    rclpy.init(args=args)
    node = LLMNode()

    try:
        asyncio.run(node.run())
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
