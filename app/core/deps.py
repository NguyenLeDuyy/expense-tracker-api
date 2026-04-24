from app.core.exceptions import UnauthorizedException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.jwt import decode_token
from database import SessionLocal
from models.user import User



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Dependency pattern in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),   # lấy token từ đâu?
    db: Session = Depends(get_db)
) -> User:
    payload = decode_token(token)
    
    if payload.get("type") != "access":
        raise UnauthorizedException("Invalid token type")
    
    user_id_raw = payload.get("sub")
    if user_id_raw is None:
            raise UnauthorizedException("Invalid token payload")
    
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        raise UnauthorizedException("Invalid token payload")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
                raise UnauthorizedException("Invalid token payload")

    return user