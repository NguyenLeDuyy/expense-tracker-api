import time
from app.core.logging_config import setup_logging
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from app.core.exceptions import AppException
from fastapi import FastAPI
from routers.expense import router as expense_router
from routers.user import router as user_router
from routers.category import router as category_router

logger = setup_logging()

tags_metadata = [
    {"name": "Auth", "description": "Register, login, token refresh, and user profile"},
    {"name": "Expenses", "description": "CRUD operations, filtering, sorting, and pagination for expenses"},
    {"name": "Categories", "description": "Manage expense categories and monthly budgets"},
    {"name": "Statistics", "description": "Spending summaries and month-over-month analytics"},
]

app = FastAPI(
    title="Expense Tracker API",
    description="RESTful API for personal expense tracking with JWT authentication, budget management, and spending analytics.",
    version="1.0.0",
    contact={"name": "Nguyen Le Duy", "url": "https://github.com/NguyenLeDuyy"},
    openapi_tags=tags_metadata
)

# Thêm middleware log mỗi request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)
    logger.info(f"{request.method} {request.url.path} → {response.status_code} ({duration}s)")
    return response

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(f"{request.method} {request.url.path} → {exc.status_code}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "data": None, "message": exc.message}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"{request.method} {request.url.path} → 422: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"status": "error", "data": None, "message": str(exc.errors())}
    )

# Create database tables
# Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(expense_router)
app.include_router(user_router)
app.include_router(category_router)