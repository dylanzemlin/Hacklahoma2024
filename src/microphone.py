#! python3.7
import speech_recognition as sr
import time
import socket

HOST = "24.144.83.34"
PORT = 65431
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
type_message = "MICROPHONE"
sock.sendall(type_message.encode())

def record_callback(_, audio:sr.AudioData) -> None:
    global sock
    # Grab the raw bytes and push it into the thread safe queue.
    data = audio.get_raw_data()
    try:
        sock.sendto(data, (HOST, PORT))
    except Exception as e:
        print(f"Failed to send data to {HOST}:{PORT}: {e}")
        try:
            sock.close()
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            type_message = "MICROPHONE"
            sock.sendall(type_message.encode())
        except Exception as e:
            print(f"Failed to reconnect to {HOST}:{PORT}: {e}")

def main():
    # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = 3200

    source = sr.Microphone(sample_rate=16000)
    with source:
        recorder.adjust_for_ambient_noise(source, duration = 3)

    # Create a background thread that will pass us raw audio bytes.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=5)
    
    while True:
        try:
            time.sleep(0.25)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
