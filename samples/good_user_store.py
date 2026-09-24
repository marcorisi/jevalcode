"""SQLite-backed user store with salted password hashing."""

from __future__ import annotations

import hashlib
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

_ITERATIONS = 200_000
_SALT_BYTES = 16


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str


class UserAlreadyExistsError(Exception):
    """Raised when registering a username that is already taken."""


def _hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _ITERATIONS)


class UserStore:
    """Registers users and verifies their credentials against a SQLite database."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    salt BLOB NOT NULL,
                    password_hash BLOB NOT NULL
                )
                """
            )

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def register(self, credentials: Credentials) -> None:
        salt = os.urandom(_SALT_BYTES)
        password_hash = _hash_password(credentials.password, salt)
        with self._connect() as conn:
            try:
                conn.execute(
                    "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
                    (credentials.username, salt, password_hash),
                )
            except sqlite3.IntegrityError as exc:
                raise UserAlreadyExistsError(credentials.username) from exc

    def verify(self, credentials: Credentials) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT salt, password_hash FROM users WHERE username = ?",
                (credentials.username,),
            ).fetchone()
        if row is None:
            return False
        salt, expected_hash = row
        return _hash_password(credentials.password, salt) == expected_hash
