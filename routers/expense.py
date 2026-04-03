from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from database import SessionLocal
from models.user import User
from schemas.expense import ExpenseCreate
from services.expense_service import (
    create_expense_service,
    get_expenses_service,
    delete_expense_service,
    update_expense_service
)

router = APIRouter()

# Dependency pattern in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/expenses")
def create_expense(
    expense: ExpenseCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return create_expense_service(db, expense, current_user.id)

@router.get("/expenses")
def get_expenses(db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)
                 ):
    return get_expenses_service(db, current_user.id)

@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    delete_expense_service(db, expense_id, current_user.id)
    return {"message": "Deleted"}

@router.put("/expenses/{expense_id}")
def update_expense(
    updated: ExpenseCreate, 
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return update_expense_service(db, updated, expense_id, current_user.id)