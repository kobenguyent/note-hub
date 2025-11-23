# SQLite to MySQL Migration Guide

This guide will help you migrate your existing NoteHub data from SQLite to MySQL.

## Prerequisites

- Access to your existing SQLite database file (`notes.db`)
- MySQL server installed and running
- Python environment with required packages installed

## Step 1: Setup MySQL Database

First, create a new MySQL database and user:

```bash
# Connect to MySQL as root
mysql -u root -p

# Create database with UTF-8 support
CREATE DATABASE notehub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create user and grant privileges
CREATE USER 'notehub'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON notehub.* TO 'notehub'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## Step 2: Configure Environment Variables

Update your environment variables to use MySQL:

```bash
# Old SQLite configuration (remove these)
# export NOTES_DB_PATH=notes.db

# New MySQL configuration
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=notehub
export MYSQL_PASSWORD=your_secure_password
export MYSQL_DATABASE=notehub

# Keep these as before
export NOTES_ADMIN_USERNAME=admin
export NOTES_ADMIN_PASSWORD=your_password
export FLASK_SECRET=your_secret_key
```

## Step 3: Install MySQL Dependencies

The requirements.txt has been updated to include MySQL support:

```bash
pip install -r requirements.txt
```

This will install:

- PyMySQL (MySQL database adapter)
- cryptography (for SSL connections)

## Step 4: Initialize MySQL Database

Run the application once to create all tables in MySQL:

```bash
python wsgi.py
```

The application will automatically create all necessary tables in your MySQL database. You can stop it after you see the successful initialization message.

## Step 5: Export Data from SQLite

Create a Python script to export your data from SQLite:

```python
# export_sqlite_data.py
import sqlite3
import json
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('notes.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Export users
cursor.execute('SELECT * FROM users')
users = [dict(row) for row in cursor.fetchall()]

# Export notes
cursor.execute('SELECT * FROM notes')
notes = [dict(row) for row in cursor.fetchall()]

# Export tags
cursor.execute('SELECT * FROM tags')
tags = [dict(row) for row in cursor.fetchall()]

# Export note_tag relationships
cursor.execute('SELECT * FROM note_tag')
note_tags = [dict(row) for row in cursor.fetchall()]

# Export tasks
cursor.execute('SELECT * FROM tasks')
tasks = [dict(row) for row in cursor.fetchall()]

# Export share_notes
cursor.execute('SELECT * FROM share_notes')
share_notes = [dict(row) for row in cursor.fetchall()]

# Export invitations
cursor.execute('SELECT * FROM invitations')
invitations = [dict(row) for row in cursor.fetchall()]

# Export password_reset_tokens
cursor.execute('SELECT * FROM password_reset_tokens')
reset_tokens = [dict(row) for row in cursor.fetchall()]

# Save to JSON file
export_data = {
    'users': users,
    'notes': notes,
    'tags': tags,
    'note_tags': note_tags,
    'tasks': tasks,
    'share_notes': share_notes,
    'invitations': invitations,
    'password_reset_tokens': reset_tokens
}

with open('sqlite_export.json', 'w') as f:
    json.dump(export_data, f, indent=2, default=str)

conn.close()
print("✅ Data exported to sqlite_export.json")
```

Run the export script:

```bash
python export_sqlite_data.py
```

## Step 6: Import Data into MySQL

Create a Python script to import the data into MySQL:

```python
# import_to_mysql.py
import json
import sys
import os

# Add src directory to path
sys.path.insert(0, 'src')

from notehub import create_app
from notehub.config import AppConfig
from notehub.database import get_session
from notehub.models import User, Note, Tag, Task, ShareNote, Invitation, PasswordResetToken, note_tag

# Create Flask app
app = create_app(AppConfig())

# Load exported data
with open('sqlite_export.json', 'r') as f:
    data = json.load(f)

def import_data():
    with app.app_context():
        with get_session() as session:
            print("📦 Importing data to MySQL...")

            # Import users (skip admin if exists)
            print(f"👥 Importing {len(data['users'])} users...")
            for user_data in data['users']:
                existing = session.query(User).filter_by(username=user_data['username']).first()
                if not existing:
                    user = User(
                        id=user_data['id'],
                        username=user_data['username'],
                        password_hash=user_data['password_hash'],
                        theme=user_data.get('theme', 'light'),
                        bio=user_data.get('bio'),
                        email=user_data.get('email'),
                        totp_secret=user_data.get('totp_secret'),
                        created_at=user_data.get('created_at'),
                        last_login=user_data.get('last_login')
                    )
                    session.add(user)
            session.commit()
            print("✅ Users imported")

            # Import tags
            print(f"🏷️  Importing {len(data['tags'])} tags...")
            for tag_data in data['tags']:
                tag = Tag(
                    id=tag_data['id'],
                    name=tag_data['name'],
                    color=tag_data.get('color', '#3B82F6'),
                    created_at=tag_data.get('created_at')
                )
                session.add(tag)
            session.commit()
            print("✅ Tags imported")

            # Import notes
            print(f"📝 Importing {len(data['notes'])} notes...")
            for note_data in data['notes']:
                note = Note(
                    id=note_data['id'],
                    title=note_data['title'],
                    body=note_data['body'],
                    pinned=note_data.get('pinned', False),
                    archived=note_data.get('archived', False),
                    favorite=note_data.get('favorite', False),
                    created_at=note_data.get('created_at'),
                    updated_at=note_data.get('updated_at'),
                    owner_id=note_data.get('owner_id')
                )
                session.add(note)
            session.commit()
            print("✅ Notes imported")

            # Import note-tag relationships
            print(f"🔗 Importing {len(data['note_tags'])} note-tag relationships...")
            for nt_data in data['note_tags']:
                stmt = note_tag.insert().values(
                    note_id=nt_data['note_id'],
                    tag_id=nt_data['tag_id']
                )
                session.execute(stmt)
            session.commit()
            print("✅ Note-tag relationships imported")

            # Import tasks
            print(f"✅ Importing {len(data['tasks'])} tasks...")
            for task_data in data['tasks']:
                task = Task(
                    id=task_data['id'],
                    title=task_data['title'],
                    description=task_data.get('description'),
                    completed=task_data.get('completed', False),
                    due_date=task_data.get('due_date'),
                    priority=task_data.get('priority', 'medium'),
                    owner_id=task_data['owner_id'],
                    created_at=task_data.get('created_at'),
                    updated_at=task_data.get('updated_at')
                )
                session.add(task)
            session.commit()
            print("✅ Tasks imported")

            # Import share notes
            print(f"🔗 Importing {len(data['share_notes'])} share notes...")
            for share_data in data['share_notes']:
                share = ShareNote(
                    id=share_data['id'],
                    note_id=share_data['note_id'],
                    shared_by_id=share_data['shared_by_id'],
                    shared_with_id=share_data['shared_with_id'],
                    can_edit=share_data.get('can_edit', False),
                    created_at=share_data.get('created_at')
                )
                session.add(share)
            session.commit()
            print("✅ Share notes imported")

            # Import invitations
            print(f"📨 Importing {len(data['invitations'])} invitations...")
            for inv_data in data['invitations']:
                invitation = Invitation(
                    id=inv_data['id'],
                    token=inv_data['token'],
                    inviter_id=inv_data['inviter_id'],
                    email=inv_data.get('email'),
                    message=inv_data.get('message'),
                    used=inv_data.get('used', False),
                    used_by_id=inv_data.get('used_by_id'),
                    expires_at=inv_data['expires_at'],
                    created_at=inv_data.get('created_at')
                )
                session.add(invitation)
            session.commit()
            print("✅ Invitations imported")

            # Import password reset tokens
            print(f"🔑 Importing {len(data['password_reset_tokens'])} password reset tokens...")
            for token_data in data['password_reset_tokens']:
                token = PasswordResetToken(
                    id=token_data['id'],
                    user_id=token_data['user_id'],
                    token=token_data['token'],
                    expires_at=token_data['expires_at'],
                    used=token_data.get('used', False),
                    created_at=token_data.get('created_at')
                )
                session.add(token)
            session.commit()
            print("✅ Password reset tokens imported")

            print("\n🎉 Migration completed successfully!")
            print(f"📊 Summary:")
            print(f"   - Users: {len(data['users'])}")
            print(f"   - Notes: {len(data['notes'])}")
            print(f"   - Tags: {len(data['tags'])}")
            print(f"   - Tasks: {len(data['tasks'])}")

if __name__ == '__main__':
    try:
        import_data()
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
```

Run the import script:

```bash
python import_to_mysql.py
```

## Step 7: Verify Migration

1. Start your application:

   ```bash
   python wsgi.py
   ```

2. Log in with your existing credentials

3. Verify:
   - All notes are present
   - Tags are preserved
   - Tasks are showing correctly
   - User profiles are intact

## Step 8: Backup and Cleanup

Once you've verified everything works:

1. **Backup your SQLite database** (just in case):

   ```bash
   cp notes.db notes.db.backup
   ```

2. **Test MySQL backups**:

   ```bash
   mysqldump -u notehub -p notehub > backup.sql
   ```

3. **Optional: Remove SQLite files** after confirming everything works:
   ```bash
   # Only do this after thorough testing!
   # rm notes.db
   # rm notes.db-shm
   # rm notes.db-wal
   ```

## Troubleshooting

### Connection Errors

If you get connection errors:

- Verify MySQL is running: `mysql -u notehub -p`
- Check environment variables are set correctly
- Ensure firewall isn't blocking port 3306

### Import Errors

If import fails:

- Check the export file: `cat sqlite_export.json`
- Verify MySQL tables exist: `mysql -u notehub -p notehub -e "SHOW TABLES;"`
- Check for foreign key constraints

### Character Encoding Issues

If you see strange characters:

- Ensure database is created with UTF-8: `utf8mb4_unicode_ci`
- Check your MySQL configuration for default character set

## Benefits of MySQL over SQLite

- ✅ Better concurrency - multiple users can access simultaneously
- ✅ Better performance for larger datasets
- ✅ Network access - database can be on separate server
- ✅ Better backup tools and replication
- ✅ More suitable for production environments
- ✅ Better scalability for growing applications

## Need Help?

If you encounter issues during migration:

1. Check the application logs for detailed error messages
2. Verify MySQL connection with: `mysql -u notehub -p notehub`
3. Check that all environment variables are set correctly
4. Ensure you have the latest version of requirements installed

## Rollback Plan

If you need to rollback to SQLite:

1. Stop the application
2. Restore old environment variables:
   ```bash
   export NOTES_DB_PATH=notes.db
   unset MYSQL_HOST MYSQL_PORT MYSQL_USER MYSQL_PASSWORD MYSQL_DATABASE
   ```
3. Checkout previous code version (before MySQL migration)
4. Start the application

Your original SQLite database will still be intact if you didn't delete it.
