import sqlite3

conn = sqlite3.connect("process_tracker.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS process_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        status TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

def log_process(file_name, status):
    cursor.execute("INSERT INTO process_log (file_name, status) VALUES (?, ?)", (file_name, status))
    conn.commit()

