from typing import Dict
from app import db


def db_get_achievement(type: str, user_id) -> Dict | None:
    query = """
        SELECT achievements.*, achievement_types.* FROM achievements
        JOIN achievement_types ON achievement_types.achievement_type_id = achievements.achievement_type_id
        WHERE achievements.user_id = %s AND achievement_types.type = %s LIMIT 1;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id, type))
        return cursor.fetchone()


def db_inc_achievement_progress(achievement_id: int) -> Dict:
    """
    Increment achievement progress and update user achievement count if completed

    Args:
        achievement_id: The ID of the achievement to increment

    Returns:
        The updated achievement record
    """
    # First, get the current state of the achievement
    get_current_query = """
        SELECT a.*, at.* FROM achievements a
        JOIN achievement_types at ON at.achievement_type_id = a.achievement_type_id
        WHERE a.achievement_id = %s;
    """

    update_query = """
        UPDATE achievements SET progress = progress + 1 WHERE achievement_id = %s;
    """

    select_query = """
        SELECT a.*, at.* FROM achievements a
        JOIN achievement_types at ON at.achievement_type_id = a.achievement_type_id
        WHERE a.achievement_id = %s;
    """

    with db.get_cursor() as cursor:
        # Get current state
        cursor.execute(get_current_query, (achievement_id,))
        current_achievement = cursor.fetchone()

        # Check if this will be a newly completed achievement
        was_completed = current_achievement["progress"] >= current_achievement["goal"]
        will_complete = current_achievement["progress"] + 1 >= current_achievement["goal"]

        # Update the achievement progress
        cursor.execute(update_query, (achievement_id,))

        # If this is a new completion, update the user's achievement count
        if not was_completed and will_complete:
            update_user_query = """
                UPDATE users SET achievement_count = achievement_count + 1 WHERE user_id = %s;
            """
            cursor.execute(update_user_query, (current_achievement["user_id"],))

        # Get the updated achievement
        cursor.execute(select_query, (achievement_id,))
        return cursor.fetchone()


def db_create_achievement(type: str, user_id) -> None:
    """
    Create a new achievement for a user and update achievement_count if immediately completed

    Args:
        type: The type of achievement to create
        user_id: The ID of the user
    """
    # Get the goal for this achievement type
    get_goal_query = """
        SELECT goal FROM achievement_types WHERE type = %s;
    """

    insert_query = """
        INSERT INTO achievements (achievement_type_id, user_id, progress)
        SELECT achievement_types.achievement_type_id, %s, %s
        FROM achievement_types WHERE achievement_types.type = %s;
    """

    with db.get_cursor() as cursor:
        # Determine initial progress
        progress = 1
        if type == "40_event_likes":
            progress = 21
        if type == "60_event_likes":
            progress = 41

        # Get the goal for this achievement
        cursor.execute(get_goal_query, (type,))
        goal_record = cursor.fetchone()
        goal = goal_record["goal"] if goal_record else 1

        # Insert the achievement
        cursor.execute(insert_query, (user_id, progress, type))

        # If progress already meets the goal, increment achievement_count
        if progress >= goal:
            update_count_query = """
                UPDATE users SET achievement_count = achievement_count + 1 WHERE user_id = %s;
            """
            cursor.execute(update_count_query, (user_id,))


def db_get_achievements(user_id: int) -> list[Dict]:
    query = """
        SELECT
            achievements.*,
            achievement_types.*,
            COALESCE(achievements.progress, 0) >= achievement_types.goal as achieved,
            COALESCE(achievements.progress, 0) / achievement_types.goal as achieve_progress
        FROM achievement_types
        LEFT JOIN achievements ON achievement_types.achievement_type_id = achievements.achievement_type_id AND achievements.user_id = %s
        ORDER BY achieve_progress DESC, achievement_types.achievement_type_id ASC;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id,))
        return cursor.fetchall()


def db_get_achievements_count(user_id: int) -> int:
    query = """
        SELECT COUNT(achievement_id) as count FROM achievements
        JOIN achievement_types ON achievements.achievement_type_id = achievement_types.achievement_type_id
        WHERE achievements.user_id = %s AND achievements.progress >= achievement_types.goal;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id,))
        res = cursor.fetchone()
        return res["count"]


def db_get_recently_awarded_achievements_count() -> int:
    """
    Get the total count of recently awarded achievements (where progress >= goal)

    Returns:
        The total count of awarded achievements
    """
    query_count = """
        SELECT COUNT(*) as count
        FROM achievements a
        JOIN achievement_types at ON a.achievement_type_id = at.achievement_type_id
        JOIN users u ON a.user_id = u.user_id
        WHERE a.progress >= at.goal AND u.profile_public = TRUE
    """

    with db.get_cursor() as cursor:
        cursor.execute(query_count)
        total_count = cursor.fetchone()["count"]
        return total_count


def db_get_recently_awarded_achievements(
    current_page: int = 1, page_size: int = 8
) -> list[Dict]:
    """
    Get a list of recently awarded achievements (where progress >= goal)

    Args:
        current_page: The page number (1-indexed)
        page_size: Number of items per page

    Returns:
        A list of awarded achievements
    """
    query = """
        SELECT a.*, at.*, u.username, u.profile_image, u.user_id,
               CONCAT(u.first_name, ' ', u.last_name) as full_name
        FROM achievements a
        JOIN achievement_types at ON a.achievement_type_id = at.achievement_type_id
        JOIN users u ON a.user_id = u.user_id
        WHERE a.progress >= at.goal AND u.profile_public = TRUE
        ORDER BY a.updated_at DESC
        LIMIT %s OFFSET %s
    """

    offset = (current_page - 1) * page_size

    with db.get_cursor() as cursor:
        cursor.execute(query, (page_size, offset))
        achievements = cursor.fetchall()
        return achievements


def db_get_achievement_leaderboard_count() -> int:
    query_count = """
        SELECT COUNT(*) as count
        FROM users
        WHERE profile_public = TRUE AND achievement_count > 0
    """

    with db.get_cursor() as cursor:
        cursor.execute(query_count)
        total_count = cursor.fetchone()["count"]
        return total_count


def db_get_achievement_leaderboard(current_page: int = 1, page_size: int = 8) -> list[Dict]:
    """
    Get a leaderboard of users ranked by number of completed achievements
    """
    query = """
        SELECT
            user_id,
            username,
            profile_image,
            achievement_count AS completed_achievements,
            RANK() OVER (ORDER BY achievement_count DESC) as ranking
        FROM users
        WHERE profile_public = TRUE AND achievement_count > 0
        ORDER BY achievement_count DESC, username ASC
        LIMIT %s OFFSET %s
    """

    offset = (current_page - 1) * page_size

    with db.get_cursor() as cursor:
        cursor.execute(query, (page_size, offset))
        users = cursor.fetchall()
        return users
