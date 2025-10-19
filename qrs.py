#!/usr/bin/env python3
"""
Generate QR codes for a team's full path.

Usage:
  python qrs.py --base-url "https://YOUR-TUNNEL.trycloudflare.com" --team red-1234
"""

import argparse, csv, re, sys
from pathlib import Path
import qrcode

from db import supabase  # your existing Supabase client

def slugify(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")[:40] or "Station"

def get_team_and_path(team_slug: str):
    team_slug = (team_slug or "").strip().lower()
    team_rows = (
        supabase.table("teams")
        .select("id, name, slug")
        .eq("slug", team_slug)
        .limit(1).execute()
    ).data or []
    if not team_rows:
        sys.exit(f"Team not found: {team_slug}")
    team = team_rows[0]

    path_rows = (
        supabase.table("paths")
        .select("station_order, current_index")
        .eq("team_id", team["id"])
        .limit(1).execute()
    ).data or []
    if not path_rows or not path_rows[0].get("station_order"):
        sys.exit(f"No path for team: {team_slug}")
    return team, path_rows[0]

def get_station_names(ids):
    id_strs = [str(x) for x in ids]
    rows = (
        supabase.table("stations")
        .select("id, name")
        .in_("id", id_strs)
        .execute()
    ).data or []
    return {row["id"]: row["name"] for row in rows}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True, help="Public base URL (ngrok / Cloudflare)")
    ap.add_argument("--team", required=True, help="Team slug, e.g. red-1234")
    args = ap.parse_args()

    base = args.base_url.rstrip("/")
    team_slug = args.team.strip().lower()

    team, path = get_team_and_path(team_slug)
    order = path["station_order"]
    names = get_station_names(order)

    out_dir = Path("qr_out") / team_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = out_dir / "manifest.csv"

    with manifest.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["step", "station_id", "station_name", "url", "filename"])
        for i, sid in enumerate(order, start=1):
            sid_str = str(sid)
            station_name = names.get(sid_str, "Unknown")
            short = sid_str.split("-")[0]
            step = f"{i:02d}"
            fname = f"{step}_{slugify(station_name)}_{short}.png"
            url = f"{base}/?team={team_slug}&station={sid_str}&scan=1"

            img = qrcode.make(url)
            img.save(out_dir / fname)
            w.writerow([i, sid_str, station_name, url, fname])

    print(f"✅ Wrote {len(order)} QR codes and {manifest}")

if __name__ == "__main__":
    main()
