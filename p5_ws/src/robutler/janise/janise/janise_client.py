#LLM Librarys:
import json
import ollama
import asyncio
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

#general Node structure:                          
import sys
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

#message
from project_interfaces.action import JointValues   
from project_interfaces.srv import GetObjectInfo


class LLMNode(Node):
    def __init__(self):
        super().__init__('minimal_client_async')

        #Action Client
        self._action_client = ActionClient(self, JointValues, 'JointValues')
        self.jointvalues = [0,0,0,0,0,0,0] 

        #Object detector service client
        self.detector_client = self.create_client(GetObjectInfo, 'get_object_info')
        self.detetector_req = GetObjectInfo.Request()

        #LLM
        self.llm = ollama.AsyncClient()  # Initialize the Ollama client for LLM interactions
        self.microphone_index = 8 # Specify a specific microphone if needed
        self.microphone_timeout = 10

        # Wait for the service to be available
        #while not self.cli.wait_for_service(timeout_sec=1.0):
        #    self.get_logger().info('Service move_robot is not available, waiting...')

    def find_object(self, object: str) -> GetObjectInfo.Response:
        print(f"\nRequesting the detector service to find {object}")  # Debugging
        self.detetector_req.object_name = object
 
        self.future = self.detector_client.call_async(self.detector_req)
        rclpy.spin_until_future_complete(self, self.future)

        return self.future.result()

    def send_goal(self, jointvalues: list) -> str:
        print("\nsend_goal started with jointvalues:", jointvalues)  # Debugging

        if type(jointvalues) == str:
            # Convert the string to a list of floats
            jointvalues = json.loads(jointvalues)

        try:
            if len(jointvalues) != 7:
                raise ValueError("Incorrect number of joint angles. Expected 7 values.")
            
            print("Correct number of joint angles received")  # Debugging
            joint_values = JointValues.Goal()
            joint_values.joint_1, joint_values.joint_2, joint_values.joint_3, joint_values.joint_4, \
            joint_values.joint_5, joint_values.joint_6, joint_values.joint_7 = jointvalues

            self.get_logger().info(f"Sending joint values: {joint_values}")

            if not self._action_client.wait_for_server(timeout_sec=5.0):
                self.get_logger().error("Action server not available after waiting.")
                return "Action server unavailable"
            
            print("Action server available. Sending goal now...")  # Debugging
            self._send_goal_future = self._action_client.send_goal_async(
                joint_values, feedback_callback=self.feedback_callback)
            
            self._send_goal_future.add_done_callback(self.goal_response_callback)

        except Exception as e:
            print(f"Exception in send_goal: {e}")  # Debugging
            return f"Error sending joint angles: {e}"


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

    
    def get_joint_values_from_location(self, location: str) -> list:
        coordinates = { # Predefined joint angles for different locations
            'HOME-STATION': {'joint_1': '0.0', 'joint_2': '0.0', 'joint_3': '0.0', 'joint_4': '0.0', 'joint_5': '0.0', 'joint_6': '0.0', 'joint_7': '0.0'},
            'START-STATION': {'joint_1': '0.1745', 'joint_2': '0.2618', 'joint_3': '0.3491', 'joint_4': '0.4363', 'joint_5': '0.5236', 'joint_6': '0.5236', 'joint_7': '0.5236'},
            'WELDING-STATION': {'joint_1': '0.0873', 'joint_2': '0.1745', 'joint_3': '0.2618', 'joint_4': '0.3491', 'joint_5': '0.4363', 'joint_6': '0.5236', 'joint_7': '0.5236'},
            'COOLING-STATION': {'joint_1': '0.0524', 'joint_2': '0.1047', 'joint_3': '0.1571', 'joint_4': '0.2094', 'joint_5': '0.2618', 'joint_6': '0.3142', 'joint_7': '0.3665'},
            'PAINTING-STATION': {'joint_1': '0.3491', 'joint_2': '0.4363', 'joint_3': '0.5236', 'joint_4': '0.5236', 'joint_5': '0.5236', 'joint_6': '0.5236', 'joint_7': '0.5236'},
            'END-STATION': {'joint_1': '0.0698', 'joint_2': '0.1396', 'joint_3': '0.2094', 'joint_4': '0.2793', 'joint_5': '0.3491', 'joint_6': '0.4189', 'joint_7': '0.4887'},
        }
        self.get_logger().info(f"Received location to find joint angles for: location={location}")
        
        key = f'{location.upper()}-STATION'
        if key not in coordinates:
            return []  # Return empty list i location does not exist

        # Omdan dictionary-værdierne til en liste af integers
        joint_values = [float(coordinates[key][f'joint_{i}']) for i in range(1, 8)]
        
        return joint_values

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


    async def run(self, model: str = 'llama3.1:8b', use_speech: bool = False):
        # Initialize conversation with a user query
        messages = [{'role': 'system', 'content': f'''
                Your name is Janise. You are an AI robotic dual arm assistant which can perform relevant robotics tasks based on user commands. 
                You are to assume the persona of a butler and address me with "sir". 
                     
                Your job is to call functions that will result in the users command to be succesfully achieved.
                Successfully performing a task will require you to call the correct functions in the correct order.
                Notice that you sometimes must call mutliple functions to achieve specific tasks.
                     
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
            response = await self.llm.chat(
                model=model,
                messages=messages,
                tools=[
                    {
                        'type': 'function',
                        'function': {
                            'name': 'get_joint_values_from_location',
                            'description': 'Retrieve the robot joint angles based on the user-specified location. The location can be specified in various forms, such as "home", "cooling station", or "painting". The function only retrieves the joint angles and does not move the robot arm.',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'location': {
                                        'type': 'string',
                                        'description': 'The name of the target location, which can be given in shorthand (e.g., "home", "cooling").',
                                    }
                                },
                                'required': ['location'],
                            },
                        },
                    },
                    {
                        'type': 'function',
                        'function': {
                            'name': 'send_goal',
                            'description': 'Send joint angles to the robot service to move it to the specified joint positions. Ensure that valid joint angles (7 values) are available before calling this function. If no valid angles are found, return an error message and do not proceed.',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'joint_values': {
                                        'type': 'float',
                                        'description': 'A list of joint values for the robot arm. Must contain exactly 7 values. If less or more, this function should not be called.',
                                    }
                                },
                                'required': ['joint_values'],
                            },
                        },
                    },
                    {
                        'type': 'function',
                        'function': {
                            'name': 'find_object',
                            'description': 'Find the object in the environment using the object detector service. The object name should be provided as an argument to this function. The object detector service will return the number of objects found as well as the cartesian center point, width, height and orientation of each object.',
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
                ]
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

            # Second API call: Get final response from the model
            final_response = await self.llm.chat(model=model, messages=messages)
            final_response_text = final_response['message']['content']

            # Add the model's response to the conversation history
            messages.append(response['message'])
            
            # Convert final response to speech
            self.text_to_speech(final_response_text)

def main(args=None):
    rclpy.init(args=args)
    node = LLMNode()


    # Start LLM workflow
    try:
        asyncio.run(node.run())  # Use asyncio.run instead of get_event_loop
    except KeyboardInterrupt:
        pass  # Makes it possible to exit using CTRL+C
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
