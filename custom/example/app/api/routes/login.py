from typing import Any

from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.models import UserPublic

router = APIRouter(tags=["login"])


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token (validates external JWT token from backend/app)
    """
    return current_user
