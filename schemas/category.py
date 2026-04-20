from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str
    monthly_budget: int = Field(ge=0)

class CategoryResponse(BaseModel):
    id: int
    name: str
    monthly_budget: int
    user_id: int

    class Config:
        from_attributes = True