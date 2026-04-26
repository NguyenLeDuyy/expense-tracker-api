from pydantic import BaseModel, Field, ConfigDict


class CategoryCreate(BaseModel):
    name: str
    monthly_budget: int = Field(ge=0)

class CategoryResponse(BaseModel):
    id: int
    name: str
    monthly_budget: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)