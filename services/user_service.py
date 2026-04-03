from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from models.user import User
from schemas.user import UserCreate, UserLogin


def create_user_service(db: Session, user_data: UserCreate):
    
    checked_user = db.query(User).filter(User.email == user_data.email).first()
    if checked_user is not None:
        raise HTTPException(status_code=400, detail="Email existed")

    hashed_password = hash_password(user_data.password)

    user = User(email=user_data.email, hashed_password=hashed_password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user_service(db: Session, user_data: UserLogin):

    checked_user = db.query(User).filter(User.email == user_data.email).first()
    if checked_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if (verify_password(user_data.password, checked_user.hashed_password)) is False:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(checked_user)

    return {
        "access_token": token,
        "token_type": "bearer"
    }