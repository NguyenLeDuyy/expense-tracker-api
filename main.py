from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from app.core.exceptions import AppException
from fastapi import FastAPI
from routers.expense import router as expense_router
from routers.user import router as user_router
from routers.category import router as category_router

app = FastAPI()

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "data": None, "message": exc.message}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
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