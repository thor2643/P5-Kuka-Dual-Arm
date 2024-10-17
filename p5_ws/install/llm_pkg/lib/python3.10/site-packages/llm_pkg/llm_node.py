import json
import ollama
import asyncio
from langchain_core.prompts import ChatPromptTemplate
import rclpy
from rclpy.node import Node
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
from example_interfaces.srv import Trigger  # Import Trigger service from ROS2


class LLMNode(Node):
    def __init__(self):
        super().__init__('llm_node')
        self.llm = ollama.AsyncClient()  # Initialize the Ollama client for LLM interactions
        self.microphone_index = 8 # You can specify a specific microphone if needed

        # Service client for moving the robot arm(s)
        self.cli = self.create_client(Trigger, 'move_robot')  # Client for ROS2 service

        # Wait for the service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service move_robot is not available, waiting...')

    async def call_move_robot_service(self):
        """Kald ROS2-servicen for at starte robotbevægelsen."""
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

    async def send_request_to_llm(self, user_input):
        """Send request to LLM (Ollama) using LangChain."""
        messages = [{
            'role': 'user', 
            'content': f'''Your name is Jarvis. You are an AI robotic arm assistant which uses the LLM llama3-groq-tool-use for task reasoning and manipulation task. You are to assume the persona of a butler and address me with "sir". You use a service called `MoveRobotInWorld`, which moves the robot between two predefined locations in a repetitive motion.

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
            robot_response = await self.call_move_robot_service()

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

def main(args=None):
    rclpy.init(args=args)
    node = LLMNode()

    try:
        # Start LLM workflow in an endless loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(node.run_llm_workflow())
    except KeyboardInterrupt:
        pass  # Possibility for exit using CTRL+c
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
