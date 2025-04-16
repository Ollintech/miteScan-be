from sqlalchemy import Column, Integer, String
from db.database import Base

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)
    cnpj = Column(String(14), nullable = False)