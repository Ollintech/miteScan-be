from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserAssociatedCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    access_id: int
    user_root_id: int
    
    @field_validator('password')
    @classmethod
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres')
        return v

class UserAssociatedResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    status: bool
    access_id: int
    user_root_id: int

    class Config:
        from_attributes = True

class UserAssociatedUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    status: Optional[bool] = False
    access_id: Optional[int] = None
    user_root_id: Optional[int] = None