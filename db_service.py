import sqlite3
from pathlib import Path

SAMPLE_DB_PATH = Path(__file__).resolve().parent / "sample.db"

def execute_query(sql: str) -> list[dict]:
    conn = sqlite3.connect(SAMPLE_DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()