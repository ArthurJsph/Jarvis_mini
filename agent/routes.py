from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from agent.core import AgentCore
import time
import logging
from config.config import API_KEY
from fastapi.responses import JSONResponse

app = FastAPI(title="Jarvis Chatbot API", version="1.0")

# Configura CORS para permitir frontends acessarem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste para domínios específicos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = AgentCore()
start_time = time.time()
logger = logging.getLogger("uvicorn.error")


class ChatRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto enviado pelo usuário")


class ChatResponse(BaseModel):
    response: str


def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if not api_key or api_key != API_KEY:
        logger.warning(f"Unauthorized access attempt with API Key: {api_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: API Key inválida.",
        )
    return True


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    start = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error(f"Exception handling request: {exc}")
        raise
    process_time = (time.time() - start) * 1000
    logger.info(f"Response status: {response.status_code} completed in {process_time:.2f}ms")
    return response


@app.get("/health", dependencies=[Depends(verify_api_key)], tags=["Status"])
async def health_check():
    uptime = time.time() - start_time
    return {
        "status": "running",
        "uptime_seconds": int(uptime),
        "memory_status": "ok",
        "llm_api_status": "ok"
    }


@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(verify_api_key)], tags=["Chat"])
async def chat_endpoint(chat_req: ChatRequest):
    user_text = chat_req.text.strip()
    if not user_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'text' não pode estar vazio."
        )
    try:
        response_text = agent.get_response(user_text)
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a solicitação."
        )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )
