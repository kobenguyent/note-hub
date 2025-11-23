"""Netlify Function entrypoint that wraps the Flask app via serverless-wsgi."""

import sys
import os
from pathlib import Path

# Set up paths
ROOT_DIR = Path(__file__).resolve().parents[4]
SRC_DIR = ROOT_DIR / "src"

# Add to Python path
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Ensure PYTHONPATH environment variable is set
os.environ['PYTHONPATH'] = str(SRC_DIR)

try:
    import serverless_wsgi
    from notehub import create_app
    from notehub.config import AppConfig

    # Create app instance once
    app = create_app(AppConfig())

    def handler(event, context):
        """Netlify function handler that processes HTTP requests."""
        return serverless_wsgi.handle_request(app, event, context)

except Exception as e:
    import traceback
    
    # Provide detailed error message for debugging
    def handler(event, context):
        error_details = traceback.format_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'''Error initializing app: {str(e)}

Traceback:
{error_details}

Python version: {sys.version}
Python path: {sys.path}
Root directory: {ROOT_DIR}
Source directory: {SRC_DIR}
Current directory: {os.getcwd()}
Environment PYTHONPATH: {os.environ.get("PYTHONPATH", "NOT SET")}
'''
        }
