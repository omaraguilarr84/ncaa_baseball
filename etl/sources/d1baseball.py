"""
Source: D1Baseball HTML fetch + table extraction.

Responsibilities:
- Fetch the stats page HTML in-memory (no writing to disk).
- Parse the batting and pitching tables by their DOM ids.

Notes:
- If D1Baseball blocks automated requests (e.g., 403), this module will raise
  a clear error. You can then provide HTML via --html-file for development.
"""

from __future__ import annotations

from typing import List, Tuple

import httpx
import pandas as pd
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential


BAT_TABLE_ID = "batting-stats"
PIT_TABLE_ID = "pitching-stats"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def fetch_team_stats_html(team_slug: str, season_year: int, timeout_s: float = 20.0) -> str:
    url = f"https://d1baseball.com/team/{team_slug}/{season_year}/stats/"
    headers = {
        # Honest, minimal headers. We are not trying to bypass restrictions.
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    with httpx.Client(timeout=timeout_s, follow_redirects=True, headers=headers) as client:
        r = client.get(url)
        if r.status_code != 200:
            raise RuntimeError(f"Failed to fetch {url} (status={r.status_code}).")
        return r.text


def _parse_table_by_id(soup: BeautifulSoup, table_id: str) -> pd.DataFrame:
    table = soup.find("table", id=table_id)
    if not table:
        return pd.DataFrame()

    rows: List[List[str]] = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue
        row = [c.get_text(" ", strip=True) for c in cells]
        if any(cell != "" for cell in row):
            rows.append(row)

    if not rows:
        return pd.DataFrame()

    max_len = max(len(r) for r in rows)
    rows = [r + [""] * (max_len - len(r)) for r in rows]
    headers = [f"col_{i+1}" for i in range(max_len)]
    return pd.DataFrame(rows, columns=headers)


def parse_batting_pitching_tables(html: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    soup = BeautifulSoup(html, "lxml")
    batting_df = _parse_table_by_id(soup, BAT_TABLE_ID)
    pitching_df = _parse_table_by_id(soup, PIT_TABLE_ID)
    return batting_df, pitching_df
