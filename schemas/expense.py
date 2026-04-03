from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: int
    category: str