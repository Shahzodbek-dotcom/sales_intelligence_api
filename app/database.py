from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # .env dan o'qiydi
# Masalan: postgresql://user:password@localhost:5432/sales_db

engine = create_engine(DATABASE_URL, echo=False)  # echo=True debug uchun
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Bir marta ishlatib, jadvalarni yaratish uchun"""
    from .models import Base
    Base.metadata.create_all(bind=engine)