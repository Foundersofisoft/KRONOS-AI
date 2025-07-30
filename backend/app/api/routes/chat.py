import os
import requests
import json
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# --- Модели данных ---
class UserRequest(BaseModel):
    message: str

# --- Настройки API Hugging Face ---
API_URL = "https://api-inference.huggingface.co/models/gpt2"
API_TOKEN = os.getenv("HF_API_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# --- Роутер (эта строка была потеряна) ---
router = APIRouter()

def query_mistral(payload):
    """Отправляет запрос к модели и возвращает итерируемый ответ."""
    
    # --- ОТЛАДКА ---
    print("--- DEBUG START ---")
    print(f"API URL: {API_URL}")
    print(f"TOKEN LOADED: {API_TOKEN}")
    print("--- DEBUG END ---")
    # --- КОНЕЦ ОТЛАДКИ ---

    data = json.dumps(payload)
    response = requests.post(API_URL, headers=headers, data=data, stream=True)
    
    if response.status_code != 200:
        error_message = f"Error: {response.status_code}, {response.text}"
        print(error_message)
        yield f"data: {json.dumps({'error': error_message})}\n\n"
        return

    try:
        for byte_payload in response.iter_lines():
            if byte_payload:
                if byte_payload == b":":
                    continue
                
                if byte_payload.startswith(b'data:'):
                    chunk = byte_payload[5:].strip()
                    if chunk:
                        yield f"data: {chunk.decode('utf-8')}\n\n"

    except Exception as e:
        error_message = f"Stream Error: {e}"
        print(error_message)
        yield f"data: {json.dumps({'error': error_message})}\n\n"


@router.post("/chat", tags=["Chat"])
async def handle_chat_stream(request: UserRequest):
    """
    Принимает сообщение и стримит ответ от AI.
    """
    print(f"Запрос к gpt2: {request.message}")
    payload = {"inputs": request.message}
    return StreamingResponse(query_mistral(payload), media_type="text/event-stream")