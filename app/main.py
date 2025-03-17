from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Invoice API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens (altere para um domínio específico em produção)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os headers
)
app.include_router(router)
