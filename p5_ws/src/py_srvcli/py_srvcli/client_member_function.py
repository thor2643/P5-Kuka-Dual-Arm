#LLM Librarys:
import json
import ollama
import asyncio
import rclpy
from rclpy.node import Node
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

#general Node structure:
from tutorial_interfaces.srv import GetSevenInts                             
import sys
import rclpy
from rclpy.node import Node


class LLMNode(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        self.llm = ollama.AsyncClient()  # Initialize the Ollama client for LLM interactions
        self.microphone_index = 8 # Specify a specific microphone if needed
        self.microphone_timeout = 10

        # Service client for moving the robot arm(s)
        self.cli = self.create_client(GetSevenInts, 'get_seven_ints')  # Client for ROS2 service

        # Wait for the service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service move_robot is not available, waiting...')
        self.req = GetSevenInts.Request() 


    def send_request(self, jointvalues):
        # Forvent, at jointvalues er en liste med 7 float-værdier
        if len(jointvalues) != 7:
            raise ValueError("Incorrect number of joint angles. Expected 7 values.")

        self.req.joint_1, self.req.joint_2, self.req.joint_3, self.req.joint_4, self.req.joint_5, self.req.joint_6, self.req.joint_7 = jointvalues

        self.get_logger().info(f"Sending joint values: a={self.req.a}, b={self.req.b}, c={self.req.c}, d={self.req.d}, e={self.req.e}, f={self.req.f}, g={self.req.g}")

        # Kalder ROS-service og venter på svar
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        
        return self.future.result()  # Returnerer resultatet af servicen
    

    def get_joint_angles_from_location(self, location: str) -> list:
        """Returns joint angles for a specific location as a list of integers."""
        coordinates = {
            'HOME-STATION': {'joint_1': '0', 'joint_2': '0', 'joint_3': '0', 'joint_4': '0', 'joint_5': '0', 'joint_6': '0', 'joint_7': '0'},
            'START-STATION': {'joint_1': '10', 'joint_2': '15', 'joint_3': '20', 'joint_4': '25', 'joint_5': '30', 'joint_6': '35', 'joint_7': '40'},
            'WELDING-STATION': {'joint_1': '5', 'joint_2': '10', 'joint_3': '15', 'joint_4': '20', 'joint_5': '25', 'joint_6': '30', 'joint_7': '35'},
            'COOLING-STATION': {'joint_1': '3', 'joint_2': '6', 'joint_3': '9', 'joint_4': '12', 'joint_5': '15', 'joint_6': '18', 'joint_7': '21'},
            'PAINTING-STATION': {'joint_1': '20', 'joint_2': '25', 'joint_3': '30', 'joint_4': '35', 'joint_5': '40', 'joint_6': '45', 'joint_7': '50'},
            'END-STATION': {'joint_1': '4', 'joint_2': '8', 'joint_3': '12', 'joint_4': '16', 'joint_5': '20', 'joint_6': '24', 'joint_7': '28'},
        }
        self.get_logger().info(f"Received location to find joint angles for: location={location}")
        
        key = f'{location.upper()}-STATION'
        if key not in coordinates:
            return []  # Return empty list i location does not exist

        # Omdan dictionary-værdierne til en liste af integers
        joint_angles = [int(coordinates[key][f'joint_{i}']) for i in range(1, 8)]
        
        return joint_angles



    def send_joint_angles_to_robot(self, joint_angles: list) -> str:
        """Sends joint angle values to the ROS2 service."""
        try:
            # Check if 7 joint angles are present in list
            if len(joint_angles) != 7:
                raise ValueError("Incorrect number of joint angles provided. Expected 7 values.")
            
            # Send joint vinklerne til ROS service
            self.send_request(joint_angles)
            return "Joint angles sent successfully to the robot service."
        except Exception as e:
            return f"Error sending joint angles: {e}"



    def speech_to_text(self):
        """Capture audio from microphone and convert to text with a timeout."""
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
        """Convert text to speech and play it."""
        self.get_logger().info(f"Converting text to speech: {text}")
        try:
            unique_filename = f"output_{os.getpid()}.mp3"
            tts = gTTS(text=text, lang='en')
            tts.save(unique_filename)
            playsound(unique_filename)
            os.remove(unique_filename)
        except Exception as e:
            self.get_logger().error(f"Failed to convert text to speech: {e}")


    async def run(self, model: str = 'llama3-groq-tool-use', use_speech: bool = False):
        # Initialize conversation with a user query
        messages = [{'role': 'user', 'content': f'''Your name is Janise. You are an AI robotic arm assistant which uses the LLM llama3-groq-tool-use for task reasoning and manipulation task. You are to assume the persona of a butler and address me with "sir". 
                     
                Your job is to move the arm to different locations based on the user's requests.
                First, retrieve the joint angles for the location using the function get_joint_angles_from_location(location).
                Only if valid joint angles are retrieved should you proceed to call the send_joint_angles_to_robot(joint_angles) function.
                If joint angles are not available, inform the user and ask for clarification.
                
                You are only permitted to use functions that I have specified. If you are in doubt, please ask the operator to repeat themselves. 
                Your job is to decide whether to use one of the following functions based on the user's request:
                1. Use the `get_joint_angles_from_location(location)` function when the user asks to move the robot to a location.
                2. After retrieving the joint angles, use the `send_joint_angles_to_robot(joint_angles)` function to move the robot.
                3. If the user input is unrelated to moving the robot, respond without calling any functions.

                Also, if the location is not specified in the examples provided later on, still try to parse them to the function `get_joint_angles_from_location("location")`. This will then either return a list of joint values or an empty list, and then you can take it from there.    

                [The following are all built-in function descriptions]
                Get joint angles required to reach a specific location: get_joint_angles_from_location(location)
                Move the robot to a designated location: send_joint_angles_to_robot(joint_angles)

                [Here are some specific examples]
                My instruction: Move the gripper to production home. You output: {{'function':['get_joint_angles_from_location(home)', 'send_joint_angles_to_robot([0, 0, 0, 0, 0, 0, 0])'], 'response':'Moving the robot to home position.'}}
                My instruction: Begin moving the gripper to cooling station. You output: {{'function':['get_joint_angles_from_location(cooling)', 'send_joint_angles_to_robot([3, 6, 9, 12, 15, 18, 21])'], 'response':'Moving the robot to cooling station.'}}
                My instruction: Make me a millionaire. You output: {{'function':[], 'response':'I am unable to fulfill your request.'}}
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

            # Perform the POST request with data
            response = await self.llm.chat(
                model=model,
                messages=messages,
                tools=[
                    {
                        'type': 'function',
                        'function': {
                            'name': 'get_joint_angles_from_location',
                            'description': 'Retrieve the robot joint angles based on the user-specified location. The location can be specified in various forms, such as "home", "cooling station", or "painting". These are mapped to predefined locations like "PRODUCTION-HOME" or "PRODUCTION-COOLING".',
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
                            'name': 'send_joint_angles_to_robot',
                            'description': 'Send joint angles to the robot service to move it to the specified joint positions. Ensure that valid joint angles (7 values) are available before calling this function. If no valid angles are found, return an error message and do not proceed.',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'joint_angles': {
                                        'type': 'array',
                                        'description': 'A list of joint values for the robot arm. Must contain exactly 7 values. If less or more, this function should not be called.',
                                    }
                                },
                                'required': ['joint_angles'],
                            },
                        },
                    }
                ]
            )

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
                    'get_joint_angles_from_location': self.get_joint_angles_from_location,
                    'send_joint_angles_to_robot': self.send_joint_angles_to_robot,
                }
                
                for tool in response['message']['tool_calls']:
                    function_to_call = available_functions[tool['function']['name']]

                    if tool['function']['name'] == 'get_joint_angles_from_location':
                        # Call get_joint_angles_from_location and check if joint angles are valid
                        function_response = function_to_call(tool['function']['arguments']['location']) 
                        
                        if not function_response:  # If no valid joint angles were found
                            messages.append({'role': 'tool', 'content': 'No valid joint angles found for this location.'})
                            break  # Stop the process here, do not call send_joint_angles_to_robot

                        # Add the joint angles to the conversation history
                        messages.append({'role': 'tool', 'content': f"Retrieved joint angles: {function_response}"})
                        print(function_response)

                    elif tool['function']['name'] == 'send_joint_angles_to_robot':
                        # Only proceed if the previous call returned valid joint angles
                        function_response = function_to_call(tool['function']['arguments']['joint_angles']) 
                        
                        # Add the robot movement response to the conversation
                        messages.append({'role': 'tool', 'content': function_response})

            # Second API call: Get final response from the model
            final_response = await self.llm.chat(model=model, messages=messages)
            final_response_text = final_response['message']['content']
            print(final_response_text)
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
