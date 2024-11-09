# Exponha os roteadores para importação mais fácil, se necessário.
from .home import router as home_router
from .predict import router as predict_router

__all__ = ["home_router", "predict_router"]
