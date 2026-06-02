from flask import render_template, request, redirect, url_for, session, flash
from app import app
from app.achievement import check_seven_days_journey_achieved
from app.auth import login_required
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
from app.achievement import check_achieved
from app.repositories.event_comment_repository import (
    db_add_comment,
    db_add_event_comment_reaction,
    db_add_user_event_reaction,
    db_create_report,
    db_delete_reaction,
    db_get_comment,
    db_get_event_comment_reaction,
    db_get_event_comments,
    db_get_event_comments_count_by_event_id,
    db_get_user_comments_reactions,
    db_get_user_event_reaction,
    db_update_comment_dislike_count,
    db_update_comment_like_count,
    db_update_event_comment_reaction,
    db_update_event_like_count,
    db_get_most_comments_event_by_user_id,
    db_get_most_likes_event_by_user_id,
)
from app.repositories.community_repository import (
    db_get_location_by_user_id,
)
from app.repositories.journey_repository import (
    db_add_events,
    db_delete_event,
    db_delete_event_photos,
    db_edit_event,
    db_get_event_by_event_id,
    db_get_journey_by_journey_id,
    db_get_location_options,
    db_get_user_id_by_event_id,
    db_get_user_id_by_journey_id,
    db_save_event_photo
)
from app.repositories.subscription_repository import db_have_active_subscription
from app.repositories.user_repository import db_event_photo_exists
from app.repositories.achievement_repository import db_get_achievement


def check_event_form(
    title=None,
    description=None,
    start_date=None,
    start_time=None,
    end_date=None,
    end_time=None,
    location=None,
    journey_start_date=None
):
    title_error = None
    description_error = None
    start_date_error = None
    start_time_error = None
    end_date_error = None
    end_time_error = None
    location_error = None
    form_error = {}
    if not title:
        title_error = "Title is required."
    elif len(title) > 100:
        title_error = "Your title cannot exceed 100 characters."
    form_error.update({"title_error": title_error})
    if not description:
        description_error = "Description is required."
    elif len(description) > 1000:
        description_error = "Your description cannot exceed 1000 characters."
    form_error.update({"description_error": description_error})
    if not start_date:
        start_date_error = "Start date is required."
    else:
        start_datetime = datetime.fromisoformat(f"{start_date} {start_time}:00")
        journey_start_datetime = datetime.fromisoformat(journey_start_date)
        if start_datetime < journey_start_datetime:
            start_date_error = "Start date should be later than the journey start date."
    form_error.update({"start_date_error": start_date_error})
    if not start_time:
        start_time_error = "Start time is required."
    form_error.update({"start_time_error": start_time_error})

    if end_date and not end_time:
        end_time_error = "End time is required."

    elif end_time and not end_date:
        end_date_error = "End date is required."
    elif start_date and start_time and end_date and end_time:
        start_datetime = datetime.fromisoformat(f"{start_date} {start_time}:00")
        end_datetime = datetime.fromisoformat(f"{end_date} {end_time}:00")
        if (end_datetime - start_datetime) < timedelta(days=0):
            end_date_error = "End date time should be later than start date and time."
            end_time_error = "End date time should be later than start date and time."
    form_error.update({"end_date_error": end_date_error})
    form_error.update({"end_time_error": end_time_error})
    if location and len(location) > 255:
        location_error = "Your location cannot exceed 255 characters."
    form_error.update({"location_error": location_error})

    return form_error


def allowed_image(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.get("/journeys/<int:journey_id>/events/new")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def new_event_form(journey_id):
    try:
        user_id = db_get_user_id_by_journey_id(journey_id)
        message = None
        if not user_id:
            message = "No journey found.", "warning"
        if not user_id == session["user_id"]:
            message = "You do not have access to this journey.."
        if message:
            return (
                render_template(
                    "error.html",
                    error_message=message,
                    home_url=url_for("my_journeys"),
                ),
                403,
            )
        location_options = db_get_location_options(journey_id)
        return render_template(
            "event/new.html",
            journey_id=journey_id,
            my_locations=location_options[0],
            other_locations=location_options[1],
        )
    except:
        flash("Something went wrong, please try again.", "danger")
        return redirect(url_for("journey", journey_id=journey_id))


@app.post("/journeys/<int:journey_id>/events")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def add_event(journey_id):
    try:
        user_id = db_get_user_id_by_journey_id(journey_id)
        journey = db_get_journey_by_journey_id(journey_id)
        journey_start_date = None
        if journey:
            journey_start_date = str(journey["start_date"])
        message = None
        if not user_id:
            message = "No journey found.", "warning"
        if not user_id == session["user_id"]:
            message = "You do not have access to this journey.."
        if not journey_start_date:
            message = "Please provide a journey start date.", "warning"
        if message:
            return (
                render_template(
                    "error.html",
                    error_message=message,
                    home_url=url_for("my_journeys"),
                ),
                403,
            )
    except:
        return (
            render_template(
                "error.html",
                error_message="Something went wrong, please try again.",
                home_url=url_for("journey", journey_id=journey_id),
            ),
            403,
        )

    title = request.form.get("event-title", "").strip()
    description = request.form.get("event-description", "").strip()
    start_date = request.form.get("event-start-date", None)
    start_time = request.form.get("event-start-time", None)
    end_date = request.form.get("event-end-date", None)
    end_time = request.form.get("event-end-time", None)
    location = request.form.get("event-location", "").strip()

    form_error = check_event_form(
        title=title,
        description=description,
        start_date=start_date,
        start_time=start_time,
        end_date=end_date,
        end_time=end_time,
        location=location,
        journey_start_date =journey_start_date
    )
    if (
        form_error["title_error"]
        or form_error["description_error"]
        or form_error["start_date_error"]
        or form_error["start_time_error"]
        or form_error["end_date_error"]
        or form_error["end_time_error"]
        or form_error["location_error"]
    ):
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
        location_options = db_get_location_options(journey_id)
        return render_template(
            "event/new.html",
            journey_id=journey_id,
            title=title,
            description=description,
            start_date=start_date,
            start_time=start_time,
            end_date=end_date,
            end_time=end_time,
            location=location,
            title_error=form_error["title_error"],
            description_error=form_error["description_error"],
            start_date_error=form_error["start_date_error"],
            start_time_error=form_error["start_time_error"],
            end_date_error=form_error["end_date_error"],
            end_time_error=form_error["end_time_error"],
            location_error=form_error["location_error"],
            my_locations=location_options[0],
            other_locations=location_options[1],
        )

    try:
        start_datetime = datetime.fromisoformat(f"{start_date} {start_time}:00")
        end_datetime = None
        if end_date and end_time:
            end_datetime = datetime.fromisoformat(f"{end_date} {end_time}:00")
        event_id, is_new_location_for_user = db_add_events(
            journey_id,
            title,
            description,
            start_datetime,
            end_datetime=end_datetime,
            location=location,
            user_id=session["user_id"]
        )
        if check_seven_days_journey_achieved(journey_id):
            flash("You have earned an achievement for a journey lasting 7 days!", "primary")
        flash("Event has been added successfully.", "success")
        # Check achievement
        if is_new_location_for_user:
            achievement = check_achieved("five_locations", session["user_id"])
            if achievement:
                flash("You have earned an achievement for visiting 5 different places!", "primary")
        if check_achieved("first_event", session["user_id"]):
            flash("You have earned an achievement for creating your first event!", "primary")
        return redirect(url_for("journey", journey_id=journey_id))
    except Exception as e:
        print(e)
        flash("Something went wrong, please try again.", "danger")
        return (
            render_template(
                "error.html",
                error_message="Something went wrong, please try again.",
                home_url=url_for("journey", journey_id=journey_id),
            ),
            403,
        )


def can_add_photo_to_event(event_id):
    event = db_get_event_by_event_id(event_id)
    if not event:
        flash("Event not found", "warning")
        return [False, url_for("my_journeys")]
    journey = db_get_journey_by_journey_id(event["journey_id"])
    if not journey:
        flash("Journey not found", "warning")
        return [False, url_for("my_journeys")]

    if journey["user_id"] != session["user_id"]:
        flash("You are not allowed to add photo to this event.", "warning")
        return [False, url_for("journey", journey_id=journey["journey_id"])]

    return [True, url_for("journey", journey_id=journey["journey_id"])]


def check_user_id_journey_id_against_event(user_id, journey_id, event):

    if not event:
        return [False, "No event found."]
    if not user_id == session["user_id"]:
        return [False, "Not event of current user."]
    if not int(journey_id) == event["journey_id"]:
        return [False, "Not event of current journey."]
    return [True, url_for("journey", journey_id=event["journey_id"])]


@app.get("/events/<int:event_id>/edit")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def edit_event_form(event_id):
    try:
        event = db_get_event_by_event_id(event_id)
        user_id = db_get_user_id_by_event_id(event_id)
        journey_id = request.args.get("journey_id", None)
        can_edit_event, message = check_user_id_journey_id_against_event(
            user_id, journey_id, event
        )
        if not can_edit_event:
            flash(message, "warning")
            return (
                render_template(
                    "error.html",
                    error_message=message,
                    home_url=url_for("journey", journey_id=journey_id),
                ),
                403,
            )
        location_options = db_get_location_options(journey_id)
        end_date = ""
        end_time = ""
        location = ""
        if event["end_datetime"]:
            end_date = event["end_datetime"].strftime("%Y-%m-%d")
            end_time = event["end_datetime"].strftime("%H:%M")
        if event["location_name"]:
            location = event["location_name"]
        return render_template(
            "event/new.html",
            event_id=event_id,
            journey_id=journey_id,
            title=event["title"],
            description=event["description"],
            start_date=event["start_datetime"].strftime("%Y-%m-%d"),
            start_time=event["start_datetime"].strftime("%H:%M"),
            end_date=end_date,
            end_time=end_time,
            location=location,
            my_locations=location_options[0],
            other_locations=location_options[1],
            form_title="Edit Event",
        )

    except:
        flash("Something went wrong, please try again.", "danger")
        return redirect(url_for("journey", journey_id=journey_id))


@app.post("/events/<int:event_id>/edit")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def edit_event(event_id):
    try:
        journey_id = request.form.get("journey_id", None)
        event = db_get_event_by_event_id(event_id)
        user_id = db_get_user_id_by_event_id(event_id)
        journey = db_get_journey_by_journey_id(journey_id)
        journey_start_date = None
        if journey:
            journey_start_date = str(journey["start_date"])
        can_edit_event, message = check_user_id_journey_id_against_event(
            user_id, journey_id, event
        )
        if not journey_start_date:
            message = "Please provide a journey start date.", "warning"
        if not can_edit_event:
            flash(message, "warning")
            return (
                render_template(
                    "error.html",
                    error_message=message,
                    home_url=url_for("journey", journey_id=journey_id),
                ),
                403,
            )

    except:
        return (
            render_template(
                "error.html",
                error_message="Something went wrong, please try again.",
                home_url=url_for("journey", journey_id=journey_id),
            ),
            403,
        )
    title = request.form.get("event-title", "").strip()
    description = request.form.get("event-description", "").strip()
    start_date = request.form.get("event-start-date", None)
    start_time = request.form.get("event-start-time", None)
    end_date = request.form.get("event-end-date", None)
    end_time = request.form.get("event-end-time", None)
    location = request.form.get("event-location", "").strip()
    form_error = check_event_form(
        title=title,
        description=description,
        start_date=start_date,
        start_time=start_time,
        end_date=end_date,
        end_time=end_time,
        location=location,
        journey_start_date =journey_start_date
    )
    if (
        form_error["title_error"]
        or form_error["description_error"]
        or form_error["start_date_error"]
        or form_error["start_time_error"]
        or form_error["end_date_error"]
        or form_error["end_time_error"]
        or form_error["location_error"]
    ):
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
            "event/new.html",
            event_id=event_id,
            journey_id=journey_id,
            title=title,
            description=description,
            start_date=start_date,
            start_time=start_time,
            end_date=end_date,
            end_time=end_time,
            location=location,
            title_error=form_error["title_error"],
            description_error=form_error["description_error"],
            start_date_error=form_error["start_date_error"],
            start_time_error=form_error["start_time_error"],
            end_date_error=form_error["end_date_error"],
            end_time_error=form_error["end_time_error"],
            location_error=form_error["location_error"],
            my_locations=location_options[0],
            other_locations=location_options[1],
            form_title="Edit Event",
        )

    try:
        start_datetime = datetime.fromisoformat(f"{start_date} {start_time}:00")
        end_datetime = None
        if end_date and end_time:
            end_datetime = datetime.fromisoformat(f"{end_date} {end_time}:00")
        is_new_location_for_user = db_edit_event(
            event_id,
            title,
            description,
            start_datetime,
            end_datetime=end_datetime,
            location=location,
            user_id=session["user_id"]
        )
        flash("Your changes have been saved successfully.", "success")

        # Check achievement
        if check_seven_days_journey_achieved(event["journey_id"]):
            flash("You have earned an achievement for a journey lasting 7 days!", "primary")
        if is_new_location_for_user:
            achievement = check_achieved("five_locations", session["user_id"])
            if achievement:
                flash("You have earned an achievement for visiting 5 different places!", "primary")

        return redirect(url_for("journey", journey_id=journey_id))
    except:
        return (
            render_template(
                "error.html",
                error_message="Something went wrong, please try again.",
                home_url=url_for("journey", journey_id=journey_id),
            ),
            403,
        )


@app.get("/events/<int:event_id>/delete")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def delete_event_modal(event_id):
    try:
        journey_id = request.args.get("journey_id", None)
        event = db_get_event_by_event_id(event_id)
        user_id = db_get_user_id_by_event_id(event_id)
        can_edit_event, message = check_user_id_journey_id_against_event(
            user_id, journey_id, event
        )
        if not can_edit_event:
            flash(message, "warning")
            return (
                render_template(
                    "error.html",
                    error_message=message,
                    home_url=url_for("journey", journey_id=journey_id),
                ),
                403,
            )
        return render_template(
            "event/delete_event.html",
            event_id=event_id,
            journey_id=journey_id,
            event=event,
        )
    except:
        flash("Something went wrong, please try again.", "danger")
        return redirect(url_for("journey", journey_id=journey_id))


@app.post("/events/<int:event_id>/delete")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def delete_event(event_id):

    try:
        journey_id = request.form.get("journey_id", None)
        event = db_get_event_by_event_id(event_id)
        user_id = db_get_user_id_by_event_id(event_id)
        can_edit_event, message = check_user_id_journey_id_against_event(
            user_id, journey_id, event
        )
        if not can_edit_event:
            flash(message, "warning")
            return (
                render_template(
                    "error.html",
                    error_message=message,
                    home_url=url_for("journey", journey_id=journey_id),
                ),
                403,
            )
        # photo_image = event["photo"]
        # if photo_image:
        #     image_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_image)
        #     if os.path.exists(image_path):
        #         os.remove(image_path)
        db_delete_event(event_id)
        flash("Event has been removed.", "success")
        return redirect(url_for("journey", journey_id=journey_id))
    except:
        return (
            render_template(
                "error.html",
                error_message="Something went wrong, please try again.",
                home_url=url_for("journey", journey_id=journey_id),
            ),
            403,
        )


@app.get("/events/<int:event_id>/photos/upload")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def add_event_photos(event_id):
    try:
        event = db_get_event_by_event_id(event_id)
        user_id = db_get_user_id_by_event_id(event_id)
        journey_id = request.args.get("journey_id", None)
        can_edit_event, message = check_user_id_journey_id_against_event(
            user_id, journey_id, event
        )
        have_active_subscription = db_have_active_subscription(user_id)
        can_upload_multiple_photos = False
        if session.get("role") in ["editor", "admin", "supporttech", "moderator"] or have_active_subscription:
            can_upload_multiple_photos = True

        if not can_edit_event:
            flash(message, "warning")
            return (
                render_template(
                    "error.html",
                    error_message=message,
                    home_url=url_for("journey", journey_id=journey_id),
                ),
                403,
            )

        return render_template(
            "event/add_photos.html",
            event_id=event_id,
            journey_id=journey_id,
            can_upload_multiple_photos=can_upload_multiple_photos,
        )

    except:
        flash("Something went wrong, please try again.", "danger")
        return redirect(url_for("journey", journey_id=journey_id))


@app.post("/events/<int:event_id>/photos/upload")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def upload_photos_to_event(event_id):
    can_add_photo, redirect_url = can_add_photo_to_event(event_id)
    user_id = db_get_user_id_by_event_id(event_id)
    have_active_subscription = db_have_active_subscription(user_id)
    can_upload_multiple_photos = False
    if session.get("role") in ["editor", "admin", "supporttech", "moderator"] or have_active_subscription:
        can_upload_multiple_photos = True

    if not can_add_photo:
        return redirect(redirect_url)

    if can_upload_multiple_photos:
        # Upload multiple images
        files = request.files.getlist("image_files")
        skipped = False
        for file in files:
            if not file or not file.filename:
                flash("No file selected.", "warning")
                return redirect(redirect_url)
            if not allowed_image(file.filename):
                flash("File type not allowed.", "warning")
                return redirect(redirect_url)

            filename = secure_filename(file.filename)
            # File name could be: event_photo_30_test.jpg
            filename = "event_photo_" + str(event_id) + filename

            photo_exist = db_event_photo_exists(filename)
            if photo_exist:
                skipped = True
                continue  # Skip to next file

            try:
                file.save(
                    os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename)
                )
                db_save_event_photo(filename, event_id)
                if skipped:
                    flash(
                        "Some photos were skipped because they already exist in this event.",
                        "success",
                    )
                else:
                    flash("Photo has been added successfully.", "success")
            except:
                flash("Something went wrong, please try again.", "danger")
    else:
        # Upload single image
        file = request.files["image_file"]
        if not file or not file.filename:
            flash("No file selected.", "warning")
            return redirect(redirect_url)
        if not allowed_image(file.filename):
            flash("File type not allowed.", "warning")
            return redirect(redirect_url)

        filename = secure_filename(file.filename)
        filename = "event_photo_" + str(event_id) + filename

        try:
            file.save(
                os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename)
            )
            db_save_event_photo(filename, event_id)
            flash("Photo has been added successfully.", "success")
        except:
            flash("Something went wrong, please try again.", "danger")

    return redirect(redirect_url)


@app.get("/journeys/<int:journey_id>/delete_event_photos/<int:photo_id>")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def delete_event_photos(photo_id, journey_id):
    try:
        db_delete_event_photos(photo_id)
        flash("Event photo has been removed.", "success")
    except:
        flash("Something went wrong, please try again.", "danger")
    return redirect(url_for("journey", journey_id=journey_id))


@app.get("/journeys/<int:journey_id>/events/<int:event_id>/like_event")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def like_event(journey_id, event_id):
    user_id = session["user_id"]
    try:
        existing_reaction = db_get_user_event_reaction(user_id, event_id)

        if existing_reaction:
            # If like reaction is existing, then unlike this event (delete the like reaction).
            db_delete_reaction(existing_reaction["reaction_id"])
            # Decrease the like count in events table.
            db_update_event_like_count(event_id, -1)
        else:
            # If no existing_reaction then add a new one.
            db_add_user_event_reaction(user_id, event_id, True)
            # Increase the like count in events table.
            db_update_event_like_count(event_id, 1)

            #check achievements by event likes
            event_owner = db_get_user_id_by_event_id(event_id)
            event_likes_20 = db_get_achievement("20_event_likes", event_owner)
            event_likes_40 = db_get_achievement("40_event_likes", event_owner)
            event_likes_60 = db_get_achievement("60_event_likes", event_owner)

            # Check whether this event has most likes
            most_likes_event = db_get_most_likes_event_by_user_id(event_owner)
            if (most_likes_event['event_id'] == event_id):
                if not (event_likes_20 and event_likes_20["progress"] >= 20):
                    if event_likes_20 == None or most_likes_event["like_count"] > event_likes_20["progress"]:
                        check_achieved("20_event_likes", event_owner)
                elif not (event_likes_40 and event_likes_40["progress"] >= 40):
                    if event_likes_40 == None or most_likes_event["like_count"] > event_likes_40["progress"]:
                        check_achieved("40_event_likes", event_owner)
                elif not (event_likes_60 and event_likes_60["progress"] >= 60):
                    if event_likes_60 == None or most_likes_event["like_count"] > event_likes_60["progress"]:
                        check_achieved("60_event_likes", event_owner)

    except:
        return (
                render_template(
                    "error.html",
                    error_message="Something went wrong, please try again.",
                    home_url=url_for("journey", journey_id=journey_id),
                ),
                403,
            )

    return redirect(url_for("journey", journey_id=journey_id))

@app.get("/departure_board/events/<int:event_id>/like_event")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def like_event_from_departure_board(event_id):
    user_id = session["user_id"]
    try:
        existing_reaction = db_get_user_event_reaction(user_id, event_id)

        if existing_reaction:
            # If like reaction is existing, then unlike this event (delete the like reaction).
            db_delete_reaction(existing_reaction["reaction_id"])
            # Decrease the like count in events table.
            db_update_event_like_count(event_id, -1)
        else:
            # If no existing_reaction then add a new one.
            db_add_user_event_reaction(user_id, event_id, True)
            # Increase the like count in events table.
            db_update_event_like_count(event_id, 1)

            #check achievements by event likes
            event_owner = db_get_user_id_by_event_id(event_id)
            event_likes_20 = db_get_achievement("20_event_likes", event_owner)
            event_likes_40 = db_get_achievement("40_event_likes", event_owner)
            event_likes_60 = db_get_achievement("60_event_likes", event_owner)

            # Check whether this event has most likes
            most_likes_event = db_get_most_likes_event_by_user_id(event_owner)
            if (most_likes_event['event_id'] == event_id):
                if not (event_likes_20 and event_likes_20["progress"] >= 20):
                    if event_likes_20 == None or most_likes_event["like_count"] > event_likes_20["progress"]:
                        check_achieved("20_event_likes", event_owner)
                elif not (event_likes_40 and event_likes_40["progress"] >= 40):
                    if event_likes_40 == None or most_likes_event["like_count"] > event_likes_40["progress"]:
                        check_achieved("40_event_likes", event_owner)
                elif not (event_likes_60 and event_likes_60["progress"] >= 60):
                    if event_likes_60 == None or most_likes_event["like_count"] > event_likes_60["progress"]:
                        check_achieved("60_event_likes", event_owner)

    except:
        return (
                render_template(
                    "error.html",
                    error_message="Something went wrong, please try again.",
                    home_url=url_for("departure_board"),
                ),
                403,
            )

    return redirect(url_for("departure_board"))

@app.get("/events/<int:event_id>/comments")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def show_event(event_id):
    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 8, type=int)
    event = db_get_event_by_event_id(event_id)
    # Get current user's reactions for this event
    existing_reaction = db_get_user_event_reaction(
        session["user_id"], event["event_id"]
    )
    event["is_liked"] = True if existing_reaction else False
    journey_id = event.get("journey_id", None)
    journey = db_get_journey_by_journey_id(journey_id)
    comments = db_get_event_comments(
        event_id, session["user_id"], current_page, page_size
    )
    # Get current user's reactions for all comments
    user_reactions = db_get_user_comments_reactions(session["user_id"])
    # Build a map of comment_id to is_like
    reaction_map = {r["comment_id"]: r["is_like"] for r in user_reactions}
    # Add is_liked and is_disliked to each comment
    for comment in comments:
        is_like = reaction_map.get(comment["comment_id"])
        comment["is_liked"] = is_like is 1
        comment["is_disliked"] = is_like is 0
    total_comments_count = db_get_event_comments_count_by_event_id(event_id)
    total_pages = (total_comments_count + page_size - 1) // page_size

    return render_template(
        "event/show.html",
        event=event,
        journey=journey,
        comments=comments,
        event_id=event_id,
        journey_id=journey_id,
        current_page=current_page,
        total_pages=total_pages,
        page_size=page_size,
    )


@app.post("/events/<int:event_id>/owner/<int:event_owner>/comments/add")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def add_comment(event_id, event_owner):
    content = request.form.get("content", "").strip()
    if not content:
        flash("Comment cannot be empty.", "warning")
        return redirect(url_for("show_event", event_id=event_id))

    try:
        user_id = session["user_id"]
        db_add_comment(event_id, user_id, content)

        # Check whether this event has most comments
        most_comments_event = db_get_most_comments_event_by_user_id(event_owner)
        if (most_comments_event['event_id'] == event_id):
            total_comments_count = db_get_event_comments_count_by_event_id(event_id)
            # Check user achievement for 5/10/20 comments
            if total_comments_count <= 5:
                check_achieved("five_comments_for_event", event_owner)
            elif total_comments_count <= 10:
                check_achieved("ten_comments_for_event", event_owner)
            else:
                check_achieved("twenty_comments_for_event", event_owner)

        flash("Comment has been added successfully.", "success")
    except:
        flash("Something went wrong. Please try again.", "danger")

    return redirect(url_for("show_event", event_id=event_id))


@app.post("/comments/<int:comment_id>/report")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def report_comment(comment_id):
    comment = db_get_comment(comment_id)
    if not comment:
        return (
            render_template(
                "error.html",
                error_message="Comment not found",
                home_url=url_for("root"),
            ),
            404,
        )

    reason = request.form.get("reason")
    if not reason:
        flash("Reason cannot be empty.", "warning")
        return redirect(url_for("show_event", event_id=comment["event_id"]))

    try:
        user_id = session["user_id"]
        db_create_report(comment_id, user_id, reason)
        flash("Comment has been reported successfully. Thank you.", "success")
    except:
        flash("Something went wrong. Please try again.", "danger")

    return redirect(url_for("show_event", event_id=comment["event_id"]))


@app.get("/events/<int:event_id>/comments/<int:comment_id>/like")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def like_comment(event_id, comment_id):
    user_id = session["user_id"]
    existing_reaction = db_get_event_comment_reaction(user_id, comment_id)

    # If comment like reaction is existing
    if existing_reaction:
        if existing_reaction["is_like"]:
            # If comment is liked, then unlike this comment (delete the comment like reaction).
            db_delete_reaction(existing_reaction["reaction_id"])
            # Decrease the like count in events table.
            db_update_comment_like_count(comment_id, -1)
        else:
            # If comment is disliked, then change the reaction from dislike to like
            db_update_event_comment_reaction(existing_reaction["reaction_id"], True)
            # Update the like and dislike count in commments table
            db_update_comment_like_count(comment_id, 1)
            db_update_comment_dislike_count(comment_id, -1)
    else:
        # If no existing_reaction then add a comment like reaction
        db_add_event_comment_reaction(user_id, comment_id, True)
        # Increase the like count in comments table.
        db_update_comment_like_count(comment_id, 1)

    return redirect(url_for("show_event", event_id=event_id))


@app.get("/events/<int:event_id>/comments/<int:comment_id>/dislike")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def dislike_comment(event_id, comment_id):
    user_id = session["user_id"]
    existing_reaction = db_get_event_comment_reaction(user_id, comment_id)

    if existing_reaction:
        if not existing_reaction["is_like"]:
            # If comment is disliked, then un-dislike this comment (delete the comment like reaction).
            db_delete_reaction(existing_reaction["reaction_id"])
            # Decrease the like count in events table.
            db_update_comment_dislike_count(comment_id, -1)
        else:
            # If comment is liked, then change the reaction from like to dislike
            db_update_event_comment_reaction(existing_reaction["reaction_id"], False)
            # Update the like and dislike count in commments table
            db_update_comment_like_count(comment_id, -1)
            db_update_comment_dislike_count(comment_id, 1)
    else:
        # If no existing_reaction then add a comment dislike reaction
        db_add_event_comment_reaction(user_id, comment_id, False)
        # Increase the dislike count in comments table.
        db_update_comment_dislike_count(comment_id, 1)

    return redirect(url_for("show_event", event_id=event_id))
