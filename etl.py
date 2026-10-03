"""Load Sparkify song and event-log JSON data into PostgreSQL."""

from __future__ import annotations

import glob
import os
from typing import Any, Callable

import pandas as pd
import psycopg2

from sql_queries import (
    artist_table_insert,
    song_select,
    song_table_insert,
    songplay_table_insert,
    time_table_insert,
    user_table_insert,
)


def process_song_file(cur: Any, filepath: str) -> None:
    """Load one song JSON file into the songs and artists dimensions."""
    df = pd.read_json(filepath, typ="series")

    cur.execute(
        song_table_insert,
        tuple(df[["song_id", "title", "artist_id", "year", "duration"]].values),
    )
    cur.execute(
        artist_table_insert,
        tuple(
            df[
                [
                    "artist_id",
                    "artist_name",
                    "artist_location",
                    "artist_latitude",
                    "artist_longitude",
                ]
            ].values
        ),
    )


def process_log_file(cur: Any, filepath: str) -> None:
    """Transform one event-log file and load its dimension/fact records."""
    df = pd.read_json(filepath, lines=True)
    df = df[df["page"] == "NextSong"].copy()

    if df.empty:
        return

    df["ts"] = pd.to_datetime(df["ts"], unit="ms")

    time_df = pd.DataFrame(
        {
            "timestamp": df["ts"].dt.time,
            "hour": df["ts"].dt.hour,
            "day": df["ts"].dt.day,
            "week": df["ts"].dt.isocalendar().week.astype(int),
            "month": df["ts"].dt.month,
            "year": df["ts"].dt.year,
            "weekday": df["ts"].dt.weekday,
        }
    ).drop_duplicates()

    for row in time_df.itertuples(index=False):
        cur.execute(time_table_insert, row)

    user_df = df[["userId", "firstName", "lastName", "gender", "level"]].drop_duplicates(
        subset=["userId"]
    )

    for row in user_df.itertuples(index=False):
        cur.execute(user_table_insert, row)

    for row in df.itertuples(index=False):
        cur.execute(song_select, (row.song, row.artist, row.length))
        result = cur.fetchone()
        song_id, artist_id = result if result else (None, None)

        cur.execute(
            songplay_table_insert,
            (
                row.ts,
                row.userId,
                row.level,
                song_id,
                artist_id,
                row.sessionId,
                row.location,
                row.userAgent,
            ),
        )


def process_data(
    cur: Any,
    conn: Any,
    filepath: str,
    func: Callable[[Any, str], None],
) -> None:
    """Find JSON files recursively and process them one at a time."""
    all_files = []
    for root, _, _ in os.walk(filepath):
        all_files.extend(glob.glob(os.path.join(root, "*.json")))

    all_files.sort()
    print(f"{len(all_files)} files found in {filepath}")

    for index, datafile in enumerate(all_files, start=1):
        func(cur, datafile)
        conn.commit()
        print(f"{index}/{len(all_files)} files processed.")


def insert_songs_and_logs() -> None:
    """Connect to PostgreSQL and run the complete Sparkify load."""
    conn = psycopg2.connect(
        host=os.getenv("SPARKIFY_DB_HOST", "127.0.0.1"),
        port=os.getenv("SPARKIFY_DB_PORT", "5432"),
        dbname=os.getenv("SPARKIFY_DB_NAME", "sparkifydb"),
        user=os.getenv("SPARKIFY_DB_USER", "student"),
        password=os.getenv("SPARKIFY_DB_PASSWORD", "student"),
    )
    cur = conn.cursor()

    try:
        process_data(cur, conn, "data/song_data", process_song_file)
        process_data(cur, conn, "data/log_data", process_log_file)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    insert_songs_and_logs()
