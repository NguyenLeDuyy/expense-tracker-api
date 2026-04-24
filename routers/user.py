from schemas.response import success_response, ApiResponse
from schemas.auth import RefreshRequest
from app.core.deps import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from models.user import User
from schemas.auth import LoginRequest, RegisterRequest
from services.user_service import create_user_service, login_user_service, refresh_access_token_service
from fastapi import Form


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = create_user_service(db, payload)
    return success_response(data=user, message="User registered successfully")

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    result = login_user_service(db, payload)
    return success_response(data=result, message="Login successful")

@router.post("/token")
def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    result = login_user_service(db, LoginRequest(email=username, password=password))
    return {
        "access_token": result["tokens"].access_token,
        "token_type": "bearer"
    }
    
@router.post("/refresh")
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    result = refresh_access_token_service(db, payload.refresh_token)
    return success_response(data=result, message="Token refreshed successfully")

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return success_response(data={"id": current_user.id, "email": current_user.email}, message="User retrieved successfully")