import os
import importlib
import hashlib
import json
from fastapi import APIRouter
from redis import Redis  # Usando a versão síncrona do Redis
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    input_data: dict

# Initialize the API Router
router = APIRouter()

# Base path to the models folder
MODELS_PACKAGE = "models"  # Base package name for the models folder
MODELS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", MODELS_PACKAGE)

# Store available models for use in the API
available_models = []

# Initialize Redis
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
print(REDIS_PASSWORD)
REDIS_URL = os.getenv("REDIS_URL", f"redis://:{REDIS_PASSWORD}@redis:6379")  # Inclui a senha aqui
redis: Redis = Redis.from_url(REDIS_URL, decode_responses=True)  # Usando a versão síncrona do Redis

# Helper function to generate cache keys
def generate_cache_key(input_data: dict) -> str:
    """
    Generate a unique cache key based on the model name and input data.
    """
    input_hash = hashlib.md5(json.dumps(input_data, sort_keys=True).encode()).hexdigest()
    return f"{input_hash}"

# Dynamically load predict functions from each model
for model_dir in os.listdir(MODELS_PATH):
    model_path = os.path.join(MODELS_PATH, model_dir)

    # Check if the directory contains an __init__.py file
    if os.path.isdir(model_path) and os.path.exists(os.path.join(model_path, "__init__.py")):
        # Add the model name to the list of available models
        available_models.append(model_dir)

        # Import the predict function dynamically
        module_name = f"{MODELS_PACKAGE}.{model_dir}.predict"
        try:
            predict_module = importlib.import_module(module_name)
            predict_function = getattr(predict_module, "predict")

            # Define a route for the model
            @router.post(f"/{model_dir}/predict")
            def predict_endpoint(data: PredictionRequest):
                """
                Route for making predictions using the specific model.
                """
                cache_key = generate_cache_key(data.input_data)

                # Check if prediction is cached
                cached_prediction = redis.get(cache_key)
                if cached_prediction:
                    return {"prediction": json.loads(cached_prediction), "cached": True}

                # If not cached, compute the prediction
                prediction = predict_function(data.input_data)  # Função de predição agora síncrona

                # Store the prediction in Redis
                redis.set(cache_key, json.dumps(prediction), ex=3600)  # Cache for 1 hour
                return {"prediction": prediction, "cached": False}

        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Error loading predict function for model {model_dir}: {e}")

# Health Check Route
@router.get("/hc", tags=["Utility"])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok"}

# List Available Models Route
@router.get("/list-models", tags=["Utility"])
def list_models():
    """
    List all available machine learning models.
    """
    return {"available_models": available_models}
