from contextlib import AbstractContextManager, contextmanager
from typing import ContextManager
import os
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy import create_engine


DB_URL = os.environ.get("PG_DSN")


class Base(DeclarativeBase):
    pass


class DBWriter:
    def __init__(self, dsn: str | None = None):
        self.engine = create_engine(dsn or DB_URL)
    
    def session(self) -> AbstractContextManager:
        return get_session(sessionmaker(self.engine))


@contextmanager
def get_session(maker: sessionmaker[Session]) -> ContextManager[Session]: # type: ignore
    with maker.begin() as session:
        try:
            yield session
        except Exception as e:
            print(f"Session {maker} rollback: {e}")
            session.rollback()
            raise
