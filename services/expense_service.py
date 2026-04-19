from schemas.expense import ExpenseResponse
from models.expense import Expense
from sqlalchemy import func
from models.category import Category
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

    warning_message = None

    category = db.query(Category).filter(Category.id == expense_data.category_id).first()


    if category and category.monthly_budget > 0:
        first_day_of_month = expense.date.replace(day=1)

        total_spent = db.query(func.sum(Expense.amount)).filter(
            Expense.category_id == category.id,
            Expense.user_id == user_id,
            Expense.date >= first_day_of_month
        ).scalar() or 0

        if total_spent > category.monthly_budget:
            warning_message = f"Budget exceeded for {category.name}: spent {total_spent:,} / limit {category.monthly_budget:,}"

        expense.warning=warning_message

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
