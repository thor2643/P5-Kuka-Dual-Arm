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
from project_interfaces.srv import GetSixInts                             
import sys
import rclpy
from rclpy.node import Node


class LLMNode(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        self.llm = ollama.AsyncClient()  # Initialize the Ollama client for LLM interactions
        self.microphone_index = 8 # You can specify a specific microphone if needed

        # Service client for moving the robot arm(s)
        self.cli = self.create_client(GetSixInts, 'get_six_ints')  # Client for ROS2 service

        # Wait for the service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service move_robot is not available, waiting...')
        self.req = GetSixInts.Request() 

    def send_request(self, jointvalues):
        self.req.a = float(jointvalues[0])  
        self.req.b = float(jointvalues[1])
        self.req.c = float(jointvalues[2])     
        self.req.d = float(jointvalues[3])
        self.req.e = float(jointvalues[4])
        self.req.f = float(jointvalues[5])    
        self.req.g = float(jointvalues[6])                                     
        self.future = self.cli.call_async(self.req)

    """
    async def call_move_robot_service(self):
        "Kald ROS2-servicen for at starte robotbevægelsen." #her var der 3 x " på hver side
        request = Trigger.Request()  
        future = self.cli.call_async(request)

        # Wait for the result
        while not future.done():
            await asyncio.sleep(0.1)  

        try:
            response = future.result()
            if response.success:
                self.get_logger().info(f'Service result: {response.message}')
                return f"Robot is moving: {response.message}"
            else:
                self.get_logger().error(f'Service failed: {response.message}')
                return f"Service call failed: {response.message}"
        except Exception as e:
            self.get_logger().error(f"Service call failed with error: {e}")
            return f"Service call failed with error: {e}"
    """

    async def send_request_to_llm(self, user_input):
        """Send request to LLM (Ollama) using LangChain."""
        messages = [{
            'role': 'user', 
            'content': f'''Your name is Janise. You are an AI robotic arm assistant which uses the LLM llama3-groq-tool-use for task reasoning and manipulation task. You are to assume the persona of a butler and address me with "sir". You use a service called `MoveRobotInWorld`, which moves the robot between two predefined locations in a repetitive motion.

                Your task is to generate a command that will initiate the movement of the robot between these locations. The movement does not require any arguments, as the locations are already defined in the system.
                
                You are only permitted to use functions that I have specified. If you are in doubt, please ask the operator to repeat themselves. You can use the following functions to perform the task:
                
                [The following are all built-in function descriptions]
                Move the robot between to designated locations: move_robot()

                [Here are some specific examples]
                My instruction: Move the robot. You output: {{'function':['move_robot()'], 'response':'Moving the robot.'}}
                My instruction: Start moving the robot. You output: {{'function':['move_robot()'], 'response':'Commencing movement of the robot.'}}
                My instruction: Make me a millionaire. You output: {{'function':[], 'response':'I am unable to fulfill your request.'}}
            '''
        }]
        
        # Call LLM and receive its answer
        response = await self.llm.chat(
            model='llama3-groq-tool-use',
            messages=messages
        )

        llm_response = response['message']['content']

        # If the LLM proposes to move the robot, print it and call the service.
        if "move_robot" in llm_response.lower():
            self.get_logger().info("LLM has proposed to move the robot")
            
            # Call the service that moves the robot
            robot_response = await self.send_request()   # call_move_robot_service

            # Save the response
            llm_response = robot_response

        # Return the answer/response
        return llm_response

    def speech_to_text(self):
        """Capture audio from microphone and convert to text."""
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone(device_index=self.microphone_index) as source:
                self.get_logger().info("Listening for speech...")
                audio = recognizer.listen(source)

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

   # Simulates an API to move the gripper to a specific location in world coordinates
    def move_gripper_in_world(self, location: str) -> str:
        coordinates = {
        'PRODUCTION-HOME': {'joint_1': '0', 'joint_2': '0', 'joint_3': '0', 'joint_4': '0', 'joint_5': '0', 'joint_6': '0', 'joint_7': '0'},
        'PRODUCTION-START': {'joint_1': '10', 'joint_2': '15', 'joint_3': '20', 'joint_4': '25', 'joint_5': '30', 'joint_6': '35', 'joint_7': '40'},
        'PRODUCTION-WELDING': {'joint_1': '5', 'joint_2': '10', 'joint_3': '15', 'joint_4': '20', 'joint_5': '25', 'joint_6': '30', 'joint_7': '35'},
        'PRODUCTION-COOLING': {'joint_1': '3', 'joint_2': '6', 'joint_3': '9', 'joint_4': '12', 'joint_5': '15', 'joint_6': '18', 'joint_7': '21'},
        'PRODUCTION-PAINTING': {'joint_1': '20', 'joint_2': '25', 'joint_3': '30', 'joint_4': '35', 'joint_5': '40', 'joint_6': '45', 'joint_7': '50'},
        'PRODUCTION-END': {'joint_1': '4', 'joint_2': '8', 'joint_3': '12', 'joint_4': '16', 'joint_5': '20', 'joint_6': '24', 'joint_7': '28'},
        }

        key = location.upper()
        return json.dumps(coordinates.get(key, {'error': 'Coordinates cannot be reached'}))


    async def run_llm_workflow(self):
        """Run the LLM workflow: Listen > Process > Respond."""
        while True: 
            self.get_logger().info('Waiting for user input...')
            user_input = self.speech_to_text()

            if user_input and not user_input.startswith("Error"):
                self.get_logger().info(f'User said: {user_input}')

                # Send input to LLM to get a response
                llm_response = await self.send_request_to_llm(user_input)
                self.get_logger().info(f'LLM response: {llm_response}')

                # Play the response using text-to-speech
                self.text_to_speech(llm_response)
            else:
                self.get_logger().error('Failed to obtain valid speech input')

    async def run(self, model: str):
        client = ollama.AsyncClient()
        # Initialize conversation with a user query
        messages = [{'role': 'user', 'content': '''Your name is Jarvis. You are an AI robotic arm assistant which can text-to-text assistance. You use LLM for task reasoning and manipulation task. The LLM you are using is Llama3-groq-tool-use from Ollama. You are to assume the persona of a butler and address me with "sir". The robotic arm has some built-in functions. Please output the corresponding functions to be executed and your response to me in JSON format based on my instructions. It is very important that you output the function you use and the argument you pass to them. You are only permitted to use functions that I have specified. If you are in doubt, please ask the operator to repeat themselves. You can use the following functions to perform the task.

            [The following are all built-in function descriptions]
            Move the gripper to a specific location in world coordinates: move_gripper_in_world(location)
            Perform head shaking motion: head_shake()
            Perform nodding motion: head_nod()
            Perform dancing motion: head_dance()

            Further explanation of move_gripper_in_world() function: You can use the function to find the coordinates of a designated area described with all capital letters. The function will return the coordinates of the designated area in the form of a JSON object. The JSON object will contain the x, y and z coordinates of the designated area, as well as the duration of the movement in seconds. Please extract the x, y and z coordinates from the JSON object and use them to move the gripper to the designated area. A designated area could be such as the cooling station would be called PRODUCTION-COOLING. The function will return an error message if the designated area is not found.
                
            [Output JSON format]
            In the 'function' key, output a list of function names, each element in the list is a string representing the function name and parameters to run. Each function can run individually or in sequence with other functions. The order of list elements indicates the order of function execution.
            In the 'response' key, based on my instructions and your arranged actions, output your reply to me in first person, no more than 20 words.

            [Here are some specific examples]
            My instruction: Move to production start position. You output: {'function':['move_gripper_in_world(PRODUCTION-HOME)'], 'response':'Moving to production start position (100, 100, 100).'}
            My instruction: Move to cooling station. You output: {'function':['move_gripper_in_world(PRODUCTION-COOLING)'], 'response':'Moving to cooling station (40, 60, 60).'}
            My instruction: Make me a millionaire. You output: {'function':['head_shake()'], 'response':'I am unable to fulfill your request.'}

            [My instruction:]
            '''}]

        while True:
            # Convert speech to text
            prompt = self.speech_to_text()
            if prompt is None:
                continue

            # Add user input to messages
            messages.append({'role': 'user', 'content': prompt})

            # Perform the POST request with data
            response = await client.chat(
                model=model,
                messages=messages,
                tools=[
                    {
                        'type': 'function',
                        'function': {
                            'name': 'move_gripper_in_world',
                            'description': 'Move the gripper to a specific location described by its name (e.g., PRODUCTION-HOME).',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'location': {
                                        'type': 'string',
                                        'description': 'The name of the target location in all capital letters (e.g., PRODUCTION-COOLING).',
                                    }
                                },
                                'required': ['location'],
                            },
                        },
                    },
                ], 
            )

            # Add the model's response to the conversation history
            messages.append(response['message'])

            # Check if the model decided to use the provided function
            if not response['message'].get('tool_calls'):
                print("The model didn't use the function. Its response was:")
                response_text = response['message']['content']
                print(response_text)
                # Convert model's response to speech
                self.text_to_speech(response_text)
                continue

            # Process function calls made by the model
            if response['message'].get('tool_calls'):
                available_functions = {
                    'move_gripper_in_world': self.move_gripper_in_world,
                }
                for tool in response['message']['tool_calls']:
                    function_to_call = available_functions[tool['function']['name']]
                    function_response = function_to_call(tool['function']['arguments']['location']) 
                    # Add function response to the conversation
                    messages.append(
                        {
                            'role': 'tool',
                            'content': function_response,
                        }
                    )

            # Second API call: Get final response from the model
            final_response = await client.chat(model=model, messages=messages)
            final_response_text = final_response['message']['content']
            print(final_response_text)
            # Convert final response to speech
            self.text_to_speech(final_response_text)

def main(args=None):
    rclpy.init(args=args)
    node = LLMNode()
    #her køres LLM som giver 7 værdier.

    #asyncio.run('llama3-groq-tool-use')


    jointvalues = [1, 2,3,4,5,6,7]

    node.send_request(jointvalues)

    while rclpy.ok():
        rclpy.spin_once(node)
        if node.future.done():
            try:
                response = node.future.result()
            except Exception as e:
                node.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                node.get_logger().info(
                    'Result for sending: %f, %f, %f, %f, %f, %f, %f. Succes = %d' %                                 
                    (node.req.a, node.req.b, node.req.c, node.req.d, node.req.e, node.req.f, node.req.g, response.succes))   
            break

    """
    try:
        # Start LLM workflow in an endless loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(node.run_llm_workflow())
    except KeyboardInterrupt:
        pass  # Possibility for exit using CTRL+c
    finally:
        node.destroy_node()
        rclpy.shutdown()
    """

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
