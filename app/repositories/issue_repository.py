from typing import Dict, List
from app import db


def db_add_helpdesk_issue(
    title: str, category: str, content: str, status: str, user_id: str
) -> None:
    with db.get_cursor() as cursor:
        qstr = """
               INSERT INTO `issues` (`title`, `category`, `content`, `status`, `user_id`)
               VALUES(%s, %s, %s, %s, %s);
               """
        qargs = (title, category, content, status, user_id)
        cursor.execute(qstr, qargs)


# get all helpdesk issues made by a user
def db_get_helpdesk_issues_by_user_id(
    user_id: int, current_page: int = 1, page_size: int = 10
) -> List[Dict]:
    """Get paginated issues (not deleted) for a user"""
    offset = (current_page - 1) * page_size
    with db.get_cursor() as cursor:
        query = """
            SELECT i.user_id, i.issue_id, i.title, i.category, i.content, i.status, i.created_at
            FROM issues i
            WHERE i.user_id = %s AND i.status != 'Delete'
            ORDER BY i.created_at DESC
            LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (user_id, page_size, offset))
        return cursor.fetchall()


def db_get_helpdesk_issue_by_id(issue_id: int) -> Dict:
    """Get a single helpdesk issue by its id, including the username."""
    with db.get_cursor() as cursor:
        query = """
            SELECT i.*, u.username
            FROM issues i
            JOIN users u ON i.user_id = u.user_id
            WHERE i.issue_id = %s
            LIMIT 1
        """
        cursor.execute(query, (issue_id,))
        return cursor.fetchone()


def db_get_helpdesk_comments_by_issue_id(
    issue_id: int, page: int = 1, per_page: int = 10
) -> list:
    """Get paginated comments for a helpdesk issue, with user info."""
    offset = (page - 1) * per_page
    with db.get_cursor() as cursor:
        query = """
            SELECT ic.*, u.username AS user_name
            FROM issue_comments ic
            JOIN users u ON ic.user_id = u.user_id
            WHERE ic.issue_id = %s
            ORDER BY ic.created_at ASC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (issue_id, per_page, offset))
        return cursor.fetchall()


def db_add_helpdesk_comment(issue_id: int, user_id: int, content: str) -> None:
    """Add a comment to a helpdesk issue."""
    with db.get_cursor() as cursor:
        query = """
            INSERT INTO issue_comments (issue_id, user_id, content, created_at)
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(query, (issue_id, user_id, content))


def db_get_helpdesk_comments_count_by_issue_id(issue_id: int) -> int:
    """Return the total number of comments for a helpdesk issue."""
    with db.get_cursor() as cursor:
        query = "SELECT COUNT(*) as count FROM issue_comments WHERE issue_id = %s"
        cursor.execute(query, (issue_id,))
        result = cursor.fetchone()
        return result["count"] if result else 0


def db_get_helpdesk_issues_count_by_user_id(user_id: int) -> int:
    """Return the total number of issues for a user."""
    with db.get_cursor() as cursor:
        query = "SELECT COUNT(*) as count FROM issues WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result["count"] if result else 0


def db_get_all_helpdesk_issues(
    status_filter: str | None = None,
    category_filter: str | None = None,
    premium_filter: str | None = None,
    current_page: int = 1,
    page_size: int = 10,
) -> List[Dict]:
    """Get paginated issues for the helpdesk queue with optional status and category filters"""
    offset = (current_page - 1) * page_size
    with db.get_cursor() as cursor:
        query_conditions = []
        query_params = []

        if premium_filter and premium_filter != "All":
            query_conditions.append(
                "u.role IN ('admin', 'editor', 'moderator', 'supporttech') OR s.end_datetime > NOW()"
            )

        if status_filter and status_filter != "All":
            query_conditions.append("i.status = %s")
            query_params.append(status_filter)

        if category_filter and category_filter != "All":
            query_conditions.append("i.category = %s")
            query_params.append(category_filter)

        where_clause = "WHERE i.status != 'Delete'"
        if query_conditions:
            where_clause += " AND " + " AND ".join(query_conditions)

        query = f"""
            SELECT i.issue_id, i.title, i.category, i.content, i.status, i.created_at, 
                   i.user_id, u.username, u.role, i.assigned_to, s.end_datetime AS subscription_end_date,
                   CASE WHEN i.assigned_to IS NOT NULL THEN a.username ELSE NULL END AS assignee_name
            FROM issues i
            LEFT JOIN subscriptions s ON s.user_id = i.user_id
            JOIN users u ON i.user_id = u.user_id
            LEFT JOIN users a ON i.assigned_to = a.user_id
            {where_clause}
            ORDER BY i.created_at DESC
            LIMIT %s OFFSET %s;
        """

        query_params.extend([page_size, offset])
        cursor.execute(query, tuple(query_params))
        return cursor.fetchall()


def db_get_all_helpdesk_issues_count(
    status_filter: str | None = None,
    category_filter: str | None = None,
    premium_filter: str | None = None,
) -> int:
    """Return the total number of issues in the helpdesk queue with optional status and category filters"""
    with db.get_cursor() as cursor:
        query_conditions = []
        query_params = []

        if premium_filter and premium_filter != "All":
            query_conditions.append(
                "u.role IN ('admin', 'editor', 'moderator', 'supporttech') OR s.end_datetime > NOW()"
            )

        if status_filter and status_filter != "All":
            query_conditions.append("i.status = %s")
            query_params.append(status_filter)

        if category_filter and category_filter != "All":
            query_conditions.append("i.category = %s")
            query_params.append(category_filter)

        where_clause = "WHERE i.status != 'Delete'"
        if query_conditions:
            where_clause += " AND " + " AND ".join(query_conditions)

        query = f"""
            SELECT COUNT(*) as count
            FROM issues i
            LEFT JOIN subscriptions s ON s.user_id = i.user_id
            JOIN users u ON i.user_id = u.user_id
            {where_clause}
        """
        cursor.execute(query, tuple(query_params))
        result = cursor.fetchone()
        return result["count"] if result else 0


def db_assign_helpdesk_issue(issue_id: int, user_id: int) -> bool:
    """Assign a helpdesk issue to a support technician"""
    with db.get_cursor() as cursor:
        status_query = "SELECT status FROM issues WHERE issue_id = %s"
        cursor.execute(status_query, (issue_id,))
        result = cursor.fetchone()

        if not result:
            return False

        # Don't change status if it's already Resolved or Stalled
        current_status = result["status"]
        new_status = current_status
        if current_status not in ["Resolved", "Stalled"]:
            new_status = "Open"

        # Update the assignment and status
        query = """
            UPDATE issues 
            SET assigned_to = %s, 
                status = %s
            WHERE issue_id = %s
        """
        cursor.execute(query, (user_id, new_status, issue_id))
        return cursor.rowcount > 0


def db_get_issue_statuses() -> List[str]:
    """Get all unique issue statuses for filtering"""
    with db.get_cursor() as cursor:
        query = "SELECT DISTINCT status FROM issues ORDER BY status"
        cursor.execute(query)
        return [row["status"] for row in cursor.fetchall()]


def db_get_issue_categories() -> List[str]:
    """Get all unique issue categories for filtering"""
    with db.get_cursor() as cursor:
        query = "SELECT DISTINCT category FROM issues ORDER BY category"
        cursor.execute(query)
        return [row["category"] for row in cursor.fetchall()]


def db_update_issue_status(issue_id: int, status: str) -> None:
    """update issue status.

    Args:
        issue_id (int): Issue id.
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE issues
                SET status = %s
                WHERE issue_id = %s;
                """
        cursor.execute(query, (status, issue_id))


def db_drop_issue_assignment(issue_id: int) -> bool:
    """Remove the assignment from an issue and set its status back to New
    """
    with db.get_cursor() as cursor:
        query = """
                UPDATE issues
                SET assigned_to = NULL, status = 'New'
                WHERE issue_id = %s
                """
        cursor.execute(query, (issue_id,))
        return cursor.rowcount > 0
