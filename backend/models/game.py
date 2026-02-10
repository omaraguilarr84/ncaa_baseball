"""
Game ORM model.

Maps the `games` table. Each game links to two teams via:
- home_team_id -> teams.id
- away_team_id -> teams.id
"""

from sqlalchemy import Column, BigInteger, Integer, Date, Enum, TIMESTAMP, func
from backend.models.base import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    game_date = Column(Date, nullable=False)
    season_year = Column(Integer, nullable=False)

    home_team_id = Column(BigInteger, nullable=False)
    away_team_id = Column(BigInteger, nullable=False)

    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)

    status = Column(
        Enum("scheduled", "final", "in_progress"),
        nullable=False,
        default="final",
    )

    created_at = Column(TIMESTAMP, server_default=func.now())
