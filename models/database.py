from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.db_config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@"
                           f"{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, bind=engine, autoflush=True)

Base = declarative_base()

Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
