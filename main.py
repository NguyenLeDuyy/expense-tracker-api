from fastapi import FastAPI
from database import engine, Base
from routers.expense import router as expense_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(expense_router)
