from sqlite3 import Date
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///zernoapp.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    tonnes = Column(Integer, nullable=False)
    culture = Column(String, nullable=False)
    people = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    summ = Column(Integer, nullable=False)
    date = Column(String, nullable=False)

Base.metadata.create_all(engine)