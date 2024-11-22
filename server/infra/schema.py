from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from infra import engine

Base = declarative_base()


class Strategy(Base):
    __tablename__ = "starategy"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)


Base.metadata.create_all(bind=engine.engine)
