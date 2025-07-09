import sqlite3
from typing import List, Tuple

class Database:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        username TEXT,
                        service TEXT,
                        description TEXT
                    )"""
            )

    def add_request(self, user_id: int, username: str, service: str, description: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO requests (user_id, username, service, description) VALUES (?, ?, ?, ?)",
                (user_id, username, service, description)
            )

    def get_requests(self) -> List[Tuple]:
        with self.conn:
            return self.conn.execute("SELECT id, user_id, username, service, description FROM requests").fetchall()
