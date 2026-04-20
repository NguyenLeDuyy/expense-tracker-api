from datetime import date
from schemas.expense import PaginatedExpenseResponse
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

    category = db.query(Category).filter(
        Category.id == expense_data.category_id,
        Category.user_id == user_id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.commit()
    db.refresh(expense)

    warning_message = None
    if category.monthly_budget > 0:
        first_day_of_month = expense.date.replace(day=1)

        total_spent = db.query(func.sum(Expense.amount)).filter(
            Expense.category_id == category.id,
            Expense.user_id == user_id,
            Expense.date >= first_day_of_month
        ).scalar() or 0

        if total_spent > category.monthly_budget:
            warning_message = f"Budget exceeded for {category.name}: spent {total_spent:,} / limit {category.monthly_budget:,}"

    return ExpenseResponse(
        id=expense.id,
        amount=expense.amount,
        category_id=category.id,
        date=expense.date,
        warning=warning_message
    )

def get_expenses_service(db: Session, user_id: int, category_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    min_amount: int | None = None,
    max_amount: int | None = None,
    sort_by: str = "date_desc",
    page: int = 1,
    page_size: int = 10,):
    items, total = get_expenses(db, user_id, category_id, start_date, end_date, min_amount, max_amount, sort_by, page, page_size)
    return PaginatedExpenseResponse(
        items=items,
        total_count=total,
        page=page,
        page_size=page_size,
    )
    
    
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
