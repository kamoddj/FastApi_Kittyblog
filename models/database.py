from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:nuttertools@localhost/cat_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# engine = create_engine("sqlite:///./cat_DB.db",
#                        connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, bind=engine, autoflush=True)

Base = declarative_base()

Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
