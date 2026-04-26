from pydantic import BaseModel, Field, ConfigDict


class CategoryCreate(BaseModel):
    name: str = Field(json_schema_extra={"example": "Food"})
    monthly_budget: int = Field(ge=0, json_schema_extra={"example": 1000000})

class CategoryResponse(BaseModel):
    id: int
    name: str
    monthly_budget: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)