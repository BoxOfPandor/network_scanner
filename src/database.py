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
    
def add_device(ip, mac, vendor):
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO devices (ip, mac, vendor) VALUES (?, ?, ?)", 
                      (ip, mac, vendor))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def remove_device(mac):
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM devices WHERE mac = ?", (mac,))
    conn.commit()
    conn.close()