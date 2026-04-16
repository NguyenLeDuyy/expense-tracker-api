from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from database import SessionLocal
from models.user import User
from schemas.auth import LoginRequest, RegisterRequest
from services.user_service import create_user_service, login_user_service, refresh_access_token_service


router = APIRouter(prefix="/auth", tags=["Auth"])

# Dependency pattern in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return create_user_service(db, payload)

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_user_service(db, payload)

from fastapi import Form

@router.post("/token")
def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    return login_user_service(db, LoginRequest(email=username, password=password))
    
@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    return refresh_access_token_service(db, refresh_token)

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}