import serial
from enum import Enum

BAUD_RATE = 9600

class Face(Enum):
    TALKFACE = "talkface"
    NOTALKFACE = "notalkface"
    HAPPY = "happy"
    SAD = "sad"
    SMILE = "smile"


class FaceLcdWriter():
    def __init__(self):
        self.face_port = 0 #TODO
        self.lcd_port = 0 #TODO

        self.face_serial = serial.Serial("COM3", BAUD_RATE, timeout=1) # we might need to close this at some point
        self.lcd_serial = serial.Serial("COM4", BAUD_RATE, timeout=1) # same
    
    def open(self):
        self.face_serial.open()
        self.lcd_serial.open()
    
    def close(self)
        self.face_serial.close()
        self.lcd_serial.close()

    def write_face(self, face):
        self.face_serial.write(face)

    def write_lcd(self, msg):
        self.face_serial.write(msg)