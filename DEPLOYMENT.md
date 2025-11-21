# Deployment Guide for Note Hub

## Deploy to Render (Recommended)

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up with your GitHub account
3. Connect your GitHub repository

### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Select your `note-hub` repository
3. Configure the following:
   - **Name:** `note-hub` (or any name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn simple_app:app`
   - **Free tier:** Select if you want free (may sleep after 15 mins of inactivity)

### Step 3: Environment Variables

Add these in Render dashboard under "Environment":

```
NOTES_ADMIN_USERNAME=admin
NOTES_ADMIN_PASSWORD=your-secure-password
FLASK_SECRET=your-secret-key-here
NOTES_DB_PATH=/tmp/notes.db
```

### Step 4: Deploy

- Render will automatically deploy on every push to `main`
- Your app will be available at: `https://note-hub.onrender.com`

## Deploy to Railway

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Create Project

1. Click "Create New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `note-hub` repository

### Step 3: Configure

1. Add environment variables (same as above)
2. Railway will auto-detect Procfile

### Step 4: Deploy

- Your app will be live automatically
- Get URL from Railway dashboard

## Deploy to PythonAnywhere

### Step 1: Create Account

1. Go to https://www.pythonanywhere.com
2. Sign up for free account

### Step 2: Upload Code

- Clone your repo or upload files manually

### Step 3: Configure Web App

1. Create new Web app (Python 3.11 + Flask)
2. Configure WSGI file to point to `simple_app:app`

### Step 4: Set Environment Variables

- Add in "Web" section

## Local Deployment Notes

- Database will be created at specified `NOTES_DB_PATH`
- For production, consider using PostgreSQL instead of SQLite
- Always change default admin password
- Use strong `FLASK_SECRET` value

## Monitoring

After deployment:

1. Test login with your credentials
2. Create a test note
3. Verify all features work (search, tags, dark mode)
4. Check logs for any errors

Need help? Check the main [README.md](README.md)
