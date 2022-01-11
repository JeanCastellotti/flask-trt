from flask import Blueprint, render_template
from app.models import Job

main = Blueprint("main", __name__)

@main.route("/")
def home():    
    jobs = Job.query.filter_by(is_active=True).order_by(Job.id.desc()).all()
    return render_template("index.html", jobs=jobs)