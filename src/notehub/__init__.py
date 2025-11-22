"""Application factory for the Note Hub project."""

from __future__ import annotations

from flask import Flask

from .config import AppConfig
from .extensions import csrf
from .database import init_database
from .routes import register_routes
from .services.bootstrap import ensure_admin, migrate_database


def create_app(config: AppConfig | None = None) -> Flask:
    config = config or AppConfig()
    app = Flask(__name__, template_folder="../templates")
    app.config.update(config.flask_settings)

    csrf.init_app(app)
    init_database(config.database_uri)
    migrate_database()
    ensure_admin(config.admin_username, config.admin_password)
    register_routes(app)

    return app


app = create_app()
