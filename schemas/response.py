from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status: str
    data: T | None = None
    message: str | None = None

def success_response(data: Any = None, message: str = "Success"):
    return ApiResponse(status="success", data=data, message=message)

def error_response(message: str = "Error"):
    return ApiResponse(status="error", data=None, message=message)