from gtts import gTTS
import speech_recognition as sr
from googletrans import Translator
import playsound
import os

translator = Translator()

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



def translator_fun(text, src_lang):
    return translator.translate(text, src=src_lang, dest='en')


def text_to_voice(text_data):
    myobj = gTTS(text=text_data, lang='en', slow=False)
    myobj.save("cache_file.mp3")
    playsound.playsound("cache_file.mp3")
    os.remove("cache_file.mp3")


def main():
    print("Choose a language to translate from:")
    for code, language in languages.items():
        print(f"{code}: {language}")

    src_lang = input("Enter the language code: ").strip()

    if src_lang not in languages:
        print("Invalid language code. Exiting.")
        return

    while True:
        rec = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=25)

        try:
            print("Processing...")
            spoken_text = rec.recognize_google(audio, language=src_lang)

            print("Translating...")
            translated_text = translator_fun(spoken_text, src_lang)

            print("Text to Speech...")
            text_to_voice(translated_text.text)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
