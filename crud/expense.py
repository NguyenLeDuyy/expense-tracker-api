from datetime import datetime
from models.expense import Expense
from schemas.expense import ExpenseCreate
from sqlalchemy.orm import Session

def get_expense_by_id(db: Session, expense_id, user_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()

def create_expense(db: Session, expense_data: ExpenseCreate, user_id: int):
    expense_date = expense_date = expense_data.date or datetime.date.today()
    
    
    expense = Expense(
            amount=expense_data.amount,
            category_id=expense_data.category_id,
            user_id=user_id,
            date = expense_date
        )
    db.add(expense)
    return expense

def get_expenses(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()
    
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
