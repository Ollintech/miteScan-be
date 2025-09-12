from sqlalchemy import Column, Integer, Float, ForeignKey
from db.database import Base

class Sensor(Base):
    __tablename__ = 'sensor_readings'

    id = Column(Integer, primary_key=True)
    hive_id = Column(Integer, ForeignKey('hives.id'), nullable = False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)