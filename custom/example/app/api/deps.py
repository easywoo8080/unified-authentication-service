from collections.abc import Generator
from typing import Annotated

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.config import settings
from app.core.db import engine
from app.models import UserPublic

# Point to external auth service
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.AUTH_SERVICE_URL}{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(token: TokenDep) -> UserPublic:
    """
    Get current user by validating token with external auth service
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.AUTH_SERVICE_URL}{settings.API_V1_STR}/login/test-token",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
            
        user_data = response.json()
        return UserPublic(**user_data)
        
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


CurrentUser = Annotated[UserPublic, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> UserPublic:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
