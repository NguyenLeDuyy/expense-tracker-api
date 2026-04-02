from models import Expense
from schemas import ExpenseCreate
from sqlalchemy.orm import Session

def get_expense_by_id(db: Session, expense_id) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id).first()

def create_expense(db: Session, expense_data: ExpenseCreate):
    expense = Expense(amount=expense_data.amount, category=expense_data.category)
    db.add(expense)
    return expense

def get_expenses(db: Session):
    return db.query(Expense).all()
    
def delete_expense(db: Session, expense_id: int):
    expense = get_expense_by_id(db, expense_id)

    if not expense:
        return None
    
    db.delete(expense)
    return expense

def update_expense(db: Session, expense_data: ExpenseCreate, expense_id: int):
    expense = get_expense_by_id(db, expense_id)

    if not expense:
        return None
    
    expense.amount = expense_data.amount
    expense.category = expense_data.category
    return expense
