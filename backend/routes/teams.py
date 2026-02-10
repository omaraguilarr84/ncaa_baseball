"""
Teams API routes.

Defines endpoints under `/teams`:
- GET /teams  -> list teams
- POST /teams -> create a team

Uses a per-request SQLAlchemy Session via the get_db() dependency.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db_session import SessionLocal
from backend.models.team import Team
from backend.schemas.team import TeamCreate, TeamOut

router = APIRouter(prefix="/teams", tags=["Teams"])

def get_db():
    """Yield a DB session per request and ensure it closes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[TeamOut])
def get_teams(db: Session = Depends(get_db)):
    """Return all teams."""
    return db.query(Team).order_by(Team.id.asc()).all()

@router.post("/", response_model=TeamOut, status_code=201)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    """
    Create a team. If a team with the same name already exists, return 409.
    """
    existing = db.query(Team).filter(Team.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Team already exists")

    team = Team(
        name=payload.name,
        short_name=payload.short_name,
        conference=payload.conference,
    )
    db.add(team)
    db.commit()
    db.refresh(team)
    return team
