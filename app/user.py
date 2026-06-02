from flask_bcrypt import Bcrypt
from app import app
from flask import redirect, url_for, session, render_template, request, flash, abort
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
from app.auth import login_required
from app.repositories.achievement_repository import db_get_achievements, db_get_achievements_count
from app.repositories.community_repository import (
    db_get_comments_by_user_id,
    db_get_community_users,
    db_get_event_comments_count_by_user_id,
    db_get_event_likes_count,
    db_get_liked_event_by_user_id,
    db_get_location_by_user_id,
    db_get_community_users_count,
)
from app.repositories.journey_repository import (
    db_get_journeys_by_user_id,
    db_get_journeys_count_by_user_id,
)
from app.repositories.subscription_repository import (
    db_add_subscription,
    db_get_latest_subscription_end_date,
    db_get_sub_plans_by_type,
    db_get_subscription_plan,
    db_get_subscription_plan_by_id,
    has_used_free_trial,
)
from app.repositories.user_repository import (
    db_create_user,
    db_get_user_by_email,
    db_get_user_by_username,
    db_get_user_by_id,
    db_get_users,
    db_get_users_count,
    db_update_user_role,
    db_update_user_status,
    db_update_user_profile,
    db_remove_user_profile_image,
    db_get_user_password_hash,
    db_update_user_password,
)

# Create an instance of the Bcrypt class, which we'll be using to hash user
# passwords during login and registration.
flask_bcrypt = Bcrypt(app)

role_badges_mapping = {
    "admin": "danger",
    "editor": "info",
    "moderator": "warning",
    "traveller": "primary",
    "supporttech": "warning",
}
status_badges_mapping = {
    "active": "primary",
    "blocked": "secondary",
    "banned": "danger",
}


@app.context_processor
def utility_processor():
    def user_profile_image(user):
        return (
            user["profile_image"]
            if user["profile_image"]
            else "/static/images/default-profile.png"
        )

    def user_level(user_id, show_title=False):
        achievements_count = db_get_achievements_count(user_id)
        badge = ""
        if achievements_count >= 10:
            badge = "💎"
        elif achievements_count >= 5:
            badge = "🥇"
        elif achievements_count >= 3:
            badge = "🥈"
        elif achievements_count >= 1:
            badge = "🥉"

        if show_title:
            if achievements_count >= 10:
                badge += " Diamond"
            elif achievements_count >= 5:
                badge += " Gold"
            elif achievements_count >= 3:
                badge += " Sliver"
            elif achievements_count >= 1:
                badge += " Bronze"
            else:
                badge += "N/A"
        return badge


    return dict(user_profile_image=user_profile_image, user_level=user_level)


def allowed_file(filename):
    """Check if file is allowed based on its extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.get("/register")
def register():
    """Register user page
    Redirect to root path if already logged in"""

    if "user_id" in session:
        return redirect(url_for("root"))

    return render_template("auth/register.html", err_msgs=None, form=None)


@app.post("/register")
def register_post():
    form = request.form
    err_msgs = {}

    if "username" not in form:
        err_msgs["username"] = "Username is required"
    if "password" not in form:
        err_msgs["password"] = "Password is required"
    if "password_confirmation" not in form:
        err_msgs["password_confirmation"] = "Password confirmation is required"
    if "username" in form and db_get_user_by_username(form["username"]):
        err_msgs["username"] = "Username already exists"
    if "email" in form and db_get_user_by_email(form["email"]):
        err_msgs["email"] = "Email already exists"
    if "password" in form and form["password"] != form["password_confirmation"]:
        err_msgs["password_confirmation"] = "Passwords do not match"
    if "password" in form and len(form["password"]) < 8:
        err_msgs["password"] = "Password must be at least 8 characters long"
    if "password" in form and form["password"].isdigit():
        err_msgs["password"] = "Password must contain at least one letter"
    if "password" in form and form["password"].isalpha():
        err_msgs["password"] = "Password must contain at least one number"

    # If there are any errors, render the registration page again with the error messages.
    if err_msgs:
        return render_template("auth/register.html", err_msgs=err_msgs, form=form)

    # Hash the password and create the user in the database.
    password_hash = flask_bcrypt.generate_password_hash(form["password"]).decode(
        "utf-8"
    )
    try:
        user_id = db_create_user(
            form["username"],
            password_hash,
            form["email"],
            form["first_name"],
            form["last_name"],
            form["location"],
            "traveller",
            "active",
        )

        user = db_get_user_by_id(user_id)

        # Log the user in and redirect to the root path.
        session["loggedin"] = True
        session["user_id"] = user["user_id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        flash("Your have successfully signed up!", "success")
        return redirect(url_for("root"))
    except:
        flash("Registration failed. Please try again.", "danger")
        return render_template("auth/register.html", err_msgs=err_msgs, form=form)


@app.get("/my_profile")
def view_my_profile():
    """user view their proifle"""
    if "user_id" not in session:
        return redirect(url_for("root"))
    # This case is rare, but it can happen when the user is logged in and then deleted by someone else from the database. This is a safeguard to prevent errors
    user_id = session["user_id"]
    user = db_get_user_by_id(user_id)

    if not user:
        return (
            render_template(
                "error.html",
                error_message="User not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    # Locations user has been to
    locations = db_get_location_by_user_id(user_id)
    # Journeys Pagination
    journeys_page = request.args.get("journeys_page", 1, type=int)
    journeys_page_size = request.args.get("page_size", 8, type=int)
    journeys = db_get_journeys_by_user_id(user_id, journeys_page, journeys_page_size)
    total_journeys_count = db_get_journeys_count_by_user_id(user_id)
    total_journeys_pages = (
        total_journeys_count + journeys_page_size - 1
    ) // journeys_page_size
    # Likes Pagination
    likes_page = request.args.get("likes_page", 1, type=int)
    likes = db_get_liked_event_by_user_id(user_id, likes_page, journeys_page_size)
    total_likes_count = db_get_event_likes_count(user_id)
    total_likes_pages = (
        total_likes_count + journeys_page_size - 1
    ) // journeys_page_size
    # Comments Pagination
    comments_page = request.args.get("comments_page", 1, type=int)
    comments = db_get_comments_by_user_id(user_id, comments_page, journeys_page_size)
    total_comments_count = db_get_event_comments_count_by_user_id(user_id)
    total_comments_pages = (
        total_comments_count + journeys_page_size - 1
    ) // journeys_page_size
    achievements = db_get_achievements(user_id)
    return render_template(
        "user/my_profile.html",
        user=user,
        locations=locations,
        journeys=journeys,
        likes=likes,
        comments=comments,
        journeys_page=journeys_page,
        total_journeys_pages=total_journeys_pages,
        likes_page=likes_page,
        total_likes_pages=total_likes_pages,
        comments_page=comments_page,
        total_comments_pages=total_comments_pages,
        role_badges_mapping=role_badges_mapping,
        status_badges_mapping=status_badges_mapping,
        achievements=achievements,
    )


@app.get("/my_profile/edit")
def edit_profile_form():
    """user edit their profile"""

    if "user_id" not in session:
        return redirect(url_for("root"))

    user_id = session.get("user_id")
    user = db_get_user_by_id(user_id)
    return render_template(
        "user/edit_my_profile.html", user=user, err_msgs=None, form=None
    )


@app.post("/my_profile/edit")
def edit_my_profile():
    """user edit their profile"""

    if "user_id" not in session:
        return redirect(url_for("root"))

    user_id = session.get("user_id")
    user = db_get_user_by_id(user_id)

    form = request.form
    err_msgs = {}
    name_public = "name_public" in form
    email_public = "email_public" in form
    profile_public = "profile_public" in form
    places_public = "places_public" in form
    likes_public = "likes_public" in form
    comments_public = "comments_public" in form
    if not form["username"]:
        err_msgs["username"] = "Username is required"
    if not form["email"]:
        err_msgs["email"] = "Email is required"
    if form["username"] != user["username"] and db_get_user_by_username(
        form["username"]
    ):
        err_msgs["username"] = "Username already exists"
    if form["email"] != user["email"] and db_get_user_by_email(form["email"]):
        err_msgs["email"] = "Email already exists"

    # If there are any errors, render the edit my profile page again with the error messages.
    if err_msgs:
        return render_template(
            "user/edit_my_profile.html", user=user, err_msgs=err_msgs, form=form
        )

    # Check profile image
    file = request.files["profile_image"]
    profile_image = user["profile_image"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file_path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        profile_image = f"/static/uploads/{filename}"

    try:
        db_update_user_profile(
            user_id,
            form["email"],
            form["username"],
            form["first_name"],
            form["last_name"],
            form["location"],
            form["description"],
            profile_image,
            name_public,
            email_public,
            profile_public,
            places_public,
            likes_public,
            comments_public,
        )
        flash("Your profile has been updated successfully.", "success")
        return redirect(url_for("view_my_profile"))
    except:
        flash("Failed to update profile. Please try again.", "danger")
        return render_template(
            "user/edit_my_profile.html", user=user, err_msgs=err_msgs, form=form
        )


@app.get("/my_profile/remove_profile_image")
def remove_profile_image():
    """user remove their profile image"""

    if "user_id" not in session:
        return redirect(url_for("root"))

    user_id = session.get("user_id")
    user = db_get_user_by_id(user_id)
    try:
        db_remove_user_profile_image(user_id)
        flash("Your profile image has been deleted.", "success")
        return redirect(url_for("view_my_profile"))
    except:
        flash("Failed to remove profile image. Please try again.", "danger")
        return render_template(
            "user/edit_my_profile.html", user=user, err_msgs=None, form=None
        )


@app.get("/my_profile/reset_password")
def reset_password_form():
    """user reset password form"""

    if "user_id" not in session:
        return redirect(url_for("root"))

    return render_template("user/reset_password.html", err_msgs=None, form=None)


@app.post("/my_profile/reset_password")
def reset_password():
    """user edit their password"""

    if "user_id" not in session:
        return redirect(url_for("root"))

    user_id = session.get("user_id")
    password_hash = db_get_user_password_hash(user_id)
    print(password_hash)
    form = request.form
    err_msgs = {}

    if not form["current_password"]:
        err_msgs["current_password"] = "Current password is required"
    if not form["new_password"]:
        err_msgs["new_password"] = "New password is required"
    if not form["new_password_confirmation"]:
        err_msgs["new_password_confirmation"] = "Please confirm your new password."
    if form["new_password"] and len(form["new_password"]) < 8:
        err_msgs["new_password"] = "Password must be at least 8 characters long."
    if form["new_password"] and form["new_password"].isdigit():
        err_msgs["new_password"] = "Password must contain at least one letter."
    if form["new_password"] and form["new_password"].isalpha():
        err_msgs["new_password"] = "Password must contain at least one number."
    if (
        form["new_password"]
        and form["new_password_confirmation"]
        and form["new_password"] != form["new_password_confirmation"]
    ):
        err_msgs["new_password_confirmation"] = (
            "New password and confirmation do not match."
        )
    if not flask_bcrypt.check_password_hash(password_hash, form["current_password"]):
        err_msgs["current_password"] = "Incorrect current password."
    if (
        form["new_password"]
        and form["current_password"]
        and form["new_password"] == form["current_password"]
    ):
        err_msgs["new_password_confirmation"] = (
            "New password cannot be the same as the current password."
        )

    # If there are any errors, render the reset password page again with the error messages.
    print(err_msgs)
    if err_msgs:
        return render_template("user/reset_password.html", err_msgs=err_msgs, form=form)

    try:
        new_password_hash = flask_bcrypt.generate_password_hash(
            form["new_password"]
        ).decode("utf-8")
        db_update_user_password(user_id, new_password_hash)
        flash("Your password has been reset successfully.", "success")
        return redirect(url_for("view_my_profile"))
    except:
        flash("Failed to reset password. Please try again.", "danger")
        return render_template("user/reset_password.html", err_msgs=None, form=None)


@app.get("/users/<int:user_id>")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def view_profile(user_id):
    """users view other user profile"""
    user = db_get_user_by_id(user_id)
    # If user does not exist
    if not user:
        return (
            render_template(
                "error.html",
                error_message="User not found",
                home_url=url_for("journeys"),
            ),
            404,
        )
    locations = db_get_location_by_user_id(user_id)
    # Journeys Pagination
    journeys_page = request.args.get("journeys_page", 1, type=int)
    journeys_page_size = request.args.get("page_size", 6, type=int)
    journeys = db_get_journeys_by_user_id(user_id, journeys_page, journeys_page_size)
    total_journeys_count = db_get_journeys_count_by_user_id(user_id)
    total_journeys_pages = (
        total_journeys_count + journeys_page_size - 1
    ) // journeys_page_size
    # Likes Pagination
    likes_page = request.args.get("likes_page", 1, type=int)
    likes = db_get_liked_event_by_user_id(user_id, likes_page, journeys_page_size)
    total_likes_count = db_get_event_likes_count(user_id)
    total_likes_pages = (
        total_likes_count + journeys_page_size - 1
    ) // journeys_page_size
    # Comments Pagination
    comments_page = request.args.get("comments_page", 1, type=int)
    comments = db_get_comments_by_user_id(user_id, comments_page, journeys_page_size)
    total_comments_count = db_get_event_comments_count_by_user_id(user_id)
    total_comments_pages = (
        total_comments_count + journeys_page_size - 1
    ) // journeys_page_size
    # admins can grant free subscriptions
    admin_grant_sub_plans = db_get_sub_plans_by_type("admin_granted")
    achievements = db_get_achievements(user_id)
    return render_template(
        "user/profile.html",
        user=user,
        journeys=journeys,
        locations=locations,
        likes=likes,
        comments=comments,
        journeys_page=journeys_page,
        total_journeys_pages=total_journeys_pages,
        likes_page=likes_page,
        total_likes_pages=total_likes_pages,
        comments_page=comments_page,
        total_comments_pages=total_comments_pages,
        role_badges_mapping=role_badges_mapping,
        status_badges_mapping=status_badges_mapping,
        admin_grant_sub_plans=admin_grant_sub_plans,
        achievements=achievements,
    )


@app.get("/users")
@login_required(role=["admin", "supporttech"])
def users():
    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    q = request.args.get("q", None, type=str)
    staff_only = request.args.get("staff_only", None, type=bool)
    blocked_only = request.args.get("blocked_only", None, type=bool)
    users = db_get_users(current_page, page_size, q, staff_only, blocked_only)
    total_users_count = db_get_users_count(q, staff_only, blocked_only)
    total_pages = (total_users_count + page_size - 1) // page_size
    return render_template(
        "user/users.html",
        users=users,
        current_page=current_page,
        total_pages=total_pages,
        role_badges_mapping=role_badges_mapping,
        status_badges_mapping=status_badges_mapping,
    )


@app.post("/users/<int:user_id>/status")
@login_required(role=["admin", "supporttech"])
def update_user_status(user_id: int):
    print(request.form)  # This will print the submitted form data
    user = db_get_user_by_id(user_id)
    if not user:
        abort(404)

    if user["user_id"] == session["user_id"]:
        flash("You cannot change your own status.", "danger")
        return redirect(url_for("user", user_id=user_id))

    status = request.form.get("status")
    if status not in ["active", "blocked", "banned"]:
        abort(400)

    try:
        db_update_user_status(user["user_id"], status)
    except:
        abort(500)

    flash(
        f"{user['username']}'s user status has been changed to {status}.",
        "success",
    )

    return redirect(url_for("view_profile", user_id=user_id))


@app.post("/users/<int:user_id>/role/edit")
@login_required(role=["admin"])
def update_user_role(user_id: int):
    user = db_get_user_by_id(user_id)
    if not user:
        abort(404)

    if user["user_id"] == session["user_id"]:
        flash("You cannot change your own role.", "danger")
        return redirect(url_for("user", user_id=user_id))

    role = request.form.get("role")
    if role not in ["admin", "editor", "moderator", "traveller", "supporttech"]:
        abort(400)

    try:
        db_update_user_role(user["user_id"], role)
        flash(
            f"Successfully changed user {user['username']} role to {role}.",
            "success",
        )
    except:
        flash(
            f"Failed to change user {user['username']} role to {role}.",
            "danger",
        )
    return redirect(url_for("view_profile", user_id=user_id))


@app.route("/subscriptions", methods=["GET", "POST"])
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def get_subscription_plan():
    free_trial = db_get_subscription_plan()[3]
    monthly_subscription = db_get_subscription_plan()[0]
    quarterly_subscription = db_get_subscription_plan()[1]
    yearly_subscription = db_get_subscription_plan()[2]
    # Free trial validation
    if request.method == "POST":
        if session["role"] == "traveller":
            if not has_used_free_trial(session["user_id"]):
                start_date = datetime.now()
                duration_days = free_trial["duration"]
                end_date = start_date + timedelta(days=duration_days)
                db_add_subscription(
                    session["user_id"],
                    start_date,
                    end_date,
                    free_trial["price"],
                    False,
                    None,
                    free_trial["subscription_type_id"],
                )
                flash("Your free trial is now activated.", "success")
                return redirect(url_for("root"))
            else:
                flash("You are not eligible for the free trial.", "danger")
                return redirect(url_for("get_subscription_plan"))
        else:
            flash("Staffs are not eligible for the free trial.", "danger")
            return redirect(url_for("get_subscription_plan"))
    else:
        return render_template(
            "user/subscription.html",
            free_trial=free_trial,
            monthly_subscription=monthly_subscription,
            quarterly_subscription=quarterly_subscription,
            yearly_subscription=yearly_subscription,
        )


@app.route("/subscriptions/<int:subscription_type_id>", methods=["GET", "POST"])
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def pay_subscription(subscription_type_id):
    subscription = db_get_subscription_plan_by_id(subscription_type_id)
    # Define start date and end date
    latest_end_date = db_get_latest_subscription_end_date(session["user_id"])[
        "MAX(end_datetime)"
    ]
    now = datetime.now()
    if latest_end_date and latest_end_date > now:
        start_date = latest_end_date
    else:
        start_date = now
    duration_days = subscription["duration"]
    end_date = start_date + timedelta(days=duration_days)
    # Validate card info
    billing_address_error = None
    cardholder_name_error = None
    card_number_error = None
    expiry_error = None
    cvv_error = None
    if request.method == "POST":
        billing_address = request.form.get("billing_address", "").strip()
        cardholder_name = request.form.get("cardholder_name", "").strip()
        card_number = request.form.get("card_number", "").strip()
        expiry = request.form.get("expiry", "").strip()
        cvv = request.form.get("cvv", "").strip()
        action = request.form["action"]
        # Validate billing address
        if not billing_address:
            billing_address_error = "Billing address is required."
        elif len(billing_address) > 100:
            billing_address_error = "Your billing address cannot exceed 100 characters."
        # Validate cardholder name
        if not cardholder_name:
            cardholder_name_error = "cardholder_name is required."
        elif len(cardholder_name) > 100:
            cardholder_name_error = "Your cardholder_name cannot exceed 100 characters."
        # Validate card number
        if not card_number:
            card_number_error = "Card number is required."
        elif not card_number.isdigit():
            card_number_error = "Card number must contain only digits."
        elif not (13 <= len(card_number) <= 19):
            card_number_error = "Card number must be between 13 and 19 digits."
        # Validate card expiry
        if not expiry:
            expiry_error = "Expiry date is required."
        elif "/" not in expiry:
            expiry_error = "Expiry format must be MM/YY."
        else:
            parts = expiry.split("/")
            if len(parts) != 2 or not all(part.isdigit() for part in parts):
                expiry_error = "Expiry must be numeric in MM/YY format."
            else:
                month, year = parts
                month = int(month)
                year = int(year)
                if not (1 <= month <= 12):
                    expiry_error = "Invalid month in expiry date."
                else:
                    year += 2000  # Convert YY to YYYY
                    today = datetime.today()
                    if datetime(year, month, 1) < today.replace(day=1):
                        expiry_error = "Card has expired."
        # Validate cvv
        if not cvv:
            cvv_error = "CVV is required."
        elif not cvv.isdigit():
            cvv_error = "CVV must contain only digits."
        elif len(cvv) not in [3, 4]:
            cvv_error = "CVV must be 3 or 4 digits."
        # direct to confirm page
        if action == "submit" and not (card_number_error or expiry_error or cvv_error):
            return redirect(
                url_for(
                    "confirm_subscription",
                    subscription_type_id=subscription_type_id,
                    billing_address=billing_address,
                    card_number=card_number,
                )
            )
        # return error message
        else:
            return render_template(
                "user/payment.html",
                subscription=subscription,
                billing_address_error=billing_address_error,
                cardholder_name_error=cardholder_name_error,
                card_number_error=card_number_error,
                expiry_error=expiry_error,
                cvv_error=cvv_error,
                billing_address=billing_address,
                card_number=card_number,
                expiry=expiry,
                cvv=cvv,
            )
    return render_template(
        "user/payment.html",
        subscription=subscription,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
    )


@app.route(
    "/subscriptions/<int:subscription_type_id>/payment_confirm", methods=["GET", "POST"]
)
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def confirm_subscription(subscription_type_id):
    subscription = db_get_subscription_plan_by_id(subscription_type_id)
    # check billing address and gst
    if request.method == "GET":
        billing_address = request.args.get("billing_address", "")
    else:
        billing_address = request.form.get("billing_address", "")
    price = subscription["price"]
    normalized_address = (
        billing_address.strip().lower().replace(" ", "").replace("-", "")
    )
    if "newzealand" in normalized_address or "nz" in normalized_address:
        gst = round(price * 0.15, 2)
    else:
        gst = 0
    total_price = round(price + gst, 2)
    gst_applied = bool(gst > 0)
    # Define start date and end date
    latest_end_date = db_get_latest_subscription_end_date(session["user_id"])[
        "MAX(end_datetime)"
    ]
    now = datetime.now()
    if latest_end_date and latest_end_date > now:
        start_date = latest_end_date
    else:
        start_date = now
    duration_days = subscription["duration"]
    end_date = start_date + timedelta(days=duration_days)
    # submit and update in database
    if request.method == "POST":
        card_number = request.form.get("card_number", "").strip()
        # Fail the payment if the test card number is used
        # Only for presenting a failed payment
        if card_number == "11111111111111":
            flash("Payment failed: Invalid card number.", "danger")
            return redirect(
                url_for("pay_subscription", subscription_type_id=subscription_type_id)
            )
        try:
            db_add_subscription(
                session["user_id"],
                start_date,
                end_date,
                total_price,
                gst_applied,
                billing_address,
                subscription_type_id,
            )
            flash("You have successfully subscribed.", "success")
            return redirect(url_for("root"))
        except Exception as e:
            flash("Your payment has failed.", "danger")
            return redirect(
                url_for(
                    "pay_subscription",
                    subscription=subscription,
                    subscription_type_id=subscription_type_id,
                )
            )
    return render_template(
        "user/payment_confirm.html",
        subscription=subscription,
        billing_address=billing_address,
        gst=gst,
        total_price=total_price,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
    )


@app.get("/community_users")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def community_users():
    current_page = request.args.get("current_page", 1, type=int)
    page_size = request.args.get("page_size", 8, type=int)
    q = request.args.get("q", None, type=str)

    users = db_get_community_users(current_page, page_size, q)
    total_users_count = db_get_community_users_count(q)
    total_pages = (total_users_count + page_size - 1) // page_size
    return render_template(
        "user/community_users.html",
        users=users,
        current_page=current_page,
        total_pages=total_pages,
        role_badges_mapping=role_badges_mapping,
        status_badges_mapping=status_badges_mapping,
    )
