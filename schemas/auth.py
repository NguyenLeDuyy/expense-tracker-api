from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(json_schema_extra={"example": "user@example.com"})
    password: str = Field(min_length=8, max_length=128, json_schema_extra={"example": "securepassword123"})


class LoginRequest(BaseModel):
    email: EmailStr = Field(json_schema_extra={"example": "user@example.com"})
    password: str = Field(min_length=8, max_length=128, json_schema_extra={"example": "securepassword123"})


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    id: int
    email: EmailStr

class RefreshRequest(BaseModel):
    refresh_token: str = Field(json_schema_extra={"example": "<your_refresh_token>"})