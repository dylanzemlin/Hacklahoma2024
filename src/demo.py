#! python3.7
import socket

HOST = "24.144.83.34"
PORT = 62431
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
type_message = "MICROPHONE"
sock.sendall(type_message.encode())

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    type_message = "MICROPHONE"
    sock.sendall(type_message.encode())
    sock.sendall(b"DEMO_MSG")


if __name__ == "__main__":
    main()
