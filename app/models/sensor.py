from sqlalchemy import Column, Integer, Float
from db.database import Base

class Sensor(Base):
    __tablename__ = 'sensores'

    id = Column(Integer, primary_key = True)
    humidity = Column(Float, nullable = True)
    temperature = Column(Float, nullable = True)