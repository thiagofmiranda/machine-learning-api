from fastapi import APIRouter
from app.models.model import __version__ as model_version

router = APIRouter()

@router.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}