from app.core.config import settings
import os
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import HTTPException, status
from jose import JWTError, jwt
import datetime

load_dotenv()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE_DAYS = int(settings.REFRESH_TOKEN_EXPIRE_DAYS)
JWT_ISSUER = os.getenv("JWT_ISSUER", "expense-tracker-api")

def _utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

def create_access_token(*, user_id: int, email: str) -> str:
    now = _utc_now()

    payload = {
        "sub": str(user_id),
        "email": email,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iss": JWT_ISSUER,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(*, user_id: int) -> tuple[str, str, datetime.datetime]:
    now = _utc_now()
    jti = str(uuid4())
    expires_at = now + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": expires_at,
        "iss": JWT_ISSUER,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti, expires_at

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], issuer=JWT_ISSUER)
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc