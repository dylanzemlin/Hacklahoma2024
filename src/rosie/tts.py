import pyttsx3

class TTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 225)
        self.engine.setProperty('volume', 1.0)
        
        voices = self.engine.getProperty('voices') 
        self.engine.setProperty('voice', voices[1].id)

    def speak(self, msg):
        self.engine.save_to_file(msg, 'temp.mp3')
        self.engine.runAndWait()