from openai import OpenAI
import pyttsx3

class Rosie():
    def __init__(self):
        # https://platform.openai.com/docs/guides/text-generation/chat-completions-api

        # create the client
        self.client = OpenAI()

        self.personality_msg = {
            "role": "system", # to modify the behavior of the assistant
            "content": "You are Rosie from The Jetsons." #this could probably be a lot better
        }

    
    def get_response(self, question: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                self.personality_msg,
                {"role":"user", "content": question}
            ]
        )

        return response.choices[0].message.content # extract ChatGPT's reply


class TTS:
    def __init__(self):
        # https://pypi.org/project/pyttsx3/
        self.engine = pyttsx3.init() # object creation
        self.engine.setProperty('rate', 225)     # setting up new voice rate
        self.engine.setProperty('volume', 1.0)    # setting up volume level  between 0 and 1
        
        voices = self.engine.getProperty('voices')       #getting details of current voice   
        for idx, voice in enumerate(voices):
            if "hazel" in voice.name.lower():
                self.engine.setProperty('voice', voices[idx].id)

    def speak(self, msg):
        self.engine.say(msg)
        self.engine.runAndWait()