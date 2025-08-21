from fastapi import APIRouter
from app.models import Message

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> Message:
    """
    Health check endpoint
    """
    return Message(message="OK")