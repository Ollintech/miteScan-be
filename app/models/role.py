from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(100), nullable = False)
    description = Column(String(255), nullable = False)

    users = relationship('User', back_populates = 'role')

