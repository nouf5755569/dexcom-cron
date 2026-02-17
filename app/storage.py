import sqlite3
from typing import List, Dict, Any

def init_db(db_path: str) -> None:
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS glucose_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        systemTime TEXT,
        displayTime TEXT,
        value REAL,
        unit TEXT,
        trend TEXT,
        raw_json TEXT,
        UNIQUE(systemTime, value)
    )
    """)
    con.commit()
    con.close()

def upsert_glucose_readings(db_path: str, readings: List[Dict[str, Any]]) -> int:
    if not readings:
        return 0

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    count = 0
    for rec in readings:
        system_time = rec.get("systemTime") or rec.get("timestamp") or rec.get("time")
        display_time = rec.get("displayTime")
        value = rec.get("value") or rec.get("egv") or rec.get("glucose")
        unit = rec.get("unit") or "mg/dL"
        trend = rec.get("trend") or rec.get("trendArrow") or ""

        raw_json = str(rec)

        try:
            cur.execute("""
                INSERT OR IGNORE INTO glucose_readings
                (systemTime, displayTime, value, unit, trend, raw_json)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (system_time, display_time, value, unit, trend, raw_json))
            if cur.rowcount > 0:
                count += 1
        except Exception:
            # ignore bad rows, continue
            continue

    con.commit()
    con.close()
    return count
