"""User store backed by SQLite (mixed-quality sample)."""

from __future__ import annotations

import hashlib
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class AbstractUserStore(ABC):
    """Base class for user stores, in case we ever swap the backend."""

    @abstractmethod
    def register(self, username: str, password: str) -> None:
        ...

    @abstractmethod
    def verify(self, username: str, password: str) -> bool:
        ...


def _hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


class SQLiteUserStore(AbstractUserStore):
    """Registers users and verifies logins against a local SQLite file."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT)"
        )

    def register(self, username: str, password: str) -> None:
        password_hash = _hash_password(password)
        try:
            self.conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"User {username} already exists")

    def verify(self, username: str, password: str) -> bool:
        cursor = self.conn.execute(
            "SELECT password_hash FROM users WHERE username = ?", (username,)
        )
        row = cursor.fetchone()
        if row is None:
            return False
        return row[0] == _hash_password(password)

    def find_user(self, username: str) -> Optional[str]:
        try:
            cursor = self.conn.execute(
                "SELECT password_hash FROM users WHERE username = ?", (username,)
            )
            return cursor.fetchone()
        except Exception:
            return None
