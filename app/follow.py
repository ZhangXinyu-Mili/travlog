from flask import flash, redirect, url_for, g, request, render_template, session
from app import app
from app.auth import login_required
from app.repositories.community_repository import (
    db_create_follow,
    db_get_events_user_following,
    db_get_events_user_following_count,
    db_get_follow_by_followable,
    db_get_journeys_user_following,
    db_get_journeys_user_following_count,
    db_get_users_user_following,
    db_get_users_user_following_count,
    db_get_locations_user_following,
    db_get_locations_user_following_count,
    db_get_follows_by_event_id,
    db_unfollow
)
from app.repositories.journey_repository import (
    db_get_event_photos_by_event_id,
    db_get_journey_by_journey_id,
    db_get_location_by_id,
    db_get_user_id_by_event_id
)
from app.repositories.subscription_repository import db_have_active_subscription
from app.repositories.user_repository import db_get_user_by_id
from app.repositories.event_comment_repository import db_get_user_event_reaction

role_badges_mapping = {
    "admin": "danger",
    "editor": "info",
    "moderator": "warning",
    "supporttech": "warning",
    "traveller": "primary",
}
status_badges_mapping = {
    "active": "primary",
    "blocked": "secondary",
    "banned": "danger",
}


@app.post("/journeys/<int:journey_id>/follow")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def follow_journey(journey_id):
    return follow_content("journey", journey_id)


@app.post("/locations/<int:location_id>/follow")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def follow_location(location_id):
    return follow_content("location", location_id)


@app.post("/users/<int:user_id>/follow")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def follow_user(user_id):
    return follow_content("user", user_id)


def follow_content(followable_type: str, followable_id: int):
    if not g.premium:
        return {
            "category": "danger",
            "message": "You must have a subscription to access premium features. <a href='/subscriptions' style='color: #fff; text-decoration: underline; font-weight: bold;'>Subscribe now</a>"
        }, 403

    match followable_type:
        case "journey":
            journey = db_get_journey_by_journey_id(followable_id)
            if not journey or journey["status"] == "private":
                return {
                    "category": "danger",
                    "message": "Journey not found"
                }, 404
        case "location":
            location = db_get_location_by_id(followable_id)
            if not location:
                return {
                    "category": "danger",
                    "message": "Location not found"
                }, 404
        case "user":
            user = db_get_user_by_id(followable_id)
            if not user:
                return {
                    "category": "danger",
                    "message": "User not found"
                }, 404

    follow = db_get_follow_by_followable(g.user["user_id"], followable_type, followable_id)
    if follow:
        return {
            "category": "success",
            "message": f"You have already followed the {followable_type}."
        }

    try:
        db_create_follow(g.user["user_id"], followable_type, followable_id)
        return {
            "category": "success",
            "message": f"Success! You are now following this {followable_type}."
        }
    except:
        return {
            "category": "danger",
            "message": "Something went wrong, please try again."
        }, 500


def get_followable_type(follow) -> str:
    return follow["followable_type"]


@app.get("/departure_board")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def departure_board():
    if not g.premium:
        flash(
            "You must have a subscription to access premium features. <a href='/subscriptions'>subscribe now</a>",
            "danger",
        )
        return redirect(url_for("root"))

    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 9, type=int)

    events = db_get_events_user_following(g.user["user_id"], current_page, page_size)
    for event in events:
        photos = db_get_event_photos_by_event_id(event["event_id"])
        user_id = db_get_user_id_by_event_id(event["event_id"])
        user = db_get_user_by_id(user_id)
        have_active_subscription = db_have_active_subscription(user_id)
        # Get current user's reactions for this event
        existing_reaction = db_get_user_event_reaction(
            g.user["user_id"], event["event_id"]
        )
        event["is_liked"] = True if existing_reaction else False
        # Unsubscribe user can only display first photo
        if photos and not have_active_subscription and not (
            user["role"] in ["editor", "admin", "moderator", "supporttech"]
        ):
            photos = (photos[0],)
        follows = db_get_follows_by_event_id(g.user["user_id"], event["event_id"])
        event["photos"] = photos
        event["followable_types"] = list(map(get_followable_type, follows))
    events_count = db_get_events_user_following_count(g.user["user_id"])
    total_pages = (events_count + page_size - 1) // page_size

    return render_template(
        "departure_board.html",
        events=events,
        current_page=current_page,
        total_pages=total_pages,
    )


@app.get("/my_followings")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def my_followings():
    """users view their current followings"""
    if not g.premium:
        flash("You must have a subscription to access premium features. <a href='/subscriptions'>subscribe now</a>", "danger")
        return redirect(url_for("root"))
    #Journeys Pagination
    journeys_page = request.args.get("journeys_page", 1, type=int)
    journeys_page_size = request.args.get("page_size", 6, type=int)
    journeys = db_get_journeys_user_following(g.user["user_id"], journeys_page, journeys_page_size)
    total_journeys_count = db_get_journeys_user_following_count(g.user["user_id"])
    total_journeys_pages = (total_journeys_count + journeys_page_size - 1) // journeys_page_size
    #users Pagination
    users_page = request.args.get("users_page", 1, type=int)
    users = db_get_users_user_following(g.user["user_id"], users_page, journeys_page_size)
    total_users_count = db_get_users_user_following_count(g.user["user_id"])
    total_users_pages = (total_users_count + journeys_page_size - 1) // journeys_page_size
    #locations Pagination
    locations_page = request.args.get("locations_page", 1, type=int)
    locations = db_get_locations_user_following(g.user["user_id"], locations_page, journeys_page_size)
    total_locations_count = db_get_locations_user_following_count(g.user["user_id"])
    total_locations_pages = (total_locations_count + journeys_page_size - 1) // journeys_page_size
    return render_template(
        "user/followings.html",
        journeys=journeys,
        users=users,
        locations=locations,
        journeys_page=journeys_page,
        total_journeys_pages=total_journeys_pages,
        users_page=users_page,
        total_users_pages=total_users_pages,
        locations_page=locations_page,
        total_locations_pages=total_locations_pages,
        role_badges_mapping=role_badges_mapping,
        status_badges_mapping=status_badges_mapping,
    )


@app.post("/my_followings/<int:followable_id>/<string:followable_type>/unfollow")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def unfollow(followable_id, followable_type):
    if not g.premium:
        flash("You must have a subscription to access premium features. <a href='/subscriptions'>subscribe now</a>", "danger")
        return redirect(url_for("root"))

    try:
        db_unfollow(followable_id, followable_type)
        flash("You have unfollowed the related content.", "success")
    except:
        flash("Something went wrong, please try again.", "danger")

    return redirect(url_for("my_followings"))

