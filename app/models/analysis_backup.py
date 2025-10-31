from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class AnalysisBackup(Base):
    __tablename__ = 'analysis_backups'

    id = Column(Integer, primary_key = True, nullable = False)
    account = Column(String, ForeignKey('users_root.account'), nullable = False)
    file_path = Column(String(255), nullable = False)
    analysis_id = Column(Integer, ForeignKey('hive_analyses.id'), nullable = False)