from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
)

from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(100), nullable = False)
    email = Column(String(100),unique = True, nullable = False)
    password_hash = Column(String(255), nullable = False)
    last_login = Column(DateTime, nullable = True)
    status = Column(Boolean, nullable = False, default = False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', back_populates = 'users')
    hives = relationship('Hive', back_populates = 'owner')
    analyses = relationship('HiveAnalysis', back_populates = 'user')
    backups = relationship('AnalysisBackup', back_populates = 'user')

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(100), nullable = False)
    description = Column(String(255), nullable = False)

    users = relationship('User', back_populates = 'role')

class BeeType(Base):
    __tablename__ = 'bee_types'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(100), unique = True, nullable = False)
    description = Column(Text, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id"))

    hives = relationship('Hive', back_populates = 'bee_type')
    user = relationship('User', back_populates = 'bee_types')

class Hive(Base):
    __tablename__ = 'hives'

    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bee_type_id = Column(Integer, ForeignKey('bee_types.id'))
    location_lat = Column(Float, nullable = False)
    location_lng = Column(Float, nullable = False)
    size = Column(Integer, nullable = False)
    humidity = Column(Float, nullable = False)
    temperature = Column(Float, nullable = False)

    owner = relationship('User', back_populates = 'hives')
    bee_type = relationship('BeeType', back_populates = 'hives')
    analyses = relationship('HiveAnalysis', back_populates = 'hive')

class HiveAnalysis(Base):
    __tablename__ = 'hive_analyses'

    id = Column(Integer, primary_key = True, autoincrement = True)
    hive_id = Column(Integer, ForeignKey('hives.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    image_path = Column(String(255), nullable = False)
    varroa_detected = Column(Boolean, nullable = False, default = False)
    detection_confidence = Column(Float, nullable = False)

    hive = relationship('Hive', back_populates = 'analyses')
    user = relationship('User', back_populates = 'analyses')
    backup = relationship('AnalysisBackup', back_populates = 'analysis')

class AnalysisBackup(Base):
    __tablename__ = 'analysis_backups'

    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_path = Column(String(255), nullable = False)
    analysis_id = Column(Integer, ForeignKey('hive_analyses.id'))

    analysis = relationship('HiveAnalysis', back_populates = 'backup')
    user = relationship('User', back_populates='backups')


DATABASE_URL = 'url do banco de dados que será utilizado. Exemplo: sqlite:///hive_analysis.db'
engine = create_engine(DATABASE_URL, echo = True)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind = engine)

# Testando o Banco de dados

session = SessionLocal()

new_user = User(name = "João Apicultor", email = "joao@example.com", password_hash = "hash")
session.add(new_user)
session.commit()

bee_type = BeeType(name = "Apis mellifera", description = "Abelha europeia comum")
session.add(bee_type)
session.commit()

hive = Hive(user_id = new_user.id, bee_type_id = bee_type.id, location_lat = -23.55, location_lng = -46.63, size = 5000)
session.add(hive)
session.commit()

analysis = HiveAnalysis(hive_id = hive.id, user_id = new_user.id, image_path = "images/colmeia1.jpg", varroa_detected = True, detection_confidence = 95.0)
session.add(analysis)
session.commit()

analyses = session.query(HiveAnalysis).all()
for a in analyses:
    print(f"Análise ID {a.id}: Varroa {'Detectada' if a.varroa_detected else 'Não Detectada'} - Confiança {a.detection_confidence}%")

session.close()
