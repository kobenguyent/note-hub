"""Task management routes."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import case, func, select

from ..forms import TaskForm
from ..models import Task
from ..services.utils import current_user, db, login_required


def register_task_routes(app):
    """Register task-related routes."""
    
    @app.route("/tasks")
    @login_required
    def tasks():
        user = current_user()
        filter_type = request.args.get('filter', 'all')
        with db() as s:
            stmt = select(Task).where(Task.owner_id == user.id)
            if filter_type == 'active':
                stmt = stmt.where(Task.completed == False)
            elif filter_type == 'completed':
                stmt = stmt.where(Task.completed == True)
            priority_order = case((Task.priority == 'high', 1), (Task.priority == 'medium', 2), (Task.priority == 'low', 3), else_=2)
            tasks_list = s.execute(stmt.order_by(Task.completed.asc(), priority_order, Task.due_date.asc().nullslast(), Task.created_at.desc())).scalars().all()
            total_tasks = s.execute(select(func.count(Task.id)).where(Task.owner_id == user.id)).scalar() or 0
            completed_tasks = s.execute(select(func.count(Task.id)).where(Task.owner_id == user.id, Task.completed == True)).scalar() or 0
            active_tasks = total_tasks - completed_tasks
        return render_template("tasks.html", tasks=tasks_list, filter_type=filter_type, total_tasks=total_tasks, completed_tasks=completed_tasks, active_tasks=active_tasks)

    @app.route("/task/new", methods=["GET", "POST"])
    @login_required
    def new_task():
        user = current_user()
        form = TaskForm()
        if form.validate_on_submit():
            try:
                with db() as s:
                    due_date = None
                    if form.due_date.data:
                        due_date = datetime.combine(form.due_date.data, datetime.min.time()).replace(tzinfo=timezone.utc)
                    task = Task(title=form.title.data.strip(), description=form.description.data or None, due_date=due_date, priority=form.priority.data, owner_id=user.id)
                    s.add(task)
                    s.commit()
                    flash("Task created!", "success")
                    return redirect(url_for("tasks"))
            except Exception as exc:
                flash(f"Error creating task: {exc}", "error")
        if request.method == "GET":
            form = TaskForm()
        return render_template("edit_task.html", form=form, task=None, is_edit=False)

    @app.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_task(task_id: int):
        user = current_user()
        with db() as s:
            task = s.get(Task, task_id)
            if not task or task.owner_id != user.id:
                flash("Task not found or you don't have permission to edit it.", "error")
                return redirect(url_for("tasks"))
            form = TaskForm(obj=task)
            if request.method == "GET" and task.due_date:
                form.due_date.data = task.due_date.date()
            if form.validate_on_submit():
                try:
                    task.title = form.title.data.strip()
                    task.description = form.description.data or None
                    if form.due_date.data:
                        task.due_date = datetime.combine(form.due_date.data, datetime.min.time()).replace(tzinfo=timezone.utc)
                    else:
                        task.due_date = None
                    task.priority = form.priority.data
                    s.commit()
                    flash("Task updated!", "success")
                    return redirect(url_for("tasks"))
                except Exception as exc:
                    flash(f"Error updating task: {exc}", "error")
            return render_template("edit_task.html", form=form, task=task, is_edit=True)

    @app.route("/task/<int:task_id>/toggle", methods=["POST"])
    @login_required
    def toggle_task(task_id: int):
        user = current_user()
        with db() as s:
            task = s.get(Task, task_id)
            if not task or task.owner_id != user.id:
                flash("Task not found.", "error")
                return redirect(url_for("tasks"))
            task.completed = not task.completed
            s.commit()
            status = "completed" if task.completed else "marked as active"
            flash(f"Task {status}!", "success")
        return redirect(url_for("tasks", filter=request.args.get('filter', 'all')))

    @app.route("/task/<int:task_id>/delete", methods=["POST"])
    @login_required
    def delete_task(task_id: int):
        user = current_user()
        try:
            with db() as s:
                task = s.get(Task, task_id)
                if not task or task.owner_id != user.id:
                    flash("Task not found or you don't have permission to delete it.", "error")
                else:
                    s.delete(task)
                    s.commit()
                    flash("Task deleted!", "success")
        except Exception as exc:
            flash(f"Error deleting task: {exc}", "error")
        return redirect(url_for("tasks", filter=request.args.get('filter', 'all')))
