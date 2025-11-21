# 🔄 CI/CD Pipeline Documentation

## Overview

This project uses **GitHub Actions** for continuous integration and continuous deployment (CI/CD). The pipeline automatically tests, lints, scans for security vulnerabilities, and deploys your application on every push to the `main` branch.

---

## 📊 Status Badges

Add these badges to your README to show the current status:

```markdown
![CI/CD Pipeline](https://github.com/thienng-it/note-hub/actions/workflows/ci-cd.yml/badge.svg?branch=main)
![Deploy to Render](https://github.com/thienng-it/note-hub/actions/workflows/deploy-render.yml/badge.svg?branch=main)
![Deploy GitHub Pages](https://github.com/thienng-it/note-hub/actions/workflows/deploy-pages.yml/badge.svg?branch=main)
```

---

## 🔧 Workflows Configuration

### 1. **CI/CD Pipeline** (`ci-cd.yml`)

**Triggers:** Push or PR to `main` or `develop` branches

**Jobs:**

#### Test Job

- **Python Versions:** 3.9, 3.10, 3.11
- **Tasks:**
  - Install dependencies from `requirements.txt`
  - Run pytest with coverage reporting
  - Upload coverage to Codecov
  - Matrix testing across multiple Python versions

```bash
# Equivalent local command:
python -m pytest test_app.py -v --cov=. --cov-report=xml
```

#### Lint Job

- **Tasks:**
  - Code formatting check with `black`
  - Import sorting check with `isort`
  - Linting with `flake8`
  - Security scanning with `bandit`

```bash
# Equivalent local commands:
black --check simple_app.py
isort --check-only simple_app.py
flake8 simple_app.py
bandit -r . -ll
```

#### Security Job

- **Tasks:**
  - Trivy filesystem vulnerability scanning
  - Results uploaded to GitHub Security tab

#### Dependency Check Job

- **Tasks:**
  - Run `safety` to check for known vulnerabilities in dependencies

---

### 2. **Deploy to Render** (`deploy-render.yml`)

**Triggers:** Push to `main` branch (excluding docs and markdown files)

**Prerequisites:**

1. Create a web service on [Render.com](https://render.com)
2. Get the Deploy Hook URL from Render settings
3. Add it as a GitHub secret

**Steps:**

1. **Verify Deployment Files**

   - Checks for `Procfile`, `requirements.txt`, `runtime.txt`, `simple_app.py`

2. **Validate Application**

   - Installs dependencies
   - Tests Python imports

3. **Deploy**
   - Sends webhook to Render to trigger deployment
   - Deployment typically takes 2-5 minutes

**Setup Instructions:**

```bash
# 1. Go to https://render.com and create account/login

# 2. Create a new Web Service with these settings:
#    Build Command: pip install -r requirements.txt
#    Start Command: gunicorn simple_app:app
#    Environment Variables:
#      - NOTES_ADMIN_USERNAME=admin
#      - NOTES_ADMIN_PASSWORD=your-secure-password
#      - FLASK_SECRET=your-secret-key

# 3. Get Deploy Hook from Render:
#    Settings → Deploy Hook → Copy URL

# 4. Add to GitHub Secrets:
#    Repo → Settings → Secrets and variables → Actions
#    Secret name: RENDER_DEPLOY_HOOK
#    Secret value: [paste Render hook URL]
```

---

### 3. **Deploy GitHub Pages** (`deploy-pages.yml`)

**Triggers:** Push to `main` branch (docs, README, or workflow changes)

**Steps:**

1. **Build**

   - Copy `docs/` folder content to `_site/`
   - Verify `index.html` exists

2. **Deploy**
   - GitHub automatically deploys `_site` as static content
   - Available at: `https://thienng-it.github.io/note-hub`

**Site Location:** `/docs` directory

---

## 🚀 Deployment Flow

```
Developer Push to main
       ↓
GitHub Actions Triggered
       ├─→ CI/CD Pipeline (test + lint + security)
       ├─→ Deploy to Render (if RENDER_DEPLOY_HOOK is set)
       └─→ Deploy GitHub Pages (if docs changed)
       ↓
All Workflows Complete ✅
```

---

## 📋 Running Workflows Locally

### Test Pipeline

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
python -m pytest test_app.py -v --cov=. --cov-report=term
```

### Code Quality

```bash
# Install linting tools
pip install black isort flake8 bandit

# Check formatting
black --check simple_app.py

# Check import sorting
isort --check-only simple_app.py

# Run linter
flake8 simple_app.py

# Security scan
bandit -r . -ll
```

### Security Check

```bash
# Install safety
pip install safety

# Check dependencies
safety check
```

---

## 🔐 Secrets Management

**Required Secrets:**

| Secret Name          | Where to Get        | Purpose               |
| -------------------- | ------------------- | --------------------- |
| `RENDER_DEPLOY_HOOK` | Render.com Settings | Auto-deploy to Render |

**To Add Secrets:**

1. Go to GitHub repo
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Enter name and value
5. Save

---

## ✅ Best Practices

1. **Always test locally before pushing**

   ```bash
   pytest test_app.py
   black --check simple_app.py
   ```

2. **Commit with conventional messages** (already set up)

   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `chore:` for maintenance

3. **Review workflow results**

   - Go to repo → Actions tab
   - Check individual workflow runs
   - Fix any failures before merging PRs

4. **Keep dependencies up to date**
   - Regularly update `requirements.txt`
   - Run `safety check` to catch vulnerabilities

---

## 🐛 Troubleshooting

### Render Deployment Not Triggering

**Issue:** Deploy to Render shows warning about `RENDER_DEPLOY_HOOK`

**Solution:**

1. Verify secret is added: Settings → Secrets and variables → Actions
2. Secret name must be exactly: `RENDER_DEPLOY_HOOK`
3. Render hook URL must be valid
4. Restart deployment in Render dashboard

### Tests Failing in CI but Passing Locally

**Possible Causes:**

- Python version differences (check matrix in `ci-cd.yml`)
- Missing environment variables
- Database state issues

**Solution:**

```bash
# Test with same Python version as CI
python3.11 -m pytest test_app.py -v

# Check environment
echo $FLASK_ENV
echo $NOTES_DB_PATH
```

### GitHub Pages Not Updating

**Issue:** Changes to `docs/` not showing on GitHub Pages

**Solution:**

1. Ensure changes are pushed to `main` branch
2. Check Actions tab for deploy-pages workflow status
3. Go to repo Settings → Pages → verify source is `/docs`
4. Wait 1-2 minutes for GitHub to update

---

## 📊 Monitoring

**View Workflow Status:**

1. Go to repo homepage
2. Click "Actions" tab
3. Select workflow to view details
4. Click specific run to see logs

**Coverage Reports:**

- Uploaded to Codecov on each test run
- View at: `https://codecov.io/gh/thienng-it/note-hub`

**Security Scanning:**

- Results in GitHub Security tab
- Vulnerabilities sorted by severity

---

## 🎯 Next Steps

1. ✅ Add `RENDER_DEPLOY_HOOK` secret for auto-deployment
2. ✅ Push changes to trigger workflows
3. ✅ Verify all workflows pass in Actions tab
4. ✅ Add badges to README.md

---

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Render Deploy Hooks](https://render.com/docs/deploy-hooks)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Python Testing with pytest](https://docs.pytest.org/)
- [Code Formatting with Black](https://black.readthedocs.io/)

---

**Last Updated:** November 22, 2025
**Maintained By:** CI/CD Pipeline Documentation
