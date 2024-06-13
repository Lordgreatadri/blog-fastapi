from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip/hostname>/<database_name>"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

#https://fastapi.tiangolo.com/tutorial/sql-databases/
engine = create_engine(
    SQLALCHEMY_DATABASE_URL #, connect_args={"check_same_thread": False} exclusively add this if using sqlite runnig in memory
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()