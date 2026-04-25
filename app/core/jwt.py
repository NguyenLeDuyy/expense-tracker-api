import logging
from app.core.exceptions import UnauthorizedException
from app.core.config import settings
from uuid import uuid4
from jose import JWTError, jwt
import datetime

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
JWT_ISSUER = settings.JWT_ISSUER

logger = logging.getLogger("app.jwt")

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
        logger.warning(f"Token decode failed: {exc}")
        raise UnauthorizedException("Invalid or expired token") from exc