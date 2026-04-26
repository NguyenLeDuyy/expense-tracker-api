# Expense Tracker API

A RESTful API for personal expense tracking with JWT authentication, budget management, and spending analytics.

**Tech Stack:** Python · FastAPI · SQLAlchemy · PostgreSQL · Alembic · Docker

**[Live Demo](https://expense-tracker-api-production-0b8c.up.railway.app/docs)**

---

## 🚀 Features

- 🔐 JWT auth (access + refresh token)
- 🔑 Secure password hashing (bcrypt)
- 👤 Multi-user data isolation
- 💸 Expense management (CRUD)
- 🗂️ Category CRUD with monthly budget limit
- ⚠️ Budget overspend warning
- 🔍 Filtering, sorting, and pagination
- 📊 Monthly summary + statistics
- 🚨 Unified error response format
- 📝 Request logging middleware
- 🧱 Clean layered architecture (Router → Service → CRUD)
- 🗄️ Database migration with Alembic
- ✅ 17 unit tests

---

## 📡 API Endpoints

### 🔐 Auth

| Method | Path | Description | Auth |
|--------|------|-------------|:----:|
| `POST` | `/auth/register` | Register a new user | ❌ |
| `POST` | `/auth/login` | Login, returns access + refresh token | ❌ |
| `POST` | `/auth/refresh` | Refresh access token | ❌ |
| `GET` | `/auth/me` | Get current user profile | ✅ |

### 💸 Expenses

| Method | Path | Description | Auth |
|--------|------|-------------|:----:|
| `POST` | `/expenses/` | Create a new expense | ✅ |
| `GET` | `/expenses/` | List expenses (filter / sort / paginate) | ✅ |
| `PUT` | `/expenses/{id}` | Update an expense | ✅ |
| `DELETE` | `/expenses/{id}` | Delete an expense | ✅ |
| `GET` | `/expenses/summary` | Monthly spending summary by category | ✅ |
| `GET` | `/expenses/stats` | Month-over-month spending statistics | ✅ |

### 🗂️ Categories

| Method | Path | Description | Auth |
|--------|------|-------------|:----:|
| `POST` | `/categories/` | Create a category | ✅ |
| `GET` | `/categories/` | List all categories | ✅ |
| `PUT` | `/categories/{id}` | Update a category | ✅ |
| `DELETE` | `/categories/{id}` | Delete a category | ✅ |

---

## 🧱 Tech Stack

- **Backend:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Migration:** Alembic
- **Authentication:** JWT (python-jose), bcrypt
- **Config:** pydantic-settings
- **Testing:** pytest
- **DevOps:** Docker, Docker Compose

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
├── main.py                  # App entry point, middleware, exception handlers
├── database.py              # Database engine and session
├── models/                  # SQLAlchemy models
├── schemas/                 # Pydantic request/response schemas
├── crud/                    # Database operations
├── services/                # Business logic
├── routers/                 # API route handlers
├── app/core/                # Config, auth, logging, exceptions
├── alembic/                 # Database migrations
├── tests/                   # Unit tests
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## 🚀 Quick Start (Local)

1. Clone repo
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in values
5. Run migrations: `alembic upgrade head`
6. Start server: `uvicorn main:app --reload`
7. Open http://localhost:8000/docs

## 🐳 Quick Start (Docker)

1. `docker-compose up --build`
2. Open http://localhost:8000/docs

---

## 📊 API Documentation

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 🧪 Running Tests

```bash
pytest -v
pytest --cov=. --cov-report=term-missing -v
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

| Variable | Description | Required | Default |
|----------|-------------|:--------:|---------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ | — |
| `SECRET_KEY` | JWT signing key (`secrets.token_hex(32)`) | ✅ | — |
| `ALGORITHM` | JWT signing algorithm | ❌ | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes | ❌ | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime in days | ❌ | `7` |
| `JWT_ISSUER` | JWT issuer claim | ❌ | `expense-tracker-api` |

Example `.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/expense_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
JWT_ISSUER=expense-tracker-api
```

---

## 👤 Author

**Nguyen Le Duy**
- GitHub: [@NguyenLeDuyy](https://github.com/NguyenLeDuyy)
- Email: nguyenleduy10122004@gmail.com
