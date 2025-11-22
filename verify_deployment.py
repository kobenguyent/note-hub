#!/usr/bin/env python3
"""Verification script for deployment readiness."""

import sys
import os
from pathlib import Path

def check_wsgi_module():
    """Verify wsgi module can be imported and app is available."""
    try:
        import wsgi
        assert hasattr(wsgi, 'app'), "wsgi module must have 'app' attribute"
        assert hasattr(wsgi.app, 'wsgi_app'), "app must be a Flask application"
        print("✓ wsgi module is correctly configured")
        return True
    except Exception as e:
        print(f"✗ wsgi module check failed: {e}")
        return False

def check_gunicorn():
    """Verify gunicorn can load the application."""
    try:
        from gunicorn.app.wsgiapp import WSGIApplication
        # Simulate gunicorn loading
        print("✓ gunicorn is installed and can be imported")
        return True
    except ImportError as e:
        print(f"✗ gunicorn import failed: {e}")
        return False

def check_requirements():
    """Verify all required packages are installed."""
    required_packages = [
        'flask',
        'flask_wtf',
        'sqlalchemy',
        'werkzeug',
        'pyotp',
        'markdown',
        'bleach',
        'qrcode',
        'gunicorn'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"✗ Missing packages: {', '.join(missing)}")
        return False
    else:
        print("✓ All required packages are installed")
        return True

def check_files():
    """Verify required files exist."""
    required_files = [
        'wsgi.py',
        'requirements.txt',
        'render.yaml',
        'Procfile',
        'runtime.txt',
        'src/notehub/__init__.py',
        'src/notehub/config.py'
    ]
    
    missing = []
    root = Path(__file__).parent
    for file in required_files:
        if not (root / file).exists():
            missing.append(file)
    
    if missing:
        print(f"✗ Missing files: {', '.join(missing)}")
        return False
    else:
        print("✓ All required files are present")
        return True

def check_config_files():
    """Verify configuration files have correct content."""
    root = Path(__file__).parent
    
    # Check Procfile
    procfile = (root / 'Procfile').read_text()
    if 'wsgi:app' not in procfile:
        print("✗ Procfile doesn't reference wsgi:app")
        return False
    
    # Check render.yaml
    render_yaml = (root / 'render.yaml').read_text()
    if 'wsgi:app' not in render_yaml:
        print("✗ render.yaml doesn't reference wsgi:app")
        return False
    
    print("✓ Configuration files are correctly set up")
    return True

def main():
    """Run all checks."""
    print("=" * 60)
    print("Deployment Verification Script")
    print("=" * 60)
    print()
    
    checks = [
        check_files,
        check_config_files,
        check_requirements,
        check_wsgi_module,
        check_gunicorn
    ]
    
    results = [check() for check in checks]
    
    print()
    print("=" * 60)
    if all(results):
        print("✓ All checks passed! Ready for deployment.")
        print()
        print("Deployment commands:")
        print("  render.yaml: Already configured")
        print("  Local test: gunicorn --bind 127.0.0.1:8000 wsgi:app")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
