from sqlalchemy import Column, Integer, String
from db.database import Base

class Access(Base):
    __tablename__ = 'accesses'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    description = Column(String(255), nullable = False)