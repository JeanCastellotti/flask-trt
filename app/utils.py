import os
import validators
from functools import wraps
from flask import request, abort, current_app as app
from flask_login import current_user
from flask_mail import Message
from urllib.parse import urlparse, urljoin
from app import mail
from app.models import Job, Candidate, Recruiter
import cloudinary.uploader

def is_safe_url(url):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, url))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def save_file(file):
    print(current_user.resume_file)
    # random_hex = secrets.token_hex(8)
    # _, file_ext = os.path.splitext(file.filename)
    # file_name = random_hex + file_ext
    # path = os.path.join(app.root_path, 'static/uploads/', file_name)
    # file.save(path)
    # delete_file(current_user.resume_file)
    # return file_name
    upload_result = cloudinary.uploader.upload(file)
    if validators.url(current_user.resume_file or ''):
        public_id = urlparse(current_user.resume_file).path.split('.')[0].split('/')[-1]
        cloudinary.uploader.destroy(public_id)
    return upload_result["secure_url"]


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


def send_email(job: Job, recruiter: Recruiter, candidate: Candidate):
    message = Message("Nouvelle candidature", 
                      sender=("TRT Conseil", "server.smtp.dev@gmail.com"), 
                      recipients=[recruiter.email])
    message.body = f"""
    Bonjour,

    Vous avez une nouvelle candidature pour le poste de {job.title} !

    Veuillez trouver ci-joint le CV du candidat ({candidate.first_name} {candidate.last_name}).
    """
    with app.open_resource(f"static/uploads/{candidate.resume_file}") as fp:
        message.attach('cv.pdf', 'application/pdf', fp.read())
    mail.send(message)