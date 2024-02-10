from openai import OpenAI

# https://platform.openai.com/docs/guides/text-generation/chat-completions-api


# create the client
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

personality_msg = {
    "role": "system", # to modify the behavior of the assistant
    "content": "You are Rosie from The Jetsons"
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