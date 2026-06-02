from flask import flash, redirect, render_template, request, url_for, session
from datetime import datetime
from app import app
from app.auth import login_required
from app.repositories.issue_repository import (
    db_add_helpdesk_comment,
    db_add_helpdesk_issue,
    db_get_helpdesk_comments_count_by_issue_id,
    db_get_helpdesk_issues_count_by_user_id,
    db_get_helpdesk_comments_by_issue_id,
    db_get_helpdesk_issue_by_id,
    db_get_helpdesk_issues_by_user_id,
    db_get_all_helpdesk_issues,
    db_get_all_helpdesk_issues_count,
    db_assign_helpdesk_issue,
    db_get_issue_statuses,
    db_get_issue_categories,
    db_update_issue_status,
    db_drop_issue_assignment,
)

from app.repositories.user_repository import db_get_helpdesk_staff


@app.get("/helpdesk/my-issues")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def my_issues():
    user_id = session["user_id"]
    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    issues = db_get_helpdesk_issues_by_user_id(
        user_id, current_page=current_page, page_size=page_size
    )
    total_issues = db_get_helpdesk_issues_count_by_user_id(user_id)
    total_pages = (total_issues + page_size - 1) // page_size if page_size else 1
    return render_template(
        "helpdesk/my-issues.html",
        issues=issues,
        current_page=current_page,
        page_size=page_size,
        total_pages=total_pages,
    )


@app.post("/helpdesk/add_issue")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def add_issue():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    category = request.form.get("category", "")

    print(category)

    if not title:
        flash("Title cannot be empty.", "warning")
        return redirect(url_for("my_issues"))
    if not content:
        flash("Content cannot be empty.", "warning")
        return redirect(url_for("my_issues"))
    if not category:
        flash("Category cannot be empty.", "warning")
        return redirect(url_for("my_issues"))

    try:
        user_id = session["user_id"]
        db_add_helpdesk_issue(title, category, content, "New", user_id)
        flash("Ticket has been added successfully.", "success")
    except:
        flash("Something went wrong. Please try again.", "danger")

    return redirect(url_for("my_issues"))


@app.get("/helpdesk/issues/<int:issue_id>")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def view_issue(issue_id):
    user_id = session["user_id"]
    staff_list = db_get_helpdesk_staff()
    # Filter out the current user
    filtered_staff_list = tuple(
        staff for staff in staff_list if staff.get("user_id") != user_id
    )
    issue = db_get_helpdesk_issue_by_id(issue_id)

    # First check if the issue exists
    if not issue:
        flash("Ticket not found.", "danger")
        return redirect(url_for("my_issues"))

    # Then check if user has permission to view this issue
    is_support_role = session["role"] in ["editor", "supporttech", "admin"]
    is_issue_owner = issue["user_id"] == user_id

    if not (is_issue_owner or is_support_role):
        flash("You do not have permission to view this ticket.", "danger")
        return redirect(url_for("my_issues"))

    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)

    # Get comments and count
    comments = db_get_helpdesk_comments_by_issue_id(
        issue_id, page=current_page, per_page=page_size
    )
    total_comments = db_get_helpdesk_comments_count_by_issue_id(issue_id)
    total_pages = (total_comments + page_size - 1) // page_size if page_size else 1

    # Check if current user is the owner (assigned_to) of the issue
    is_owner = issue["assigned_to"] == user_id

    return render_template(
        "helpdesk/view_issue.html",
        issue=issue,
        comments=comments,
        current_page=current_page,
        page_size=page_size,
        total_pages=total_pages,
        is_owner=is_owner,
        staff_list=filtered_staff_list
    )


@app.post("/helpdesk/issues/<int:issue_id>/comments")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def add_issue_comment(issue_id):
    user_id = session["user_id"]
    comment_content = request.form.get("comment", "").strip()
    if not comment_content:
        flash("Comment cannot be empty.", "warning")
        return redirect(url_for("view_issue", issue_id=issue_id))

    issue = db_get_helpdesk_issue_by_id(issue_id)
    if not issue:
        flash("Ticket not found.", "danger")
        return redirect(url_for("my_issues"))

    # Check if the issue is resolved
    if issue["status"] == "Resolved":
        flash("You cannot comment on a resolved ticket.", "warning")
        return redirect(url_for("view_issue", issue_id=issue_id))

    # Check if the user is the creator of the issue or the assigned owner
    is_creator = issue["user_id"] == user_id
    is_owner = issue["assigned_to"] == user_id

    if not is_creator and not is_owner:
        flash("You do not have permission to comment on this ticket.", "danger")
        return redirect(url_for("view_issue", issue_id=issue_id))

    try:
        db_add_helpdesk_comment(issue_id, user_id, comment_content)
        flash("Comment has been added.", "success")
    except:
        flash("Failed to add comment.", "danger")
    return redirect(url_for("view_issue", issue_id=issue_id))


@app.get("/helpdesk/queue")
@login_required(role=["editor", "admin", "supporttech"])
def helpdesk_queue():
    """View for support staff to see all helpdesk tickets"""
    status_filter = request.args.get("status", "All")
    category_filter = request.args.get("category", "All")
    premium_filter = request.args.get("premium", "All")
    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)

    issues = db_get_all_helpdesk_issues(
        status_filter=status_filter if status_filter != "All" else None,
        category_filter=category_filter if category_filter != "All" else None,
        premium_filter=premium_filter if premium_filter != "All" else None,
        current_page=current_page,
        page_size=page_size,
    )

    total_issues = db_get_all_helpdesk_issues_count(
        status_filter=status_filter if status_filter != "All" else None,
        category_filter=category_filter if category_filter != "All" else None,
        premium_filter=premium_filter if premium_filter != "All" else None,
    )

    total_pages = (total_issues + page_size - 1) // page_size if page_size else 1
    statuses = ["All"] + db_get_issue_statuses()
    categories = ["All"] + db_get_issue_categories()

    return render_template(
        "helpdesk/queue.html",
        issues=issues,
        current_page=current_page,
        page_size=page_size,
        total_pages=total_pages,
        status_filter=status_filter,
        statuses=statuses,
        category_filter=category_filter,
        premium_filter=premium_filter,
        categories=categories,
        now=datetime.now(),
    )


@app.post("/helpdesk/issues/<int:issue_id>/assign")
@login_required(role=["editor", "admin", "supporttech"])
def assign_issue(issue_id):
    """Assign a helpdesk issue to the current user"""
    staff_id = request.form.get('staff_id')
    user_id = staff_id if staff_id else session["user_id"]

    try:
        success = db_assign_helpdesk_issue(issue_id, user_id)
        if success:
            if staff_id:
                flash("Ticket has been assigned successfully.", "success")
            else:
                flash("Ticket has been assigned to you successfully.", "success")
        else:
            flash(
                "Failed to assign ticket. It may not exist or already be assigned.",
                "warning",
            )
    except Exception as e:
        flash(f"Error assigning ticket: {str(e)}", "danger")

    # Redirect back to the issue view page instead of the queue
    return redirect(url_for("view_issue", issue_id=issue_id))


@app.get("/helpdesk/admin")
@login_required(role=["editor", "admin", "supporttech"])
def helpdesk_admin():
    """Admin page for helpdesk management"""
    return render_template("helpdesk/admin.html")


@app.post("/helpdesk/issues/<int:issue_id>/delete")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def user_delete_own_issue(issue_id):
    """Soft delete by user, update issue status to delete, hide from user but visible for admins."""
    user_id = session["user_id"]
    issue = db_get_helpdesk_issue_by_id(issue_id)
    if not issue or issue["user_id"] != user_id:
        flash("Ticket not found.", "danger")
        return redirect(url_for("my_issues"))

    try:
        db_update_issue_status(issue_id, "Delete")
        flash("Ticket has been deleted.", "success")
    except:
        flash("Failed to delete ticket.", "danger")

    return redirect(url_for("my_issues"))


@app.post("/helpdesk/issues/<int:issue_id>/update-status")
@login_required(role=["editor", "admin", "supporttech"])
def update_issue_status(issue_id):
    """Update the status of an issue."""
    user_id = session["user_id"]
    new_status = request.form.get("status", "").strip()

    # Validate the new status
    if new_status not in ["Open", "Stalled", "Resolved"]:
        flash("Invalid status selected.", "danger")
        return redirect(url_for("view_issue", issue_id=issue_id))

    # Get the issue
    issue = db_get_helpdesk_issue_by_id(issue_id)
    if not issue:
        flash("Ticket not found.", "danger")
        return redirect(url_for("helpdesk_queue"))

    # Check if user is the owner of the issue
    is_owner = issue["assigned_to"] == user_id

    # Check if the issue is already in "New" status and trying to set back to "New"
    if issue["status"] != "New" and new_status == "New":
        flash(
            "Tickets cannot be returned to 'New' status after processing.",
            "warning",
        )
        return redirect(url_for("view_issue", issue_id=issue_id))

    # Handle permissions
    if not is_owner:
        # If not the owner, the user can assign it to themselves
        assign_to_me = request.form.get("assign_to_me", "").strip().lower() == "true"
        if assign_to_me:
            success = db_assign_helpdesk_issue(issue_id, user_id)
            if not success:
                flash("Failed to assign the ticket to you.", "danger")
                return redirect(url_for("view_issue", issue_id=issue_id))
            flash("Ticket has been assigned to you successfully.", "success")
        else:
            flash("Only assigned users can update the ticket status.", "warning")
            return redirect(url_for("view_issue", issue_id=issue_id))

    # Update the status
    try:
        db_update_issue_status(issue_id, new_status)
        flash(f"Ticket status updated to '{new_status}'.", "success")
    except Exception as e:
        flash(f"Failed to update ticket status: {str(e)}", "danger")

    return redirect(url_for("view_issue", issue_id=issue_id))


@app.post("/helpdesk/issues/<int:issue_id>/drop")
@login_required(role=["editor", "admin", "supporttech"])
def drop_issue(issue_id):
    """Drop ownership of an issue, setting it back to New status and removing assignment."""
    user_id = session["user_id"]

    # Get the issue
    issue = db_get_helpdesk_issue_by_id(issue_id)
    if not issue:
        flash("Ticket not found.", "danger")
        return redirect(url_for("helpdesk_queue"))

    # Check if user is the owner of the issue
    is_owner = issue["assigned_to"] == user_id

    if not is_owner:
        flash("You can only drop tickets assigned to you.", "warning")
        return redirect(url_for("view_issue", issue_id=issue_id))

    # Drop the issue
    try:
        success = db_drop_issue_assignment(issue_id)
        if success:
            flash(
                "Ticket has been dropped and is now available for others to take.",
                "success",
            )
        else:
            flash("Failed to drop the ticket. It may not exist.", "warning")
    except Exception as e:
        flash(f"Error dropping ticket: {str(e)}", "danger")

    return redirect(url_for("view_issue", issue_id=issue_id))
