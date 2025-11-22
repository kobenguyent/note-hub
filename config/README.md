# Configuration Directory

This directory contains configuration-related files and examples for the Note Hub application.

## Structure

```
config/
├── examples/          # Configuration file templates and examples
│   └── .env.example  # Environment variables template
└── README.md         # This file
```

## Usage

### Environment Configuration

Copy the example environment file and customize it for your environment:

```bash
# Copy the example file
cp config/examples/.env.example .env

# Edit with your actual values
nano .env
```

**Important:** Never commit your actual `.env` file to version control. It should contain sensitive information like:

- Secret keys
- Database credentials
- API keys
- reCAPTCHA keys

## File Descriptions

### `examples/.env.example`

Template file showing all available environment variables for configuring the Note Hub application. This includes:

- Flask secret key
- Admin credentials
- Database configuration
- reCAPTCHA settings (optional)

Copy this file to `.env` in the project root and update with your actual values.

## Security Notes

⚠️ **Never commit sensitive configuration files:**

- `.env` files are automatically ignored by `.gitignore`
- Keep API keys and secrets out of version control
- Use environment-specific values in production
- Rotate secrets regularly

## Related Documentation

- [CAPTCHA Setup Guide](../docs/CAPTCHA_SETUP.md)
- [Main README](../README.md)
