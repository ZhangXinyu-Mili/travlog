from datetime import datetime, timedelta
from app import app
from flask import (
    redirect,
    url_for,
    session,
    render_template,
    request,
    flash,
    abort,
    Response,
)
import os, io, pdfkit
import platform
from app.auth import login_required
from app.repositories.community_repository import (
    db_delete_message,
    db_get_messages,
    db_get_summaries,
    db_save_message,
    db_update_message_status,
)
from app.repositories.subscription_repository import (
    db_add_subscription,
    db_get_latest_subscription_end_date,
    db_get_subscription_plan_by_id,
    db_get_subscription,
    db_get_subscriptions,
    db_get_subscriptions_count,
    db_have_active_subscription
)
from app.repositories.user_repository import db_get_user_by_id
from app.repositories.community_repository import (
    db_get_summaries,
    db_get_messages,
    db_save_message,
    db_update_message_status,
    db_delete_message,
    db_user_or_location_followed
)
from app.user import role_badges_mapping
import json


@app.context_processor
def utility_processor():
    def user_or_location_followed(user_id, followable_id, followable_type):
        return list(db_user_or_location_followed(user_id, followable_id, followable_type).values())[0]
    return dict(user_or_location_followed=user_or_location_followed)

@app.post("/grant-subscriptions")
@login_required(role=["admin"])
def admin_grant_subscriptions():
    form = request.form

    if not form["user_id"]:
        flash("User id is required", "danger")
        return redirect(url_for("users"))
    user = db_get_user_by_id(form["user_id"])
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("users"))

    if not form["subscription_type_id"]:
        flash("Subscription type id is required", "danger")
        return redirect(url_for("view_profile", user_id=user["user_id"]))
    sub = db_get_subscription_plan_by_id(form["subscription_type_id"])
    if not sub:
        flash("Subscription type not found", "danger")
        return redirect(url_for("view_profile", user_id=user["user_id"]))
    if sub["type"] != "admin_granted":
        flash("Subscription type incorrect", "danger")
        return redirect(url_for("view_profile", user_id=user["user_id"]))

    latest_end_date = db_get_latest_subscription_end_date(user["user_id"])
    start_date = latest_end_date["MAX(end_datetime)"]

    if not start_date:
        start_date = datetime.now()

    end_date = start_date + timedelta(days=sub["duration"])

    try:
        db_add_subscription(
            user["user_id"],
            start_date,
            end_date,
            0,
            False,
            "",
            sub["subscription_type_id"],
        )
    except:
        flash("Something went wrong", "danger")
        return redirect(url_for("view_profile", user_id=user["user_id"]))

    flash("The subscription has been granted.", "success")
    return redirect(url_for("view_profile", user_id=user["user_id"]))


@app.get("/subscriptions/<int:user_id>/list")
@login_required(role=["admin", "supporttech"])
def subscription_list(user_id):
    # get a subscription list for a user by admin
    current_page = request.args.get("current_page", 1, type=int)
    page_size = 5
    try:
        subscriptions = db_get_subscriptions(user_id, current_page, page_size)
        total_count = db_get_subscriptions_count(user_id)
        total_pages = (total_count + page_size - 1) // page_size
        return render_template(
            "user/subscription_list.html",
            subscriptions=subscriptions,
            current_page=current_page,
            total_pages=total_pages
        )
    except:
        return "Something went wrong", 403


@app.get("/my_subscriptions")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def my_subscription_list():
    # get a subscription list for a user
    current_page = request.args.get("current_page", 1, type=int)
    page_size = 5
    user_id = session["user_id"]
    try:
        subscriptions = db_get_subscriptions(user_id, current_page, page_size)
        total_count = db_get_subscriptions_count(user_id)
        total_pages = (total_count + page_size - 1) // page_size
        return render_template(
            "user/subscription_list.html",
            subscriptions=subscriptions,
            current_page=current_page,
            total_pages=total_pages
        )
    except:
        return "Something went wrong", 403


def download_receipt(subscription_id):
    # download receipt by a user from browser
    try:
        subscription = db_get_subscription(subscription_id)
    except:
        abort(500)

    os_name = platform.system()
    if os_name == "Linux":
        #below path is for PythonAnywhere
        file_path = "/usr/bin/wkhtmltopdf"
    elif os_name == "Windows":
        # below path is for Windows local test
        file_path = os.path.join(
            "c:\\", "Users", "yangj", "wkhtmltopdf", "bin", "wkhtmltopdf.exe"
        )
    elif os_name == "Darwin":
        # below path is for macOS local test, need to specify a path
        file_path = None
        print("Please config your file path")
        abort(500)
    config = pdfkit.configuration(wkhtmltopdf=file_path)
    options = {
        "page-size": "A5",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "no-outline": None,
    }

    template = render_template(
        "user/receipt.html", subscription=subscription, download=False
    )
    save_path = os.path.join(
        app.config["UPLOAD_FOLDER"], f"receipt_{{subscription_id}}.pdf"
    )
    pdfkit.from_string(template, save_path, configuration=config, options=options)

    return_data = io.BytesIO()
    with open(save_path, "rb") as fo:
        return_data.write(fo.read())
    return_data.seek(0)
    os.remove(save_path)
    # w = FileWrapper(return_data)
    # send_file(w, mimetype="application/pdf", download_name="receipt.pdf")
    return Response(return_data.getvalue(), mimetype="application/pdf")


@app.get("/my_subscription/<int:subscription_id>/receipt")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def my_receipt(subscription_id):
    # view receipt by user or download it
    try:
        subscription = db_get_subscription(subscription_id)
    except:
        abort(500)
    if not subscription:
        return (
            render_template(
                "error.html",
                error_message="No receipt found.",
                home_url=url_for("view_my_profile"),
            ),
            403,
        )
    elif subscription["user_id"] != session["user_id"] and session["role"] != "admin":
        return (
            render_template(
                "error.html",
                error_message="The receipt does not belong to you.",
                home_url=url_for("view_my_profile"),
            ),
            403,
        )
    return download_receipt(subscription_id)


@app.get("/my_messages")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def my_message_list():
    # get a list of messages for a user
    from_id = request.args.get("from_id", None)
    from_name = request.args.get("from_name", None)
    current_page = request.args.get("current_page", 1, type=int)
    page_size = 20
    user_id = session["user_id"]
    try:
        summaries = db_get_summaries(user_id, current_page, page_size, from_id)
        messages = db_get_messages(user_id, from_id)
    except:
        abort(500)
    total_count = len(summaries)
    total_pages = (total_count + page_size - 1) // page_size

    for i in range(0, len(summaries)):
        summaries[i]["directions"] = json.loads(summaries[i]["directions"])
        row = []
        for key, value in summaries[i]["directions"].items():
            for id in value:
                row.append({key: id})
        row.sort(key=lambda x: (x["f"] if "f" in x else x["t"]))
        summaries[i]["directions"] = row

    if from_id:
        active = "slide3"
    else:
        active = "slide1"
    return render_template(
        "user/messages.html",
        summaries=summaries,
        messages=messages,
        current_page=current_page,
        total_pages=total_pages,
        role_badges_mapping=role_badges_mapping,
        total_count=total_count,
        json=json,
        active=active,
        from_id=from_id,
        from_name=from_name
    )


@app.post("/messages/change_status")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def change_message_status():
    from_id = request.form.get("from_id", None)
    try:
        db_update_message_status(from_id, False)
    except:
        abort(500)
    return "ok"


@app.post("/messages/new")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def send_message():
    try:
        is_active_subscriper = db_have_active_subscription(session["user_id"])
    except:
        abort(500)

    if is_active_subscriper or session["role"] in ["editor", "admin", "moderator", "supporttech"]:
        from_id = int(request.form.get("from_id"))
        to_id = int(request.form.get("to_id"))
        from_name = request.form.get("from_name")
        content = request.form.get("message-text")
        try:
            db_save_message(from_id, to_id, content)
        except:
            abort(500)
    else:
        flash(f"Only editors, admins, or users with active subscriptions can send a message. <a href=.{url_for('get_subscription_plan')}>Get a subscription</a>", "warning")
    return redirect(url_for("my_message_list", from_id = to_id, from_name=from_name))


@app.get("/messages/<int:message_id>/delete")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def delete_message_modal(message_id):
    from_id = int(request.args.get("from_id"))
    from_name = request.args.get("from_name")
    try:
        is_active_subscriper = db_have_active_subscription(session["user_id"])
    except:
        abort(500)
    if is_active_subscriper or session["role"] in ["editor", "admin", "moderator", "supporttech"]:
        try:
            user = db_get_user_by_id(from_id)
            return render_template(
                "user/delete_message.html",
                user=user,
                message_id=message_id,
                from_id=from_id,
                from_name=from_name
            )
        except:
            abort(500)
    else:
        flash(f"Only editors, admins, or users with active subscriptions can delete a message. <a href=.{url_for('get_subscription_plan')}>Get a subscription</a>", "warning")
        return {"from_id":from_id}, 403
@app.post("/messages/<int:message_id>/delete")
@login_required(role=["traveller", "moderator", "editor", "supporttech", "admin"])
def delete_message(message_id):
    from_id = int(request.form.get("from_id"))
    from_name = request.form.get("from_name")
    try:
        is_active_subscriper = db_have_active_subscription(session["user_id"])
    except:
        abort(500)

    if is_active_subscriper or session["role"] in ["editor", "admin", "moderator", "supporttech"]:
        try:
            db_delete_message(message_id)
            flash("Message deleted", "success")
        except:
            abort(500)
    else:
        flash(f"Only editors, admins, or users with active subscriptions can delete a message. <a href=.{url_for('get_subscription_plan')}>Get a subscription</a>", "warning")
    return redirect(url_for("my_message_list", from_id = from_id, from_name=from_name))
