import logging
from app.core.exceptions import UnauthorizedException
from app.core.exceptions import BadRequestException
import datetime

from sqlalchemy.orm import Session
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.core.security import hash_password, verify_password
from models.refresh_token import RefreshToken
from models.user import User
from schemas.auth import LoginRequest, RegisterRequest, TokenPairResponse, UserPublic

logger = logging.getLogger("app.auth")

def _issue_token_pair(db: Session, user: User) -> TokenPairResponse:
    access_token = create_access_token(user_id=user.id, email=user.email)
    refresh_token, jti, expires_at = create_refresh_token(user_id=user.id)

    db.add(
        RefreshToken(
            jti=jti,
            user_id=user.id,
            expires_at=expires_at,
        )
    )
    db.commit()

    return TokenPairResponse(access_token=access_token, refresh_token=refresh_token)


def create_user_service(db: Session, user_data: RegisterRequest):
    
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user is not None:
        raise BadRequestException("Email already exists")

    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"User registered: {user.email}")
    
    tokens = _issue_token_pair(db, user)

    return {
        "user": UserPublic(id=user.id, email=user.email),
        "tokens": tokens,
    }

def login_user_service(db: Session, user_data: LoginRequest):

    user = db.query(User).filter(User.email == user_data.email).first()
    if user is None or not verify_password(user_data.password, user.hashed_password):
        logger.warning(f"Login failed: {user_data.email}")
        raise UnauthorizedException("Invalid credentials")

    tokens = _issue_token_pair(db, user)

    logger.info(f"User logged in: {user.email}")

    return {
        "user": UserPublic(id=user.id, email=user.email),
        "tokens": tokens,
    }

def refresh_access_token_service(db: Session, refresh_token: str):
    payload = decode_token(refresh_token)
    
    if payload.get("type") != "refresh":
        raise UnauthorizedException("Invalid token type")
    
    user_id = payload.get("sub")
    jti = payload.get("jti")
    if user_id is None or jti is None:
        raise UnauthorizedException("Invalid token payload")

    token_row = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.jti == jti,
            RefreshToken.user_id == int(user_id),
            RefreshToken.revoked_at.is_(None),
        )
        .first()
    )
    if token_row is None:
        raise UnauthorizedException("Refresh token revoked or not found")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.is_active:
        raise UnauthorizedException("User not found")
    
    # rotate refresh token
    token_row.revoked_at = datetime.datetime.now(datetime.timezone.utc)  # import datetime, timezone at top
    db.commit()

    return _issue_token_pair(db, user)
