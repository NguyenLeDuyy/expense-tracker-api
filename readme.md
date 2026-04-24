# Expense Tracker API

A production-oriented RESTful backend for managing personal expenses, built with FastAPI following a layered architecture.

---

## 🚀 Features

- User authentication (JWT-based login & register)
- Secure password hashing (bcrypt)
- Multi-user system (each user accesses only their own data)
- Expense management (CRUD)
- Category management
- Filtering, sorting, and pagination
- Advanced analytics (monthly reports, trends)
- Refresh token mechanism
- Clean layered architecture (Router → Service → CRUD)
- Database migration with Alembic

---

## 🧱 Tech Stack

- **Backend:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL / SQLite
- **Migration:** Alembic
- **Authentication:** JWT (python-jose), bcrypt
- **Tools:** Docker, pytest (planned)

---

## 🧠 Architecture

`Client → Router → Service → CRUD → Database`

### Responsibilities

- **Router:** Handle HTTP request/response
- **Service:** Business logic, transaction handling
- **CRUD:** Direct database interaction

---

## 🔐 Authentication & Authorization

- JWT access token
- Password hashing using bcrypt
- Protected routes using dependency injection
- User-based data isolation

---

## 📂 Project Structure

```text
app/
├── core/       # config, security (JWT, hashing)
├── models/     # SQLAlchemy models
├── schemas/    # Pydantic schemas
├── crud/       # database operations
├── services/   # business logic
├── routers/    # API endpoints
└── main.py     # entry point

alembic/        # database migrations
alembic.ini
```

---

## ⚙️ Setup (Local)

### 1. Clone repository

```bash
git clone https://github.com/NguyenLeDuyy/expense-tracker-api.git
cd expense-tracker-api
```

### 2. Create virtual environment

```bash
python -m venv venv

# Activate:
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file in the root directory and configure your database URL. You can use the provided example:

```bash
cp .env.example .env
# Edit .env to set your DATABASE_URL, SECRET_KEY, etc.
```

### 5. Run migrations

```bash
alembic upgrade head
```

### 6. Start server

```bash
uvicorn main:app --reload
```

---

## 📊 API Documentation

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 🐳 Run with Docker (optional)

```bash
docker-compose up --build
```

---

## 🧪 Testing (coming soon)

```bash
pytest -v
```

---

## 🌐 Deployment

Live demo: *(update your Railway/Render link here)*

---

## 📌 Future Improvements

- [ ] Role-based access control (RBAC)
- [ ] Performance optimization
- [ ] Full test coverage

---

## 👤 Author

**Nguyen Le Duy**
- GitHub: [@NguyenLeDuyy](https://github.com/NguyenLeDuyy)
- Email: nguyenleduy10122004@gmail.com
