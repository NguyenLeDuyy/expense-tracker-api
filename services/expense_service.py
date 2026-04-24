from sqlalchemy import desc
from schemas.expense import SummaryEachCategory
from schemas.expense import StatisticsExpenseResponse
from calendar import monthrange
from schemas.expense import SummaryExpenseResponse
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

def get_summary_service(db: Session, user_id: int, month: int, year: int):

    year = year or date.today().year
    month = month or date.today().month

    total_spent_of_month = db.query(
            func.sum(Expense.amount)
        ).filter(
            Expense.user_id == user_id,
            func.extract("month", Expense.date) == month,
            func.extract("year", Expense.date) == year
        ).scalar() or 0

    rows = db.query(
        Category.name.label("category_name"),
        func.sum(Expense.amount).label("total")
    ).select_from(Expense
    ).join(Category, Expense.category_id == Category.id
    ).filter(
        Expense.user_id == user_id,
        func.extract("month", Expense.date) == month,
        func.extract("year", Expense.date) == year,
    ).group_by(Category.name
    ).all()

    by_category = [
        SummaryEachCategory(category_name=category_name, total=total)
        for category_name, total in rows
    ]

    return SummaryExpenseResponse(
        month=f"{year}-{month}",
        by_category=by_category,
        total=total_spent_of_month
    )

def get_stats_service(db: Session, user_id: int, month: int, year: int):

    year = year or date.today().year
    month = month or date.today().month

    this_month_total = db.query(
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == user_id,
        func.extract("month", Expense.date) == month,
        func.extract("year", Expense.date) == year,
    ).scalar() or 0

    if year == date.today().year and month == date.today().month:
        days_passed = date.today().day
        daily_average = int(this_month_total / days_passed) if days_passed > 0 else 0
    else:
        days_in_month = monthrange(year, month)[1]
        daily_average = int(this_month_total / days_in_month)

    row = db.query(
        Category.name.label("category_name"),
        func.sum(Expense.amount).label("total")
    ).select_from(Expense
    ).join(Category, Expense.category_id == Category.id
    ).filter(
        Expense.user_id == user_id,
        func.extract("month", Expense.date) == month,
        func.extract("year", Expense.date) == year,
    ).group_by(Category.name
    ).order_by(desc("total")
    ).first()

    if row:
        top_category = SummaryEachCategory(category_name=row.category_name, total=row.total)
    else:
        top_category = None

    filtered_month = month - 1
    filtered_year = year

    if filtered_month == 0:
        filtered_month = 12
        filtered_year = year - 1

    last_month_total = db.query(
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == user_id,
        func.extract("month", Expense.date) == filtered_month,
        func.extract("year", Expense.date) == filtered_year,
    ).scalar() or 0

    month_over_month_change = None
    if last_month_total == 0:
        last_month_total = None
    else:
        month_over_month_change = ((this_month_total - last_month_total) / last_month_total) * 100

    return StatisticsExpenseResponse(
        daily_average=daily_average,
        top_category=top_category,
        this_month_total=this_month_total,
        last_month_total=last_month_total,
        month_over_month_change=month_over_month_change
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
