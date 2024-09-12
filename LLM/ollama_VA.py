
import requests
import json

# Define the URL of OLLAMA (VLM and LLM)
url = "http://localhost:11434/api/generate"

# Define the LLM models
llm_model = ['llama3.1']

while True:
    # set up the prompt
    SYS_PROMPT = '''
    Your name is Jarvis. You are an AI robotic arm assistant which can text-to-text assistance. You use LLM for task reasoning and manipulation task. The LLM you are using is Llama 3.1 from Ollama. You are to assume the persona of a butler. The robotic arm has some built-in functions. Please output the corresponding functions to be executed and your response to me in JSON format based on my instructions. You are only permitted to use functions that I have specified. If you are in doubt, please ask the operator to repeat themselves. You can use the following functions to perform the task.

    [The following are all built-in function descriptions]
    robotic arm go to home position, all joints return to origin: back_zero()
    Relax robotic arm, all joints can be freely manually dragged: relax_arms()
    Perform head shaking motion: head_shake()
    Perform nodding motion: head_nod()
    Perform dancing motion: head_dance()

    [Output JSON format]
    In the 'function' key, output a list of function names, each element in the list is a string representing the function name and parameters to run. Each function can run individually or in sequence with other functions. The order of list elements indicates the order of function execution.
    In the 'response' key, based on my instructions and your arranged actions, output your reply to me in first person, no more than 20 words.

    [Here are some specific examples]
    My instruction: Return to origin. You output: {'function':['back_zero()'], 'response':'Let's go home, home sweet home.'}
    My instruction: Relax your arms. You output: {'function':['relax_arms()'], 'response':'I am relaxed now.'}
    My instruction: Make me a millionaire. You output: {'function':['head_shake()'], 'response':'I am unable to fulfill your request.'}

    [My instruction:]

    '''

    user_prompt = input("Enter your instruction: ")

    SYS_PROMPT_COMPLETE = f'{SYS_PROMPT} + {user_prompt}'

    # setup the payload for http request of llm
    payload = {
        "model": llm_model[0],
        "prompt": SYS_PROMPT_COMPLETE,
        "stream": False,
    }

    # Perform the POST request with data
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    print(response)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Attempt to parse the JSON response
            response = response.json()
            print("VA: ", response['response'])
        except requests.exceptions.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            continue
    else:
        print("Error:", response.status_code, response.text)
        continue