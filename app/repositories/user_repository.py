from typing import Dict, List, Optional

from app import db

def db_get_user_by_username(username: str) -> Dict:
    """Get user details by username.

    Args:
        username (str): Username of the user.

    Returns:
        Dict: User details.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT user_id, username, password_hash, role, status
                FROM users
                WHERE username = %s;
                """
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        return user


def db_get_user_by_id(user_id: int) -> Dict:
    """Get user details by user id.

    Args:
        user_id (int): User id.

    Returns:
        Dict: User details.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT user_id, username, email, email_public, first_name, last_name, name_public, location, profile_image, role, status, description,
                profile_public, places_public, likes_public, comments_public
                FROM users
                WHERE user_id = %s;
                """
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        return user


def db_get_user_by_email(email: str) -> Dict:
    """Get user details by email.

    Args:
        email (str): Email of the user.

    Returns:
        Dict: User details.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT user_id, username, password_hash, role
                FROM users
                WHERE email = %s;
                """
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        return user


def db_get_user_password_hash(user_id: int) -> str:
    """Get user password hash by user id.

    Args:
        user_id (int): User id.

    Returns:
        str: User password hash.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT password_hash
                FROM users
                WHERE user_id = %s;
                """
        cursor.execute(query, (user_id,))
        password = cursor.fetchone()
        return password["password_hash"]


def db_user_exists(username: str) -> bool:
    """Check if a user exists by username.

    Args:
        username (str): Username of the user.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    with db.get_cursor() as cursor:
        query = "SELECT user_id FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        return user is not None

def db_event_photo_exists(photo_path: str) -> bool:
    """Check if a event photo exists by photo_path.

    Args:
        photo_path (str): path of photo file.

    Returns:
        bool: True if the photo exists, False otherwise.
    """
    with db.get_cursor() as cursor:
        query = "SELECT event_id FROM event_photos WHERE photo_path = %s"
        cursor.execute(query, (photo_path,))
        user = cursor.fetchone()
        return user is not None

def db_create_user(
    username: str,
    password_hash: str,
    email: str,
    first_name: str,
    last_name: str,
    location: str,
    role: str,
    status: str,
) -> int:
    """Create a new user.

    Args:
        username (str): Username of the user.
        password_hash (str): Password hash of the user.
        email (str): Email of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        location (str): Location of the user.
        role (str): Role of the user. Available roles are "traveller", "editor" and "admin".
        status (str): Status of the user. Available statuses are "active", "blocked" and "banned".

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                INSERT INTO users (username, password_hash, email, first_name, last_name, location, profile_image, role, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
        cursor.execute(
            query,
            (
                username,
                password_hash,
                email,
                first_name,
                last_name,
                location,
                "",
                role,
                status,
            ),
        )
        return cursor.lastrowid


def db_update_user_profile(
    user_id: int, email: str, username: str, first_name: str, last_name: str, location: str,
    description: str, profile_image: str, name_public:bool, email_public:bool, profile_public:bool, places_public:bool, likes_public:bool, comments_public:bool
) -> None:
    """Update user profile details.

    Args:
        user_id (int): User id.
        email (str): Email of the user.
        username (str): Username of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        location (str): Location of the user.
        description (str): Description of the user.
        profile_image (str): Profile photo of the user.

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE users
                SET email = %s, username = %s, first_name = %s, last_name = %s, location = %s, description = %s, profile_image = %s, name_public = %s, email_public= %s, profile_public=%s, places_public = %s, likes_public= %s, comments_public=%s
                WHERE user_id = %s
                """
        cursor.execute(
            query,
            (
                email,
                username,
                first_name,
                last_name,
                location,
                description,
                profile_image,
                name_public,
                email_public,
                profile_public,
                places_public,
                likes_public,
                comments_public,
                user_id,
            ),
        )


def db_update_user_profile_image(user_id: int, profile_image: str) -> None:
    """Update user profile image.

    Args:
        user_id (int): User id.
        profile_image (str): Profile image file path.

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE users
                SET profile_image = %s
                WHERE user_id = %s
                """
        cursor.execute(query, (profile_image, user_id))


def db_remove_user_profile_image(user_id: int) -> None:
    """Remove user profile image.

    Args:
        user_id (int): User id.

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE users
                SET profile_image = NULL
                WHERE user_id = %s
                """
        cursor.execute(query, (user_id,))


def db_update_user_password(user_id: int, new_password_hash: str) -> None:
    """Update user password.

    Args:
        user_id (int): User id.
        new_password_hash (str): New password hash.

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE users
                SET password_hash = %s
                WHERE user_id = %s
                """
        cursor.execute(
            query,
            (
                new_password_hash,
                user_id,
            ),
        )


def db_update_user_status(user_id: int, status: str) -> None:
    """Update user status.

    Args:
        user_id (int): User id.
        status (str): User status. Available statuses are "active", "blocked" and "banned".

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE users
                SET status = %s
                WHERE user_id = %s
                """
        cursor.execute(
            query,
            (
                status,
                user_id,
            ),
        )


def db_update_user_role(user_id: int, role: str) -> None:
    """Update user role.

    Args:
        user_id (int): User id.
        role (str): User role. Available roles are "traveller", "editor", "supporttech", "moderator" and "admin".

    Returns:
        None
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE users
                SET role = %s
                WHERE user_id = %s
                """
        cursor.execute(
            query,
            (
                role,
                user_id,
            ),
        )


def db_get_users(
    current_page: int,
    page_size: int,
    q: Optional[str] = None,
    staff_only: Optional[bool] = False,
    blocked_only: Optional[bool] = False,
) -> List[Dict]:
    """Get users with pagination.

    Args:
        current_page (int): Current page number.
        page_size (int): Number of users per page.
        q (str): Search query.
        staff_only (bool): Show only staff users.

    Returns:
        List[Dict]: List of users.
    """
    offset = (current_page - 1) * page_size
    where_clause = ""
    params = [page_size, offset]
    if q:
        where_clause = "WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR email LIKE %s"
        params = [f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%", page_size, offset]
    # If staff_only is True, only show users with role "admin" and "editor" without search query
    if staff_only:
        where_clause = "WHERE role in %s"
        params = [["admin", "editor"], page_size, offset]
    # If blocked_only is True, only show users with block status without search query
    if blocked_only:
        where_clause = "WHERE status = 'blocked' "
        params = [page_size, offset]
    query = """
            SELECT user_id, username, email, first_name, last_name, location, profile_image, role, status
            FROM users
            """ + where_clause + """
            ORDER BY user_id DESC
            LIMIT %s OFFSET %s;
            """
    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        users = cursor.fetchall()
        return users


def db_get_users_count(q: Optional[str] = None, staff_only: Optional[bool] = False, blocked_only: Optional[bool] = False) -> int:

    """Get total number of users.

    Args:
        q (str): Search query.
        staff_only (bool): Show only staff users.

    Returns:
        int: Total number of users.
    """
    where_clause = ""
    params = []
    if q:
        where_clause = "WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR email LIKE %s"
        params = [f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"]
    # If staff_only is True, only show users with role "admin" and "editor" without search query
    if staff_only:
        where_clause = "WHERE role in %s"
        params = [["admin", "editor"]]
    # If blocked_only is True, only show users with block status without search query
    if blocked_only:
        where_clause = "WHERE status = 'blocked' "
    query = """
            SELECT COUNT(*) AS count
            FROM users
            """ + where_clause

    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        count = cursor.fetchone()
        return count["count"]

def db_get_helpdesk_staff() -> Dict:
    """Get helpdesk staff details.

    Returns:
        Dict: Users details.
    """
    with db.get_cursor() as cursor:
        query = """
                SELECT user_id, username
                FROM users
                WHERE role IN ('admin', 'editor', 'supporttech');
                """
        cursor.execute(query,)
        users = cursor.fetchall()
        return users