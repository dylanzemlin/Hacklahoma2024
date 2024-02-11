from openai import OpenAI
import pyttsx3

# https://pypi.org/project/pyttsx3/
engine = pyttsx3.init() # object creation
engine.setProperty('rate', 225)     # setting up new voice rate
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. 0 for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

# https://platform.openai.com/docs/guides/text-generation/chat-completions-api


# create the client
client = OpenAI()

personality_msg = {
    "role": "system", # to modify the behavior of the assistant
    "content": "You are Rosie from The Jetsons." #this could probably be a lot better
}

voices = engine.getProperty('voices')
for idx, voice in enumerate(voices):
    if "hazel" in voice.name.lower():
        engine.setProperty('voice', voices[idx].id)

while True:
    #TODO get prompts/questions from the google assistant
    question = input(">")

    if question.lower() == "q":
        print("EXIT")
        engine.stop()
        raise SystemExit

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            personality_msg,
            {"role":"user", "content":question}
        ]
    )

    #TODO pipe this back out to google assistant
    reply = response.choices[0].message.content # extract ChatGPT's reply

    print(reply)

    engine.say(reply)
    engine.runAndWait()