from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    monthly_budget: int

class CategoryResponse(BaseModel):
    id: int
    name: str
    monthly_budget: int
    user_id: int

    class Config:
        from_attributes = True