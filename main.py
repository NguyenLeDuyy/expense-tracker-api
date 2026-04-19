from fastapi import FastAPI
from database import engine, Base
from routers.expense import router as expense_router
from routers.user import router as user_router
from routers.category import router as category_router

app = FastAPI()

# Create database tables
# Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(expense_router)
app.include_router(user_router)
app.include_router(category_router)