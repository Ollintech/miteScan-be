from sqlalchemy import Column, Integer, String, ForeignKey, Text
from db.database import Base

class BeeType(Base):
    __tablename__ = 'bee_types'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), unique = True, nullable = False)
    description = Column(Text, nullable = False)
    user_root_id = Column(Integer, ForeignKey("users_root.id"), nullable = False)