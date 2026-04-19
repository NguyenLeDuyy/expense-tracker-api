import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load biến từ .env
load_dotenv()

DATABASE_URL = str(os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost:5432/expense_db"))

# SQLite cần check_same_thread
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True,  # tránh connection chết (quan trọng với Postgres)
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    )


class Base(DeclarativeBase):
    pass