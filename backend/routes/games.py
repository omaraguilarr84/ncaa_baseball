"""
Games API routes.

Defines endpoints under `/games`:
- POST /games -> create a game row

Uses a per-request SQLAlchemy Session via get_db().
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db_session import SessionLocal
from backend.models.game import Game
from backend.schemas.game import GameCreate, GameOut

router = APIRouter(prefix="/games", tags=["Games"])

def get_db():
    """Yield a DB session per request and ensure it closes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=GameOut, status_code=201)
def create_game(payload: GameCreate, db: Session = Depends(get_db)):
    """Insert a game into the database."""
    game = Game(
        game_date=payload.game_date,
        season_year=payload.season_year,
        home_team_id=payload.home_team_id,
        away_team_id=payload.away_team_id,
        home_score=payload.home_score,
        away_score=payload.away_score,
        status=payload.status,
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game
