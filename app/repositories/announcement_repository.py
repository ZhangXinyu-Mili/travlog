from typing import Dict, List

from app import db


def db_get_all_announcements(current_page: int, page_size: int, query: str = "") -> List[Dict]:
    """Get all announcements with pagination and optional search query.

    Args:
        current_page (int): Current page number.
        page_size (int): Number of announcements per page.
        query (str): Optional search query to filter announcements by title or content.

    Returns:
        List[Dict]: List of announcements.
    """
    offset = (current_page - 1) * page_size
    search_query = f"%{query}%" if query else "%"
    with db.get_cursor() as cursor:
        sql_query = """
            SELECT
                a.announcement_id,
                a.title,
                a.content,
                a.created_at,
                a.is_new,
                u.username AS publisher
            FROM announcements AS a
            LEFT JOIN users AS u ON a.user_id = u.user_id
            WHERE a.title LIKE %s OR a.content LIKE %s
            ORDER BY a.announcement_id DESC
            LIMIT %s OFFSET %s;
        """
        cursor.execute(sql_query, (search_query, search_query, page_size, offset))
        announcements = cursor.fetchall()
        return announcements

def db_get_announcements_count(query: str = "") -> int:
    """Get the total count of announcements with an optional search query.

    Args:
        query (str): Optional search query to filter announcements by title or content.

    Returns:
        int: Total count of announcements.
    """
    search_query = f"%{query}%" if query else "%"
    with db.get_cursor() as cursor:
        sql_query = """
            SELECT COUNT(*) AS count
            FROM announcements
            WHERE title LIKE %s OR content LIKE %s;
        """
        cursor.execute(sql_query, (search_query, search_query))
        count = cursor.fetchone()
        return count["count"]

def db_get_announcements(is_new: bool) -> List[Dict]:
    """Get announcements with the username of the publisher.

    Args:
        is_new (bool): Get new announcements.

    Returns:
        List[Dict]: List of announcements with publisher usernames.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT
                    a.announcement_id,
                    a.title,
                    a.content,
                    a.created_at,
                    a.is_new,
                    u.username AS publisher
                FROM announcements AS a
                LEFT JOIN users AS u ON a.user_id = u.user_id
                WHERE a.is_new = %s
                ORDER BY a.announcement_id DESC;
                """
        cursor.execute(query, (is_new,))
        announcements = cursor.fetchall()
        return announcements

def db_get_announcement_by_id(announcement_id: int) -> Dict:
    """Get an announcement by its ID.

    Args:
        announcement_id (int): Announcement ID.

    Returns:
        Dict: Announcement details.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT
                    a.announcement_id,
                    a.title,
                    a.content,
                    a.created_at,
                    a.is_new,
                    u.username AS publisher
                FROM announcements AS a
                LEFT JOIN users AS u ON a.user_id = u.user_id
                WHERE a.announcement_id = %s;
                """
        cursor.execute(query, (announcement_id,))
        announcement = cursor.fetchone()
        return announcement

def db_create_announcement(
    user_id: int, title: str, content: str, is_new: bool, created_at: str
) -> None:
    """Create a new announcement.

    Args:
        user_id (int): User id of the publisher.
        title (str): Title of the announcement.
        content (str): Content of the announcement.
        is_new (bool): Is the announcement new.
        created_at (str): Created at timestamp.

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                INSERT INTO announcements (user_id, title, content, is_new, created_at)
                VALUES (%s, %s, %s, %s, %s);
                """
        cursor.execute(query, (user_id, title, content, is_new, created_at))

def db_update_announcement(
    announcement_id: int, title: str, content: str, is_new: bool
) -> None:
    """Update an announcement.

    Args:
        announcement_id (int): Announcement id.
        title (str): Title of the announcement.
        content (str): Content of the announcement.
        is_new (bool): Is the announcement new.

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE announcements
                SET title = %s, content = %s, is_new = %s
                WHERE announcement_id = %s;
                """
        cursor.execute(query, (title, content, is_new, announcement_id))

def db_update_announcement_status(
    announcement_id: int, is_new: bool
) -> None:
    """Update the status of an announcement.

    Args:
        announcement_id (int): Announcement id.
        is_new (bool): Is the announcement new.

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE announcements
                SET is_new = %s
                WHERE announcement_id = %s;
                """
        cursor.execute(query, (is_new, announcement_id))

def db_delete_announcement(announcement_id: int) -> None:
    """Delete an announcement.

    Args:
        announcement_id (int): Announcement id.

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = "DELETE FROM announcements WHERE announcement_id = %s;"
        cursor.execute(query, (announcement_id,))
