"""
FastAPI application entrypoint.

This is the main web service. It wires together:
- the FastAPI app instance
- routers (endpoints) like /teams
- (later) middleware, auth, logging, etc.
Run with: `uvicorn backend.main:app --reload`
"""

from fastapi import FastAPI
from backend.routes.teams import router as teams_router
from backend.routes.games import router as games_router

app = FastAPI(title="NCAA Baseball Platform")

app.include_router(teams_router)
app.include_router(games_router)
