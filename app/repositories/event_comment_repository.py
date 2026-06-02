from typing import Dict, List
from app import db


def db_get_event_comments(
    event_id: int, user_id: int, page: int = 1, per_page: int = 10
) -> List[Dict]:
    """Get paginated comments for an event"""
    offset = (page - 1) * per_page
    with db.get_cursor() as cursor:
        query = """
            SELECT c.*, u.username, u.first_name, u.last_name, r.report_id
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            LEFT JOIN reports r ON r.comment_id = c.comment_id AND r.user_id = %s
            WHERE c.event_id = %s
            ORDER BY c.created_at ASC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (user_id, event_id, per_page, offset))
        return cursor.fetchall()


def db_get_event_comments_count_by_event_id(event_id: int) -> int:
    """Get total number of comments for an event"""
    query = "SELECT COUNT(*) as count FROM comments WHERE event_id = %s"
    with db.get_cursor() as cursor:
        cursor.execute(query, (event_id,))
        result = cursor.fetchone()
        return result["count"] if result else 0


def db_add_comment(event_id: int, user_id: int, content: str) -> None:
    """Add a new comment to an event."""
    with db.get_cursor() as cursor:
        try:
            # Start transaction
            cursor.execute("START TRANSACTION;")

            # Insert the comment
            query = """
                INSERT INTO comments (event_id, user_id, content, created_at)
                VALUES (%s, %s, %s, NOW());
            """
            cursor.execute(query, (event_id, user_id, content))

            # Update the event's comment count
            update_query = """
                UPDATE events
                SET comments_count = comments_count + 1
                WHERE event_id = %s;
            """
            cursor.execute(update_query, (event_id,))

            # Commit transaction
            cursor.execute("COMMIT;")
        except Exception as e:
            # Rollback transaction in case of error
            cursor.execute("ROLLBACK;")
            raise e


def db_get_comment(comment_id: int) -> dict | None:
    """Get a single comment by ID"""
    with db.get_cursor() as cursor:
        query = """
            SELECT c.*, u.username, u.first_name, u.last_name
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.comment_id = %s
        """
        cursor.execute(query, (comment_id,))
        result = cursor.fetchone()
        return result if result else None


def db_update_comment(comment_id: int, content: str) -> None:
    """Update a comment"""
    with db.get_cursor() as cursor:
        query = """
            UPDATE comments
            SET content = %s,
                updated_at = NOW()
            WHERE comment_id = %s
        """
        cursor.execute(query, (content, comment_id))


def db_delete_comment(comment_id: int) -> None:
    """Delete a comment."""
    with db.get_cursor() as cursor:
        try:
            # Start transaction
            cursor.execute("START TRANSACTION;")

            # Update the event's comment count
            update_query = """
                UPDATE events
                SET comments_count = comments_count - 1
                WHERE event_id = (SELECT event_id FROM comments WHERE comment_id = %s);
            """
            cursor.execute(update_query, (comment_id,))

            # Delete the comment
            delete_query = "DELETE FROM comments WHERE comment_id = %s"
            cursor.execute(delete_query, (comment_id,))

            # Delete associated reports
            delete_reports_query = "DELETE FROM reports WHERE comment_id = %s"
            cursor.execute(delete_reports_query, (comment_id,))

            # Delete associated reactions
            delete_reactions_query = "DELETE FROM reactions WHERE comment_id = %s"
            cursor.execute(delete_reactions_query, (comment_id,))

            # Commit transaction
            cursor.execute("COMMIT;")
        except Exception as e:
            # Rollback transaction in case of error
            cursor.execute("ROLLBACK;")
            raise e


# reports
def db_create_report(comment_id: int, user_id: int, reason: str) -> None:
    """Report a comment"""
    query = """
        INSERT INTO reports (comment_id, user_id, reason)
        VALUES (%s, %s, %s)
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (comment_id, user_id, reason))


def db_get_reported_comments(
    current_page: int, page_size: int, is_hidden: bool | None, escalated: bool | None
) -> List[Dict]:
    """List reported comment"""
    offset = (current_page - 1) * page_size

    where_clause = ""
    where_clauses = []
    params = []
    if is_hidden == True and escalated == True:
        where_clause = "WHERE comments.is_hidden = True OR comments.escalated = True"
    else:
        if is_hidden != None:
            where_clauses.append("comments.is_hidden = %s")
            params.append(int(is_hidden))
        if escalated != None:
            where_clauses.append("comments.escalated = %s")
            params.append(escalated)
        if len(where_clauses) != 0:
            where_clause = " AND ".join(where_clauses)
            where_clause = f"WHERE {where_clause}"

    params.append(page_size)
    params.append(offset)
    query = f"""
        SELECT
            comments.*,
            users.*,
            COUNT(DISTINCT reports.user_id) as reports_count,
            COUNT(DISTINCT abusive_reports.user_id) as abusive_count,
            COUNT(DISTINCT offensive_reports.user_id) as offensive_count,
            COUNT(DISTINCT spam_reports.user_id) as spam_count
        FROM comments
        JOIN users ON users.user_id = comments.user_id
        JOIN reports ON reports.comment_id = comments.comment_id
        LEFT JOIN reports abusive_reports ON abusive_reports.comment_id = comments.comment_id AND abusive_reports.reason = 'abusive'
        LEFT JOIN reports offensive_reports ON offensive_reports.comment_id = comments.comment_id AND offensive_reports.reason = 'offensive'
        LEFT JOIN reports spam_reports ON spam_reports.comment_id = comments.comment_id AND spam_reports.reason = 'spam'
        {where_clause}
        GROUP BY reports.comment_id
        ORDER BY reports_count DESC
        LIMIT %s OFFSET %s
    """
    print(query, params)
    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        comments = cursor.fetchall()
        return comments


def db_get_reported_comments_count(
    is_hidden: bool | None, escalated: bool | None
) -> int:
    """Get reported comments count"""

    where_clause = ""
    where_clauses = []
    params = []
    if is_hidden == True and escalated == True:
        where_clause = "WHERE comments.is_hidden = True OR comments.escalated = True"
    else:
        if is_hidden != None:
            where_clauses.append("comments.is_hidden = %s")
            params.append(int(is_hidden))
        if escalated != None:
            where_clauses.append("comments.escalated = %s")
            params.append(escalated)
        if len(where_clauses) != 0:
            where_clause = " AND ".join(where_clauses)
            where_clause = f"WHERE {where_clause}"

    query = f"""
        SELECT COUNT(*) as count FROM comments
        JOIN reports ON reports.comment_id = comments.comment_id
        {where_clause}
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, params)
        count = cursor.fetchone()
        return count["count"]


def db_hide_comment(comment_id: int) -> None:
    """Hide comment"""
    query = """
        UPDATE comments SET is_hidden = True WHERE comment_id = %s
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (comment_id,))


def db_escalate_comment(comment_id: int) -> None:
    """Escalate comment to admin"""
    query = """
        UPDATE comments SET escalated = True WHERE comment_id = %s
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (comment_id,))


def db_get_user_event_reaction(user_id: int, event_id: int) -> dict:
    with db.get_cursor() as cursor:
        query = """
            SELECT reaction_id, is_like FROM reactions
            WHERE user_id = %s AND event_id = %s
        """
        cursor.execute(query, (user_id, event_id))
        reaction = cursor.fetchone()
        return reaction


def db_add_user_event_reaction(user_id: int, event_id: int, is_like: bool) -> None:
    with db.get_cursor() as cursor:
        query = """
            INSERT INTO reactions (user_id, event_id, is_like)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (user_id, event_id, is_like))


def db_delete_reaction(reaction_id: int) -> None:
    with db.get_cursor() as cursor:
        query = """
            DELETE FROM reactions
            WHERE reaction_id = %s
        """
        cursor.execute(query, (reaction_id,))


def db_update_event_like_count(event_id: int, count: int) -> None:
    with db.get_cursor() as cursor:
        query = """
            UPDATE events
            SET like_count = like_count + %s
            WHERE event_id = %s
        """
        cursor.execute(query, (count, event_id))


def db_get_event_comment_reaction(user_id: int, comment_id: int) -> dict:
    with db.get_cursor() as cursor:
        query = """
            SELECT reaction_id, is_like FROM reactions
            WHERE user_id = %s AND comment_id = %s
        """
        cursor.execute(query, (user_id, comment_id))
        reaction = cursor.fetchone()
        return reaction


def db_update_comment_like_count(comment_id: int, count: int) -> None:
    with db.get_cursor() as cursor:
        query = """
            UPDATE comments
            SET like_count = like_count + %s
            WHERE comment_id = %s
        """
        cursor.execute(query, (count, comment_id))


def db_update_comment_dislike_count(comment_id: int, count: int) -> None:
    with db.get_cursor() as cursor:
        query = """
            UPDATE comments
            SET dislike_count = dislike_count + %s
            WHERE comment_id = %s
        """
        cursor.execute(query, (count, comment_id))


def db_add_event_comment_reaction(user_id: int, comment_id: int, is_like: bool) -> None:
    with db.get_cursor() as cursor:
        query = """
            INSERT INTO reactions (user_id, comment_id, is_like, reaction_type)
            VALUES (%s, %s, %s, 'comment')
        """
        cursor.execute(query, (user_id, comment_id, is_like))


def db_update_event_comment_reaction(reaction_id: int, is_like: bool) -> None:
    with db.get_cursor() as cursor:
        query = """
            UPDATE reactions
            SET is_like = %s
            WHERE reaction_id = %s
        """
        cursor.execute(query, (is_like, reaction_id))


def db_reinstate_comment(comment_id: int) -> None:
    """Reinstate comment"""
    query = """
        UPDATE comments SET is_hidden = False, escalated = False WHERE comment_id = %s
    """
    with db.get_cursor() as cursor:
        cursor.execute(query, (comment_id,))


def db_get_user_comments_reactions(user_id: int) -> dict:
    with db.get_cursor() as cursor:
        query = """
            SELECT comment_id, is_like
            FROM reactions
            WHERE user_id = %s AND comment_id IS NOT NULL
        """
        cursor.execute(query, (user_id,))
        reactions = cursor.fetchall()
        return reactions

def db_get_most_comments_event_by_user_id(user_id: int) -> dict:
    with db.get_cursor() as cursor:
        query = """
            SELECT e.event_id
            FROM events e
            JOIN journeys j ON e.journey_id = j.journey_id
            WHERE j.user_id = %s
            ORDER BY e.comments_count DESC
            LIMIT 1
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result if result else None

def db_get_most_likes_event_by_user_id(user_id: int) -> dict:
    with db.get_cursor() as cursor:
        query = """
            SELECT e.event_id, e.like_count
            FROM events e
            JOIN journeys j ON e.journey_id = j.journey_id
            WHERE j.user_id = %s
            ORDER BY e.like_count DESC
            LIMIT 1
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result if result else None
