"""Database helpers and session management."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker


Base = declarative_base()
SessionLocal = scoped_session(sessionmaker())
_engine = None


def init_database(database_uri: str):
    """Bind the SQLAlchemy session/metadata to the configured database."""
    global _engine
    _engine = create_engine(database_uri, echo=False)
    SessionLocal.remove()
    SessionLocal.configure(bind=_engine)
    Base.metadata.create_all(_engine)
    return _engine


@contextmanager
def get_session() -> Iterator[sessionmaker]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def session_factory():
    return SessionLocal
