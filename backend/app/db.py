import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def make_engine(url: str):
    return create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=5)


engine = make_engine(os.getenv("DATABASE_URL", "postgresql+psycopg://invalid@localhost/invalid"))
Session = sessionmaker(engine, expire_on_commit=False)


def get_db():
    with Session() as session:
        yield session
