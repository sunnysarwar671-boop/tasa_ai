import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Files ----------------

HISTORY_FILE = "history.json"
MEMORY_FILE = "memory.json"

# সর্বোচ্চ কতটি message রাখা হবে
MAX_HISTORY = 20

# ---------------- Groq ----------------

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
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

# ---------------- JSON ----------------

def load_json(file):
    if not os.path.exists(file):
        return []

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ---------------- Request ----------------

class Chat(BaseModel):
    message: str

# ---------------- Chat ----------------

@app.post("/chat")
def chat(data: Chat):

    history = load_json(HISTORY_FILE)
    memory = load_json(MEMORY_FILE)

    messages = [SYSTEM]

    # গুরুত্বপূর্ণ Memory পাঠানো
    if memory:
        messages.append({
            "role": "system",
            "content": "Saved Memory:\n\n" + "\n".join(memory)
        })

    # শুধু শেষ MAX_HISTORY টি message পাঠাবে
    messages.extend(history[-MAX_HISTORY:])

    messages.append({
        "role": "user",
        "content": data.message
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    reply = response.choices[0].message.content

    # নতুন Message Save
    history.append({
        "role": "user",
        "content": data.message
    })

    history.append({
        "role": "assistant",
        "content": reply
    })

    # history.json বড় হতে দেবে না
    history = history[-MAX_HISTORY:]

    save_json(HISTORY_FILE, history)

    return {
        "reply": reply
}
