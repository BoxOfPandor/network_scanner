import sqlite3

def init_db():
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            mac TEXT UNIQUE,
            vendor TEXT
        )
    """)
    conn.commit()
    conn.close()

def is_registered(mac):
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices WHERE mac = ?", (mac,))
    result = cursor.fetchone()
    conn.close()
    return result is not None