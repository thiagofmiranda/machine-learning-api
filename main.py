from fastapi import FastAPI
from routes.endpoints import router

# Initialize the FastAPI app
app = FastAPI()

# Include dynamically created routes
app.include_router(router)

