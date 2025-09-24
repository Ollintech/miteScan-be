from sqlalchemy import Column, Integer, Float, ForeignKey
from db.database import Base

class Hive(Base):
    __tablename__ = 'hives'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users_root.id'))
    bee_type_id = Column(Integer, ForeignKey('bee_types.id'))
    location_lat = Column(Float, nullable = False)
    location_lng = Column(Float, nullable = False)
    size = Column(Integer, nullable = False)
    humidity = Column(Float, nullable = True)
    temperature = Column(Float, nullable = True)