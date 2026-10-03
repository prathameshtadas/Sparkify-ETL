"""Create the Sparkify PostgreSQL database and star-schema tables."""

from __future__ import annotations

import os

import psycopg2

from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """Create the Sparkify database and return an open cursor/connection."""
    conn = psycopg2.connect(
        host=os.getenv("SPARKIFY_DB_HOST", "127.0.0.1"),
        port=os.getenv("SPARKIFY_DB_PORT", "5432"),
        dbname=os.getenv("SPARKIFY_ADMIN_DB", "postgres"),
        user=os.getenv("SPARKIFY_DB_USER", "student"),
        password=os.getenv("SPARKIFY_DB_PASSWORD", "student"),
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'sparkifydb'")
    if cur.fetchone() is None:
        cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'UTF8' TEMPLATE template0")

    cur.close()
    conn.close()

    conn = psycopg2.connect(
        host=os.getenv("SPARKIFY_DB_HOST", "127.0.0.1"),
        port=os.getenv("SPARKIFY_DB_PORT", "5432"),
        dbname=os.getenv("SPARKIFY_DB_NAME", "sparkifydb"),
        user=os.getenv("SPARKIFY_DB_USER", "student"),
        password=os.getenv("SPARKIFY_DB_PASSWORD", "student"),
    )
    return conn.cursor(), conn


def drop_tables(cur, conn):
    """Drop existing Sparkify tables."""
    for query in drop_table_queries:
        cur.execute(query)
    conn.commit()


def create_tables(cur, conn):
    """Create the Sparkify dimension and fact tables."""
    for query in create_table_queries:
        cur.execute(query)
    conn.commit()


def main():
    """Rebuild the Sparkify schema from scratch."""
    cur, conn = create_database()
    try:
        drop_tables(cur, conn)
        create_tables(cur, conn)
    finally:
        cur.close()
        conn.close()
    print("Sparkify database and tables are ready.")


if __name__ == "__main__":
    main()
