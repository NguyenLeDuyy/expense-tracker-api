from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import create_expense, get_expenses, update_expense, delete_expense
from database import engine, Base, SessionLocal
from models import Expense
from schemas import ExpenseCreate


app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependency pattern in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "DB ready 🚀"}

@app.post("/expense")
def create_expense_api(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return create_expense(db, expense.amount, expense.category)

@app.get("/expenses")
def get_expenses_api(db: Session = Depends(get_db)):
    return get_expenses(db)

@app.delete("/expense/{expense_id}")
def delete_expense_api(expense_id: int, db: Session = Depends(get_db)):
    deleted = delete_expense(db, expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense does not exist")
    return {"message": "Deleted"}

@app.put("/expense/{expense_id}")
def update_expense_api(expense_id: int, updated: ExpenseCreate, db: Session = Depends(get_db)):
    expense = update_expense(db, updated.amount, updated.category, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense does not exist")
    return {"message": "Updated"}