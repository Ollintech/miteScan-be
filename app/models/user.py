from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    email = Column(String(100),unique = True, nullable = False)
    password_hash = Column(String(255), nullable = False)
    last_login = Column(DateTime, nullable = True)
    status = Column(Boolean, nullable = False, default = False)
    access_id = Column(Integer, ForeignKey('accesses.id'), nullable = False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable = False)    