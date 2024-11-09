from fastapi import FastAPI
from app.api.endpoints import home_router, predict_router

app = FastAPI()

# Incluindo os roteadores
app.include_router(home_router)
app.include_router(predict_router)