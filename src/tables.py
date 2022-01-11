from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from src.database import Base
from src.types import GitObjectType


class Site(Base):
    __tablename__ = 'sites'

    id: int = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    site_name: str = Column('site_name', String)

class Log(Base):
    __tablename__ = 'logs'

    id: int= Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    time: int = Column('time', Integer)
    log_type: int = Column('log_type', Integer)
    text: str = Column('text', String)

class GitObject(Base):
    __tablename__ = 'git_objects'

    id: int = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    site_id: int = Column('site_id', ForeignKey('sites.id'))
    object_type: GitObjectType = Column('type', Integer)
    download: bool = Column('download', Boolean)
    _hash: str = Column('hash', String)
    path: str = Column('path', String)
    name: str = Column('name', String)

class InterestedFileName(Base):
    __tablename__ = 'interested_filename'

    id: int = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name: str = Column('name', String)



