from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class HiveAnalysis(Base):
    __tablename__ = 'hive_analyses'

    id = Column(Integer, primary_key = True, autoincrement = True)
    hive_id = Column(Integer, ForeignKey('hives.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    image_path = Column(String(255), nullable = False)
    varroa_detected = Column(Boolean, nullable = False, default = False)
    detection_confidence = Column(Float, nullable = False)
    created_at = Column(DateTime, default = datetime.utcnow)

    hive = relationship('Hive', back_populates = 'analyses')
    user = relationship('User', back_populates = 'analyses')
    backup = relationship('AnalysisBackup', back_populates = 'analysis')
