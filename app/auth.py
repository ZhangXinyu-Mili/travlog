from datetime import datetime, timedelta
from functools import wraps
from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from app import app
from flask_bcrypt import Bcrypt

from app.repositories.subscription_repository import db_get_latest_subscription_end_date
from app.repositories.user_repository import db_get_user_by_id, db_get_user_by_username

# Create an instance of the Bcrypt class, which we'll be using to hash user
# passwords during login and registration.
flask_bcrypt = Bcrypt(app)


def login_required(role=None):
    """Decorator to require that a user is logged in to access a route.

    Args:
        role (list): A list of roles that are allowed to access the route. If
            the user's role is not in this list, they will see an "Access Denied"
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            user = db_get_user_by_id(session["user_id"])
            if user["status"] == "banned":
                # Delete user_id in session to log out the banned user
                session.pop("loggedin", None)
                session.pop("user_id", None)
                session.pop("username", None)
                session.pop("role", None)

                flash(
                    "Your account has been banned. Please contact the administrator.",
                    "danger",
                )
                return redirect(url_for("login"))
            # Only check role if a role is specified
            if role is not None and user["role"] not in role:
                return (
                    render_template(
                        "error.html",
                        error_message="Your account isn't authorised to view this page.",
                        home_url=url_for("journeys"),
                    ),
                    403,
                )
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@app.get("/login")
def login():
    """Renders the login page.
    If the user is already logged in, redirect to their role-specific homepage."""

    # Redirect to root path if user already logged in
    if "user_id" in session:
        return redirect(url_for("root"))

    return render_template("auth/login.html")


@app.post("/login")
def login_post():
    """Attempts to log the user in using the credentials supplied via the login form, and either:
    - Redirects the user to their role-specific homepage (if successful)
    - Renders the login page again with an error message (if unsuccessful)."""

    # Redirect to root path if user already logged in
    if "user_id" in session:
        return redirect(url_for("root"))

    # Get the login details submitted by the user.
    username = request.form["username"]
    password = request.form["password"]

    # Set username in session to avoid re-entering username if login fails
    session["username"] = username

    user = db_get_user_by_username(username)

    if user is None:
        flash("Can't find your account", "danger")
        return render_template("auth/login.html", username_invalid=True)

    password_hash = user["password_hash"]
    if not flask_bcrypt.check_password_hash(password_hash, password):
        flash("Invalid username or password.", "danger")
        return render_template("auth/login.html", password_invalid=True)
    if user["status"] == "banned":
        flash(
            "Your account has been banned. Please contact the administrator.", "danger"
        )
        return render_template("auth/login.html")

    # Check if traveller's subscription expired or due to expire
    if user["role"] not in ["editor", "admin"]:
        latest_sub_end_date = db_get_latest_subscription_end_date(user["user_id"])[
            "MAX(end_datetime)"
        ]
        # subscription expires in 7 days
        if (
            latest_sub_end_date
            and latest_sub_end_date > datetime.now()
            and latest_sub_end_date < datetime.now() + timedelta(days=7)
        ):
            flash(
                f"Your subscription ends in {(latest_sub_end_date - datetime.now()).days} days, would you like to <a href='{url_for("get_subscription_plan")}'>renew</a>?",
                "warning",
            )
        # subscription expired
        if latest_sub_end_date and latest_sub_end_date < datetime.now():
            flash(
                f"Your subscription has expired, would you like to <a href='{url_for("get_subscription_plan")}'>renew</a>?",
                "warning",
            )

    # Password is correct. Save the user's ID as session data,
    # which we can access from other routes to determine who's currently logged in.
    #
    # Users can potentially see and edit these details using their
    # web browser. However, the session cookie is signed with our
    # app's secret key. That means if they try to edit the cookie
    # to impersonate another user, the signature will no longer
    # match and Flask will know the session data is invalid.
    session["loggedin"] = True
    session["user_id"] = user["user_id"]
    session["username"] = user["username"]
    session["role"] = user["role"]

    return redirect("/")


@app.post("/logout")
def logout():
    # Delete user_id in session to log out the user
    session.pop("loggedin", None)
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("role", None)

    return redirect(url_for("root"))
