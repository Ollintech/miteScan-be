from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)
    cnpj = Column(Integer, nullable = False)