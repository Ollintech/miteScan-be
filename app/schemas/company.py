from pydantic import BaseModel
from typing import Optional

class CompanyCreate(BaseModel):
    name: str
    cnpj: int

class CompanyResponse(BaseModel):
    id: int
    name: str
    cnpj: int

    class Config:
        from_attributes = True

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    cnpj: Optional[int] = None