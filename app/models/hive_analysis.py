from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, func
from db.database import Base

class HiveAnalysis(Base):
    __tablename__ = 'hive_analyses'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement= True)
    hive_id = Column(Integer, ForeignKey('hives.id'), nullable = False)
    account = Column(String(50), ForeignKey('users_root.account'), nullable = False)
    image_path = Column(String(255), nullable = False)
    varroa_detected = Column(Boolean, nullable = False, default = False)
    detection_confidence = Column(Float, nullable = False)
    created_at = Column(DateTime, default = func.now())