from datetime import datetime
from typing import Dict

from flask import render_template, request, session

from app import app
from app.auth import login_required
from app.repositories.achievement_repository import (
    db_create_achievement,
    db_get_achievement,
    db_inc_achievement_progress,
    db_get_recently_awarded_achievements,
    db_get_recently_awarded_achievements_count,
    db_get_achievement_leaderboard,
    db_get_achievement_leaderboard_count,
)
from app.repositories.journey_repository import (
    db_get_journey_by_journey_id,
    db_get_journey_duration,
)


def check_achieved(type: str, user_id: int) -> Dict | None:
    achievement = db_get_achievement(type, user_id)
    # Achievement already exists and achieved, means no new achievement -> return None
    if achievement and achievement["progress"] >= achievement["goal"]:
        return None

    print(achievement)
    # Achievement already exists and not achieved
    if achievement and achievement["progress"] < achievement["goal"]:
        # Increase progress of the Achievement
        achievement = db_inc_achievement_progress(achievement["achievement_id"])
        # If achieved after increase, means new achievement -> return achievement
        if achievement["progress"] >= achievement["goal"]:
            return achievement
        # If not achieved after increase, means no new achievement -> return None
        else:
            return None

    # Achievement not exists, create a new achievement with progress = 1
    db_create_achievement(type, user_id)
    achievement = db_get_achievement(type, user_id)
    # If achieved after creation, means new achievement -> return achievement
    if achievement and achievement["progress"] >= achievement["goal"]:
        return achievement
    # If not achieved after creation, means no new achievement -> return None
    else:
        return None


def check_seven_days_journey_achieved(journey_id: int) -> Dict | None:
    journey = db_get_journey_by_journey_id(journey_id)
    journey_start_date = datetime.combine(journey["start_date"], datetime.min.time())

    duration = db_get_journey_duration(journey_id)
    min_start_datetime = duration["min_start_datetime"]
    min_end_datetime = duration["min_end_datetime"]
    max_start_datetime = duration["max_start_datetime"]
    max_end_datetime = duration["max_end_datetime"]

    datetimes = list(
        filter(
            lambda x: x != None,
            [
                journey_start_date,
                min_start_datetime,
                min_end_datetime,
                max_start_datetime,
                max_end_datetime,
            ],
        )
    )

    min_datetime = min(datetimes)
    max_datetime = max(datetimes)
    print(min_datetime, max_datetime)
    if (max_datetime - min_datetime).days >= 7:
        return check_achieved("seven_days_journey", journey["user_id"])

    return None


@app.route("/achievements/lists")
@login_required()
def recently_awarded_achievements():
    """View a list of users who have been recently awarded achievements and the achievement leaderboard"""

    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 8, type=int)
    active_tab = request.args.get("tab", "recent")    # Recent achievements tab
    total_count = db_get_recently_awarded_achievements_count()
    achievements = db_get_recently_awarded_achievements(current_page, page_size)
    total_pages = (total_count + page_size - 1) // page_size
    
    # Leaderboard tab
    leaderboard_total_count = db_get_achievement_leaderboard_count()
    leaderboard = db_get_achievement_leaderboard(current_page, page_size)
    leaderboard_total_pages = (leaderboard_total_count + page_size - 1) // page_size
    
    return render_template(
        "achievement/lists.html",
        achievements=achievements,
        current_page=current_page,
        page_size=page_size,
        total_pages=total_pages,
        total_count=total_count,
        leaderboard=leaderboard,
        leaderboard_total_pages=leaderboard_total_pages,
        leaderboard_total_count=leaderboard_total_count,
        active_tab=active_tab
    )
