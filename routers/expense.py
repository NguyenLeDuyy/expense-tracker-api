from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from schemas import ExpenseCreate
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
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return create_expense_service(db, expense)

@router.get("/expenses")
def get_expenses(db: Session = Depends(get_db)) -> list[models.Expense]:
    return get_expenses_service(db)

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    delete_expense_service(db, expense_id)
    return {"message": "Deleted"}

@router.put("/expenses/{expense_id}")
def update_expense(updated: ExpenseCreate, expense_id: int, db: Session = Depends(get_db)):
    return update_expense_service(db, updated, expense_id)