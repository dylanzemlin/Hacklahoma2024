#! python3.7

import argparse
import numpy as np
import whisper
import torch
import socket
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform
import threading
from rosie.chat import Rosie
from rosie.tts import TTS
import struct
import pickle, pyaudio, wave
from pydub import AudioSegment
import os


HOST = "24.144.83.34"
PORT = 65431
WAKE_WORDS = ["hey rosy", "hey rosie", "hey rosey"]


TARGET_HOST = "24.144.83.34"
TARGET_PORT = 65433


sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2.connect((TARGET_HOST, TARGET_PORT))
type_message = "RESPONSE"
sock2.sendall(type_message.encode())


def main():
    global sock2
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="small", help="Model to use", choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--energy_threshold", default=1000,help="Energy level for mic to detect.", type=int)
    parser.add_argument("--phrase_timeout", default=3, help="How much empty space between recordings before we consider it a new line in the transcription.", type=float)
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args()

    # The last time a recording was retrieved from the queue.
    phrase_time = None
    data_queue = Queue()
    model = args.model
    if args.model != "large":
        model = model + ".en"
    audio_model = whisper.load_model(model, torch.device("cuda:0"))
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
            if not data_queue.empty():
                # If we have a phrase timeout, check if we've passed it.
                phrase_complete = False
                if phrase_time and now - phrase_time > timedelta(seconds=args.phrase_timeout):
                    phrase_complete = True
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
                        
                        print(f"User: {line}")
                        rose = Rosie()
                        response = rose.get_response(line)
                        print(f"Rosie: {response}")
                        sock2.sendall(response.encode())
                                
                        transcription = ['']

                sleep(0.25)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
