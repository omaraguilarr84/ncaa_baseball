"""
Transform: Normalize D1Baseball batting/pitching tables into clean records.

Responsibilities:
- Detect the true header row (the one starting with 'Qual.')
- Convert numeric strings to proper types
- Split player names into first/last
- Convert innings pitched "90.1" -> outs_recorded integer

Outputs:
- list[dict] batting_records
- list[dict] pitching_records
Each record contains: player_first, player_last, class_year, pos, plus stat fields.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import pandas as pd


def split_name(full: str) -> Tuple[str, str]:
    parts = str(full).strip().split()
    if not parts:
        return ("", "")
    if len(parts) == 1:
        return (parts[0], "")
    return (parts[0], " ".join(parts[1:]))


def to_int(x) -> Optional[int]:
    s = str(x).strip()
    if s == "" or s.lower() == "nan":
        return None
    try:
        return int(s)
    except Exception:
        return None


def to_float(x) -> Optional[float]:
    s = str(x).strip()
    if s == "" or s.lower() == "nan":
        return None
    try:
        return float(s)
    except Exception:
        return None


def ip_to_outs(ip_val) -> Optional[int]:
    """
    Convert innings pitched like '90.1' or '28.2' into outs recorded.
    D1Baseball decimals represent thirds: .0/.1/.2 -> 0/1/2 outs.
    """
    s = str(ip_val).strip()
    if not s or s.lower() == "nan":
        return None
    try:
        whole, frac = (s.split(".") + ["0"])[:2]
        whole_i = int(whole)
        frac_i = int(frac)
        if frac_i not in (0, 1, 2):
            return None
        return whole_i * 3 + frac_i
    except Exception:
        return None


def _find_header_idx(df: pd.DataFrame) -> int:
    for i in range(len(df)):
        if str(df.iloc[i, 0]).strip().lower() == "qual.":
            return i
    raise ValueError("Could not find header row starting with 'Qual.'")


def normalize_batting(raw: pd.DataFrame, team_name: str) -> List[Dict]:
    if raw.empty:
        return []

    header_idx = _find_header_idx(raw)
    headers = [str(x).strip() for x in raw.iloc[header_idx].tolist()]
    df = raw.iloc[header_idx + 1 :].copy()
    df.columns = headers

    # Keep only this team
    if "Team" in df.columns:
        df = df[df["Team"].astype(str).str.strip() == team_name].copy()

    records: List[Dict] = []
    for _, row in df.iterrows():
        first, last = split_name(row.get("Player", ""))
        rec = {
            "player_first": first,
            "player_last": last,
            "class_year": str(row.get("Class", "")).strip() or None,
            "pos": str(row.get("POS", "")).strip() or None,

            "ba": to_float(row.get("BA")),
            "obp": to_float(row.get("OBP")),
            "slg": to_float(row.get("SLG")),
            "ops": to_float(row.get("OPS")),

            "gp": to_int(row.get("GP")),
            "pa": to_int(row.get("PA")),
            "ab": to_int(row.get("AB")),
            "r": to_int(row.get("R")),
            "h": to_int(row.get("H")),
            "2b": to_int(row.get("2B")),
            "3b": to_int(row.get("3B")),
            "hr": to_int(row.get("HR")),
            "rbi": to_int(row.get("RBI")),
            "hbp": to_int(row.get("HBP")),
            "bb": to_int(row.get("BB")),
            "k": to_int(row.get("K")),
            "sb": to_int(row.get("SB")),
            "cs": to_int(row.get("CS")),
        }
        if rec["player_first"] or rec["player_last"]:
            records.append(rec)

    return records


def normalize_pitching(raw: pd.DataFrame, team_name: str) -> List[Dict]:
    if raw.empty:
        return []

    header_idx = _find_header_idx(raw)
    headers = [str(x).strip() for x in raw.iloc[header_idx].tolist()]
    df = raw.iloc[header_idx + 1 :].copy()
    df.columns = headers

    if "Team" in df.columns:
        df = df[df["Team"].astype(str).str.strip() == team_name].copy()

    records: List[Dict] = []
    for _, row in df.iterrows():
        first, last = split_name(row.get("Player", ""))
        rec = {
            "player_first": first,
            "player_last": last,
            "class_year": str(row.get("Class", "")).strip() or None,
            # pitching table often doesn’t have POS

            "w": to_int(row.get("W")),
            "l": to_int(row.get("L")),
            "era": to_float(row.get("ERA")),
            "app": to_int(row.get("APP")),
            "gs": to_int(row.get("GS")),
            "cg": to_int(row.get("CG")),
            "sho": to_int(row.get("SHO")),
            "sv": to_int(row.get("SV")),

            "outs_recorded": ip_to_outs(row.get("IP")),
            "h": to_int(row.get("H")),
            "r": to_int(row.get("R")),
            "er": to_int(row.get("ER")),
            "bb": to_int(row.get("BB")),
            "k": to_int(row.get("K")),
            "hbp": to_int(row.get("HBP")),
            "ba_against": to_float(row.get("BA")),
        }
        if rec["player_first"] or rec["player_last"]:
            records.append(rec)

    return records
