from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///./notes.db"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


