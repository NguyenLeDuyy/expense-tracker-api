from models import Expense
from sqlalchemy.orm import Session
def create_expense(db: Session, amount: int, category: str):
    expense = Expense(amount=amount, category=category)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_expenses(db: Session):
    return db.query(Expense).all()
    
def delete_expense(db: Session, expense_id: int):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        return None
    
    db.delete(expense)
    db.commit()
    return expense

def update_expense(db: Session, amount: int, category: str, expense_id: int):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        return None
    
    expense.amount = amount
    expense.category = category
    
    db.commit()
    db.refresh(expense)
    return expense
