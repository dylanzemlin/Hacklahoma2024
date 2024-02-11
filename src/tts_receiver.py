#! python3.7
import socket
from rosie.tts import TTS
from rosie.interface import Face, FaceLcdWriter


HOST = "24.144.83.34"
PORT = 65433


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
type_message = "TEXTTOSPEECH"
sock.sendall(type_message.encode())


def main():
    global sock
    tts = TTS()
    # writer = FaceLcdWriter()
    # writer.open()
    while True:
        try:
            data = sock.recv(1024 * 1024)
            if not data:
                break
            # decoded = data.decode()
            # print(decoded)
            
            # writer.write_face(Face.SPEAK)
            # writer.write_lcd(decoded)
            # tts.speak(decoded)
            # writer.write_face(Face.NOSPEAK)

            
            # Write data to a file and play it (.mp3)
            with open("temp.mp3", "wb") as f:
                f.write(data)
                
            # Play the file
            import os
            os.system("mpg123 temp.mp3")
        except KeyboardInterrupt:
            print("Exiting...")
            sock.close()
            # writer.close()
            break


if __name__ == "__main__":
    main()
