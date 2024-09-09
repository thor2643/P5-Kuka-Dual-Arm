
import requests
import json

# Define the URL of OLLAMA (VLM and LLM)
url = "http://localhost:11434/api/generate"

# Define the LLM models
llm_model = ['llama3.1']

while True:

    prompt = input("user: ")

    # setup the payload for http request of llm
    payload = {
        "model": llm_model[0],
        "prompt": prompt,
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