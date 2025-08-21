from datetime import datetime, timedelta, timezone
from typing import Any
import os

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "RS256"


def get_private_key() -> str:
    """Load RSA private key from file"""
    key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), settings.JWT_PRIVATE_KEY_PATH)
    with open(key_path, "r") as key_file:
        return key_file.read()


def get_public_key() -> str:
    """Load RSA public key from file"""
    key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), settings.JWT_PUBLIC_KEY_PATH)
    with open(key_path, "r") as key_file:
        return key_file.read()


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    private_key = get_private_key()
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
