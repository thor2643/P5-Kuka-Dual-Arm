import speech_recognition as sr
import os
import requests
import json
from gtts import gTTS
from playsound import playsound

def speech_to_text():
    # Create a recognizer object
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something!")
        # Listen for the first phrase and extract it into audio data
        audio = recognizer.listen(source)

    # Recognize speech using Google Speech Recognition
    try:
        print("Google Speech Recognition thinks you said:")
        text = recognizer.recognize_google(audio)
        print(text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service")

def text_to_speech(text, lang='en', filename='output.mp3'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Save the audio file
    tts.save(filename)
    print('Audio content written to file...')
    
    # Play the audio file
    print("Playing the generated audio...")
    playsound(filename)

# Define the URL of OLLAMA (VLM and LLM)
url = "http://localhost:11434/api/generate"

# Define the LLM models
llm_model = ['llama3.1']

if __name__ == "__main__":
    while True:

        prompt = speech_to_text()

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
                text_to_speech(response['response'])
            except requests.exceptions.JSONDecodeError as e:
                print("JSON Decode Error:", e)
                continue
        else:
            print("Error:", response.status_code, response.text)
            continue
    


