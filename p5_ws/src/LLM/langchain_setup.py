import os
import json
import ollama
import asyncio
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# Define your speech-to-text function

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Request error from Google Speech Recognition service")
        return None

# Define your text-to-speech function
def text_to_speech(text, lang='en', filename='output.mp3'):
    # Create a unique filename using a timestamp
    from time import time
    unique_filename = f"output_{int(time())}.mp3"

    # Create a gTTS object
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Save the audio file
    tts.save(unique_filename)
    print('Audio content written to file:', unique_filename)
    
    # Play the audio file
    print("Playing the generated audio...")
    try:
        playsound(unique_filename)
    except Exception as e:
        print(f"Error playing sound: {e}")
    finally:
        # Clean up the file
        if os.path.exists(unique_filename):
            os.remove(unique_filename)

# Simulates an API to move the gripper to a specific location in world coordinates
def move_gripper_in_world_coords(location: str) -> str:
    coordinates = {
        'PRODUCTION-HOME': {'x_coordinate': '100', 'y_coordinate': '100', 'z-coordinate': '100'},
        'PRODUCTION-START': {'x_coordinate': '50', 'y_coordinate': '120', 'z-coordinate': '20'},
        'PRODUCTION-WELDING': {'x_coordinate': '30', 'y_coordinate': '70', 'z-coordinate': '40'},
        'PRODUCTION-COOLING': {'x_coordinate': '40', 'y_coordinate': '60', 'z-coordinate': '60'},
        'PRODUCTION-PAINTING': {'x_coordinate': '130', 'y_coordinate': '20', 'z-coordinate': '90'},
        'PRODUCTION-END': {'x_coordinate': '35', 'y_coordinate': '75', 'z-coordinate': '70'},
    }

    key = location.upper()
    return json.dumps(coordinates.get(key, {'error': 'Coordinates cannot be reached'}))

async def run(model: str):
    client = ollama.AsyncClient()
    # Initialize conversation with a user query
    messages = [{'role': 'user', 'content': '''Your name is Jarvis. You are an AI robotic arm assistant which can text-to-text assistance. You use LLM for task reasoning and manipulation task. The LLM you are using is Llama3-groq-tool-use from Ollama. You are to assume the persona of a butler and address me with "sir". The robotic arm has some built-in functions. Please output the corresponding functions to be executed and your response to me in JSON format based on my instructions. It is very important that you output the function you use and the argument you pass to them. You are only permitted to use functions that I have specified. If you are in doubt, please ask the operator to repeat themselves. You can use the following functions to perform the task.

        [The following are all built-in function descriptions]
        Move the gripper to a specific location in world coordinates: move_gripper_in_world_coords(location)
        Perform head shaking motion: head_shake()
        Perform nodding motion: head_nod()
        Perform dancing motion: head_dance()

        Further explanation of move_gripper_in_world_coords() function: You can use the function to find the coordinates of a designated area described with all capital letters. The function will return the coordinates of the designated area in the form of a JSON object. The JSON object will contain the x, y and z coordinates of the designated area, as well as the duration of the movement in seconds. Please extract the x, y and z coordinates from the JSON object and use them to move the gripper to the designated area. A designated area could be such as the cooling station would be called PRODUCTION-COOLING. The function will return an error message if the designated area is not found.
               
        [Output JSON format]
        In the 'function' key, output a list of function names, each element in the list is a string representing the function name and parameters to run. Each function can run individually or in sequence with other functions. The order of list elements indicates the order of function execution.
        In the 'response' key, based on my instructions and your arranged actions, output your reply to me in first person, no more than 20 words.

        [Here are some specific examples]
        My instruction: Move to production start position. You output: {'function':['move_gripper_in_world_coords(PRODUCTION-HOME)'], 'response':'Moving to production start position (100, 100, 100).'}
        My instruction: Move to cooling station. You output: {'function':['move_gripper_in_world_coords(PRODUCTION-COOLING)'], 'response':'Moving to cooling station (40, 60, 60).'}
        My instruction: Make me a millionaire. You output: {'function':['head_shake()'], 'response':'I am unable to fulfill your request.'}

        [My instruction:]
        '''}]

    while True:
        # Convert speech to text
        prompt = speech_to_text()
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
                        'name': 'move_gripper_in_world_coords',
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
            text_to_speech(response_text)
            continue

        # Process function calls made by the model
        if response['message'].get('tool_calls'):
            available_functions = {
                'move_gripper_in_world_coords': move_gripper_in_world_coords,
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
        text_to_speech(final_response_text)

# Run the async function
asyncio.run(run('llama3-groq-tool-use'))
