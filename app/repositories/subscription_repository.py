from typing import Dict, List
from app import db


def db_get_subscription_plan() -> List[Dict]:
    with db.get_cursor() as cursor:
        query = """
                SELECT * FROM subscription_types;
                """
        cursor.execute(query)
        subscription_plans = cursor.fetchall()
        return subscription_plans

def db_get_subscription_plan_by_id(subscription_type_id: int) -> List[Dict]:
    with db.get_cursor() as cursor:
        query = """
                SELECT * FROM subscription_types
                WHERE subscription_type_id = %s;

                """
        cursor.execute(query, (subscription_type_id,))
        subscription = cursor.fetchone()
        return subscription


def db_have_active_subscription(user_id:int) -> bool:
    with db.get_cursor() as cursor:
        query = """
                SELECT 1 FROM subscriptions
                WHERE user_id = %s AND end_datetime > NOW()
                LIMIT 1
                ;
                """
        cursor.execute(query, (user_id,))
        return cursor.fetchone() is not None

def db_add_subscription(user_id:int,start_date,end_date,total_price:int,gst_applied:bool,billing_address:str, subscription_type_id:int) -> None:
    with db.get_cursor() as cursor:
        query = """
                INSERT INTO subscriptions (
                user_id,
                subscription_type_id,
                start_datetime,
                end_datetime,
                payment_amount,
                gst,
                billing_address)
                SELECT
                %s,
                subscription_types.subscription_type_id,
                %s,
                %s,
                %s,
                %s,
                %s
                FROM subscription_types
                WHERE subscription_types.subscription_type_id = %s
                ;
                """
        cursor.execute(query, (user_id,start_date,end_date,total_price,gst_applied,billing_address,subscription_type_id))

def db_get_latest_subscription_end_date(user_id:int)-> Dict | None:
    with db.get_cursor() as cursor:
        query = """
                SELECT MAX(end_datetime)
                FROM subscriptions
                WHERE user_id = %s
                ;
                """
        cursor.execute(query, (user_id,))
        end_date = cursor.fetchone()
        return end_date if end_date else None

def has_used_free_trial(user_id: int) -> bool:
    with db.get_cursor() as cursor:
        query = """
                SELECT 1
                FROM subscriptions
                JOIN subscription_types ON subscriptions.subscription_type_id = subscription_types.subscription_type_id
                WHERE subscriptions.user_id = %s
                LIMIT 1;
                """
        cursor.execute(query, (user_id,))
        return cursor.fetchone() is not None


def db_get_sub_plans_by_type(type: str) -> List[Dict]:
     with db.get_cursor() as cursor:
         query = """
                 SELECT * FROM subscription_types
                 WHERE type = %s;
                 """
         cursor.execute(query, (type,))
         subscriptions = cursor.fetchall()
         return subscriptions

## get subscription history
def db_get_subscriptions(user_id: int, current_page: int, page_size: int) -> list[Dict]:
    """Get all subscriptionss of a user.
    Args:
        user_id (int): user id.
        current_page (int): Current page number.
        page_size (int): Number of subscriptions per page.
        query (str): Optional search query to filter subscriptions by title or content.

    Returns:
        List[Dict]: List of subscriptions,
    """
    offset = (current_page - 1) * page_size

    with db.get_cursor() as cursor:

        query = """
                    SELECT  s1.subscription_id, s1.start_datetime, s1.end_datetime, s1.payment_amount, s1.gst, s1.created_at, s2.type, s2.duration
                    FROM subscriptions s1
                    INNER JOIN subscription_types s2 ON s2.subscription_type_id = s1.subscription_type_id
                    WHERE s1.user_id = %s order by s1.end_datetime desc
                    LIMIT %s OFFSET %s;
                    """
        cursor.execute(query, (user_id, page_size, offset))
        subscriptions = cursor.fetchall()
        return subscriptions

## get subscription
def db_get_subscription(subscription_id: int
                  ) -> dict:
    """Get subscription of a user
    Args:
        subscription_id (int): subscription id.
    Returns:
        dict: one subscription of given subscription id.
    """

    with db.get_cursor() as cursor:

        query = """
                    SELECT u1.first_name, u1.last_name, g1.user_id, g1.subscription_id, g1.start_datetime, g1.end_datetime, g1.payment_amount, g1.gst, g1.created_at, g1.type, g1.duration, g1.billing_address
                    FROM users u1
                    INNER JOIN
                        (
                        SELECT s1.user_id, s1.subscription_id, s1.start_datetime, s1.end_datetime, s1.payment_amount, s1.gst, s1.created_at, s2.type, s2.duration, s1.billing_address
                        FROM subscriptions s1
                        INNER JOIN subscription_types s2 ON s2.subscription_type_id = s1.subscription_type_id
                        WHERE s1.subscription_id = %s
                        ) g1 ON g1.user_id = u1.user_id;
                """
        cursor.execute(query, (subscription_id,))
        subscription = cursor.fetchone()
        return subscription

def db_get_subscriptions_count(user_id: int) -> int:
    """Get the total count of subscription of a user.

    Args:
        user_id (int): user id.

    Returns:
        int: Total count of subscriptions.
    """

    with db.get_cursor() as cursor:
        sql_query = """
            SELECT COUNT(*) AS count
            FROM subscriptions
            WHERE user_id = %s;
        """
        cursor.execute(sql_query, (user_id, ))
        count = cursor.fetchone()
        return count["count"]
    
