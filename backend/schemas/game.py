"""
Pydantic schemas for Games.

- GameCreate: request payload for POST /games
- GameOut: response payload for created games
"""

from pydantic import BaseModel
from datetime import date
from typing import Optional

class GameCreate(BaseModel):
    game_date: date
    season_year: int
    home_team_id: int
    away_team_id: int
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    status: str = "scheduled"  # scheduled | final | in_progress

class GameOut(GameCreate):
    id: int

    class Config:
        from_attributes = True
