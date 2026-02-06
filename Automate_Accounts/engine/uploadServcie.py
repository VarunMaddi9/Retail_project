from datetime import datetime
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("automate.db")
    conn.row_factory = sqlite3.Row
    return conn


def upload_file_metadata(id, file_name, file_path, is_valid, invalid_reason, is_processed):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipt_file (
            id TEXT PRIMARY KEY,
            file_name TEXT,
            file_path TEXT,
            is_valid INTEGER,
            invalid_reason TEXT,
            is_processed INTEGER,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    now = datetime.utcnow().isoformat()

    cursor.execute("""
        INSERT INTO receipt_file
        (id, file_name, file_path, is_valid, invalid_reason, is_processed, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id,
        file_name,
        file_path,
        is_valid,
        invalid_reason,
        is_processed,
        now,
        now
    ))

    conn.commit()
    conn.close()