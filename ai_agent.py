import os
import requests
from dotenv import load_dotenv

load_dotenv()

# LLM_PROVIDER: "ollama" (local, default) or "openrouter"
PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()

if PROVIDER == "openrouter":
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    MODEL = os.getenv("LLM_MODEL", "mistralai/mistral-7b-instruct:free")
else:
    # Ollama exposes an OpenAI-compatible endpoint
    API_URL = os.getenv("OLLAMA_URL", "http://localhost:11434") + "/v1/chat/completions"
    API_KEY = "ollama"
    MODEL = os.getenv("LLM_MODEL", "gemma3:4b")

def query_llm(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": messages
    }
    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("🚨 Response error:", response.text)
        response.raise_for_status()
