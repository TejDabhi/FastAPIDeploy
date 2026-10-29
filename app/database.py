from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://socialmedia_user:4aGTF5w8KOzd2AUuTR8xOHzF5Npx2Z9X@dpg-dbhiiim1egvs73flnp40-a.oregon-postgres.render.com/socialmedia_hffq"

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autoflush=False,bind=engine)

Base= declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()