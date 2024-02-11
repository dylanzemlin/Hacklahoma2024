#! python3.7
import socket
from rosie.tts import TTS


HOST = "24.144.83.34"
PORT = 65433


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
type_message = "TEXTTOSPEECH"
sock.sendall(type_message.encode())


def main():
    global sock
    while True:
        try:
            data = sock.recv(1024 * 1024)
            if not data:
                break
            decoded = data.decode()
            print(decoded)
            TTS().speak(decoded)
        except KeyboardInterrupt:
            print("Exiting...")
            sock.close()
            break


if __name__ == "__main__":
    main()
