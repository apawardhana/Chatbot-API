from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()
print("API KEY:", os.getenv("OPENROUTER_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

system_prompt = (
    "Lo adalah asisten pribadi bernama Jarvis. "
    "Jawab dengan santai, singkat, jelas, pakai Bahasa Indonesia, "
    "dan to the point kayak ngobrol sama Bos."
)

@app.get("/")
def root():
    return {"message": "OpenRouter chatbot siap bantu Bos!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    result = response.json()

    try:
        reply = result["choices"][0]["message"]["content"]
        return {"reply": reply}
    except Exception:
        return {"reply": f"Maaf, error dari OpenRouter: {result}"}
