"""
Load: DB upserts for teams/players and season stats.

Responsibilities:
- Provide small, reusable functions for DB writes (upserts).
- ETL jobs call these functions.
- Later your API endpoints can also call these if you want a shared “repository layer”.

Assumes tables exist:
- teams
- players
- player_batting_season
- player_pitching_season
"""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
ENGINE = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)


def get_or_create_team_id(team_name: str, short_name: Optional[str] = None, conference: Optional[str] = None) -> int:
    with ENGINE.begin() as conn:
        row = conn.execute(text("SELECT id FROM teams WHERE name = :n"), {"n": team_name}).fetchone()
        if row:
            return int(row[0])

        res = conn.execute(
            text("INSERT INTO teams (name, short_name, conference) VALUES (:n, :s, :c)"),
            {"n": team_name, "s": short_name or team_name, "c": conference},
        )
        return int(res.lastrowid)


def upsert_player(team_id: int, first: str, last: str, class_year: Optional[str], pos: Optional[str]) -> int:
    with ENGINE.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO players (team_id, first_name, last_name, class_year, position)
                VALUES (:team_id, :first, :last, :class_year, :pos)
                ON DUPLICATE KEY UPDATE
                  class_year = VALUES(class_year),
                  position = VALUES(position)
            """),
            {"team_id": team_id, "first": first, "last": last, "class_year": class_year, "pos": pos},
        )

        row = conn.execute(
            text("""
                SELECT id FROM players
                WHERE team_id=:team_id AND first_name=:first AND last_name=:last
            """),
            {"team_id": team_id, "first": first, "last": last},
        ).fetchone()
        return int(row[0])


def upsert_batting_season(player_id: int, season_year: int, r: dict) -> None:
    with ENGINE.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO player_batting_season (
                  player_id, season_year,
                  ba, obp, slg, ops,
                  gp, pa, ab, r, h, `2b`, `3b`, hr, rbi, hbp, bb, k, sb, cs
                )
                VALUES (
                  :player_id, :season_year,
                  :ba, :obp, :slg, :ops,
                  :gp, :pa, :ab, :r, :h, :b2, :b3, :hr, :rbi, :hbp, :bb, :k, :sb, :cs
                )
                ON DUPLICATE KEY UPDATE
                  ba=VALUES(ba), obp=VALUES(obp), slg=VALUES(slg), ops=VALUES(ops),
                  gp=VALUES(gp), pa=VALUES(pa), ab=VALUES(ab), r=VALUES(r), h=VALUES(h),
                  `2b`=VALUES(`2b`), `3b`=VALUES(`3b`), hr=VALUES(hr), rbi=VALUES(rbi),
                  hbp=VALUES(hbp), bb=VALUES(bb), k=VALUES(k), sb=VALUES(sb), cs=VALUES(cs)
            """),
            {
                "player_id": player_id,
                "season_year": season_year,
                "ba": r.get("ba"),
                "obp": r.get("obp"),
                "slg": r.get("slg"),
                "ops": r.get("ops"),
                "gp": r.get("gp"),
                "pa": r.get("pa"),
                "ab": r.get("ab"),
                "r": r.get("r"),
                "h": r.get("h"),
                "b2": r.get("2b"),
                "b3": r.get("3b"),
                "hr": r.get("hr"),
                "rbi": r.get("rbi"),
                "hbp": r.get("hbp"),
                "bb": r.get("bb"),
                "k": r.get("k"),
                "sb": r.get("sb"),
                "cs": r.get("cs"),
            },
        )


def upsert_pitching_season(player_id: int, season_year: int, r: dict) -> None:
    with ENGINE.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO player_pitching_season (
                  player_id, season_year,
                  w, l, era, app, gs, cg, sho, sv,
                  outs_recorded, h, r, er, bb, k, hbp, ba_against
                )
                VALUES (
                  :player_id, :season_year,
                  :w, :l, :era, :app, :gs, :cg, :sho, :sv,
                  :outs, :h, :r, :er, :bb, :k, :hbp, :baa
                )
                ON DUPLICATE KEY UPDATE
                  w=VALUES(w), l=VALUES(l), era=VALUES(era), app=VALUES(app), gs=VALUES(gs),
                  cg=VALUES(cg), sho=VALUES(sho), sv=VALUES(sv),
                  outs_recorded=VALUES(outs_recorded),
                  h=VALUES(h), r=VALUES(r), er=VALUES(er), bb=VALUES(bb), k=VALUES(k),
                  hbp=VALUES(hbp), ba_against=VALUES(ba_against)
            """),
            {
                "player_id": player_id,
                "season_year": season_year,
                "w": r.get("w"),
                "l": r.get("l"),
                "era": r.get("era"),
                "app": r.get("app"),
                "gs": r.get("gs"),
                "cg": r.get("cg"),
                "sho": r.get("sho"),
                "sv": r.get("sv"),
                "outs": r.get("outs_recorded"),
                "h": r.get("h"),
                "r": r.get("r"),
                "er": r.get("er"),
                "bb": r.get("bb"),
                "k": r.get("k"),
                "hbp": r.get("hbp"),
                "baa": r.get("ba_against"),
            },
        )
