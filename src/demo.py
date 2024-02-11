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
    time.sleep(3)
    sock.sendall("Hi, I am Rosie, your personal assistant. How can I help you today?".encode())


if __name__ == "__main__":
    main()
