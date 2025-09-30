from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class AnalysisBackup(Base):
    __tablename__ = 'analysis_backups'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users_root.id'))
    file_path = Column(String(255), nullable = False)
    analysis_id = Column(Integer, ForeignKey('hive_analyses.id'))