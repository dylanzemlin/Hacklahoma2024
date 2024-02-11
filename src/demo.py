#! python3.7
import socket
import time

HOST = "24.144.83.34"
PORT = 62433

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    type_message = "RESPONSE"
    sock.sendall(type_message.encode())
    time.sleep(1)
    sock.sendall(b"Hi, I am Rosie, your personal assistant. How can I help you today?")


if __name__ == "__main__":
    main()
