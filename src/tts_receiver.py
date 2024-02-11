#! python3.7
import socket, openai, os, time, pyglet
from rosie.interface import Face, FaceLcdWriter


HOST = "24.144.83.34"
PORT = 66433


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
type_message = "TEXTTOSPEECH"
sock.sendall(type_message.encode())


client = openai.OpenAI()


def main():
    global sock
    writer = FaceLcdWriter()
    writer.open()
    
    while True:
        try:
            response = sock.recv(1024 * 1024)
            decoded_response = response.decode()
            if decoded_response == "" or decoded_response == "\n" or decoded_response == "\r\n" or decoded_response == "\r":
                continue
            
            decoded_response = "Hey kid. " + decoded_response
            print(decoded_response)

            # this can just carry on in the background or something idk
            writer.write_lcd(decoded_response)
            
            response = client.audio.speech.create(
                model = "tts-1",
                voice = "shimmer",
                input = decoded_response
            )
    
            response.write_to_file("output.mp3")
            time.sleep(0.75)
            sound = pyglet.media.load("output.mp3", streaming=False)
            player = sound.play()
            player.volume = 3

            # loop and do face stuff while its speaking
            lasttime = time.time()
            starttime = time.time()
            toggle = False
            while time.time() - starttime <= sound.duration:
                # flip face every quarter second
                if time.time() - lasttime > sound.duration / 6:
                    writer.write_face(Face.TALKFACE if toggle else Face.NOTALKFACE)
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
