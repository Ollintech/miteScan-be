from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from db.database import Base

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)
    cnpj = Column(String(14), nullable = False)
    email = Column(String(100),unique = True, nullable = False)
    password_hash = Column(String(255), nullable = False)
    last_login = Column(DateTime, nullable = True)
    access_id = Column(Integer, ForeignKey('accesses.id'), nullable = False)