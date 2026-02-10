"""
Database session factory.

FastAPI endpoints should NOT use a global DB connection directly.
Instead, each request should open a short-lived SQLAlchemy Session and close it
after the request finishes. This file provides the SessionLocal factory.
"""

from sqlalchemy.orm import sessionmaker
from backend.db import engine

# SessionLocal() creates a new SQLAlchemy Session connected to our MySQL engine
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
