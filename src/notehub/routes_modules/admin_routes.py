"""Admin dashboard and management routes."""

from __future__ import annotations

import os
from datetime import datetime, timezone

from flask import flash, jsonify, redirect, render_template, request, url_for
from sqlalchemy import func, select

from ..models import User
from ..services.utils import current_user, db, login_required


def register_admin_routes(app):
    """Register admin-related routes."""
    
    @app.route("/admin/users")
    @login_required
    def admin_users():
        """Admin dashboard to view and manage all users."""
        user = current_user()
        
        # Check if user is admin
        if not user or user.username != 'admin':
            flash("Access denied. Admin privileges required.", "error")
            return redirect(url_for("index"))
        
        # Get search and pagination parameters
        search_query = request.args.get('search', '').strip()
        page = max(1, int(request.args.get('page', 1)))
        per_page = 20
        
        with db() as s:
            # Build query
            stmt = select(User).order_by(User.created_at.desc())
            
            # Apply search filter
            if search_query:
                stmt = stmt.where(
                    (User.username.ilike(f'%{search_query}%')) |
                    (User.email.ilike(f'%{search_query}%'))
                )
            
            # Get total count
            total_count = s.execute(select(func.count()).select_from(stmt.subquery())).scalar()
            
            # Apply pagination
            offset = (page - 1) * per_page
            stmt = stmt.limit(per_page).offset(offset)
            
            # Execute query
            users = s.execute(stmt).scalars().all()
            
            # Get stats
            total_users = s.execute(select(func.count(User.id))).scalar()
            users_with_2fa = s.execute(
                select(func.count(User.id)).where(User.totp_secret.isnot(None))
            ).scalar()
            users_with_email = s.execute(
                select(func.count(User.id)).where(User.email.isnot(None))
            ).scalar()
            
            # Calculate pagination
            total_pages = (total_count + per_page - 1) // per_page
            
            return render_template(
                "admin_dashboard.html",
                users=users,
                search_query=search_query,
                page=page,
                total_pages=total_pages,
                total_count=total_count,
                total_users=total_users,
                users_with_2fa=users_with_2fa,
                users_with_email=users_with_email,
            )
    
    @app.route("/admin/health")
    def admin_health():
        """Health check endpoint to verify database persistence and system status."""
        try:
            from ..config import AppConfig
            config = AppConfig()
            
            # Get database path
            db_path = config.db_path
            
            # Check if database file exists
            db_exists = os.path.exists(db_path)
            db_size = os.path.getsize(db_path) if db_exists else 0
            db_dir = os.path.dirname(db_path) or "."
            
            # Check directory permissions
            dir_writable = os.access(db_dir, os.W_OK) if os.path.exists(db_dir) else False
            
            # Get disk space info (if on Unix-like system)
            disk_info = {}
            try:
                stat = os.statvfs(db_dir)
                disk_info = {
                    "total_gb": round(stat.f_blocks * stat.f_frsize / (1024**3), 2),
                    "free_gb": round(stat.f_bfree * stat.f_frsize / (1024**3), 2),
                    "available_gb": round(stat.f_bavail * stat.f_frsize / (1024**3), 2),
                }
            except:
                disk_info = {"error": "Unable to get disk stats"}
            
            # Check database connectivity
            with db() as s:
                user_count = s.execute(select(func.count(User.id))).scalar()
            
            # Determine if path is on persistent storage (common mount points)
            persistent_paths = ["/var/data", "/opt/render/project/data", "/data", "/mnt"]
            is_persistent = any(db_path.startswith(path) for path in persistent_paths)
            
            health_data = {
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "database": {
                    "path": db_path,
                    "exists": db_exists,
                    "size_bytes": db_size,
                    "size_mb": round(db_size / (1024 * 1024), 2),
                    "directory": db_dir,
                    "writable": dir_writable,
                    "likely_persistent": is_persistent,
                },
                "disk": disk_info,
                "stats": {
                    "total_users": user_count,
                },
                "warnings": [],
            }
            
            # Add warnings
            if not is_persistent:
                health_data["warnings"].append(
                    f"Database path '{db_path}' may not be on persistent storage. "
                    "Data could be lost on redeployment!"
                )
            
            if not db_exists:
                health_data["warnings"].append("Database file does not exist yet.")
            
            if not dir_writable:
                health_data["warnings"].append("Database directory is not writable!")
            
            return jsonify(health_data)
            
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }), 500

