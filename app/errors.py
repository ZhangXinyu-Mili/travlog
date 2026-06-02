from flask import render_template, url_for
from app import app


@app.errorhandler(401)
def unauthorized(e):
    """Unauthorized

    Args:
    - e: Error message

    Returns:
    - A rendered template for the error page with a 401 status
    """
    return (
        render_template(
            "error.html",
            error_message="Unauthorized",
            home_url=url_for("journeys"),
        ),
        401,
    )


@app.errorhandler(404)
def page_not_found(e):
    """Page not found

    Args:
    - e: Error message

    Returns:
    - A rendered template for the error page with a 404 status
    """
    return (
        render_template(
            "error.html",
            error_message="Page not found",
            home_url=url_for("journeys"),
        ),
        404,
    )


@app.errorhandler(403)
def forbidden(e):
    """Forbidden

    Args:
    - e: Error message

    Returns:
    - A rendered template for the error page with a 403 status
    """
    return (
        render_template(
            "error.html", error_message="Forbidden", home_url=url_for("journeys")
        ),
        403,
    )


@app.errorhandler(500)
def internal_server_error(e):
    """Internal server error

    Args:
    - e: Error message

    Returns:
    - A rendered template for the error page with a 500 status
    """
    return (
        render_template(
            "error.html",
            error_message="Internal server error",
            home_url=url_for("journeys"),
        ),
        500,
    )
