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
                        contact TEXT,
                        media TEXT
                    )"""
            )
            # handle existing databases created without the `contact` column
            cols = [row[1] for row in self.conn.execute("PRAGMA table_info(requests)")]
            if "contact" not in cols:
                self.conn.execute("ALTER TABLE requests ADD COLUMN contact TEXT")
            if "media" not in cols:
                self.conn.execute("ALTER TABLE requests ADD COLUMN media TEXT")
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT
                    )"""
            )
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS services (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        media TEXT,
                        caption TEXT
                    )"""
            )
            cols = [row[1] for row in self.conn.execute("PRAGMA table_info(services)")]
            if "media" not in cols:
                self.conn.execute("ALTER TABLE services ADD COLUMN media TEXT")
            if "caption" not in cols:
                self.conn.execute("ALTER TABLE services ADD COLUMN caption TEXT")
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS examples (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_id TEXT,
                        caption TEXT
                    )"""
            )
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS service_message (
                        id INTEGER PRIMARY KEY CHECK (id = 1),
                        message_id INTEGER
                    )"""
            )

    def add_request(
        self,
        user_id: int,
        username: str,
        service: str,
        description: str,
        contact: str,
        media: str | None = None,
    ) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO requests (user_id, username, service, description, contact, media) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, username, service, description, contact, media),
            )

    def get_requests(self) -> List[Tuple]:
        with self.conn:
            return self.conn.execute(
                "SELECT id, user_id, username, service, description, contact, media FROM requests"
            ).fetchall()

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

    def add_service(self, media: str, caption: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO services (media, caption) VALUES (?, ?)",
                (media, caption),
            )

    def update_service(self, service_id: int, media: str, caption: str) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE services SET media=?, caption=? WHERE id=?",
                (media, caption, service_id),
            )

    def get_services(self) -> List[Tuple]:
        with self.conn:
            return self.conn.execute(
                "SELECT id, name, media, caption FROM services"
            ).fetchall()

    def save_service_messages(self, message_ids: list[int]) -> None:
        """Store admin service messages to forward to users."""
        with self.conn:
            self.conn.execute("DELETE FROM service_message")
            self.conn.execute(
                "INSERT INTO service_message (id, message_id) VALUES (1, ?)",
                ("",),
            )
            if message_ids:
                ids_str = ",".join(str(i) for i in message_ids)
                self.conn.execute(
                    "UPDATE service_message SET message_id=? WHERE id=1",
                    (ids_str,),
                )

    def get_service_messages(self) -> list[int]:
        """Retrieve stored service message IDs."""
        with self.conn:
            row = self.conn.execute(
                "SELECT message_id FROM service_message WHERE id = 1"
            ).fetchone()
            if not row or not row[0]:
                return []
            return [int(x) for x in str(row[0]).split(",") if x]

    def get_request(self, request_id: int) -> Tuple:
        with self.conn:
            return self.conn.execute(
                "SELECT id, user_id, username, service, description, contact, media FROM requests WHERE id=?",
                (request_id,),
            ).fetchone()

    def delete_request(self, request_id: int) -> None:
        with self.conn:            self.conn.execute("DELETE FROM requests WHERE id=?", (request_id,))