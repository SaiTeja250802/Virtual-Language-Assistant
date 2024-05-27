import os
import time
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import Translator

# Initializing translator and pygame mixer
translator = Translator()
pygame.mixer.init()

# Global flag to control the translation process
isTranslateOn = False

# Language mapping
languages = {
    'hi': 'Hindi',
    'bn': 'Bengali',
    'kn': 'Kannada',
    'mr': 'Marathi',
    'ta': 'Tamil',
    'gu': 'Gujarati',
    'pa': 'Punjabi',
    'te': 'Telugu',
    'ml': 'Malayalam',
    'or': 'Odia',
    'as': 'Assamese',
    'ne': 'Nepali',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh-cn': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ru': 'Russian',
    'it': 'Italian',
    'pt': 'Portuguese'
}


def get_language_code(language_name):
    for code, name in languages.items():
        if name == language_name:
            return code
    return language_name


def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)


def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")
    audio.play()
    time.sleep(audio.get_length())  # Ensure the audio plays completely before removing the file
    os.remove("cache_file.mp3")


def main_process(output_placeholder, from_language, to_language):
    global isTranslateOn
    rec = sr.Recognizer()

    while isTranslateOn:
        with sr.Microphone() as source:
            output_placeholder.text("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)

        try:
            output_placeholder.text("Processing...")
            spoken_text = rec.recognize_google(audio, language=from_language)

            output_placeholder.text("Translating...")
            translated_text = translator_function(spoken_text, from_language, to_language)

            output_placeholder.text(f"Speaking: {translated_text.text}")
            text_to_voice(translated_text.text, to_language)

        except Exception as e:
            output_placeholder.text(f"Error: {e}")


st.title("Language Translator")

# selecting languages
from_language_name = st.selectbox("Select Source Language:", list(languages.values()))
to_language_name = st.selectbox("Select Target Language:", list(languages.values()))

# Converting language names to language codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# start and stop the translation process
start_button = st.button("Start")
stop_button = st.button("Stop")

# Placeholder for displaying status messages
output_placeholder = st.empty()

# Start the translation process
if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        main_process(output_placeholder, from_language, to_language)

# Stop the translation process
if stop_button:
    isTranslateOn = False
    output_placeholder.text("Translation stopped.")

#streamlit run D:\learn\git\Virtual-Language-Assistant\streamlitapp\main.py