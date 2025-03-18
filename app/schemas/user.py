from pydantic import BaseModel, EmailStr, validator, Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int

    @validator('password')
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    status: bool
    role_id: int

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None