from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import CreateJobForm
from app import db
from app.models import Job

jobs = Blueprint("jobs", __name__, url_prefix="/jobs")

@jobs.route("/create", methods=["GET", "POST"])
def create():
    form = CreateJobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, place=form.place.data, description=form.description.data)
        db.session.add(job)
        db.session.commit()
        flash("Votre annonce a été créée.", "success")
        return redirect(url_for("main.home"))
    return render_template("jobs/create.html", form=form)