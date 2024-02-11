#! python3.7
import socket
import threading
from rosie.tts import TTS


HOST = "24.144.83.34"
PORT = 65433


def main():
    def record_callback() -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        
        type_message = "RESPONSE"
        sock.sendall(type_message.encode())
        
        while True:
            data = sock.recv(1024 * 1024)
            if not data:
                break
            # Convert data to txt and print
            print(data.decode())

    speech_thread = threading.Thread(target=record_callback, args=())
    speech_thread.daemon = True
    speech_thread.start()
    
    while True:
        try:
            pass
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
