#!/usr/bin/env python3
"""
Scrape D1Baseball team stats tables with requests + BeautifulSoup (bs4).

Usage:
  pip install requests beautifulsoup4 pandas lxml
  python scrape_d1baseball_team_stats.py
"""

from __future__ import annotations

import os
import re
from typing import List, Tuple

import pandas as pd
from bs4 import BeautifulSoup

TEAM = "clemson"
SEASON = 2025
HTML_PATH = "etl/data/raw/d1baseball_clemson_2025_stats.html"
OUT_DIR = f"etl/data/{TEAM}_{SEASON}_stats"

def _clean_filename(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "table"

def _parse_table_by_id(soup: BeautifulSoup, table_id: str) -> pd.DataFrame:
    table = soup.find("table", id=table_id)
    if not table:
        return pd.DataFrame()

    rows: List[List[str]] = []
    for tr in table.find_all("tr"):
        tds = tr.find_all(["td", "th"])
        if not tds:
            continue
        row = [td.get_text(" ", strip=True) for td in tds]
        # Drop entirely empty rows
        if any(cell != "" for cell in row):
            rows.append(row)

    if not rows:
        return pd.DataFrame()

    # Normalize row lengths
    max_len = max(len(r) for r in rows)
    rows = [r + [""] * (max_len - len(r)) for r in rows]

    # Create generic headers if missing
    headers = [f"col_{i+1}" for i in range(max_len)]
    return pd.DataFrame(rows, columns=headers)

def parse_standard_tables(html: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    soup = BeautifulSoup(html, "lxml")
    batting_df = _parse_table_by_id(soup, "batting-stats")
    pitching_df = _parse_table_by_id(soup, "pitching-stats")
    return batting_df, pitching_df

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    batting_df, pitching_df = parse_standard_tables(html)

    batting_path = os.path.join(OUT_DIR, "standard_batting.csv")
    pitching_path = os.path.join(OUT_DIR, "standard_pitching.csv")

    batting_df.to_csv(batting_path, index=False)
    pitching_df.to_csv(pitching_path, index=False)

    print(f"Standard batting rows: {len(batting_df)} -> {batting_path}")
    print(f"Standard pitching rows: {len(pitching_df)} -> {pitching_path}")

if __name__ == "__main__":
    main()
