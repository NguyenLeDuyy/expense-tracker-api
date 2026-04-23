# Expense Tracker API

RESTful backend API for expense management built with FastAPI, SQLAlchemy, and Alembic.

## Features
- Authentication & authorization
- Multi-user expense management
- Expense CRUD
- Category management
- Filtering / pagination / summary
- PostgreSQL + Alembic migrations

## Architecture
Client → Router → Service → CRUD → Database

## Tech Stack
FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT, bcrypt

## ⚙️ Setup & Run

### 1. Clone repository

git clone https://github.com/<your-username>/expense-tracker-api.git
cd expense-tracker-api

---

### 2. Create virtual environment

python -m venv venv

Activate:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

---

### 3. Install dependencies

pip install -r requirements.txt

---

### 4. Run server

python -m uvicorn main:app --reload

---

### 5. Open API docs

http://127.0.0.1:8000/docs

---

## 🧪 Example API

### Create expense

POST /expense

{
"amount": 100,
"category": "food"
}

---

### Get all expenses

GET /expenses

---

## 📌 Notes

* Database file will be created automatically
* Make sure virtual environment is activated

---

## 👨‍💻 Author

Nguyen Le Duy
