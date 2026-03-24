from fastapi import FastAPI
from database import engine, Base, SessionLocal
from models import Expense
from schemas import ExpenseCreate


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "DB ready 🚀"}

@app.post("/expense")
def create_expense(expense: ExpenseCreate):
    db = SessionLocal()

    new_expense = Expense(
        amount=expense.amount,
        category=expense.category
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    db.close()

    return {"message": "Expense created"}

@app.get("/expense")
def get_expenses():
    db = SessionLocal()

    expenses = db.query(Expense).all()

    db.close()

    return expenses