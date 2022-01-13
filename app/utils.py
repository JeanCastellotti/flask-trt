import os
import secrets
from functools import wraps
from flask import request, abort, current_app as app
from flask_login import current_user
from flask_mail import Message
from urllib.parse import urlparse, urljoin
from app import mail

def is_safe_url(url):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, url))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def save_file(file):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(file.filename)
    file_name = random_hex + file_ext
    path = os.path.join(app.root_path, 'static/uploads/', file_name)
    file.save(path)
    delete_file(current_user.resume_file)
    return file_name


def delete_file(file):
    if current_user.resume_file: 
        file_path = os.path.join(app.root_path, 'static/uploads', file)
        if os.path.exists(file_path):
            os.remove(file_path)


def roles_required(*roles):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if not current_user.role in roles:
                return abort(401)
            return function(*args, **kwargs)
        return wrapper
    return decorator


def send_email(recruiter_email, file_path):
    message = Message("Nouvelle candidature", sender="noreply@trtconseil.com", recipients=[recruiter_email])
    message.body = f"""
    Bonjour,

    Vous avez une nouvelle candidature !

    Veuillez trouver ci-joint le CV du candidat.
    """
    with app.open_resource(file_path) as fp:
        message.attach('cv.pdf', 'application/pdf', fp.read())
    mail.send(message)