from sqlalchemy import Column, Integer, Float, ForeignKey
from db.database import Base

class Sensor(Base):
    __tablename__ = 'sensores'

    id = Column(Integer, primary_key=True)
    hive_id = Column(Integer, ForeignKey('hives.id'))
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
