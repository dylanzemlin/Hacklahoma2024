#! python3.7
import socket, wave, pyaudio, struct, pickle
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
    p = pyaudio.PyAudio()
    stream = p.open(
        format = p.get_format_from_width(2),
        channels = 2,
        rate = 44100,
        output = True,
        frames_per_buffer=1024
    )
    # writer = FaceLcdWriter()
    # writer.open()
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
            while len(data) < payload_size:
                packet = sock.recv(4096)
                if not packet: break
                data += packet
                
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += sock.recv(4096)
                
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            stream.write(frame)
        except KeyboardInterrupt:
            print("Exiting...")
            sock.close()
            # writer.close()
            break


if __name__ == "__main__":
    main()
