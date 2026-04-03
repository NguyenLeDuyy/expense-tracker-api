from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.jwt import ALGORITHM, SECRET_KEY
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
):
    try:
         # 1. decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 2. lấy user_id từ payload
    user_id = payload.get("user_id")

    # 3. query user từ DB
    user = db.query(User).filter(User.id == user_id).first()
   
    
    # 4. nếu lỗi → raise 401
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return user