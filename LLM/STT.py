# Install libraries to Enable the Speech Recognition
# ==================================================
# Step 1: install library for performing speech 
# recognition, with support for several engines and APIs, online and offline.
# 
# pip install SpeechRecognition
# ==================================================
# Step 2: install pyaudio library
# 
# sudo apt-get install python3-pyaudio
# ==================================================
# Step 3: FLAC conversion utility not available (error)
# 
# sudo apt-get install flac
# ==================================================

import speech_recognition as sr
import os

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


if __name__ == "__main__":
    # Speech to text
    recognized_text = speech_to_text()