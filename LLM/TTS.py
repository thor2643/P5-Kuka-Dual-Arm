# Install libraries to Enable the Text to Speech (TTS)
# ===================================================
# Step 1: install library gTTS (Google Text-to-Speech), 
# a Python library to interface with Google TTS API
# 
# pip3 install gtts 
# ===================================================
# Step 2: install playsound for playing sound
# 
# pip3 install playsound
# ==================================================

from gtts import gTTS
from playsound import playsound
import os

def text_to_speech(text, lang='en', filename='output.mp3'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Save the audio file
    tts.save(filename)
    print('Audio content written to file...')
    
    # Play the audio file
    print("Playing the generated audio...")
    playsound(filename)

def main():
    # Get text input from the user
    user_text = input("Enter the text you want to convert to speech: ")
    
    # Convert text to speech and play it
    text_to_speech(user_text)
    

if __name__ == "__main__":
    main()