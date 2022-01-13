from flask import Blueprint, render_template, request
from app.models import Job

main = Blueprint("main", __name__)

@main.route("/")
def home():    
    page = request.args.get("page", 1, type=int)
    jobs = Job.query.filter_by(is_active=True).order_by(Job.id.desc()).paginate(page=page, per_page=5)
    return render_template("index.html", jobs=jobs)