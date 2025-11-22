"""Startup helpers such as lightweight migrations and admin seeding."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select, text

from ..database import SessionLocal
from ..models import User


def migrate_database():
    """Ensure legacy SQLite databases gain the newer columns."""
    session = SessionLocal()
    try:
        migrations_applied = []
        result = session.execute(text("PRAGMA table_info(users)"))
        user_columns = {row[1]: row for row in result.fetchall()}

        def ensure(column: str, ddl: str, patch: str | None = None):
            if column not in user_columns:
                session.execute(text(ddl))
                if patch:
                    session.execute(text(patch))
                migrations_applied.append(f"users.{column}")

        ensure("theme", "ALTER TABLE users ADD COLUMN theme VARCHAR(20) DEFAULT 'light'",
               "UPDATE users SET theme = 'light' WHERE theme IS NULL")
        ensure("created_at", "ALTER TABLE users ADD COLUMN created_at DATETIME",
               "UPDATE users SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
        ensure("last_login", "ALTER TABLE users ADD COLUMN last_login DATETIME")
        ensure("bio", "ALTER TABLE users ADD COLUMN bio TEXT")
        ensure("email", "ALTER TABLE users ADD COLUMN email VARCHAR(255)")
        ensure("totp_secret", "ALTER TABLE users ADD COLUMN totp_secret VARCHAR(32)")

        if migrations_applied:
            session.commit()
            print(f"✅ Added columns: {', '.join(migrations_applied)}")
    except Exception as exc:  # pragma: no cover - defensive logging
        print(f"⚠️  Migration error: {exc}")
        session.rollback()
    finally:
        session.close()


def ensure_admin(username: str, password: str):
    session = SessionLocal()
    try:
        has_user = session.execute(select(User.id)).first()
        if not has_user:
            admin = User(username=username)
            admin.set_password(password)
            admin.created_at = datetime.now(timezone.utc)
            session.add(admin)
            session.commit()
            print(f"Created admin user: {username} / {password}")
    finally:
        session.close()
