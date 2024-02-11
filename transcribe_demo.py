#! python3.7

import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch
from openai import OpenAI
import pyttsx3


from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform
import threading


import socket

HOST = "24.144.83.34"
PORT = 65431
WAKE_WORDS = ["hey rosy", "hey rosie", "hey rosey"]


class Rosie():
    def __init__(self):
        # https://platform.openai.com/docs/guides/text-generation/chat-completions-api

        # create the client
        self.client = OpenAI(api_key = "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")

        self.personality_msg = {
            "role": "assistant", # to modify the behavior of the assistant
            "content": "You are Rosie from The Jetsons. Do not refer to who you are speaking to in your response, be generic. Keep all of your responses very short, around 2 sentences. Please do not show temperatures in multiple units, only use fahrenheit." #this could probably be a lot better
        }

    
    def get_response(self, question: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                self.personality_msg,
                {"role":"user", "content": question}
            ],
            temperature=0.18,
            max_tokens=200
        )

        return response.choices[0].message.content # extract ChatGPT's reply


class TTS:
    def __init__(self):
        # https://pypi.org/project/pyttsx3/
        self.engine = pyttsx3.init() # object creation
        self.engine.setProperty('rate', 225)     # setting up new voice rate
        self.engine.setProperty('volume', 1.0)    # setting up volume level  between 0 and 1
        
        voices = self.engine.getProperty('voices')       #getting details of current voice   
        for idx, voice in enumerate(voices):
            if "hazel" in voice.name.lower():
                self.engine.setProperty('voice', voices[idx].id)

    def speak(self, msg):
        # self.engine.save_to_file(msg, "response.mp3")
        self.engine.say(msg)
        self.engine.runAndWait()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="medium", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the english model.")
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=2,
                        help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=3,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args()

    # The last time a recording was retrieved from the queue.
    phrase_time = None
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()

    # Load / Download model
    model = args.model
    if args.model != "large" and not args.non_english:
        model = model + ".en"
    audio_model = whisper.load_model(model, torch.device("cuda:0"))

    phrase_timeout = args.phrase_timeout

    transcription = ['']

    def record_callback() -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        
        type_message = "TRANSCRIBER"
        sock.sendall(type_message.encode())
        
        while True:
            data = sock.recv(1024 * 1024)
            if not data:
                break
            data_queue.put(data)

    speech_thread = threading.Thread(target=record_callback, args=())
    speech_thread.daemon = True
    speech_thread.start()

    # Cue the user that we're ready to go.
    print("Model loaded.\n")

    while True:
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                phrase_complete = False
                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    phrase_complete = True
                # This is the last time we received new audio data from the queue.
                phrase_time = now
                
                # Combine audio data from queue
                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()
                
                # Convert in-ram buffer to something the model can use directly without needing a temp file.
                # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
                # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                # Read the transcription.
                result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                # If we detected a pause between recordings, add a new item to our transcription.
                # Otherwise edit the existing one.
                if phrase_complete:
                    transcription.append(text)
                else:
                    transcription[-1] = text

                # Clear the console to reprint the updated transcription.
                for line in transcription:
                    # Check if line starts with any wake word (case insensitive).
                    if any(line.lower().startswith(w) for w in WAKE_WORDS):
                        detected_wake_word = filter(lambda w: line.lower().startswith(w), WAKE_WORDS)
                        # Remove the wake word
                        line = line[len(next(detected_wake_word)):].strip()
                        # Check if starts with a comma
                        if line.startswith(','):
                            line = line[1:].strip()
                        print(f"Detected wake word: {line}")
                        rose = Rosie()
                        response = rose.get_response(line)
                        print(f"Rosie: {response}")
                        tts = TTS()
                        tts.speak(response)
                        # TODO: Play mp3
                        # os.remove("response.mp3")
                        transcription = ['']

                # Infinite loops are bad for processors, must sleep.
                sleep(0.25)
        except KeyboardInterrupt:
            break

    print("\n\nTranscription:")
    for line in transcription:
        print(line)


if __name__ == "__main__":
    main()
