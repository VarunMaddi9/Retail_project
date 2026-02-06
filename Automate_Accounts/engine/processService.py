import sqlite3
import re
from datetime import datetime
from PyPDF2 import PdfReader
from engine.uploadServcie import get_db_connection


def process_receipt(receipt_id: str):

    conn = get_db_connection()
    cur = conn.cursor()

    # 1. Get file_path
    cur.execute(
        "SELECT file_path FROM receipt_file WHERE id = ?",
        (receipt_id,)
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        return {"error": "Receipt file not found"}

    file_path = row["file_path"]
    print(file_path)
    # 2. Extract text from PDF
    reader = PdfReader(file_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    # 3. Basic parsing (simple heuristics)
    merchant_name = full_text.split("\n")[0].strip() if full_text else "UNKNOWN"

    # find amount like 123.45
    amount_match = re.search(r"(\d+\.\d{2})", full_text)
    total_amount = float(amount_match.group(1)) if amount_match else 0.0

    purchased_at = datetime.now().isoformat()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS receipt (
            id TEXT PRIMARY KEY,
            purchased_at TEXT,
            merchant_name TEXT,
            total_amount REAL,
            file_path TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    now = datetime.now().isoformat()

    # 5. Insert receipt data
    cur.execute("""
    INSERT INTO receipt
    (id, purchased_at, merchant_name, total_amount, file_path, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    receipt_id,  # <-- same ID as receipt_file
    purchased_at,
    merchant_name,
    total_amount,
    file_path,
    now,
    now
))


    # 6. Mark file as processed
    cur.execute(
        "UPDATE receipt_file SET is_processed = 1 WHERE id = ?",
        (receipt_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Receipt processed successfully",
        "merchant_name": merchant_name,
        "total_amount": total_amount
    }
