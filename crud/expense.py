from datetime import date
from models.expense import Expense
from schemas.expense import ExpenseCreate
from sqlalchemy.orm import Session

def get_expense_by_id(db: Session, expense_id, user_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()

def create_expense(db: Session, expense_data: ExpenseCreate, user_id: int):
    expense_date = expense_data.date or date.today()
    
    expense = Expense(
            amount=expense_data.amount,
            category_id=expense_data.category_id,
            user_id=user_id,
            date = expense_date
        )
    db.add(expense)
    return expense

def get_expenses(
    db: Session,
    user_id: int,
    category_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    min_amount: int | None = None,
    max_amount: int | None = None,
    sort_by: str = "date_desc",
    page: int = 1,
    page_size: int = 10,
):
    
    # 1. Initialization
    query = db.query(Expense).filter(Expense.user_id == user_id)

    # 2. Filtering
    if category_id is not None:
        query = query.filter(Expense.category_id == category_id)
    
    if start_date:
        query = query.filter(Expense.date >= start_date)
        
    if end_date:
        query = query.filter(Expense.date <= end_date)
    
    if min_amount is not None:
        query = query.filter(Expense.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(Expense.amount <= max_amount)

    # Total
    total = query.count()

    # 4. Sorting
    if sort_by == "date_desc":
        query = query.order_by(Expense.date.desc())
    elif sort_by == "date_asc":
        query = query.order_by(Expense.date.asc())
    elif sort_by == "amount_desc":
        query = query.order_by(Expense.amount.desc())
    elif sort_by == "amount_asc":
        query = query.order_by(Expense.amount.asc())
    
    # 5. Pagination
    query = query.offset((page - 1) * page_size).limit(page_size)

    return query.all(), total
    
def delete_expense(db: Session, expense_id: int, user_id: int):
    expense = get_expense_by_id(db, expense_id, user_id)

    if not expense:
        return None
    
    db.delete(expense)
    return expense

def update_expense(db: Session, expense_data: ExpenseCreate, expense_id: int, user_id: int):
    expense = get_expense_by_id(db, expense_id, user_id)

    if not expense:
        return None
    
    expense.amount = expense_data.amount
    expense.category_id = expense_data.category_id
    return expense
