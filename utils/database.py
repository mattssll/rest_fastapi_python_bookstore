from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

def start_database():
    sqlite_file_name = "database.db"
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)  # create tables
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print("database was started correctly")