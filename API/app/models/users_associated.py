from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from db.database import Base

class User_Associated(Base):
    __tablename__ = 'users_associated'

    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)
    email = Column(String(100),unique = True, nullable = False)
    password_hash = Column(String(255), nullable = False)
    last_login = Column(DateTime, nullable = True)
    status = Column(Boolean, nullable = False, Default = False)
    access_id = Column(Integer, ForeignKey('accesses.id'), nullable = False)