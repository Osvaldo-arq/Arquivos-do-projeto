from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Invoice API")
app.include_router(router)
