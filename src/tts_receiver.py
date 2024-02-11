#! python3.7
import socket, openai, os, time, pyglet
from rosie.interface import Face, FaceLcdWriter


HOST = "24.144.83.34"
PORT = 65433


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
type_message = "TEXTTOSPEECH"
sock.sendall(type_message.encode())


client = openai.OpenAI()


def main():
    global sock
    writer = FaceLcdWriter()
    writer.opem()
    
    while True:
        try:
            response = sock.recv(1024 * 1024)
            decoded_response = response.decode()
            decoded_response = "Hey kid. " + decoded_response
            print(decoded_response)

            # this can just carry on in the background or something idk
            writer.write_lcd(decoded_response)
            
            response = client.audio.speech.create(
                model = "tts-1",
                voice = "nova",
                input = decoded_response
            )
    
            response.write_to_file("output.mp3")
            time.sleep(0.75)
            sound = pyglet.media.load("output.mp3", streaming=False)
            sound.play()

            # loop and do face stuff while its speaking
            lasttime = time.time()
            starttime = time.time()
            toggle = False
            while time.time() - starttime <= sound.duration:
                writer.write_face(Face.TALKFACE if toggle else Face.NOTALKFACE)

                # flip face every quarter second
                if time.time() - lasttime > 0.25:
                    lasttime = time.time()
                    toggle = not toggle 

            writer.write_face(Face.NOTALKFACE)

            os.remove("output.mp3")
            

            
        except KeyboardInterrupt:
            print("Exiting...")
            sock.close()
            writer.close()
            break


if __name__ == "__main__":
    main()
