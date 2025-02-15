import sqlite3

def init_db():
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            mac TEXT PRIMARY KEY,
            ip TEXT,
            vendor TEXT,
            name TEXT
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

def get_device_name(mac):
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM devices WHERE mac = ?", (mac,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
    
def add_device(ip, mac, vendor, name=None):
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO devices (mac, ip, vendor, name) VALUES (?, ?, ?, ?)", 
                      (mac, ip, vendor, name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_device_name(mac, name):
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE devices SET name = ? WHERE mac = ?", (name, mac))
    conn.commit()
    conn.close()

def remove_device(mac):
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM devices WHERE mac = ?", (mac,))
    conn.commit()
    conn.close()
