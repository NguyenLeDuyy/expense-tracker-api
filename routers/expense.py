from schemas.response import success_response, ApiResponse
from services.expense_service import get_stats_service
from schemas.expense import StatisticsExpenseResponse
from schemas.expense import SummaryExpenseResponse
from services.expense_service import get_summary_service
from datetime import date
from fastapi import Query
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

@router.post("/", response_model=ApiResponse[ExpenseResponse])
def create_expense(
    expense: ExpenseCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    expense = create_expense_service(db, expense, current_user.id)
    return success_response(data=expense, message="Expense created successfully")

@router.get("/")
def get_expenses(db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user),
                 category_id: int | None = Query(None),
                 start_date: date | None = Query(None),
                 end_date: date | None = Query(None),
                 min_amount: int | None = Query(None),
                 max_amount: int | None = Query(None),
                 sort_by: str = Query("date_desc"),
                 page: int = Query(1, ge=1),
                 page_size: int = Query(10, ge=1, le=100),
                 ):
    expenses = get_expenses_service(db, current_user.id,
        category_id, start_date, end_date,
        min_amount, max_amount,
        sort_by, page, page_size,
    )
    return success_response(data=expenses, message="Expenses retrieved successfully")

@router.get("/summary", response_model=ApiResponse[SummaryExpenseResponse])
def get_summary(db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user),
                month: int | None = Query(None, ge=1, le=12),
                year: int | None = Query(None, ge=0),
            ):
            summary = get_summary_service(db, current_user.id, month, year)
            return success_response(data=summary, message="Summary retrieved successfully")

@router.get("/stats", response_model=ApiResponse[StatisticsExpenseResponse])
def get_stats(db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user),
                month: int | None = Query(None, ge=1, le=12),
                year: int | None = Query(None, ge=0),
            ):
            statistic = get_stats_service(db, current_user.id, month, year)
            return success_response(data=statistic, message="Statistics retrieved successfully")

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    delete_expense_service(db, expense_id, current_user.id)
    return success_response(message="Expense deleted successfully")

@router.put("/{expense_id}", response_model=ApiResponse[ExpenseResponse])
def update_expense(
    updated: ExpenseCreate, 
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    updated_expense = update_expense_service(db, updated, expense_id, current_user.id)
    return success_response(data=updated_expense, message="Expense updated successfully")