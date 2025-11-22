"""Flask extensions live here to avoid circular imports."""

from flask_wtf import CSRFProtect

csrf = CSRFProtect()

# Note: Flask-WTF's RecaptchaField is automatically configured via Flask config
# No need for a separate ReCaptcha extension initialization
