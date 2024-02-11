#! python3.7
import socket, openai, os, time, pyglet

HOST = "24.144.83.34"
PORT = 65433


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
type_message = "TEXTTOSPEECH"
sock.sendall(type_message.encode())


client = openai.OpenAI()


def main():
    global sock
    while True:
        try:
            response = sock.recv(1024 * 1024)
            decoded_response = response.decode()
            decoded_response = "Hey kid. " + decoded_response
            print(decoded_response)
            
            response = client.audio.speech.create(
                model = "tts-1",
                voice = "nova",
                input = decoded_response
            )
            response.write_to_file("output.mp3")
            time.sleep(0.75)
            sound = pyglet.media.load("output.mp3", streaming=False)
            sound.play()
            time.sleep(sound.duration)
            os.remove("output.mp3")
            
        except KeyboardInterrupt:
            print("Exiting...")
            sock.close()
            # writer.close()
            break


if __name__ == "__main__":
    main()
