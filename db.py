import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parkease.db')
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(Session)

def init_db():
    from models.Base import Base    
    Base.metadata.create_all(bind=engine)

def shutdown_session():
    db_session.remove()
