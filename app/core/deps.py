from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.jwt import decode_token
from database import SessionLocal
from models.user import User



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id_raw = payload.get("sub")
    if user_id_raw is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Invalid token payload",
             headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )

    return user