from fastapi import FastAPI
from app.api.routes import chat  # 1. Импортируем наш новый роутер

app = FastAPI(title="KRONOS AI Core")

# 2. Подключаем роутер к основному приложению
# Все эндпоинты из chat.py теперь будут доступны с префиксом /api/v1
app.include_router(chat.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """
    Корневой эндпоинт для проверки, что сервер жив.
    """
    return {"message": "KRONOS AI Core is running"}

@app.get("/api/ping", tags=["Health Check"])
def ping():
    """
    Простой эндпоинт для проверки доступности API.
    """
    return {"status": "ok", "message": "pong"}