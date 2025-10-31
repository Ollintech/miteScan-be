from sqlalchemy import Column, Integer, Float, ForeignKey, String
from db.database import Base

class Hive(Base):
    __tablename__ = 'hives'

    id = Column(Integer, primary_key = True)
    account = Column(String(50), ForeignKey('users_root.account'), nullable = False)
    bee_type_id = Column(Integer, ForeignKey('bee_types.id'))
    location_lat = Column(Float, nullable = False)
    location_lng = Column(Float, nullable = False)
    size = Column(Integer, nullable = False)
    humidity = Column(Float, nullable = True)
    temperature = Column(Float, nullable = True)