#! python3.7
import socket, os

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
            # Read in temp.mp3 as 1024 * 1024 * 128 bytes
            data = sock.recv(1024 * 1024 * 128)
            if not data:
                break
            print("Received data")
            with open("temp.mp3", "wb") as f:
                f.write(data)
                
            # Play the audio
            os.system("mpg123 temp.mp3")
        except KeyboardInterrupt:
            print("Exiting...")
            sock.close()
            # writer.close()
            break


if __name__ == "__main__":
    main()
