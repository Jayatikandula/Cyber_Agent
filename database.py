import sqlite3

# ---------------- USERS TABLE ----------------
def create_users_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user',
        organization TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(username, password, organization):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password, role, organization) VALUES (?, ?, ?, ?)",
            (username, password, "user", organization)
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def verify_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()
    return user