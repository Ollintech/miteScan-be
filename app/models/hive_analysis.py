from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, func
from db.database import Base

class HiveAnalysis(Base):
    __tablename__ = 'hive_analyses'

    id = Column(Integer, primary_key = True)
    hive_id = Column(Integer, ForeignKey('hives.id'))
    user_root_id = Column(Integer, ForeignKey('users_root.id'))
    image_path = Column(String(255), nullable = False)
    varroa_detected = Column(Boolean, nullable = False, default = False)
    detection_confidence = Column(Float, nullable = False)
    created_at = Column(DateTime, default = func.now())