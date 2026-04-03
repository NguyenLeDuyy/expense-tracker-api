from fastapi import HTTPException

from crud.expense import (
    create_expense,
    get_expenses,
    update_expense,
    delete_expense
)
from schemas.expense import ExpenseCreate
from sqlalchemy.orm import Session
def create_expense_service(db: Session, expense_data: ExpenseCreate, user_id: int):
    expense = create_expense(db, expense_data, user_id)
    
    db.commit()
    db.refresh(expense)
    return expense

def get_expenses_service(db: Session, user_id: int):
    return get_expenses(db, user_id)
    
def delete_expense_service(db: Session, expense_id: int, user_id: int):
    expense = delete_expense(db, expense_id, user_id)

    if not expense:
        raise HTTPException(status_code=404, detail="Not found")

    db.commit()
    return expense

def update_expense_service(db: Session, expense_data: ExpenseCreate, expense_id: int, user_id: int):
    expense = update_expense(db, expense_data, expense_id, user_id)
    
    if not expense:
        raise HTTPException(status_code=404, detail="Not found")

    db.commit()
    db.refresh(expense)
    return expense
