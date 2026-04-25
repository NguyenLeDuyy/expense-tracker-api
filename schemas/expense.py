from pydantic import Field
from datetime import date as dt_date
from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: int = Field(gt=0)
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

class PaginatedExpenseResponse(BaseModel):
    items: list[ExpenseResponse]
    total_count: int
    page: int
    page_size: int

class SummaryEachCategory(BaseModel):
    category_name: str
    total: float

class SummaryExpenseResponse(BaseModel):
    month: str
    total: int
    by_category: list[SummaryEachCategory]

class StatisticsExpenseResponse(BaseModel):
    daily_average: int
    top_category: SummaryEachCategory | None = None
    this_month_total: int | None = None
    last_month_total: int | None = None
    month_over_month_change: float | None = None