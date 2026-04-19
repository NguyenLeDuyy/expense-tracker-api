from datetime import date as dt_date
from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: int
    category_id: int
    date: dt_date | None = None    

class ExpenseResponse(BaseModel):
    id: int
    amount: int
    category_id: int
    date: dt_date
    warning: str | None = None

    class Config:
        from_attributes = True