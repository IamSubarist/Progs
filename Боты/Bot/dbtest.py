from sqlite3 import Date
from numpy import integer
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

engine = create_engine('sqlite:///uborkasavoskintest.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Flight(Base):
    __tablename__ = 'flight'
    id = Column(Integer, primary_key=True)
    flight_number = Column(Integer, nullable=False)
    user_id = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date = Column(String, nullable=False)

class Tonnes(Base):
    __tablename__ = 'tonnes'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    tonnes = Column(Integer, nullable=False)

class Kilometers(Base):
    __tablename__ = 'kilometers'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    kilometers = Column(Integer, nullable=False)

class Flightsinday(Base):
    __tablename__ = 'flightsinday'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    flightsinday = Column(Integer, nullable=False)

class Flights(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    flights = Column(Integer, nullable=False)
    last_name = Column(String, nullable=False)
    date = Column(String, nullable=False)

Base.metadata.create_all(engine)