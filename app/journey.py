from flask import flash, redirect, request, session, url_for, render_template, g
from app import app
import os
from app.achievement import check_achieved
from app.auth import login_required
from werkzeug.utils import secure_filename

from datetime import datetime

from app.repositories.announcement_repository import db_get_announcements
from app.repositories.community_repository import db_get_follow_by_followable
from app.repositories.event_comment_repository import db_get_user_event_reaction
from app.repositories.journey_repository import (
    db_add_new_journey,
    db_delete_journey,
    db_edit_my_journey,
    db_get_event_by_event_id,
    db_get_event_photos_by_event_id,
    db_get_events_by_journey_id,
    db_get_hidden_journeys,
    db_get_hidden_journeys_count,
    db_get_journey_by_journey_id,
    db_get_journeys_by_user_id,
    db_get_journeys_count_by_user_id,
    db_get_location_options,
    db_get_public_journeys,
    db_get_public_journeys_count,
    db_get_published_journeys,
    db_get_published_journeys_count,
    db_get_user_id_by_journey_id,
    db_remove_journey_photo,
    db_save_journey_photo,
    db_search_public_journey,
    db_search_public_journeys_count,
    db_set_journey_visibility,
    db_update_event,
    db_update_event_location_by_editor_admin,
    db_update_journey_title_and_description,
    db_create_first_viewer,
)
from app.repositories.subscription_repository import db_have_active_subscription
from app.repositories.user_repository import db_get_user_by_id, db_update_user_status


status_badges_mapping = {
    "private": "warning",
    "public": "success",
    "published": "primary",
}


def allowed_image(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.get("/")
def root():
    """Root endpoint (/)
    Redirects unlogged-in users to homepage
    Redirects logged-in users to public journeys page.
    """
    # Get inputs
    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 8, type=int)

    journeys = db_get_published_journeys("user_id" in session, current_page, page_size)
    total_journeys_count = db_get_published_journeys_count("user_id" in session)

    total_pages = (total_journeys_count + page_size - 1) // page_size

    return render_template(
        "homepage.html",
        journeys=journeys,
        current_page=current_page,
        total_pages=total_pages,
    )


@app.route("/journeys", methods=["GET", "POST"])
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def journeys():
    # Get inputs
    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 8, type=int)

    keyword = request.args.get("search")
    if request.method == "POST":
        keyword = request.form.get("search", "")
    # if search by keywords
    if keyword:
        journeys = db_search_public_journey(keyword, current_page, page_size)
        total_issues_count = db_search_public_journeys_count(keyword)
    # else display all public journeys
    else:
        journeys = db_get_public_journeys(current_page, page_size)
        total_issues_count = db_get_public_journeys_count()

    total_pages = (total_issues_count + page_size - 1) // page_size

    # Get all new announcements
    announcements = db_get_announcements(True)
    return render_template(
        "journey/journeys.html",
        journeys=journeys,
        current_page=current_page,
        total_pages=total_pages,
        keyword=keyword,
        announcements=announcements,
    )


# show hidden journeys for editors and admins
@app.get("/hidden-journeys")
@login_required(role=["editor", "admin", "supporttech"])
def hidden_journeys():
    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 8, type=int)
    journeys = db_get_hidden_journeys(current_page, page_size)
    total_issues_count = db_get_hidden_journeys_count()
    total_pages = (total_issues_count + page_size - 1) // page_size
    return render_template(
        "journey/hidden-journeys.html",
        journeys=journeys,
        current_page=current_page,
        total_pages=total_pages,
    )


@app.get("/my-journeys")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def my_journeys():
    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 8, type=int)
    journeys = db_get_journeys_by_user_id(session["user_id"], current_page, page_size)
    total_issues_count = db_get_journeys_count_by_user_id(session["user_id"])
    total_pages = (total_issues_count + page_size - 1) // page_size
    return render_template(
        "journey/my-journeys.html",
        journeys=journeys,
        current_page=current_page,
        total_pages=total_pages,
        status_badges_mapping=status_badges_mapping,
    )


@app.route("/my-journeys/new", methods=["GET", "POST"])
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def new_journey():
    user_id = session.get("user_id", "")
    user = db_get_user_by_id(user_id)
    # initial error message
    title_error = None
    description_error = None
    startDate_error = None
    publicity_error = None
    if request.method == "POST":
        try:
            # get inputs
            title = request.form["title"]
            description = request.form["description"]
            startDate = request.form["startDate"]
            status = request.form["status"]
            action = request.form["action"]
            # validation
            if title:
                if len(title) > 100:
                    title_error = "Your title cannot exceed 100 characters."
            else:
                title_error = "Title is required."
            if description:
                if len(description) > 1000:
                    description_error = (
                        "Your description cannot exceed 1000 characters."
                    )
            else:
                description_error = "Description is required."
            if not startDate:
                startDate_error = "Please choose a start date."

            # Check if the user is allowed to share public journeys
            if user["status"] != "active" and status != "private":
                publicity_error = "You cannot share this journey publicly."
            # Check if the user is allowed to publish journeys
            if status == "published" and not g.premium:
                publicity_error = "You must have a subscription to access premium feature."

            # when user submit
            if action == "submit" and not (
                title_error or description_error or startDate_error or publicity_error
            ):
                # Check achievement
                if status == "public" and check_achieved("first_public_journey", session["user_id"]):
                    flash("You have earned an achievement for sharing your first public journey!", "primary")
                elif check_achieved("first_journey", session["user_id"]):
                    flash("You You have earned an achievement for creating your first journey!", "primary")
                if status == "published" and check_achieved("first_published_journey", session["user_id"]):
                    flash("You have earned an achievement for sharing your first published journey!", "primary")

                db_add_new_journey(
                    session["user_id"],
                    title,
                    description,
                    startDate,
                    status,
                    datetime.now(),
                )
                flash("Your journey has been created.", "success")

                return redirect(url_for("my_journeys"))
        except Exception as e:
            # Print it to the console for debugging
            print(f"Error occurred: {e}")
            flash("An error occurred while processing your request. Please try again.")
        return render_template(
            "journey/new.html",
            title=title,
            description=description,
            startDate=startDate,
            status=status,
            title_error=title_error,
            description_error=description_error,
            startDate_error=startDate_error,
            publicity_error=publicity_error,
        )
    return render_template("journey/new.html")


# Edit my journey
@app.get("/journeys/<int:journey_id>/edit")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def view_my_journey(journey_id):
    journey = db_get_journey_by_journey_id(journey_id)
    # Check if the journey exists
    if not journey:
        return (
            render_template(
                "error.html",
                error_message="Journey not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    # Check if the user is the owner of the journey
    if session["user_id"] != journey["user_id"]:
        return (
            render_template(
                "error.html",
                error_message="You are not the owner of this journey",
                home_url=url_for("journeys"),
            ),
            403,
        )
    return render_template(
        "journey/edit-my-journey.html",
        journey_id=journey_id,
        title=journey["title"],
        description=journey["description"],
        startDate=journey["start_date"],
        status=journey["status"],
    )


@app.post("/journeys/<int:journey_id>/edit")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def edit_my_journey(journey_id):
    user_id = session.get("user_id")
    user = db_get_user_by_id(user_id)

    # Initial error message
    title_error = None
    description_error = None
    startDate_error = None
    title = request.form["title"]
    description = request.form["description"]
    startDate = request.form["startDate"]
    status = request.form["status"]

    # Validation
    if title:
        if len(title) > 100:
            title_error = "Your title cannot exceed 100 characters."
    else:
        title_error = "Title is required."
    if description:
        if len(description) > 1000:
            description_error = "Your description cannot exceed 1000 characters."
    else:
        description_error = "Description is required."
    if not startDate:
        startDate_error = "Please choose a start date."

    if title_error or description_error or startDate_error:
        return render_template(
            "journey/edit-my-journey.html",
            journey_id=journey_id,
            title=title,
            description=description,
            startDate=startDate,
            title_error=title_error,
            description_error=description_error,
            startDate_error=startDate_error,
        )
    # Check if the user is allowed to share public journeys
    if user["status"] != "active" and status != "private":
        flash(f"You cannot share this journey publicly.", "danger")
        return redirect(url_for("edit_my_journey", journey_id=journey_id))
    # Check if the user is allowed to publish journeys
    if status == "published" and not g.premium:
        flash(f"You must have a subscription to access premium feature.", "danger")
        return redirect(url_for("edit_my_journey", journey_id=journey_id))

    try:
        journey = db_get_journey_by_journey_id(journey_id)
        # Check if the journey exists
        if not journey:
            return (
                render_template(
                    "error.html",
                    error_message="Journey not found",
                    home_url=url_for("journeys"),
                ),
                404,
            )
        # Check if the user is the owner of the journey
        if session["user_id"] != journey["user_id"]:
            return (
                render_template(
                    "error.html",
                    error_message="You are not the owner of this journey",
                    home_url=url_for("journeys"),
                ),
                403,
            )
        db_edit_my_journey(journey_id, title, description, startDate, status)
        # Check achievement
        if status == "public" and check_achieved("first_public_journey", session["user_id"]):
            flash("You have earned an achievement for sharing your first public journey!", "primary")
        if status == "published" and check_achieved("first_published_journey", session["user_id"]):
            flash("You have earned an achievement for sharing your first published journey!", "primary")
        flash("The journey has been updated successfully.", "success")
    except Exception as e:
        flash(f"Failed to update journey: {str(e)}", "danger")
    return redirect(url_for("journey", journey_id=journey_id))


@app.get("/journeys/<int:journey_id>")
def journey(journey_id):
    user_id = session.get("user_id", "")
    journey = db_get_journey_by_journey_id(journey_id)
    have_active_subscription = db_have_active_subscription(journey["user_id"])
    author = db_get_user_by_id(journey["user_id"])

    # Check if the journey exists
    if not journey:
        return (
            render_template(
                "error.html",
                error_message="Journey not found",
                home_url=url_for("journeys"),
            ),
            404,
        )

    journey["start_date"] = journey["start_date"].strftime("%d/%m/%Y")

    events = db_get_events_by_journey_id(journey_id)
    events_list = []
    for event in events:
        existing_reaction = db_get_user_event_reaction(user_id, event["event_id"])
        # Fetch list of photo paths for the event
        photos = db_get_event_photos_by_event_id(
            event["event_id"]
        )
        # Unsubscribe user can only display first photo
        if photos and not have_active_subscription and not (
            author["role"] in ["editor", "admin", "supporttech", "moderator"]
        ):
            photos = (photos[0],)
        events_list.append(
            {
                "event_id": event["event_id"],
                "title": event["title"],
                "description": event["description"],
                "start_at": event["start_datetime"].strftime("%d/%m/%Y %H:%M:%S"),
                "end_at": (
                    event["end_datetime"].strftime("%d/%m/%Y %H:%M:%S")
                    if event["end_datetime"]
                    else ""
                ),
                "photos": photos,
                "comments_count": event["comments_count"],
                "location": event["location_name"],
                "like_count": event["like_count"],
                "is_liked": True if existing_reaction else False,
                "location_id": event["location_id"]
            }
        )
    follow = db_get_follow_by_followable(user_id, "journey", journey["journey_id"])
    followed = follow != None

    # Users can view their own journey
    if user_id == journey["user_id"]:
        return render_template(
            "journey/journey.html",
            journey=journey,
            events=events_list,
            is_my_journey=True,
            can_edit=False,
            author=author,
            status_badges_mapping=status_badges_mapping,
            followed=followed,
        )

    # No one can view private journey if not owner
    if journey["status"] == "private":
        return render_template(
            "error.html",
            error_message="This journey is private",
            home_url=url_for("journeys"),
        )

    # Staff can view any non private journey
    if "role" in session and session["role"] in ["editor", "admin", "supporttech"]:
        #check first viewer achievement
        if journey["first_viewer_id"] is None and journey["user_id"] != user_id:
            db_create_first_viewer(journey_id, user_id)
            if check_achieved("first_viewer", session["user_id"]):
                flash("You have earned an achievement for being the first viewer on a shared journey!", "primary")
        return render_template(
            "journey/journey.html",
            journey=journey,
            events=events_list,
            is_my_journey=False,
            can_edit=True,
            author=author,
            status_badges_mapping=status_badges_mapping,
            followed=followed,
        )

    # No one else can view hidden journey
    if journey["is_hidden"]:
        return render_template(
            "error.html",
            error_message="This journey is unavailable",
            home_url=url_for("journeys"),
        )

    # logged-in user can view public and published journey
    if journey["status"] in ["public", "published"] and "user_id" in session:
        #check first viewer achievement
        if journey["first_viewer_id"] is None and journey["user_id"] != user_id:
            db_create_first_viewer(journey_id, user_id)
            if check_achieved("first_viewer", session["user_id"]):
                flash("You have earned an achievement for being the first viewer on a shared journey!", "primary")
        return render_template(
            "journey/journey.html",
            journey=journey,
            events=events_list,
            is_my_journey=False,
            can_edit=False,
            author=author,
            status_badges_mapping=status_badges_mapping,
            followed=followed,
        )

    # anyone can view published journey if the owner has premium feature access
    have_active_subscription = db_have_active_subscription(author["user_id"])
    if journey["status"] == "published" and (
        have_active_subscription or author["role"] in ["editor", "admin", "moderator", "supporttech"]
    ):
        return render_template(
            "journey/journey.html",
            journey=journey,
            events=events_list,
            is_my_journey=False,
            can_edit=False,
            author=author,
            status_badges_mapping=status_badges_mapping,
            followed=followed,
        )

    return render_template(
        "error.html",
        error_message="Journey not found",
        home_url=url_for("journeys"),
    )


@app.get("/journeys/public/<int:journey_id>/edit")
@login_required(role=["editor", "admin", "supporttech"])
def edit_public_journey(journey_id):
    journey = db_get_journey_by_journey_id(journey_id)
    # Check if the journey exists
    if not journey:
        return (
            render_template(
                "error.html",
                error_message="Journey not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    if journey["status"] == "private":
        return (
            render_template(
                "error.html",
                error_message="This journey is not public",
                home_url=url_for("journeys"),
            ),
            403,
        )
    return render_template(
        "journey/edit-public.html",
        journey_id=journey_id,
        title=journey["title"],
        description=journey["description"],
        status=journey["status"],
    )


@app.post("/journeys/public/<int:journey_id>/edit")
@login_required(role=["editor", "admin", "supporttech"])
def update_public_journey_title_and_description(journey_id):
    journey = db_get_journey_by_journey_id(journey_id)
    # Check if the journey exists
    if not journey:
        return (
            render_template(
                "error.html",
                error_message="Journey not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    if journey["status"] == "private":
        return (
            render_template(
                "error.html",
                error_message="This journey is not public",
                home_url=url_for("journeys"),
            ),
            403,
        )
    # Initial error message
    title_error = None
    description_error = None

    title = request.form.get("title")
    description = request.form.get("description")
    # Validation
    if title:
        if len(title) > 100:
            title_error = "Your title cannot exceed 100 characters."
    else:
        title_error = "Title is required."
    if description:
        if len(description) > 1000:
            description_error = "Your description cannot exceed 1000 characters."
    else:
        description_error = "Description is required."

    if title_error or description_error:
        return render_template(
            "journey/edit-public.html",
            journey_id=journey_id,
            title=title,
            description=description,
            title_error=title_error,
            description_error=description_error,
        )
    try:
        db_update_journey_title_and_description(journey_id, title, description)
        flash("The journey has been updated successfully.", "success")
    except Exception as e:
        flash(f"Failed to update journey: {str(e)}", "danger")
    return redirect(url_for("journey", journey_id=journey_id))


@app.post("/journeys/<int:journey_id>/delete")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def delete_journey(journey_id):
    journey = db_get_journey_by_journey_id(journey_id)
    if not journey:
        return (
            render_template(
                "error.html",
                error_message="Journey not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    if session["user_id"] != journey["user_id"]:
        return (
            render_template(
                "error.html",
                error_message="You are not the owner of this journey",
                home_url=url_for("journeys"),
            ),
            403,
        )
    try:
        db_delete_journey(journey_id)
        flash("The journey has been deleted.", "success")
    except Exception as e:
        flash(f"Failed to delete journey: {str(e)}", "danger")
    return redirect(url_for("my_journeys"))


@app.post("/journeys/<int:journey_id>/block")
@login_required(role=["editor", "admin", "supporttech"])
def block_user(journey_id):
    journey = db_get_journey_by_journey_id(journey_id)
    user = db_get_user_by_id(journey["user_id"])
    user_status = request.form.get("status")
    if user["status"] != "banned" or user["user_id"] != session.get("user_id", ""):
        try:
            db_update_user_status(journey["user_id"], user_status)
            flash(
                f"This user has been {'blocked' if user_status == 'blocked' else 'actived'}.",
                "success",
            )
            return redirect(url_for("journey", journey_id=journey_id))
        except Exception as e:
            flash(f"Failed to set user status: {str(e)}", "danger")
            return redirect(url_for("journey", journey_id=journey_id))
    return redirect(url_for("journey", journey_id=journey_id))


@app.post("/journeys/<int:journey_id>/visibility")
@login_required(role=["editor", "admin", "supporttech"])
def update_visibility(journey_id):
    journey = db_get_journey_by_journey_id(journey_id)
    # Check if the journey exists
    if not journey:
        return (
            render_template(
                "error.html",
                error_message="Journey not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    visibility = request.form.get("visibility")
    try:
        db_set_journey_visibility(journey_id, visibility == "hidden")

        flash(
            f"This journey has been set as {'hidden' if visibility == 'hidden' else 'visible'}.",
            "success",
        )
        return redirect(url_for("journey", journey_id=journey_id))
    except Exception as e:
        flash(f"Failed to update journey visibility: {str(e)}", "danger")
        return redirect(url_for("journey", journey_id=journey_id))


@app.get("/journeys/public/<int:journey_id>/event/<int:event_id>/edit")
@login_required(role=["editor", "admin", "supporttech"])
def edit_public_event(journey_id, event_id):
    journey = db_get_journey_by_journey_id(journey_id)
    # Check if the journey exists
    if not journey:
        return (
            render_template(
                "error.html",
                error_message="Journey not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    # Check if the journey is public
    if journey["status"] == "private":
        return (
            render_template(
                "error.html",
                error_message="This journey is not public",
                home_url=url_for("journeys"),
            ),
            403,
        )
    event = db_get_event_by_event_id(event_id)
    # Check if the event exists
    if not event:
        return (
            render_template(
                "error.html",
                error_message="Event not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    # Check if the event belongs to the journey
    if event["journey_id"] != journey_id:
        return (
            render_template(
                "error.html",
                error_message="This event does not belong to this journey",
                home_url=url_for("journeys"),
            ),
            403,
        )
    try:
        location_options = db_get_location_options(journey_id)
    except:
        return (
            render_template(
                "error.html",
                error_message="Something went wrong, please try again.",
                home_url=url_for("journey", journey_id=journey_id),
            ),
            403,
        )
    return render_template(
        "event/edit-public.html",
        event=event,
        journey_id=journey_id,
        my_locations=location_options[0],
        other_locations=location_options[1],
    )


@app.post("/journeys/public/<int:journey_id>/event/<int:event_id>/edit")
@login_required(role=["editor", "admin", "supporttech"])
def update_public_event(journey_id, event_id):
    journey = db_get_journey_by_journey_id(journey_id)
    # Check if the journey exists
    if not journey:
        return (
            render_template(
                "error.html",
                error_message="Journey not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    # Check if the journey is public
    if journey["status"] == "private":
        return (
            render_template(
                "error.html",
                error_message="This journey is not public",
                home_url=url_for("journeys"),
            ),
            403,
        )
    event = db_get_event_by_event_id(event_id)
    # Check if the event exists
    if not event:
        return (
            render_template(
                "error.html",
                error_message="Event not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    # Check if the event belongs to the journey
    if event["journey_id"] != journey_id:
        return (
            render_template(
                "error.html",
                error_message="This event does not belong to this journey",
                home_url=url_for("journeys"),
            ),
            403,
        )

    title = request.form.get("title").strip()
    description = request.form.get("description").strip()
    location = request.form.get("event-location", "").strip()

    # Check the title and description are not empty
    title_error = None
    description_error = None
    if not title:
        title_error = "Title is required."
    elif len(title) > 100:
        title_error = "Title cannot exceed 100 characters."
    if not description:
        description_error = "Description is required."
    elif len(description) > 1000:
        description_error = "Description cannot exceed 1000 characters."
    if title_error or description_error:
        try:
            location_options = db_get_location_options(journey_id)
        except:
            return (
                render_template(
                    "error.html",
                    error_message="Something went wrong, please try again.",
                    home_url=url_for("journey", journey_id=journey_id),
                ),
                403,
            )
        flash("Title and description are required", "warning")
        return render_template(
            "event/edit-public.html",
            event=event,
            journey_id=journey_id,
            my_locations=location_options[0],
            other_locations=location_options[1],
            title_error=title_error,
            description_error=description_error,
        )
    try:
        db_update_event(event_id, title, description)
        db_update_event_location_by_editor_admin(
            event_id, event["location_name"], location
        )
        flash("The event has been updated successfully", "success")
    except Exception as e:
        flash(f"Failed to update event: {str(e)}", "danger")
    return redirect(url_for("journey", journey_id=journey_id))


def can_add_photo_to_journey(journey_id):
    journey = db_get_journey_by_journey_id(journey_id)
    have_active_subscription = db_have_active_subscription(journey["user_id"])

    if not have_active_subscription and not (
        "role" in session and session["role"] != "traveller"
    ):
        flash("You are not allowed to add photo to this journey.", "warning")
        return [False, url_for("journey", journey_id=journey["journey_id"])]

    if not journey:
        flash("Journey not found", "warning")
        return [False, url_for("my_journeys")]

    if journey["user_id"] != session["user_id"]:
        flash("You are not allowed to add photo to this journey.", "warning")
        return [False, url_for("journey", journey_id=journey["journey_id"])]

    return [True, url_for("journey", journey_id=journey["journey_id"])]


@app.get("/journey/<int:journey_id>/photos/add")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def add_photo_form(journey_id):
    can_add_photo, redirect_url = can_add_photo_to_journey(journey_id)
    if not can_add_photo:
        return redirect(redirect_url)

    journey = db_get_journey_by_journey_id(journey_id)
    return render_template(
        "journey/add_photo_journey.html", journey_id=journey_id, journey=journey
    )


@app.post("/journey/<int:journey_id>/photos/add")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def add_photo_to_journey(journey_id):
    can_add_photo, redirect_url = can_add_photo_to_journey(journey_id)
    if not can_add_photo:
        return redirect(redirect_url)

    file = request.files["journey_photo"]
    if not file or not file.filename:
        flash("No file selected.", "warning")
        return redirect(redirect_url)
    if not allowed_image(file.filename):
        flash("File type not allowed.", "warning")
        return redirect(redirect_url)

    filename = secure_filename(file.filename)
    filename = "journey_photo_" + str(journey_id) + os.path.splitext(filename)[1]

    try:
        file.save(os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename))
        db_save_journey_photo(filename, journey_id)
        # Check whether user has added 5 journey cover images. If so display the achievement message
        achievement = check_achieved("five_journeys_with_cover_image", session["user_id"])
        if achievement:
            flash("You have earned an achievement for adding 5 journey cover images!", "primary")
        flash("Photo has been added successfully.", "success")
    except:
        flash("Something went wrong, please try again.", "danger")

    return redirect(redirect_url)


def check_user_id_against_journey(user_id, journey_id):

    if not user_id == session["user_id"]:
        return [False, "Not journey of current user."]
    return [True, url_for("journey", journey_id=journey_id)]


@app.post("/journey/<int:journey_id>/photos/remove")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def remove_photo(journey_id):
    try:
        journey_id = request.form.get("journey_id", None)
        journey = db_get_journey_by_journey_id(journey_id)
        user_id = db_get_user_id_by_journey_id(journey_id)
        can_edit_journey, message = check_user_id_against_journey(user_id, journey_id)
        if not can_edit_journey:
            flash(message, "warning")
            return (
                render_template(
                    "error.html",
                    error_message=message,
                    home_url=url_for("journey", journey_id=journey_id),
                ),
                403,
            )
        photo_image = journey["photo"]
        if photo_image:
            image_path = os.path.join(
                app.root_path, app.config["UPLOAD_FOLDER"], photo_image
            )
            if os.path.exists(image_path):
                os.remove(image_path)
        db_remove_journey_photo(journey_id)
        flash("Journey photo has been removed.", "success")
        return "Journey photo removed successfully."
    except:
        flash("Something went wrong, please try again.", "danger")
        return redirect(url_for("journey", journey_id=journey_id))
