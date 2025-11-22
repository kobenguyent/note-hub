"""Netlify Function entrypoint that wraps the Flask app via serverless-wsgi."""

import sys
from pathlib import Path

import serverless_wsgi

ROOT_DIR = Path(__file__).resolve().parents[3]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from notehub import create_app
from notehub.config import AppConfig


_app = create_app(AppConfig())


def handler(event, context):
    return serverless_wsgi.handle_request(_app, event, context)
