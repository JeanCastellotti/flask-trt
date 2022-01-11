from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import CreateJobForm
from app import db
from app.models import Job

jobs = Blueprint("jobs", __name__, url_prefix="/jobs")

@jobs.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if not current_user.company or not current_user.address:
        flash("Vous devez compléter votre profil avant de pouvoir publier une annonce.", "warning")
        return redirect(url_for("main.home"))
    form = CreateJobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data.strip(), 
                  salary=form.salary.data.strip(), 
                  place=form.place.data.strip(), 
                  description=form.description.data.strip())
        db.session.add(job)
        db.session.commit()
        flash("Votre annonce a été créée.", "success")
        return redirect(url_for("main.home"))
    return render_template("jobs/create.html", form=form)


@jobs.route("/<int:id>")
def show(id):
    job = Job.query.get_or_404(id)
    return render_template("jobs/show.html", job=job)