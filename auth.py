import sqlite3
from datetime import datetime

def init_auth():
    conn = sqlite3.connect("intel.db")
    cur = conn.cursor()
    # Audit log for operator actions
    cur.execute("CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, action TEXT, timestamp TEXT)")
    # Sightings log for target hits
    cur.execute("CREATE TABLE IF NOT EXISTS sightings (target_name TEXT, camera_id TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()

def log_action(username, action):
    conn = sqlite3.connect("intel.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO audit_log (username, action, timestamp) VALUES (?, ?, ?)",
                (username or "SYSTEM", action, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def log_sighting(target, camera):
    conn = sqlite3.connect("intel.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO sightings (target_name, camera_id, timestamp) VALUES (?, ?, ?)",
                (target, camera, datetime.now().isoformat()))
    conn.commit()
    conn.close()