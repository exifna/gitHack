from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

#   init all tables

from src.tables import *

engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})  # connect to db
Base.metadata.create_all(engine)  # run init

DBSession = sessionmaker(autoflush=False, bind=engine)
session = DBSession()