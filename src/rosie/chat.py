from openai import OpenAI
from dotenv import dotenv_values
cfg = dotenv_values(".env")

class Rosie():
    def __init__(self):
        # https://platform.openai.com/docs/guides/text-generation/chat-completions-api
        self.client = OpenAI(api_key = cfg.get("OPENAI_API_KEY"))
        self.personality_msg = {
            "role": "assistant",
            "content": "You are Rosie from The Jetsons. Do not refer to who you are speaking to in your response, be generic. Keep all of your responses very short, around 2 sentences. Please do not show temperatures in multiple units, only use fahrenheit." #this could probably be a lot better
        }

    
    def get_response(self, question: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                self.personality_msg,
                {"role":"user", "content": question}
            ],
            temperature=0.18,
            max_tokens=200
        )

        return response.choices[0].message.content