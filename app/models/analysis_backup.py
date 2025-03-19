from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class AnalysisBackup(Base):
    __tablename__ = 'analysis_backups'

    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_path = Column(String(255), nullable = False)
    analysis_id = Column(Integer, ForeignKey('hive_analyses.id'))

    analysis = relationship('HiveAnalysis', back_populates = 'backup')
    user = relationship('User', back_populates='backups')

