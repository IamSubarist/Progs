from sqlite3 import Date
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

engine = create_engine('sqlite:///pravo.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class People(Base):
    __tablename__ = 'peoples'
    user_id = Column(String, nullable=False)
    people_id = Column(Integer, primary_key=True)
    nickname = Column(String, nullable=False)
    rang = Column(String, nullable=False)
    post = Column(String, nullable=False)
    raising = Column(String, nullable=False)
    # date = Column(String, nullable=False)

Base.metadata.create_all(engine)