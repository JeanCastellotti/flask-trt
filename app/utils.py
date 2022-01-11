import os
import secrets
from flask import request, current_app as app
from flask_login import current_user
from urllib.parse import urlparse, urljoin

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