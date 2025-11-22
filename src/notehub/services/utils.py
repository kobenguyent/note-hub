"""Generic helpers shared across views."""

from __future__ import annotations

from functools import wraps
from typing import Callable, List, Optional

from flask import flash, redirect, session, url_for

from ..database import get_session
from ..models import User


def db():
    return get_session()


def current_user() -> Optional[User]:
    user_id = session.get("user_id")
    if not user_id:
        return None
    with db() as s:
        return s.get(User, user_id)


def login_required(view: Callable):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapper


def normalize_tag(name: str) -> str:
    if not name:
        return ""
    normalized = "".join(c for c in name.lower().strip() if c.isalnum() or c in "_-")
    return normalized[:64]


def parse_tags(tag_string: str) -> List[str]:
    if not tag_string:
        return []
    return [normalize_tag(tag.strip()) for tag in tag_string.split(",") if tag.strip()]
