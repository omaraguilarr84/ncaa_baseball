"""
Pydantic schemas for Teams.

These classes define the shape of data coming IN to the API (TeamCreate)
and going OUT of the API (TeamOut). This keeps validation and API contracts
clean and explicit.
"""

from pydantic import BaseModel
from typing import Optional


class TeamCreate(BaseModel):
    name: str
    short_name: Optional[str] = None
    conference: Optional[str] = None


class TeamOut(BaseModel):
    id: int
    name: str
    short_name: Optional[str] = None
    conference: Optional[str] = None

    class Config:
        # Allows FastAPI to serialize SQLAlchemy ORM objects into this schema
        from_attributes = True