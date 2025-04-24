from sqlalchemy.orm import relationship
from .access import Access
from .company import Company
from .user import User
from .bee_type import BeeType
from .hive import Hive
from .hive_analysis import HiveAnalysis
from .analysis_backup import AnalysisBackup

def configure_relationships():
    Access.users = relationship('User', back_populates = 'access', cascade = "all, delete")
    User.access = relationship('Access', back_populates = 'users')

    Company.users = relationship('User', back_populates = 'company', cascade = "all, delete")
    User.company = relationship('Company', back_populates = 'users')

    User.bee_types = relationship("BeeType", back_populates = "user", cascade = "all, delete-orphan")
    BeeType.user = relationship('User', back_populates = 'bee_types')

    User.hives = relationship('Hive', back_populates = 'owner', cascade = "all, delete")
    Hive.owner = relationship('User', back_populates = 'hives')

    User.analysis = relationship('HiveAnalysis', back_populates = 'user', cascade = "all, delete")
    HiveAnalysis.user = relationship('User', back_populates = 'analysis')

    User.backups = relationship('AnalysisBackup', back_populates='user', cascade = "all, delete")
    AnalysisBackup.user = relationship('User', back_populates='backups')

    BeeType.hives = relationship('Hive', back_populates = 'bee_type', cascade = "all, delete")
    Hive.bee_type = relationship('BeeType', back_populates = 'hives')

    Hive.analyses = relationship("HiveAnalysis", back_populates = "hive", cascade = "all, delete-orphan")
    HiveAnalysis.hive = relationship("Hive", back_populates = "analyses")

    HiveAnalysis.backup = relationship('AnalysisBackup', back_populates = 'analysis', cascade = "all, delete")
    AnalysisBackup.analysis = relationship('HiveAnalysis', back_populates = 'backup')