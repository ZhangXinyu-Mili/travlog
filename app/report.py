from flask import flash, redirect, render_template, request, url_for
from app import app
from app.auth import login_required
from app.repositories.event_comment_repository import (
    db_delete_comment,
    db_escalate_comment,
    db_get_comment,
    db_get_reported_comments,
    db_get_reported_comments_count,
    db_hide_comment,
    db_reinstate_comment,
)


@app.get("/reports")
@login_required(role=["moderator", "editor", "supporttech", "admin"])
def reports():
    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 8, type=int)
    is_hidden = request.args.get("is_hidden", type=bool)
    escalated = request.args.get("escalated", type=bool)

    reported_comments = db_get_reported_comments(
        current_page, page_size, is_hidden, escalated
    )
    total_comments_count = db_get_reported_comments_count(is_hidden, escalated)
    total_pages = (total_comments_count + page_size - 1) // page_size

    return render_template(
        "report/reports.html",
        comments=reported_comments,
        current_page=current_page,
        page_size=page_size,
        total_pages=total_pages,
    )


@app.post("/comments/<int:comment_id>/hide")
@login_required(role=["moderator", "editor", "admin", "supporttech"])
def hide_comment(comment_id):
    comment = db_get_comment(comment_id)
    if not comment:
        flash("Comment not found", "danger")
        return redirect(url_for("reports"))

    try:
        db_hide_comment(comment_id)
    except Exception as e:
        print(e)
        flash("Something went wrong, please try again.", "danger")
        return redirect(url_for("reports"))

    flash("The comment is now hidden.", "success")
    return redirect(url_for("reports"))


@app.post("/comments/<int:comment_id>/escalate")
@login_required(role=["moderator", "editor", "admin", "supporttech"])
def escalate_comment(comment_id):
    comment = db_get_comment(comment_id)
    if not comment:
        flash("Comment not found", "danger")
        return redirect(url_for("reports"))

    try:
        db_escalate_comment(comment_id)
    except:
        flash("Something went wrong, please try again.", "danger")
        return redirect(url_for("reports"))

    flash("Escalate comment to admin successfully.", "success")
    return redirect(url_for("reports"))


@app.post("/comments/<int:comment_id>/delete")
@login_required(role=["editor", "admin", "supporttech"])
def delete_comment(comment_id):
    comment = db_get_comment(comment_id)
    if not comment:
        flash("Comment not found", "danger")
        return redirect(url_for("reports", is_hidden=True, escalated=True))

    try:
        db_delete_comment(comment_id)
    except Exception as e:
        print(e)
        flash("Something went wrong, please try again.", "danger")
        return redirect(url_for("reports", is_hidden=True, escalated=True))

    flash("The comment has been deleted.", "success")
    return redirect(url_for("reports", is_hidden=True, escalated=True))


@app.post("/comments/<int:comment_id>/reinstate")
@login_required(role=["editor", "admin", "supporttech"])
def reinstate_comment(comment_id):
    comment = db_get_comment(comment_id)
    if not comment:
        flash("Comment not found", "danger")
        return redirect(url_for("reports", is_hidden=True, escalated=True))

    try:
        db_reinstate_comment(comment_id)
    except Exception as e:
        print(e)
        flash("Something went wrong, please try again.", "danger")
        return redirect(url_for("reports", is_hidden=True, escalated=True))

    flash("The comment has been reinstated successfully.", "success")
    return redirect(url_for("reports", is_hidden=True, escalated=True))
