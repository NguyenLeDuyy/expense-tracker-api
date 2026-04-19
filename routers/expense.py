from schemas.expense import ExpenseResponse
from app.core.deps import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from models.user import User
from schemas.expense import ExpenseCreate
from services.expense_service import (
    create_expense_service,
    get_expenses_service,
    delete_expense_service,
    update_expense_service
)

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return create_expense_service(db, expense, current_user.id)

@router.get("/")
def get_expenses(db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)
                 ):
    return get_expenses_service(db, current_user.id)

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    delete_expense_service(db, expense_id, current_user.id)
    return {"message": "Deleted"}

@router.put("/{expense_id}")
def update_expense(
    updated: ExpenseCreate, 
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return update_expense_service(db, updated, expense_id, current_user.id)