import os
from loguru import logger
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(os.getenv("CLICKHOUSE_URL"))

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

ClickhouseBase = declarative_base()


def get_session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.exception(str(e))
        db.rollback()
    finally:
        db.close()


__all__ = ["get_session", "ClickhouseBase", "engine"]
