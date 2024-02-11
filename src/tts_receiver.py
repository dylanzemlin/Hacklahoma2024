#! python3.7
import socket
from rosie.tts import TTS
from rosie.interface import Face, FaceLcdWriter
import time


HOST = "24.144.83.34"
PORT = 65433


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
type_message = "TEXTTOSPEECH"
sock.sendall(type_message.encode())


def main():
    global sock
    tts = TTS()
    writer = FaceLcdWriter()
    writer.open()
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            decoded = data.decode()
            print(decoded)
            
            # this can just carry on in the background or something idk
            writer.write_lcd(decoded)

            # start the speak
            tts.speak(decoded)
            tts.engine.startLoop()

            # loop and do face stuff while its speaking
            lasttime = time.time()
            toggle = False
            while tts.engine.isBusy():
                writer.write_face(Face.TALKFACE if toggle else Face.NOTALKFACE)

                # flip face every quarter second
                if time.time() - lasttime > 0.25:
                    lasttime = time.time()
                    toggle = not toggle 

                tts.engine.iterate()

            tts.engine.endLoop()
            writer.write_face(Face.NOTALKFACE)

            
            # Write to "temp.mp3" until b"DONE"
            with open("temp.mp3", "wb") as f:
                while True:
                    f.write(data)
                    data = sock.recv(1024)
                    if data == b"DONE":
                        break
                
            # Play the file
            import os
            os.system("mpg123 temp.mp3")
        except KeyboardInterrupt:
            print("Exiting...")
            sock.close()
            writer.close()
            break


if __name__ == "__main__":
    main()
