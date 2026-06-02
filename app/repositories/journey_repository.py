from datetime import datetime
from typing import Dict, List, Optional

from app import db


def db_add_new_journey(
    user_id: int,
    title: str,
    description: str,
    startDate: str,
    status: str,
    created_at: str,
) -> None:
    with db.get_cursor() as cursor:
        qstr = """
               INSERT INTO `journeys` (`user_id`, `title`, `description`, `start_date`, `status`, `created_at`)
               VALUES(%s, %s, %s, %s, %s, %s);
               """
        qargs = (user_id, title, description, startDate, status, created_at)
        cursor.execute(qstr, qargs)


# Edit a journey
def db_edit_my_journey(
    journey_id: int, title: str, description: str, startDate: str, status: str
) -> None:
    with db.get_cursor() as cursor:
        qstr = """
               UPDATE journeys
               set title = %s, description = %s, start_date = %s, status = %s
               WHERE journey_id = %s;
               """
        qargs = (title, description, startDate, status, journey_id)
        cursor.execute(qstr, qargs)


## Journeys


def db_get_journeys_by_user_id(
    user_id: int, current_page: int, page_size: int
) -> List[Dict]:
    """Get journeys by user id with pagination.

    Args:
        user_id (int): User id.
        current_page (int): Current page number.
        page_size (int): Number of journeys per page.

    Returns:
        List[Dict]: List of journeys.
    """
    offset = (current_page - 1) * page_size
    with db.get_cursor() as cursor:
        query = """
                SELECT journey_id, user_id, title, description, start_date, status, is_hidden, created_at, photo
                FROM journeys
                WHERE user_id = %s
                ORDER BY start_date DESC
                LIMIT %s OFFSET %s;
                """
        cursor.execute(query, (user_id, page_size, offset))
        journeys = cursor.fetchall()
        return journeys


def db_get_journeys_count_by_user_id(user_id: int) -> int:
    """Get total number of journeys by user id.

    Args:
        user_id (int): User id.

    Returns:
        int: Total number of journeys.
    """
    with db.get_cursor() as cursor:
        query = "SELECT COUNT(*) AS count FROM journeys WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        count = cursor.fetchone()
        if count is None:
            return 0
        return count["count"]


def db_get_journey_by_journey_id(journey_id: int) -> Dict:
    """Get journey by journey id.

    Args:
        journey_id (int): Journey id.

    Returns:
        Dict: Journey details.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT
                    j.journey_id, j.user_id, j.title, j.description, j.status, j.is_hidden, j.start_date, j.photo, u.username, j.first_viewer_id
                FROM
                    journeys AS j
                LEFT JOIN
                    users AS u ON u.user_id = j.user_id
                WHERE
                    j.journey_id = %s;
                """
        cursor.execute(query, (journey_id,))
        journey = cursor.fetchone()
        return journey


def db_update_journey_title_and_description(
    journey_id: int, title: str, description: str
) -> None:
    """Update journey title and description. This function is used by editors and admins.

    Args:
        journey_id (int): Journey id.
        title (str): Title of the journey.
        description (str): Description of the journey.
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE journeys
                SET title = %s, description = %s
                WHERE journey_id = %s;
                """
        cursor.execute(query, (title, description, journey_id))


def db_set_journey_visibility(journey_id: int, is_hidden: bool) -> None:
    """Set journey visibility to other users.
    Args:
        journey_id (int): Journey id.
        is_hidden (bool): visibility to other users.
    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE journeys
                SET is_hidden = %s
                WHERE journey_id = %s;
                """
        cursor.execute(query, (is_hidden, journey_id))


def db_get_events_by_journey_id(journey_id: int) -> Dict:
    """Get events by journey id.

    Args:
        journey_id (int): Journey id.

    Returns:
        Dict: Events details.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT
                    event_id, title, description, start_datetime, end_datetime, like_count, comments_count, location_name, events.location_id
                FROM
                    events
                LEFT JOIN
                    locations ON events.location_id = locations.location_id
                WHERE
                    journey_id = %s
                ORDER BY
                    events.start_datetime ASC;
                """
        cursor.execute(query, (journey_id,))
        events = cursor.fetchall()
        return events


def db_set_journey_publicity(journey_id: int, status: str) -> None:
    """Set journey visibility.

    Args:
        journey_id (int): Journey id.
        status (str): Status.

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE journeys
                SET status = %s
                WHERE journey_id = %s;
                """
        cursor.execute(query, (status, journey_id))


def db_delete_journey(journey_id: int) -> None:
    """Delete journey.

    Args:
        journey_id (int): Journey id.

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = "DELETE FROM events WHERE journey_id = %s;"
        cursor.execute(query, (journey_id,))
        query = "DELETE FROM journeys WHERE journey_id = %s;"
        cursor.execute(query, (journey_id,))


def db_get_event_by_event_id(event_id: int) -> Dict:
    """Get event by event id.

    Args:
        event_id (int): Event id.

    Returns:
        Dict: Event details.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT
                    event_id, journey_id, title, description, start_datetime, end_datetime, location_name, like_count
                FROM
                    events
                LEFT JOIN
                    locations ON events.location_id = locations.location_id
                WHERE
                    event_id = %s;
                """
        cursor.execute(query, (event_id,))
        events = cursor.fetchone()
        return events


def db_get_event_photos_by_event_id(event_id: int) -> Dict:
    """Get event photos by event id.

    Args:
        event_id (int): Event id.

    Returns:
        Dict: Event details.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT
                    photo_id, photo_path
                FROM
                    event_photos
                WHERE
                    event_id = %s;
                """
        cursor.execute(query, (event_id,))
        photos = cursor.fetchall()
        return photos


def db_update_event(event_id: int, title: str, description: str) -> None:
    """Update Event title, description. This function is used by editors and admins.

    Args:
        event_id (int): Event id.
        title (str): Title of the event.
        description (str): Description of the event.
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE events
                SET title = %s, description = %s
                WHERE event_id = %s;
                """
        cursor.execute(query, (title, description, event_id))


##public journeys
def db_get_public_journeys(current_page: int, page_size: int) -> List[Dict]:
    offset = (current_page - 1) * page_size
    with db.get_cursor() as cursor:
        query = """
                SELECT journey_id, username, title, journeys.description, start_date, journeys.status, journeys.created_at, journeys.photo, journeys.user_id
                FROM journeys
                LEFT JOIN users ON users.user_id = journeys.user_id
                WHERE journeys.status IN ('public', 'published') and is_hidden = False
                ORDER BY journeys.created_at DESC
                LIMIT %s OFFSET %s;
                """
        cursor.execute(query, (page_size, offset))
        journeys = cursor.fetchall()
        return journeys


def db_get_public_journeys_count() -> int:
    with db.get_cursor() as cursor:
        query = "SELECT COUNT(*) AS count FROM journeys WHERE status IN ('public', 'published') and is_hidden = False;"
        cursor.execute(query)
        count = cursor.fetchone()
        if count is None:
            return 0
        return count["count"]


# search public journeys by title and description
def db_search_public_journey(
    keyword: str, current_page: int, page_size: int
) -> List[Dict]:
    """Search Journey by title or description.

    Args:
        query (str): Search query.
        current_page (int): Current page number.
        page_size (int): Number of users per page.

    Returns:
        List[Dict]: List of journeys.
    """
    offset = (current_page - 1) * page_size

    with db.get_cursor() as cursor:
        keyword = f"%{keyword}%"
        sql_query = """
                    SELECT DISTINCT journeys.journey_id, username, journeys.title, journeys.description, journeys.start_date, journeys.status, journeys.created_at, locations.location_id, locations.location_name, journeys.photo
                    FROM journeys
                    LEFT JOIN users ON users.user_id = journeys.user_id
                    LEFT JOIN events ON events.journey_id = journeys.journey_id
                    LEFT JOIN locations ON locations.location_id = events.location_id
                    WHERE journeys.status IN ('public', 'published') and is_hidden = False and (journeys.title LIKE %s or journeys.description LIKE %s or locations.location_name LIKE %s)
                    ORDER BY start_date DESC
                    LIMIT %s OFFSET %s;
                    """
        cursor.execute(sql_query, (keyword, keyword, keyword, page_size, offset))
        journeys = cursor.fetchall()
        return journeys


def db_search_public_journeys_count(keyword: str) -> int:

    with db.get_cursor() as cursor:
        keyword = f"%{keyword}%"
        query = """
                SELECT COUNT(DISTINCT journeys.journey_id) AS count
                FROM journeys
                LEFT JOIN events ON events.journey_id = journeys.journey_id
                LEFT JOIN locations ON locations.location_id = events.location_id
                WHERE journeys.status IN ('public', 'published') and is_hidden = False and (journeys.title LIKE %s or journeys.description LIKE %s or locations.location_name LIKE %s);
                """
        cursor.execute(query, (keyword, keyword, keyword))
        count = cursor.fetchone()
        if count is None:
            return 0
        return count["count"]


# hidden journeys
def db_get_hidden_journeys(current_page: int, page_size: int) -> List[Dict]:
    offset = (current_page - 1) * page_size
    with db.get_cursor() as cursor:
        query = """
                SELECT
                    users.user_id,
                    users.username,
                    GROUP_CONCAT(journeys.journey_id, ',', journeys.title ORDER BY journeys.created_at) AS journey_ids_and_titles
                FROM journeys
                LEFT JOIN users ON users.user_id = journeys.user_id
                WHERE journeys.status IN ('public', 'published') and journeys.is_hidden = True
                GROUP BY users.username
                ORDER BY users.username
                LIMIT %s OFFSET %s;
                """
        cursor.execute(query, (page_size, offset))
        journeys = cursor.fetchall()
        return journeys


def db_get_hidden_journeys_count() -> int:
    with db.get_cursor() as cursor:
        query = "SELECT COUNT(*) AS count FROM journeys WHERE is_hidden = True;"
        cursor.execute(query)
        count = cursor.fetchone()
        if count is None:
            return 0
        return count["count"]


## Events
def db_add_events(
    journey_id: int,
    title: str,
    description: str,
    start_datetime: datetime,
    end_datetime: Optional[datetime],
    location: Optional[str],
    user_id: int,
) -> tuple[int, bool]:
    """Add event to a journey.
    title, description, start_datetime
    Args:
        journey_id (int): journey id.
        title (str): event title.
        description (str): event description.
        start_datetime (datetime): event start date and time.
        end_datetime (datetime): event end date and time.
        location (str): event location

    Returns:
        int: event id.
    """

    with db.get_cursor() as cursor:
        count_location_query = """
            SELECT COUNT(DISTINCT locations.location_id) AS location_count
            FROM users
            JOIN journeys ON journeys.user_id = users.user_id
            JOIN events ON events.journey_id = journeys.journey_id
            JOIN locations ON locations.location_id = events.location_id
            WHERE users.user_id = %s AND events.location_id IS NOT NULL;
        """
        cursor.execute(count_location_query, (user_id,))
        initial_count = cursor.fetchone()["location_count"] or 0

        location_id = None

        if location:
            sql_query = "INSERT INTO locations (location_name) VALUES (%s);"

            cursor.execute(
                "SELECT * FROM locations WHERE location_name like %s;", (location,)
            )
            exists_location = cursor.fetchone()
            if exists_location:
                location_id = exists_location["location_id"]
            else:
                cursor.execute(sql_query, (location,))
                location_id = cursor.lastrowid

        sql_query = """
                    INSERT INTO events (journey_id, title, description, start_datetime, end_datetime, location_id)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """
        cursor.execute(
            sql_query,
            (journey_id, title, description, start_datetime, end_datetime, location_id),
        )
        event_id = cursor.lastrowid

        cursor.execute(count_location_query, (user_id,))
        updated_count = cursor.fetchone()["location_count"] or 0

        is_new_location_for_user = updated_count > initial_count
        return event_id, is_new_location_for_user


def db_get_location_options(journey_id: int) -> List[Dict]:
    """Get an option list of event locations for users whening adding a event.
    Args:
        journey_id (int): journey id.

    Returns:
        List[Dict]: List of locations.
    """
    with db.get_cursor() as cursor:

        sql_query = """
                    SELECT distinct l.location_id, l.location_name
                    FROM events e
                    RIGHT JOIN locations l ON l.location_id = e.location_id
                    WHERE l.location_id in
	                    (
                            SELECT distinct e1.location_id
                            FROM events e1
                            INNER JOIN journeys j1 ON j1.journey_id = e1.journey_id
                            INNER JOIN users u1 ON u1.user_id = j1.user_id
                            INNER JOIN (select j2.user_id from journeys j2 inner join users u2 where j2.journey_id =%s) g1
								ON g1.user_id = u1.user_id
                            WHERE e1.location_id is not NULL
                        )
                    ORDER BY l.location_name;
                    """
        cursor.execute(sql_query, (journey_id,))
        my_locations = cursor.fetchall()

        sql_query = """
                    SELECT distinct l.location_id, l.location_name
                    FROM events e
                    RIGHT JOIN locations l ON l.location_id = e.location_id
                    WHERE l.location_id NOT in
	                    (
                            SELECT distinct e1.location_id
                            FROM events e1
                            INNER JOIN journeys j1 ON j1.journey_id = e1.journey_id
                            INNER JOIN users u1 ON u1.user_id = j1.user_id
                            INNER JOIN (select j2.user_id from journeys j2 inner join users u2 where j2.journey_id =%s) g1
								ON g1.user_id = u1.user_id
                            WHERE e1.location_id is not NULL
                        )
                    ORDER BY l.location_name;
                    """
        cursor.execute(sql_query, (journey_id,))
        other_locations = cursor.fetchall()

        locations = []
        locations.append(my_locations)
        locations.append(other_locations)
        return locations


def db_get_user_id_by_journey_id(journey_id: int) -> int:
    """Get user id of a user by journey id.
    Args:
        journey_id (int): journey id.

    Returns:
        int: user id.
    """
    with db.get_cursor() as cursor:

        sql_query = """
                    SELECT distinct u1.user_id
                    FROM journeys j1
                    INNER JOIN users u1 ON u1.user_id = j1.user_id
                    WHERE j1.journey_id = %s;
                    """
        cursor.execute(sql_query, (journey_id,))
        result = cursor.fetchone()
        user_id = None
        if result:
            user_id = result["user_id"]
        return user_id


def db_get_user_id_by_event_id(event_id: int) -> int:
    """Get user id of a user by event id.
    Args:
        event_id (int): event id.

    Returns:
        int: user id.
    """
    with db.get_cursor() as cursor:

        sql_query = """
                    SELECT distinct j1.user_id
                    FROM events e1
                    INNER JOIN journeys j1 ON j1.journey_id = e1.journey_id
                    WHERE e1.event_id = %s;
                    """
        cursor.execute(sql_query, (event_id,))
        result = cursor.fetchone()
        user_id = None
        if result:
            user_id = result["user_id"]
        return user_id


def db_save_event_photo(file_path: str, event_id: int) -> None:
    """Save event photo path to event_photos table.
    Args:
        file_path (str): file save path.
        event_id (int): event id.
    Returns:
        None
    """
    with db.get_cursor() as cursor:
        sql_query = """
            INSERT INTO event_photos (event_id, photo_path)
            VALUES (%s, %s);
        """
        cursor.execute(sql_query, (event_id, file_path))


def db_save_journey_photo(file_path: str, journey_id: int) -> None:
    """Save journey photo path to journey table.
    Args:
        file_path (str): file save path.
        journey_id (int): journey id.
    Returns:
        None
    """
    with db.get_cursor() as cursor:
        sql_query = "UPDATE journeys SET photo = %s where journey_id = %s;"
        cursor.execute(
            sql_query,
            (
                file_path,
                journey_id,
            ),
        )


def db_edit_event(
    event_id: int,
    title: str,
    description: str,
    start_datetime: datetime,
    end_datetime: Optional[datetime],
    location: Optional[str],
    user_id: int,
) -> bool:
    """Edit an event, including title, description, start_datetime, end_datetime, location
    Args:
        event_id (int): event id.
        title (str): event title.
        description (str): event description.
        start_datetime (datetime): event start date and time.
        end_datetime (datetime): event end date and time.
        location (str): event location

    Returns:
        None.
    """

    with db.get_cursor() as cursor:
        count_location_query = """
            SELECT COUNT(DISTINCT locations.location_id) AS location_count
            FROM users
            JOIN journeys ON journeys.user_id = users.user_id
            JOIN events ON events.journey_id = journeys.journey_id
            JOIN locations ON locations.location_id = events.location_id
            WHERE users.user_id = %s AND events.location_id IS NOT NULL;
        """
        cursor.execute(count_location_query, (user_id,))
        initial_count = cursor.fetchone()["location_count"] or 0

        location_id = None
        if location:
            sql_query = "INSERT INTO locations (location_name) VALUES (%s);"

            cursor.execute(
                "SELECT * FROM locations WHERE location_name like %s;", (location,)
            )
            exists_location = cursor.fetchone()
            if exists_location:
                location_id = exists_location["location_id"]
            else:
                cursor.execute(sql_query, (location,))
                location_id = cursor.lastrowid

        sql_query = """
                    UPDATE events SET title = %s, description = %s, start_datetime =%s, end_datetime =%s, location_id = %s WHERE event_id = %s;
                    """
        cursor.execute(
            sql_query,
            (title, description, start_datetime, end_datetime, location_id, event_id),
        )

        cursor.execute(count_location_query, (user_id,))
        updated_count = cursor.fetchone()["location_count"] or 0

        is_new_location_for_user = updated_count > initial_count

        return is_new_location_for_user



def db_remove_journey_photo(journey_id: int) -> None:
    """Save journey photo path to journey table.
    Args:
        journey_id (int): journey id.
    Returns:
        None
    """
    with db.get_cursor() as cursor:
        sql_query = "UPDATE journeys SET photo = NULL where journey_id = %s;"
        cursor.execute(sql_query, (journey_id,))


def db_delete_event_photos(photo_id: int) -> None:
    """Delete photo from event_photos table.
    Args:
        photo_id (int): photo id.
    Returns:
        None
    """
    with db.get_cursor() as cursor:

        sql_query = "DELETE FROM event_photos WHERE photo_id = %s"
        cursor.execute(sql_query, (photo_id,))


def db_delete_event(event_id: int) -> None:
    """Delete an event in a journey.
    Args:
        event_id (int): event id.
    Returns:
        None
    """
    with db.get_cursor() as cursor:

        sql_query = "DELETE FROM events WHERE event_id = %s;"
        cursor.execute(sql_query, (event_id,))


def db_update_event_location_by_editor_admin(
    event_id: int, previous_location: str, location: Optional[str]
) -> None:
    """Update event location
    Args:
        event_id (int): event id.
        previous_location (str): previous event location.
        location (str): new event location.

    Returns:
        None.
    """

    with db.get_cursor() as cursor:

        location_id = None
        if location:
            sql_query = "INSERT INTO locations (location_name) VALUES (%s);"

            cursor.execute(
                "SELECT * FROM locations WHERE location_name like %s;", (location,)
            )
            exists_location = cursor.fetchone()
            if exists_location:
                location_id = exists_location["location_id"]
            else:
                cursor.execute(sql_query, (location,))
                location_id = cursor.lastrowid

        previous_location_id = None
        if previous_location:
            cursor.execute(
                "SELECT location_id FROM locations WHERE location_name like %s;",
                (previous_location,),
            )
            result = cursor.fetchone()
            if result:
                previous_location_id = result["location_id"]

        if previous_location_id and location_id:
            if previous_location_id == location_id:
                return
            sql_query = """
                        UPDATE events SET location_id = %s WHERE location_id = %s;
                        """
            cursor.execute(sql_query, (location_id, previous_location_id))
            sql_query = "DELETE FROM locations WHERE location_id = %s;"
            cursor.execute(sql_query, (previous_location_id,))
        else:
            sql_query = """
                        UPDATE events SET location_id = %s WHERE event_id = %s;
                        """
            cursor.execute(sql_query, (location_id, event_id))


# Published journeys
def db_get_published_journeys(
    logged_in: bool, current_page: int, page_size: int
) -> List[Dict]:
    offset = (current_page - 1) * page_size
    query = """
            SELECT journey_id, username, title, journeys.description, start_date, journeys.status, journeys.created_at, journeys.photo, journeys.user_id
            FROM journeys
            INNER JOIN users ON users.user_id = journeys.user_id
            LEFT JOIN subscriptions ON subscriptions.user_id = users.user_id
            WHERE journeys.status = 'published' AND is_hidden = 0 AND (subscriptions.end_datetime > %s OR users.role IN ("admin", "editor"))
            ORDER BY journeys.created_at DESC
            LIMIT %s OFFSET %s;
            """
    params = (datetime.now(), page_size, offset)
    if logged_in:
        query = """
                SELECT journey_id, username, title, journeys.description, start_date, journeys.status, journeys.created_at, journeys.photo, journeys.user_id
                FROM journeys
                INNER JOIN users ON users.user_id = journeys.user_id
                WHERE journeys.status = 'published' AND is_hidden = 0
                ORDER BY journeys.created_at DESC
                LIMIT %s OFFSET %s;
                """
        params = (page_size, offset)
    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        journeys = cursor.fetchall()
        return journeys


def db_get_published_journeys_count(logged_in: bool) -> int:
    query = """
            SELECT COUNT(*) as count
            FROM journeys
            INNER JOIN users ON users.user_id = journeys.user_id
            LEFT JOIN subscriptions ON subscriptions.user_id = users.user_id
            WHERE journeys.status = 'published' AND is_hidden = 0 AND (subscriptions.end_datetime > %s OR users.role IN ("admin", "editor"));
            """
    params = (datetime.now(),)
    if logged_in:
        query = """
                SELECT COUNT(*) as count
                FROM journeys
                INNER JOIN users ON users.user_id = journeys.user_id
                WHERE journeys.status = 'published' AND is_hidden = 0;
                """
        params = ()
    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        count = cursor.fetchone()
        return count["count"]


def db_get_location_by_id(location_id: int) -> Dict:
    query = "SELECT * FROM locations WHERE location_id = %s;"
    with db.get_cursor() as cursor:
        cursor.execute(query, (location_id,))
        return cursor.fetchone()


def db_get_journey_duration(journey_id) -> Dict:
    query = """
        SELECT
            MAX(events.start_datetime) as max_start_datetime,
            MAX(events.end_datetime) as max_end_datetime,
            MIN(events.start_datetime) as min_start_datetime,
            MIN(events.end_datetime) as min_end_datetime
        FROM events WHERE events.journey_id = %s;
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (journey_id,))
        return cursor.fetchone()

def db_create_first_viewer(journey_id: int, first_viewer_id: int) -> None:
    query = """
            UPDATE journeys
            SET first_viewer_id = %s 
            WHERE journey_id = %s and first_viewer_id is Null;
            """
    with db.get_cursor() as cursor:
        cursor.execute(query, (first_viewer_id, journey_id))

