from sqlalchemy.orm import relationship
from .access import Access
from .users_associated import UserAssociated
from .user_root import UserRoot
from .bee_type import BeeType
from .hive import Hive
from .sensor_readings import Sensor
from .hive_analysis import HiveAnalysis
from .analysis_backup import AnalysisBackup

def configure_relationships():
    Access.users_root = relationship('UserRoot', back_populates = 'access', cascade = "all, delete")
    UserRoot.access = relationship('Access', back_populates = 'users_root')
    
    Access.users_associated = relationship('UserAssociated', back_populates = 'access', cascade = "all, delete")
    UserAssociated.access = relationship('Access', back_populates = 'users_associated')

    UserRoot.users_associated = relationship('UserAssociated', back_populates = 'user_root', cascade = "all, delete")
    UserAssociated.user_root = relationship('UserRoot', back_populates = 'users_associated')

    UserRoot.bee_types = relationship("BeeType", back_populates = "user_root", cascade = "all, delete-orphan")
    BeeType.user_root = relationship('UserRoot', back_populates = 'bee_types')

    UserRoot.hives = relationship('Hive', back_populates = 'owner', cascade = "all, delete")
    Hive.owner = relationship('UserRoot', back_populates = 'hives')

    UserRoot.analysis = relationship('HiveAnalysis', back_populates = 'user_root', cascade = "all, delete")
    HiveAnalysis.user_root = relationship('UserRoot', back_populates = 'analysis')

    UserRoot.backups = relationship('AnalysisBackup', back_populates='user_root', cascade = "all, delete")
    AnalysisBackup.user_root = relationship('UserRoot', back_populates='backups')

    BeeType.hives = relationship('Hive', back_populates = 'bee_type', cascade = "all, delete")
    Hive.bee_type = relationship('BeeType', back_populates = 'hives')
    
    Hive.sensors = relationship("Sensor", back_populates = "hive", cascade = "all, delete-orphan")
    Sensor.hive = relationship("Hive", back_populates = "sensors")

    Hive.analyses = relationship("HiveAnalysis", back_populates = "hive", cascade = "all, delete-orphan")
    HiveAnalysis.hive = relationship("Hive", back_populates = "analyses")

    HiveAnalysis.backup = relationship('AnalysisBackup', back_populates = 'analysis', cascade = "all, delete")
    AnalysisBackup.analysis = relationship('HiveAnalysis', back_populates = 'backup')