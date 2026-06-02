from typing import Dict, List, Optional

from app import db


def db_get_community_users(
    current_page: int,
    page_size: int,
    q: Optional[str] = None,
) -> List[Dict]:
    """Get users with pagination.

    Args:
        current_page (int): Current page number.
        page_size (int): Number of users per page.
        q (str): Search query.

    Returns:
        List[Dict]: List of users.
    """
    offset = (current_page - 1) * page_size
    where_clause = ""
    params = []
    if q:
        where_clause = " WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR role LIKE %s OR location LIKE %s"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"])

    query = """
            SELECT user_id, username, location, profile_image, role, description,
                profile_public
            FROM users
            """ + where_clause + """
            ORDER BY user_id DESC
            LIMIT %s OFFSET %s;
            """
    params.extend([page_size, offset])
    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        users = cursor.fetchall()
        return users
    
def db_get_community_users_count(q: Optional[str] = None) -> int:
    """Get total number of community users with optional search query."""
    
    where_clause = ""
    params = []
    if q:
        where_clause = " WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR role LIKE %s OR location LIKE %s"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"])
    query = """
            SELECT COUNT(*) AS count
            FROM users
            """ + where_clause

    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        count = cursor.fetchone()
        return count["count"]

#get places users have been to
def db_get_location_by_user_id(user_id: int) -> list[Dict]:
    with db.get_cursor() as cursor:
        query = """
                    SELECT DISTINCT locations.location_id, locations.location_name
                    FROM users
                    JOIN journeys ON journeys.user_id = users.user_id
                    JOIN events ON events.journey_id = journeys.journey_id
                    JOIN locations ON locations.location_id = events.location_id
                    WHERE users.user_id = %s;
                    """
        cursor.execute(query, (user_id, ))
        locations = cursor.fetchall()
        return locations

#get all comments made by a user
def db_get_comments_by_user_id(user_id: int, page: int = 1, per_page: int = 10) -> List[Dict]:
    """Get paginated comments for a user"""
    offset = (page - 1) * per_page
    with db.get_cursor() as cursor:
        query = """
            SELECT c.*, u.username, u.first_name, u.last_name, r.report_id, e.title, e.description, e.start_datetime, e.end_datetime, l.location_name
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            LEFT JOIN reports r ON r.comment_id = c.comment_id
            JOIN events e ON e.event_id = c.event_id
            LEFT JOIN locations l ON e.location_id = l.location_id
            WHERE c.user_id = %s
            ORDER BY c.created_at DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (user_id, per_page, offset))
        return cursor.fetchall()
def db_get_event_comments_count_by_user_id(user_id: int) -> int:
    """Get total number of comments for an user"""
    query = """SELECT COUNT(*) as count
            FROM comments c
            WHERE c.user_id = %s"""
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result['count'] if result else 0

#get all events liked by a user
def db_get_liked_event_by_user_id(user_id: int, page: int = 1, per_page: int = 10) -> List[Dict]:
    """Get paginated liked events for a user"""
    offset = (page - 1) * per_page
    with db.get_cursor() as cursor:
        query = """
            SELECT r.*, u.username, e.title, e.description, e.start_datetime, e.end_datetime, l.location_name
            FROM reactions r
            JOIN users u ON r.user_id = u.user_id
            JOIN events e ON e.event_id = r.event_id
            LEFT JOIN locations l ON e.location_id = l.location_id
            WHERE r.user_id = %s and r.reaction_type = "event" and r.is_like = True
            ORDER BY r.created_at DESC
            LIMIT %s OFFSET %s
            """
        cursor.execute(query, (user_id, per_page, offset))
        return cursor.fetchall()
def db_get_event_likes_count(user_id: int) -> int:
    """Get total number of likes for an user"""
    query = """
            SELECT COUNT(*) as count
            FROM reactions r
            WHERE r.user_id = %s and r.reaction_type = "event" and r.is_like = True
            """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result['count'] if result else 0

## get messages
def db_get_summaries(user_id: int, current_page: Optional[int], page_size: Optional[int], from_id: Optional[int]) -> list[Dict]:
    """Get a summary list of messages for a user
    Args:
        user_id (int): user id.
        current_page (int): current page.
        page_size (int): page size.
    Returns:
        List[Dict]: List of summaries.
    """
    offset = (current_page - 1) * page_size

    with db.get_cursor() as cursor:

        if from_id:
            query = """
                    WITH summary as (
                    (SELECT COUNT(*) AS count, m1.from, m1.to, "f" as direction, sum(m1.status) as new_messages_f, 0 as new_messages_t, JSON_ARRAYAGG(m1.message_id) AS message_ids
                        FROM messages m1
                        WHERE m1.to = %s and m1.from = %s
                        GROUP BY m1.from, m1.to
                        ORDER BY m1.created_at)
                    UNION
                    (SELECT COUNT(*) AS count, m3.to, m3.from, "t" as direction, 0 as new_messages_f, sum(m3.status) as new_messages_t, JSON_ARRAYAGG(m3.message_id) AS message_ids
                        FROM messages m3
                        WHERE m3.from = %s and m3.to = %s
                        GROUP BY m3.to, m3.from
                        ORDER BY m3.created_at)
                    )
                    SELECT sum(s.count) as count, s.from as from_id, s.to as to_id, JSON_ARRAYAGG(s.message_ids) as message_ids, JSON_OBJECTAGG(s.direction, s.new_messages_f) as new_messages_f,
                        JSON_OBJECTAGG(s.direction, s.new_messages_t) as new_messages_t, u1.username, u1.role, JSON_OBJECTAGG(s.direction, s.message_ids) as directions

                        FROM summary s
                        INNER JOIN users u1 ON u1.user_id = s.from
                        GROUP BY s.from, s.to
                        ORDER BY u1.username;
                """
            parameter = (user_id, from_id, user_id, from_id,)
        else:
            query = """
                    WITH summary as (
                    (SELECT COUNT(*) AS count, m1.from, m1.to, "f" as direction, sum(m1.status) as new_messages_f, 0 as new_messages_t, JSON_ARRAYAGG(m1.message_id) AS message_ids
                        FROM messages m1
                        WHERE m1.to = %s
                        GROUP BY m1.from, m1.to
                        ORDER BY m1.created_at desc  )
                    UNION
                    (SELECT COUNT(*) AS count, m3.to, m3.from, "t" as direction, 0 as new_messages_f, sum(m3.status) as new_messages_t, JSON_ARRAYAGG(m3.message_id) AS message_ids
                        FROM messages m3
                        WHERE m3.from = %s
                        GROUP BY m3.to, m3.from
                        ORDER BY m3.created_at desc)
                    )
                    SELECT sum(s.count) as count, s.from as from_id, s.to as to_id, JSON_ARRAYAGG(s.message_ids) as message_ids, JSON_OBJECTAGG(s.direction, s.new_messages_f) as new_messages_f,
                        JSON_OBJECTAGG(s.direction, s.new_messages_t) as new_messages_t, u1.username, u1.role, JSON_OBJECTAGG(s.direction, s.message_ids) as directions

                        FROM summary s
                        INNER JOIN users u1 ON u1.user_id = s.from
                        GROUP BY s.from, s.to
                        ORDER BY u1.username
                        LIMIT %s OFFSET %s;
                """
            parameter = (user_id, user_id, page_size, offset)

        cursor.execute(query, parameter)
        summaries = cursor.fetchall()
        return summaries

def db_get_summaries_count(user_id: int) -> int:
    """Get the total count of messages of a user.

    Args:
        user_id (int): user id.

    Returns:
        int: Total count of messages.
    """

    with db.get_cursor() as cursor:
        sql_query = """
                        WITH g AS (
                        SELECT m1.from, m1.to
                            FROM messages m1
                            WHERE m1.to = %s
                        UNION
                            SELECT m3.to, m3.from
                            FROM messages m3
                            WHERE m3.from = %s
                        )
                        SELECT COUNT(*) as count from g;
                    """
        cursor.execute(sql_query, (user_id, user_id,))
        count = cursor.fetchone()
        return count["count"]

def db_get_messages(user_id: int, from_id: Optional[int]) -> Dict:
    """Get messages of a user.

    Args:
        user_id (int): user id.
        from_id (int): another user to whom a user is sending a message.

    Returns:
        Dict: Dictionary of content.
    """

    with db.get_cursor() as cursor:

        if from_id:
            sql_query = """
                        SELECT m1.message_id, m1.to as from_id, m1.from as to_id, m1.content, m1.status, m1.created_at, u1.first_name, u1.last_name, u1.username, u1.role
                            FROM messages m1
                            INNER JOIN users u1 ON u1.user_id = m1.from
                            WHERE (m1.from = %s and m1.to = %s) or (m1.from = %s and m1.to = %s)
                            ORDER BY m1.created_at;
                        """
            parameter = (from_id, user_id, user_id, from_id,)
        else:
            sql_query = """
                        SELECT m1.message_id, m1.to as from_id, m1.from as to_id, m1.content, m1.status, m1.created_at, u1.first_name, u1.last_name, u1.username, u1.role
                            FROM messages m1
                            INNER JOIN users u1 ON u1.user_id = m1.from
                            WHERE m1.from = %s
                            UNION
                        SELECT m2.message_id, m2.from as from_id, m2.to as to_id, m2.content, m2.status, m2.created_at, u2.first_name, u2.last_name, u2.username, u2.role
                            FROM messages m2
                            INNER JOIN users u2 ON u2.user_id = m2.from
                            WHERE m2.to = %s;
                    """
            parameter = (user_id, user_id, )
        cursor.execute(sql_query, parameter)
        messages_original = cursor.fetchall()
        messages ={}
        for item in messages_original:
            messages[item['message_id']]=item
        return messages

## save messages
def db_save_message(from_id: int, to_id: int, content: str) -> None:
    """save a private message from a user
    Args:
        from_id (int): user id of sender.
        to_id (int): user id of receiver.
        content (str): message content
    Returns:
        None.
    """

    with db.get_cursor() as cursor:

        query = """
                INSERT INTO messages (`from`, `to`, `content`, `status`)
                VALUES (%s, %s, %s, %s);
                """
        cursor.execute(query, (from_id, to_id, content, 1))

## update message status
def db_update_message_status(from_id: int, status: bool) -> None:
    """update status of a private message
    Args:
        message_id (int): message id.
    Returns:
        None.
    """


    with db.get_cursor() as cursor:
        query = """
                UPDATE messages m
                SET status = %s
                WHERE m.from = %s;
                """
        cursor.execute(query, (status, from_id))

## delete message
def db_delete_message(message_id: int) -> None:
    """delete a private message
    Args:
        message_id (int): message id.
    Returns:
        None.
    """


    with db.get_cursor() as cursor:
        query = """
                DELETE FROM messages m
                WHERE m.message_id = %s;
                """
        cursor.execute(query, (message_id,))


## create follow
def db_create_follow(user_id: int, followable_type: str, followable_id: int) -> None:
    """create a follow
    Args:
        user_id (int): user id.
        followable_type (str): followable type.
        followable_id (int): followable id.
    """
    query = """
            INSERT INTO follows (follower_id, followable_type, followable_id)
            VALUES (%s, %s, %s);
            """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id, followable_type, followable_id))


## get follow
def db_get_follow_by_followable(user_id: int, followable_type: str, followable_id: int) -> Dict:
    """get a follow by followable
    Args:
        user_id (int): user id.
        followable_type (str): followable type.
        followable_id (int): followable id.
    """
    query = "SELECT * FROM follows WHERE follower_id = %s AND followable_type = %s AND followable_id = %s LIMIT 1;"
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id, followable_type, followable_id))
        return cursor.fetchone()


## get events user following
def db_get_events_user_following(user_id: int, current_page: int, page_size: int) -> list[Dict]:
    """get events user following
    Args:
        user_id (int): user id.
        current_page (int): Current page number.
        page_size (int): Number of users per page.

    Returns:
        List[Dict]: List of events.
    """
    offset = (current_page - 1) * page_size
    query = """
            SELECT DISTINCT(events.event_id), events.*, locations.location_name as location_name, journeys.title as journey_title, users.user_id as user_id, users.username as username FROM events
            JOIN journeys ON journeys.journey_id = events.journey_id
            JOIN users ON users.user_id = journeys.user_id
            LEFT JOIN locations ON locations.location_id = events.location_id
            JOIN follows ON (follows.followable_type = 'journey' AND follows.followable_id = journeys.journey_id)
                OR (follows.followable_type = 'user' AND follows.followable_id = users.user_id)
                OR (follows.followable_type = 'location' AND follows.followable_id = locations.location_id)
            WHERE journeys.status IN ('public', 'published') AND journeys.is_hidden = FALSE AND follows.follower_id = %s
            ORDER BY events.start_datetime DESC
            LIMIT %s OFFSET %s;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id, page_size, offset))
        return cursor.fetchall()


## get events user following count
def db_get_events_user_following_count(user_id: int) -> int:
    """get events user following
    Args:
        user_id (int): user id.

    Returns:
        int: Events count.
    """
    query = """
            SELECT COUNT(DISTINCT(events.event_id)) as count FROM events
            JOIN journeys ON journeys.journey_id = events.journey_id
            JOIN users ON users.user_id = journeys.user_id
            LEFT JOIN locations ON locations.location_id = events.location_id
            JOIN follows ON (follows.followable_type = 'journey' AND follows.followable_id = journeys.journey_id)
                OR (follows.followable_type = 'user' AND follows.followable_id = users.user_id)
                OR (follows.followable_type = 'location' AND follows.followable_id = locations.location_id)
            WHERE journeys.status IN ('public', 'published') AND journeys.is_hidden = FALSE AND follows.follower_id = %s;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id,))
        count = cursor.fetchone()
        return count["count"]

## get journeys user following
def db_get_journeys_user_following(user_id: int, current_page: int, page_size: int) -> list[Dict]:
    """get journeys user following
    Args:
        user_id (int): user id.
        current_page (int): Current page number.
        page_size (int): Number of users per page.

    Returns:
        List[Dict]: List of journeys.
    """
    offset = (current_page - 1) * page_size
    query = """
            SELECT journeys.*
            FROM journeys
            JOIN follows ON (follows.followable_type = 'journey' AND follows.followable_id = journeys.journey_id)
            WHERE journeys.status IN ('public', 'published') AND journeys.is_hidden = FALSE AND follows.follower_id = %s
            ORDER BY journeys.created_at DESC
            LIMIT %s OFFSET %s;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id, page_size, offset))
        return cursor.fetchall()

## get journeys user following count
def db_get_journeys_user_following_count(user_id: int) -> int:
    """get journeys user following
    Args:
        user_id (int): user id.

    Returns:
        int: journeys count.
    """
    query = """
            SELECT count(journeys.journey_id) as count
            FROM journeys
            JOIN follows ON (follows.followable_type = 'journey' AND follows.followable_id = journeys.journey_id)
            WHERE journeys.status IN ('public', 'published') AND journeys.is_hidden = FALSE AND follows.follower_id = %s;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id,))
        count = cursor.fetchone()
        return count["count"]

## get users user following
def db_get_users_user_following(user_id: int, current_page: int, page_size: int) -> list[Dict]:
    """get users user following
    Args:
        user_id (int): user id.
        current_page (int): Current page number.
        page_size (int): Number of users per page.

    Returns:
        List[Dict]: List of users.
    """
    offset = (current_page - 1) * page_size
    query = """
            SELECT users.*
            FROM users
            JOIN follows ON (follows.followable_type = 'user' AND follows.followable_id = users.user_id)
            WHERE follows.follower_id = %s
            ORDER BY users.username
            LIMIT %s OFFSET %s;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id, page_size, offset))
        return cursor.fetchall()

## get users user following count
def db_get_users_user_following_count(user_id: int) -> int:
    """get users user following
    Args:
        user_id (int): user id.

    Returns:
        int: users count.
    """
    query = """
            SELECT count(users.user_id) as count
            FROM users
            JOIN follows ON (follows.followable_type = 'user' AND follows.followable_id = users.user_id)
            WHERE follows.follower_id = %s;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id,))
        count = cursor.fetchone()
        return count["count"]

## get locations user following
def db_get_locations_user_following(user_id: int, current_page: int, page_size: int) -> list[Dict]:
    """get locations user following
    Args:
        user_id (int): user id.
        current_page (int): Current page number.
        page_size (int): Number of locations per page.

    Returns:
        List[Dict]: List of locations.
    """
    offset = (current_page - 1) * page_size
    query = """
            SELECT locations.*
            FROM locations
            JOIN follows ON (follows.followable_type = 'location' AND follows.followable_id = locations.location_id)
            WHERE follows.follower_id = %s
            ORDER BY locations.location_name
            LIMIT %s OFFSET %s;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id, page_size, offset))
        return cursor.fetchall()

## get locations user following count
def db_get_locations_user_following_count(user_id: int) -> int:
    """get locations user following
    Args:
        user_id (int): user id.

    Returns:
        int: locations count.
    """
    query = """
            SELECT count(locations.location_id) as count
            FROM locations
            JOIN follows ON (follows.followable_type = 'location' AND follows.followable_id = locations.location_id)
            WHERE follows.follower_id = %s;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id,))
        count = cursor.fetchone()
        return count["count"]

def db_unfollow(followable_id: int, followable_type: str) -> None:
     with db.get_cursor() as cursor:
         query = """
            DELETE FROM follows
            WHERE followable_id = %s and followable_type = %s
        """
         cursor.execute(query, (followable_id, followable_type,))

## get follows by event ids
def db_get_follows_by_event_id(user_id: int, event_id: int) -> list[Dict]:
    """get follows by event ids
    Args:
        event_id (int): event id.

    Returns:
        list[Dict]: Follows.
    """
    query = """
            SELECT events.*, follows.followable_type FROM events
            JOIN journeys ON journeys.journey_id = events.journey_id
            JOIN users ON users.user_id = journeys.user_id
            LEFT JOIN locations ON locations.location_id = events.location_id
            JOIN follows ON (follows.followable_type = 'journey' AND follows.followable_id = journeys.journey_id)
                OR (follows.followable_type = 'user' AND follows.followable_id = users.user_id)
                OR (follows.followable_type = 'location' AND follows.followable_id = locations.location_id)
            WHERE journeys.status IN ('public', 'published') AND journeys.is_hidden = FALSE AND follows.follower_id = %s AND events.event_id = %s;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (user_id, event_id,))
        return cursor.fetchall()


## check followed user or location
def db_user_or_location_followed(user_id: int, followed_id: int, type: str) -> Dict:
    """check weather a user or location is followed by a user
    Args:
        user_id (int): user id.
        followed_id (int): id of followed user or location.
        type: following type, user or location
    Returns:
        Dictionary.
    """

    is_user = False
    is_location = False
    if type == "user":
        query = """
                SELECT user_id FROM users
                WHERE user_id = %s
                LIMIT 1;
                """
        with db.get_cursor() as cursor:
            cursor.execute(query, (followed_id,))
            if cursor.fetchone():
                is_user = True

    if type == "location":
        query = """
                SELECT location_id FROM locations
                WHERE location_id = %s
                LIMIT 1;
                """
        with db.get_cursor() as cursor:
            cursor.execute(query, (followed_id,))
            if cursor.fetchone():
                is_location = True

    if is_user or is_location:

        with db.get_cursor() as cursor:
            query = """
                    SELECT 1 FROM follows
                    WHERE follower_id = %s and followable_type = %s and followable_id = %s
                    LIMIT 1;
                    """
            cursor.execute(query, (user_id, type, followed_id))
            is_followed = cursor.fetchone()
            if is_followed:
                return {(is_user, is_location):True}
            else:
                return {(is_user, is_location):False}
    else:
        return {(is_user, is_location):True}
