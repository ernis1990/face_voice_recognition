import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///neighbordetector.db')
Base = declarative_base()

class Projektas(Base):
    __tablename__ = 'neighbordetector'
    id = Column(Integer, primary_key=True)
    name = Column("Name", String)
    time = Column("Time", String)
    # created_date = Column("Time", DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, time):
        self.name = name
        self.time = time


Base.metadata.create_all(engine)