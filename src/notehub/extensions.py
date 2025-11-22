"""Flask extensions live here to avoid circular imports."""

from flask_wtf import CSRFProtect

csrf = CSRFProtect()
