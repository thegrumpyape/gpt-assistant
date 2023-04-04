import os

import openai
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

ENGINE = pyttsx3.init()


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]


def speak_text(text):
    ENGINE.say(text)
    ENGINE.runAndWait()


def main():
    load_dotenv(".env")
    # Set your OpenAI API key
    openai.api_key = os.environ.get("OPENAI_KEY")

    while True:
        # Wait for user to say "genius"
        print("Say 'Hey GPT' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hey gpt":
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(
                            source, phrase_time_limit=None, timeout=None
                        )
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    # Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        speak_text(response)
            except Exception as e:
                print(f"An error occurred: {e}")
