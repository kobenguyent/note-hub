# Deployment Guide for Note Hub

## ⚠️ CRITICAL: MySQL Database Configuration

**NoteHub now uses MySQL instead of SQLite.** You'll need to set up a MySQL database before deploying.

### MySQL Database Setup Options

#### Option 1: Managed Database (Recommended for Production)

Use a managed MySQL service like:

- **Render Database** - Easy integration with Render web services
- **AWS RDS MySQL** - Scalable and reliable
- **Google Cloud SQL** - Managed MySQL on GCP
- **DigitalOcean Managed Database** - Simple and affordable
- **PlanetScale** - Serverless MySQL

#### Option 2: Self-Hosted MySQL

1. **Install MySQL Server**:

   ```bash
   # Ubuntu/Debian
   sudo apt-get install mysql-server

   # macOS
   brew install mysql
   ```

2. **Create Database and User**:
   ```sql
   CREATE DATABASE notehub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'notehub'@'%' IDENTIFIED BY 'secure_password_here';
   GRANT ALL PRIVILEGES ON notehub.* TO 'notehub'@'%';
   FLUSH PRIVILEGES;
   ```

### Required Environment Variables

Set these environment variables in your deployment platform:

```bash
# MySQL Database Configuration
MYSQL_HOST=your-mysql-host.com
MYSQL_PORT=3306
MYSQL_USER=notehub
MYSQL_PASSWORD=your_secure_mysql_password
MYSQL_DATABASE=notehub

# Application Configuration
NOTES_ADMIN_USERNAME=admin
NOTES_ADMIN_PASSWORD=your_secure_admin_password
FLASK_SECRET=your-random-secret-key
```

---

## Deploy to Render (Recommended for Production)

Netlify hosts the Flask backend through **Netlify Functions** using `serverless-wsgi`. Every HTTP request is proxied to the serverless function described in `infra/netlify/functions/app.py` and orchestrated by `netlify.toml`.

### Step 1: Create Netlify Site

1. Install the CLI (optional but handy): `npm install -g netlify-cli`
2. Run `netlify init` inside the repo or connect the GitHub repo directly from the Netlify dashboard
3. When prompted for build settings, simply accept the defaults (the CLI/dashboard will read `netlify.toml`)

### Step 2: Configure Environment Variables

In Netlify → Site settings → Environment variables, add:

```
NOTES_ADMIN_USERNAME=admin
NOTES_ADMIN_PASSWORD=your-secure-password
FLASK_SECRET=your-secret-key-here
NOTES_DB_PATH=/tmp/notes.db
```

### Step 3: Enable Deploy Hooks (optional)

If you want GitHub Actions to trigger deployments, create a Build Hook (Site settings → Build & deploy → Build hooks) and copy the URL into the `NETLIFY_DEPLOY_HOOK` secret in GitHub.

### Step 4: Deploy

- **Manual:** `netlify deploy --prod`
- **Git-integrated:** Every push to `main` automatically triggers a build on Netlify
- **Via GitHub Action:** The `deploy-netlify.yml` workflow will POST to your build hook and Netlify will perform the deploy

Your app will be available at `https://<your-site>.netlify.app` once the first deploy succeeds.

---

## Deploy to Render

### Prerequisites

1. Create a [Render account](https://render.com)
2. Set up a MySQL database (Render offers managed MySQL databases)
3. Connect your GitHub repository to Render

### Deployment Steps

1. **Create MySQL Database (if using Render):**

   - Click "New +" → "MySQL"
   - Choose your database name (e.g., `notehub-db`)
   - Select region and instance type
   - Wait for database to be provisioned
   - Note the connection details (host, port, username, password, database name)

2. **Create Web Service:**

   - Click "New +" → "Web Service"
   - Connect your GitHub repo: `thienng-it/note-hub`
   - Render will automatically detect `render.yaml`

3. **Configure Environment Variables:**

   In your web service settings, add:

   - `MYSQL_HOST`: (from your MySQL database)
   - `MYSQL_PORT`: `3306`
   - `MYSQL_USER`: (from your MySQL database)
   - `MYSQL_PASSWORD`: (from your MySQL database)
   - `MYSQL_DATABASE`: (from your MySQL database)
   - `NOTES_ADMIN_USERNAME`: `admin` (or your choice)
   - `NOTES_ADMIN_PASSWORD`: (set a secure password)
   - `FLASK_SECRET`: (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for first deployment to complete
   - Visit `https://your-app.onrender.com`

### Post-Deployment Verification

**IMPORTANT:** After deployment, verify database connection:

1. **Check Application Logs:**

   - Look for "MySQL Database configured" message
   - Verify no connection errors

2. **Test Application:**

   - Visit `https://your-app.onrender.com`
   - Log in with admin credentials
   - Create a test note to verify database functionality

3. **Monitor Connection:**
   - MySQL connections are automatically managed by SQLAlchemy
   - Check logs for any connection pool warnings
   - Monitor database performance in MySQL dashboard

### Troubleshooting on Render

**Problem:** Cannot connect to MySQL database

**Solutions:**

1. **Verify Environment Variables:**

   ```bash
   # Check all MySQL variables are set correctly
   echo $MYSQL_HOST
   echo $MYSQL_PORT
   echo $MYSQL_USER
   echo $MYSQL_DATABASE
   ```

2. **Check Database Accessibility:**

   - Ensure MySQL database is running
   - Verify network access between web service and database
   - Check firewall rules if using external MySQL

3. **Check Application Logs:**

   - Look for: `📊 MySQL Database configured: user@host:port/database`
   - Look for connection error messages
   - Verify SQLAlchemy connection pool messages

4. **Test MySQL Connection:**
   ```bash
   # In Render Shell
   mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE
   ```

---

## Deploy to Netlify (Serverless - Requires External MySQL!)

**⚠️ WARNING:** Netlify Functions are stateless. You MUST use an external MySQL database service (e.g., PlanetScale, AWS RDS, or any MySQL provider).

### Step 1: Create Netlify Site

---

## Local Development

### Running Locally

1. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables:**

   ```bash
   export MYSQL_HOST=localhost
   export MYSQL_PORT=3306
   export MYSQL_USER=notehub
   export MYSQL_PASSWORD=your_password
   export MYSQL_DATABASE=notehub
   export NOTES_ADMIN_USERNAME=admin
   export NOTES_ADMIN_PASSWORD=YourSecurePassword123!
   export FLASK_SECRET=your-secret-key
   ```

3. **Run Development Server:**

   ```bash
   python scripts/dev_server.py
   ```

4. **Access Application:**
   - Open: `http://localhost:5000`
   - Login with admin credentials

---

## Production Best Practices

1. **Always Change Default Password:** First login, change admin password
2. **Use Strong Secret Key:** Never use default `FLASK_SECRET`
3. **Enable HTTPS:** Render provides this automatically
4. **Monitor Database Size:** Check MySQL dashboard regularly
5. **Backup Database:** Use `mysqldump` or database provider's backup tools

### Database Backup (MySQL)

```bash
# Create backup using mysqldump
mysqldump -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE > backup.sql

# Restore from backup
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < backup.sql
```

---

## Monitoring and Health Checks

### Application Monitoring

Monitor your application health through:

- Application logs for MySQL connection status
- Database dashboard for query performance
- Connection pool metrics in SQLAlchemy logs
- Application response times

### MySQL Monitoring

Key metrics to monitor:

- Database size and growth
- Connection pool usage
- Query performance
- Replication lag (if using replicas)
- Backup status

### Example Health Check

```bash
curl https://your-app.onrender.com/
# Should return the login page successfully
```

---

## Quick Verification Checklist

After deployment, verify:

- [ ] MySQL connection successful (check logs)
- [ ] No database connection errors in logs
- [ ] Can create a test account
- [ ] Test account persists after redeployment
- [ ] Application responds correctly
- [ ] MySQL database shows tables created

---

## Additional Notes

- MySQL provides better concurrency and performance than SQLite
- Regular backups are essential - use `mysqldump` or provider backup tools
- Always change default admin password
- Use strong `FLASK_SECRET` value
- Monitor database size and connection pool

## Monitoring

After deployment:

1. Test login with your credentials
2. Create a test note
3. Verify all features work (search, tags, dark mode)
4. Check logs for any errors

Need help? Check the main [README.md](README.md)
