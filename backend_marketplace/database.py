import sqlite3


class DatabaseManager:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            role VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

    def create_user(self, name: str, email: str, role: str):
        self.cursor.execute(
            """
        INSERT INTO users (name, email, role)
        VALUES (?, ?, ?)
        """,
            (name, email, role),
        )

        return self.cursor.lastrowid

    def get_user(self, email: str):
        self.cursor.execute(
            """
        SELECT * FROM users WHERE email = ?;
        """,
            (email,),
        )

        return self.cursor.fetchone()
