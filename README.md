# Beautiful Notes App

A modern, clean, and feature-rich personal notes application built with Flask. Perfect for personal note-taking, journaling, and idea capture.

---

## 📊 Status

![CI/CD Pipeline](https://github.com/thienng-it/note-hub/actions/workflows/ci-cd.yml/badge.svg?branch=main)
![Deploy to Render](https://github.com/thienng-it/note-hub/actions/workflows/deploy-render.yml/badge.svg?branch=main)
![Deploy GitHub Pages](https://github.com/thienng-it/note-hub/actions/workflows/deploy-pages.yml/badge.svg?branch=main)

---

## 🚀 Live Demo

**[🎯 Click here to try the live app](https://note-hub.onrender.com)** (Deployed on Render)

**Default Login:** `admin` / `change-me`

---

## ✨ Features

- **📝 Rich Markdown Editing** - Full markdown support with live preview
- **🏷️ Smart Tagging** - Organize notes with tags and filter by them
- **🔍 Powerful Search** - Search notes by title, content, or tags
- **⭐ Favorites & Pinning** - Mark important notes as favorites or pin them
- **📱 Responsive Design** - Beautiful UI that works on all devices
- **🌙 Dark Mode** - Toggle between light and dark themes
- **🔐 Secure** - CSRF protection, input validation, and HTML sanitization
- **📊 Reading Time** - Automatic reading time estimation
- **🔑 Two-Factor Authentication (2FA)** - TOTP-based 2FA with QR code setup for enhanced security

## 📁 Project Structure

```
note-hub/
├── simple_app.py              # Main Flask application with 2FA support
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── CI_CD.md                   # CI/CD pipeline documentation
├── BRANCH_RULESET.md          # Branch protection ruleset configuration
├── notes.db                   # SQLite database (created automatically)
├── .github/
│   ├── workflows/             # GitHub Actions CI/CD pipelines
│   │   ├── ci-cd.yml         # Testing, linting, security scanning
│   │   ├── deploy-render.yml # Auto-deploy to Render
│   │   └── deploy-pages.yml  # Auto-deploy to GitHub Pages
│   └── CODEOWNERS            # Code ownership rules
├── docs/                      # GitHub Pages landing site
│   ├── index.html            # Landing page
│   └── .nojekyll             # Disable Jekyll processing
└── templates/                 # HTML templates
    ├── base.html             # Base layout
    ├── index.html            # Notes list
    ├── login.html            # Login page
    ├── register.html         # Registration page
    ├── edit_note.html        # Create/edit notes
    ├── view_note.html        # View single note
    ├── profile.html          # User profile & 2FA management
    ├── setup_2fa.html        # 2FA setup with QR code
    ├── verify_2fa.html       # 2FA verification on login
    ├── verify_2fa_reset.html # 2FA bypass for password reset
    └── error.html            # Error pages
```

## ⚙️ Configuration

Set environment variables to customize:

```bash
export NOTES_DB_PATH="my_notes.db"           # Database file
export NOTES_ADMIN_USERNAME="myuser"         # Admin username
export NOTES_ADMIN_PASSWORD="mypassword"     # Admin password
export FLASK_SECRET="your-secret-key"        # Flask secret key
```

## 🎯 Usage Tips

1. **Organize with tags:** Use consistent tagging (e.g., `work`, `personal`, `ideas`)
2. **Pin important notes:** Keep frequently accessed notes at the top
3. **Use markdown:** Format your notes with headers, lists, code blocks, etc.
4. **Search efficiently:** Use the search bar to quickly find notes
5. **Backup regularly:** Copy `notes.db` to backup your notes

## 🔒 Security Features

- **CSRF Protection** - All forms protected against cross-site request forgery
- **Input Validation** - Server-side validation for all user inputs
- **HTML Sanitization** - Safe markdown rendering with bleach
- **Secure Sessions** - Proper session management
- **Password Hashing** - Passwords stored securely with Werkzeug
- **Two-Factor Authentication (2FA)** - TOTP-based authentication with QR code setup

## 🔑 Two-Factor Authentication (2FA)

The app includes optional 2FA for enhanced security:

1. **Setup 2FA**

   - Navigate to Profile → Setup 2FA
   - Scan QR code with authenticator app (Google Authenticator, Authy, etc.)
   - Verify the 6-digit code to enable 2FA

2. **Login with 2FA**

   - Enter username and password
   - When prompted, enter the 6-digit code from your authenticator app
   - Access granted after successful verification

3. **Password Reset**

   - Can reset password via email verification
   - 2FA can be bypassed during password reset process
   - Re-enable 2FA after regaining access

4. **Disable 2FA**
   - Go to Profile page
   - Click "Disable 2FA" to turn off 2FA protection

**Supported Authenticator Apps:**

- Google Authenticator
- Microsoft Authenticator
- Authy
- 1Password
- Any TOTP-compatible app

## 🎨 UI/UX Highlights

- **Modern Design** - Clean, minimalist interface with Tailwind CSS
- **Responsive Layout** - Works perfectly on desktop, tablet, and mobile
- **Smooth Animations** - Subtle transitions and hover effects
- **Intuitive Navigation** - Easy-to-use sidebar and quick actions
- **Flash Messages** - Clear feedback for all actions
- **Empty States** - Helpful messages when no notes are found

## 🛠️ Technology Stack

- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **WTForms** - Form handling and validation
- **Markdown** - Content rendering
- **Bleach** - HTML sanitization
- **PyOTP** - TOTP-based two-factor authentication
- **qrcode** - QR code generation for 2FA setup
- **Pillow** - Image processing for QR codes
- **Tailwind CSS** - Modern styling

## 📝 Markdown Support

The app supports full markdown syntax:

- Headers: `# H1`, `## H2`, `### H3`
- **Bold**: `**text**`
- _Italic_: `*text*`
- Lists: `- item` or `1. item`
- Links: `[text](url)`
- Code: `` `code` ``
- Code blocks: ` ```language ... ``` `
- Tables, blockquotes, and more!

## 🔧 Development

To run in development mode:

```bash
python simple_app.py
```

The app runs on `http://127.0.0.1:5000` by default.

## 📦 Production Deployment

For production use:

1. Set strong environment variables
2. Use a production WSGI server (e.g., Gunicorn)
3. Enable HTTPS
4. Set up proper backups
5. Consider using PostgreSQL instead of SQLite

Example with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "simple_app:app"
```

## 🔄 CI/CD Pipeline

This project has automated testing, security scanning, and deployment configured:

- **Automated Testing:** Python 3.9, 3.10, 3.11
- **Code Quality:** Black, isort, flake8, bandit
- **Security Scanning:** Trivy, Safety
- **Auto-Deployment:** Render (Flask app) + GitHub Pages (documentation)

See [CI_CD.md](CI_CD.md) for detailed pipeline documentation and setup instructions.

## ⚠️ Important Notes

- This app is designed for **personal local use**
- Change the default password before use
- For multi-user scenarios, additional security measures are needed
- Regular backups of `notes.db` are recommended

## 📄 License

This project is open source and available for personal use.

---

**Perfect for:** Personal note-taking, journaling, idea capture, documentation  
**Built with:** Flask, SQLAlchemy, Tailwind CSS
