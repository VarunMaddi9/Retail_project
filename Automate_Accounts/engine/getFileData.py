import sqlite3

def get_db_connection():
    conn = sqlite3.connect("automate.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_file_meta_data(file_id: str):
    sql = "SELECT file_path FROM receipt_file WHERE id = :id"

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(sql, {"id": file_id})
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return row["file_path"]