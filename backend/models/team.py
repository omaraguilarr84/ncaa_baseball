"""
SQLAlchemy model definitions for the database.

This file defines the Team ORM model, which maps to the `teams` table in MySQL.
We use this model to read/write team records through SQLAlchemy instead of raw SQL.
"""

from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Team(Base):
    """ORM model for the `teams` table."""
    __tablename__ = "teams"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    short_name = Column(String(64))
    conference = Column(String(64))
    created_at = Column(TIMESTAMP, server_default=func.now())
