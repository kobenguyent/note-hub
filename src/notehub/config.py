"""Configuration helpers for the Note Hub application."""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass, field


@dataclass(slots=True)
class AppConfig:
    """Simple configuration container with sane defaults."""

    db_path: str = field(default_factory=lambda: os.getenv("NOTES_DB_PATH", "notes.db"))
    admin_username: str = field(default_factory=lambda: os.getenv("NOTES_ADMIN_USERNAME", "admin"))
    admin_password: str = field(default_factory=lambda: os.getenv("NOTES_ADMIN_PASSWORD", "change-me"))
    secret_key: str = field(default_factory=lambda: os.getenv("FLASK_SECRET", secrets.token_hex(32)))
    max_content_length: int = 16 * 1024 * 1024

    @property
    def flask_settings(self) -> dict[str, object]:
        return {
            "SECRET_KEY": self.secret_key,
            "WTF_CSRF_ENABLED": True,
            "MAX_CONTENT_LENGTH": self.max_content_length,
        }

    @property
    def database_uri(self) -> str:
        return f"sqlite:///{self.db_path}"
