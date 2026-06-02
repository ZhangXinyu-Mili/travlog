from flask import flash, redirect, request, session, url_for, render_template
from app import app
from app.auth import login_required
from app.repositories.announcement_repository import (
    db_get_all_announcements,
    db_get_announcement_by_id,
    db_get_announcements_count,
    db_create_announcement,
    db_update_announcement,
    db_update_announcement_status,
    db_delete_announcement,
)
from datetime import datetime

@app.get("/announcements")
@login_required(role=["editor", "admin", "supporttech"])
def list_announcements():
    query = request.args.get("q", "").lower()
    current_page = request.args.get("current_page", 1, type=int)
    page_size = 5

    all_announcements = db_get_all_announcements(current_page, page_size, query)
    total_count = db_get_announcements_count(query)
    total_pages = (total_count + page_size - 1) // page_size

    return render_template(
        "announcement/list.html",
        announcements=all_announcements,
        current_page=current_page,
        total_pages=total_pages,
        query=query,
    )

@app.post("/announcements/<int:announcement_id>/status")
@login_required(role=["editor", "admin", "supporttech"])
def update_announcement_status(announcement_id):
    status = request.form.get("status", "").strip().lower()
    if status not in ["new", "not new"]:
        flash("Invalid status.", "danger")
        return redirect(url_for("list_announcements"))
    is_new = status == "new"
    db_update_announcement_status(announcement_id, is_new)
    flash("Announcement status has been updated successfully.", "success")
    return redirect(url_for("list_announcements"))

@app.route("/announcements/create", methods=["GET", "POST"])
@login_required(role=["editor", "admin", "supporttech"])
def create_announcement():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if not title:
            flash("Title is required.", "danger")
            return render_template("announcement/create.html", title=title, content=content)
        if not content:
            flash("Content is required.", "danger")
            return render_template("announcement/create.html", title=title, content=content)
        db_create_announcement(
            user_id=session.get("user_id"),
            title=title,
            content=content,
            is_new=True,
            created_at=datetime.now(),
        )
        flash("Announcement has been created successfully.", "success")
        return redirect(url_for("list_announcements"))
    return render_template("announcement/create.html")

@app.route("/announcements/<int:announcement_id>/edit", methods=["GET", "POST"])
@login_required(role=["editor", "admin", "supporttech"])
def edit_announcement(announcement_id):
    announcement = db_get_announcement_by_id(announcement_id)
    if not announcement:
        flash("Announcement not found.", "danger")
        return redirect(url_for("list_announcements"))
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if not title:
            flash("Title is required.", "danger")
            return render_template("announcement/edit.html", title=title, content=content, status=announcement["is_new"])
        if not content:
            flash("Content is required.", "danger")
            return render_template("announcement/edit.html", title=title, content=content, status=announcement["is_new"])
        db_update_announcement(
            announcement_id=announcement_id,
            title=title,
            content=content,
            is_new=announcement["is_new"],
        )
        flash("Announcement has been updated successfully.", "success")
        return redirect(url_for("list_announcements"))
    return render_template("announcement/edit.html", title=announcement["title"], content=announcement["content"], status=announcement["is_new"])

@app.post("/announcements/<int:announcement_id>/delete")
@login_required(role=["editor", "admin", "supporttech"])
def delete_announcement(announcement_id):
    db_delete_announcement(announcement_id)
    flash("Announcement has been deleted.", "success")
    return redirect(url_for("list_announcements"))
