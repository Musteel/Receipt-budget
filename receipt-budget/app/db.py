import sqlite3
from pathlib import Path
import json
DB_PATH = Path(__file__).parent.parent / "data" / "receipts.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            raw_data TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER,
            description TEXT,
            price REAL,
            category TEXT,
            FOREIGN KEY (receipt_id) REFERENCES receipts (id)
        )
    ''')
    conn.commit()
    conn.close()

def insert_receipt_with_items(filename, items):
    conn = get_conn()
    c = conn.cursor()
    raw = json.dumps(items)
    c.execute('INSERT INTO receipts (filename, raw_data) VALUES (?, ?)', (filename, raw))
    receipt_id = c.lastrowid
    for it in items:
        c.execute('''
            INSERT INTO items (receipt_id, description, price, category)
            VALUES (?, ?, ?, ?)
        ''', (receipt_id, it.get("desc"), it.get("price"), it.get("category")))
    conn.commit()
    conn.close()
    return receipt_id