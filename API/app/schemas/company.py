from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class CompanyCreate(BaseModel):
    name: str
    cnpj: str
    email: EmailStr
    password: str
    access_id: int
    
    @field_validator('password')
    @classmethod
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres')
        return v

class CompanyResponse(BaseModel):
    id: int
    name: str
    cnpj: str
    email: EmailStr
    access_id: int

    class Config:
        from_attributes = True

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    cnpj: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    access_id: Optional[int] = None