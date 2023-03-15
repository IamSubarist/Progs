from sqlite3 import Date
from numpy import integer
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

engine = create_engine('sqlite:///uborkasavoskin.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Bunkers(Base):
    __tablename__ = 'bunkers'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    bunkers = Column(Integer, nullable=False)
    last_name = Column(String, nullable=False)
    date = Column(String, nullable=False)

Base.metadata.create_all(engine)