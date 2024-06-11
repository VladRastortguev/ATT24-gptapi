import environ
import uvicorn
import openai
import json

from fastapi import FastAPI
from pydantic import BaseModel

env = environ.Env()
environ.Env.read_env()

app = FastAPI()

openai.api_key = env('OPENAI_API_KEY')

def chat_with_gpt(system, question):
    result = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question}
        ],
        temperature=0.5
    )

    responceText = result.choices[0].message.content
    return responceText

    #['choices'][0]['message']['content']

    #return "test"

class ChatData(BaseModel):
    system: str
    question: str

@app.post('/chatgpt', status_code=200)
async def process_data(payload: ChatData):
    data = payload.model_dump()

    print(data)

    responce = chat_with_gpt(data["system"], data["question"])

    return responce

