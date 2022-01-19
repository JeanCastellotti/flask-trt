from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template("errors/not-found.html"), 404


@errors.app_errorhandler(403)
def forbidden_error(error):
    return render_template("errors/forbidden.html"), 403


@errors.app_errorhandler(401)
def unauthorized_error(error):
    return render_template("errors/unauthorized.html"), 401


@errors.app_errorhandler(500)
def server_error(error):
    return render_template("errors/server.html"), 500