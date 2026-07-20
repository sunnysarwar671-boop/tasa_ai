from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Notion / GitHub Pages থেকে Request আসতে দেবে
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("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"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.3-70b-versatile"

SYSTEM = {
    "role": "system",
    "content": """
You are Tasa.

You are friendly.
You are funny.
You explain clearly.
Always answer in Markdown.

Keep paragraphs short.
Leave one blank line between paragraphs.

Never write everything in one long line.

If the reply is long, split it into multiple paragraphs.

Use bullet points when appropriate.
"""
}

class Chat(BaseModel):
    message: str

@app.post("/chat")
def chat(data: Chat):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            SYSTEM,
            {
                "role": "user",
                "content": data.message
            }
        ]
    )

    return {
        "reply": response.choices[0].message.content
}
