from openai import OpenAI

# https://platform.openai.com/docs/guides/text-generation/chat-completions-api


# create the client
client = OpenAI()

personality_msg = {
    "role": "system", # to modify the behavior of the assistant
    "content": "You are Rosie from The Jetsons."
}


while True:
    #TODO get prompts/questions from the google assistant
    question = input(">")

    if question.lower() == "q":
        print("EXIT")
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