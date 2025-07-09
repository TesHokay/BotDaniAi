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
                        description TEXT,
                        contact TEXT
                    )"""
            )
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT
                    )"""
            )
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS services (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT
                    )"""
            )
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS examples (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_id TEXT,
                        caption TEXT
                    )"""
            )

    def add_request(self, user_id: int, username: str, service: str, description: str, contact: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO requests (user_id, username, service, description, contact) VALUES (?, ?, ?, ?, ?)",
                (user_id, username, service, description, contact)
            )

    def get_requests(self) -> List[Tuple]:
        with self.conn:
            return self.conn.execute("SELECT id, user_id, username, service, description, contact FROM requests").fetchall()

    def add_user(self, user_id: int, username: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO users (user_id, username) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET username=excluded.username",
                (user_id, username),
            )

    def get_users(self) -> List[Tuple]:
        with self.conn:
            return self.conn.execute("SELECT user_id FROM users").fetchall()

    def add_example(self, file_id: str, caption: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO examples (file_id, caption) VALUES (?, ?)",
                (file_id, caption),
            )

    def update_example(self, example_id: int, caption: str) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE examples SET caption=? WHERE id=?",
                (caption, example_id),
            )

    def get_examples(self) -> List[Tuple]:
        with self.conn:
            return self.conn.execute("SELECT id, file_id, caption FROM examples").fetchall()

    def add_service(self, name: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO services (name) VALUES (?)",
                (name,),
            )

    def update_service(self, service_id: int, name: str) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE services SET name=? WHERE id=?",
                (name, service_id),
            )

    def get_services(self) -> List[Tuple]:
        with self.conn:
            return self.conn.execute("SELECT id, name FROM services").fetchall()

    def get_request(self, request_id: int) -> Tuple:
        with self.conn:
            return self.conn.execute(
                "SELECT id, user_id, username, service, description, contact FROM requests WHERE id=?",
                (request_id,),
            ).fetchone()

    def delete_request(self, request_id: int) -> None:
        with self.conn:
            self.conn.execute("DELETE FROM requests WHERE id=?", (request_id,))
