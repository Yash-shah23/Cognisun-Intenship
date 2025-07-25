from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///qa.db')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class QA(Base):
    __tablename__ = 'qa'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
