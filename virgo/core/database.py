from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

engine = create_engine("sqlite:///virgo.db", connect_args={"check_same_thread": False}, echo=True)

# Use scoped_session for thread safety
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
