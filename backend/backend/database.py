import sqlite3

DB_NAME = "emailapp.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        subject TEXT,
        body TEXT,
        category TEXT,
        is_read INTEGER DEFAULT 0,
        sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_id) REFERENCES users(id),
        FOREIGN KEY (receiver_id) REFERENCES users(id)
    )""")

    conn.commit()
    conn.close()


def insert_user(username, email, password_hash):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash)
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    return user


def insert_email(sender_id, receiver_id, subject, body, category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO emails (sender_id, receiver_id, subject, body, category)
           VALUES (?, ?, ?, ?, ?)""",
        (sender_id, receiver_id, subject, body, category)
    )
    conn.commit()
    conn.close()


def get_emails_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM emails WHERE receiver_id = ? ORDER BY sent_at DESC",
        (user_id,)
    )
    emails = cur.fetchall()
    conn.close()
    return emails
