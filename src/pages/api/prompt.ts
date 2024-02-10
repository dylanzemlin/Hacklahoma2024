// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import OpenAI from "openai";

const openai = new OpenAI();

// system: adds context, content: part of the prompt
const personality_msg = {
    role: "system",
    content: "You are Rosie from The Jetsons."
};

// actual response handler
async function get_response(prompt_: String) {
    const ret = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [personality_msg, {role: "user", content: prompt_ }], // this content right here needs to get replaced
        stream: false,
    });

    return ret.choices[0]; // https://platform.openai.com/docs/api-reference/chat/create?lang=node.js
}


type Data = {
  response: string;
};

export default async function handler(
    req: NextApiRequest<Data>,
    res: NextApiResponse<Data>,
) {
    const result = await get_response(req.response);

    res.status(200).json({ response: result });
}

/**
 * theoretically equivalent python code, not sure though cause i don't know typescript
 * from openai import OpenAI

# https://platform.openai.com/docs/guides/text-generation/chat-completions-api


# create the client
client = OpenAI()

personality_msg = {
    "role": "system", # to modify the behavior of the assistant
    "content": "You are Rosie from The Jetsons." #this could probably be a lot better
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
 */