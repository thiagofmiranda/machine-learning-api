from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.model import predict_pipeline
from app.services.cache_service import get_cache, set_cache

router = APIRouter()

class TextIn(BaseModel):
    text: str

class PredictionOut(BaseModel):
    language: str
    from_cache: bool  

@router.post("/predict", response_model=PredictionOut)
def predict(payload: TextIn):
    cache_key = f"predict:{payload.text}"
    cache = get_cache(cache_key)
    
    if cache:
        return PredictionOut(language=cache["language"], from_cache=True)
    else:
        language = predict_pipeline(payload.text)
        set_cache(cache_key, {"language": language})
        return PredictionOut(language=language, from_cache=False)
