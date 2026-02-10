"""
Shared SQLAlchemy Base.

All ORM models should import Base from here so they share the same metadata.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
