# CAPTCHA Setup Guide

This document explains how to configure and use CAPTCHA protection in the Note Hub application to prevent bots, automated attacks, and spam.

## Overview

CAPTCHA (Completely Automated Public Turing test to tell Computers and Humans Apart) has been integrated into the following forms:

- **Login Form** - Protects against brute force attacks
- **Registration Form** - Prevents automated bot registrations
- **Forgot Password Form** - Protects against password reset abuse

## Features

- Uses Google reCAPTCHA v2 ("I'm not a robot" checkbox)
- Conditionally enabled based on configuration
- Works seamlessly with existing CSRF protection
- Minimal UI impact with centered widget placement
- Graceful degradation when not configured

## Setup Instructions

### 1. Get reCAPTCHA API Keys

1. Visit [Google reCAPTCHA Admin](https://www.google.com/recaptcha/admin)
2. Sign in with your Google account
3. Click **"+"** or **"Create"** to register a new site
4. Fill in the form:
   - **Label**: Choose a name for your site (e.g., "Note Hub Production")
   - **reCAPTCHA type**: Select **"reCAPTCHA v2"** → **"I'm not a robot" Checkbox**
   - **Domains**: Add your domain(s)
     - For local development: `localhost`, `127.0.0.1`
     - For production: `yourdomain.com`, `www.yourdomain.com`
   - Accept the reCAPTCHA Terms of Service
5. Click **"Submit"**
6. Copy your **Site Key** and **Secret Key**

### 2. Configure Environment Variables

Add the following environment variables to your deployment environment:

```bash
# Google reCAPTCHA Keys
RECAPTCHA_SITE_KEY=your_site_key_here
RECAPTCHA_SECRET_KEY=your_secret_key_here
```

#### For Local Development (.env file)

Create or update your `.env` file:

```bash
# .env
FLASK_SECRET=your_flask_secret_key
RECAPTCHA_SITE_KEY=your_recaptcha_site_key
RECAPTCHA_SECRET_KEY=your_recaptcha_secret_key
```

#### For Render.com Deployment

1. Go to your Render dashboard
2. Select your web service
3. Navigate to **"Environment"** tab
4. Add environment variables:
   - `RECAPTCHA_SITE_KEY`: Your site key
   - `RECAPTCHA_SECRET_KEY`: Your secret key

#### For Other Platforms

- **Heroku**: Use `heroku config:set RECAPTCHA_SITE_KEY=xxx RECAPTCHA_SECRET_KEY=xxx`
- **Railway**: Add variables in the Variables tab
- **Docker**: Pass via `-e` flag or `docker-compose.yml` environment section

### 3. Install Dependencies

The required package is already added to `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs `Flask-ReCaptcha==0.6.0` which provides the reCAPTCHA integration.

### 4. Restart Your Application

After setting environment variables, restart your application for changes to take effect:

```bash
# For local development
python wsgi.py

# For production (if using gunicorn)
gunicorn wsgi:app
```

## Verification

### Check if CAPTCHA is Enabled

1. Open your application in a browser
2. Navigate to the login page (`/login`)
3. If configured correctly, you should see the reCAPTCHA widget ("I'm not a robot" checkbox)
4. If not configured, the form will work without CAPTCHA (fallback behavior)

### Test CAPTCHA Validation

1. Try submitting a form without completing the CAPTCHA
2. You should see a validation error
3. Complete the CAPTCHA and submit again
4. The form should process successfully

## Configuration Options

The application uses the following reCAPTCHA settings (configurable in `src/notehub/config.py`):

```python
RECAPTCHA_ENABLED: bool        # Auto-enabled if keys are present
RECAPTCHA_SITE_KEY: str        # Public key from Google
RECAPTCHA_SECRET_KEY: str      # Private key from Google
RECAPTCHA_THEME: "light"       # Widget theme (light/dark)
RECAPTCHA_TYPE: "image"        # Challenge type (image/audio)
RECAPTCHA_SIZE: "normal"       # Widget size (normal/compact)
```

## Troubleshooting

### CAPTCHA Not Showing

**Problem**: The reCAPTCHA widget doesn't appear on forms.

**Solutions**:

1. Verify environment variables are set correctly
2. Check that both `RECAPTCHA_SITE_KEY` and `RECAPTCHA_SECRET_KEY` are non-empty
3. Restart the application after setting variables
4. Check browser console for JavaScript errors

### "Invalid site key" Error

**Problem**: reCAPTCHA shows an error message.

**Solutions**:

1. Verify the site key matches what you copied from Google
2. Ensure your domain is registered in the reCAPTCHA admin panel
3. For local development, add `localhost` and `127.0.0.1` to allowed domains

### CAPTCHA Validation Fails

**Problem**: Form submission fails even after completing CAPTCHA.

**Solutions**:

1. Verify secret key is correct
2. Check server logs for validation errors
3. Ensure your server can connect to Google's reCAPTCHA API
4. Check firewall rules if behind a corporate network

### CAPTCHA Not Required

**Problem**: Forms submit without CAPTCHA validation.

**Solutions**:

1. This is expected behavior when `RECAPTCHA_ENABLED=False`
2. Set both `RECAPTCHA_SITE_KEY` and `RECAPTCHA_SECRET_KEY` to enable
3. Check that `config.RECAPTCHA_ENABLED` returns `True` in your template

## Security Considerations

### Best Practices

1. **Keep Secret Key Private**: Never commit your secret key to version control
2. **Use Environment Variables**: Always load keys from environment variables
3. **Rotate Keys Periodically**: Generate new keys if compromised
4. **Monitor Usage**: Check reCAPTCHA analytics for suspicious patterns
5. **Domain Restrictions**: Only allow your actual domains in reCAPTCHA settings

### Additional Protection

CAPTCHA works alongside other security measures:

- CSRF tokens (always enabled)
- Password policies (12+ characters, complexity requirements)
- 2FA support for enhanced account security
- Rate limiting (recommended for production)

## Development vs Production

### Development Environment

For local development, you can:

- Use test keys from Google (won't validate but allows testing)
- Leave CAPTCHA disabled by not setting environment variables
- Use localhost in domain settings

### Production Environment

For production, you **must**:

- Use real reCAPTCHA keys
- Set environment variables properly
- Register your actual domain
- Monitor CAPTCHA analytics for abuse

## Advanced Configuration

### Custom Theme

To change the CAPTCHA theme, modify `src/notehub/config.py`:

```python
"RECAPTCHA_THEME": "dark",  # Change to "dark" for dark theme
```

### Invisible reCAPTCHA

To use invisible reCAPTCHA (v2 invisible):

1. Register a new site with "Invisible reCAPTCHA" type
2. Update form templates to use invisible widget
3. Requires JavaScript changes for submission

## Support

For issues related to:

- **reCAPTCHA Service**: Visit [reCAPTCHA Help Center](https://support.google.com/recaptcha)
- **Flask-ReCaptcha**: Check [GitHub Issues](https://github.com/mardix/flask-recaptcha)
- **Note Hub Application**: Open an issue in the repository

## References

- [Google reCAPTCHA Documentation](https://developers.google.com/recaptcha)
- [Flask-ReCaptcha GitHub](https://github.com/mardix/flask-recaptcha)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)

---

Last Updated: November 23, 2025
