import sqlite3

# ---------------- REPORTS TABLE ----------------
def create_reports_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        organization TEXT,
        report TEXT,
        risk_score INTEGER,
        sector TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_report(username, organization, report, risk_score, sector):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reports (username, organization, report, risk_score, sector)
    VALUES (?, ?, ?, ?, ?)
    """, (username, organization, report, risk_score, sector))

    conn.commit()
    conn.close()


def get_user_reports(organization):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM reports WHERE organization=? ORDER BY created_at DESC",
        (organization,)
    )

    reports = cursor.fetchall()
    conn.close()
    return reports