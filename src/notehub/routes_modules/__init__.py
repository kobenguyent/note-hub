"""Modular route organization for better maintainability."""

from .auth_routes import register_auth_routes
from .note_routes import register_note_routes
from .task_routes import register_task_routes
from .profile_routes import register_profile_routes
from .admin_routes import register_admin_routes

__all__ = [
    'register_auth_routes',
    'register_note_routes', 
    'register_task_routes',
    'register_profile_routes',
    'register_admin_routes',
]
