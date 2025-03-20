from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Hive(Base):
    __tablename__ = 'hives'

    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bee_type_id = Column(Integer, ForeignKey('bee_types.id'))
    location_lat = Column(Float, nullable = False)
    location_lng = Column(Float, nullable = False)
    size = Column(Integer, nullable = False)
    humidity = Column(Float, nullable = True)
    temperature = Column(Float, nullable = True)

    owner = relationship('User', back_populates = 'hives')
    bee_type = relationship('BeeType', back_populates = 'hives')
    analyses = relationship("HiveAnalysis", back_populates = "hive", cascade = "all, delete-orphan")
