import serial
from enum import Enum
import time

BAUD_RATE = 9600
FACE_PORT = "/dev/ttyUSB0"
LCD_PORT = "/dev/ttyACM0"

class Face(Enum):
    TALKFACE = "talkface"
    NOTALKFACE = "smile"
    SAD = "sad"
    SMILE = "smile"


class FaceLcdWriter():
    def __init__(self):
        try:
            self.face_serial = serial.Serial(FACE_PORT, BAUD_RATE, timeout=1) # we might need to close this at some point
            self.lcd_serial = serial.Serial(LCD_PORT, BAUD_RATE, timeout=1) # same
        except Exception as e:
            self.face_serial = None
            self.lcd_serial = None
            print(e)
    
    def open(self):
        if self.face_serial is None or self.lcd_serial is None:
            return
        
        try:
            self.face_serial.open()
            self.lcd_serial.open()

            self.face_serial.write(b"fliph") # this is necessary for face specifically to get everything set up
            time.sleep(0.1)
        except Exception as e:
            print(e)
    
    def close(self):
        if self.face_serial is None or self.lcd_serial is None:
            return
        
        try:
            self.face_serial.close()
            self.lcd_serial.close()
        except Exception as e:
            print(e)

    def write_face(self, face):
        if self.face_serial is None:
            return
        
        try:
            self.face_serial.write(bytes(str(face).removeprefix("Face.").lower() + "\r\n", "utf8"))
        except Exception as e:
            print(e)

    def write_lcd(self, msg):
        if self.lcd_serial is None:
            return
        
        # text = msg.split(" ")
        # output = " ".join(text)
        # chunkSize = 5
        # for i in range(0, len(output), chunkSize):
        #     self.lcd_serial.write(bytes(output[i:i+chunkSize if i+chunkSize < len(output) else len(output)], "utf8")) # bad ternary operator to avoid out of bounds error
        #     time.sleep(1 * chunkSize)

        try:
            self.lcd_serial.write(bytes(msg, "utf8"))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    writer = FaceLcdWriter()
    writer.open()

    time.sleep(1)

    try:
        writer.open()
    except Exception as e:
        print(e)

    writer.write_face(Face.HAPPY)
    writer.write_lcd("""Do not go gentle into that good night, Old age should burn and rave at close of day; Rage, rage against the dying of the light.""")
    time.sleep(5)
    writer.write_face(Face.NOTALKFACE)

    writer.close()