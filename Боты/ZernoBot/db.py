from sqlite3 import Date
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

engine = create_engine('sqlite:///zernobot.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    tonnes = Column(Float, nullable=False)
    people = Column(Integer, nullable=False)
    total_cash = Column(Integer, nullable=False)
    your_cash = Column(Integer, nullable=False)
    date = Column(String, nullable=False)

class Active_Order(Base):
    __tablename__ = 'active_orders'
    order_id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    tonnes = Column(Float, nullable=False)
    people = Column(Integer, nullable=False)
    total_cash = Column(Integer, nullable=False)
    your_cash = Column(Integer, nullable=False)
    date = Column(String, nullable=False)

class Settings(Base):
    __tablename__ = 'settings'
    user_id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)

Base.metadata.create_all(engine)