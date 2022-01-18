from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from .forms import CreateJobForm
from app import db
from app.models import Job, Application
from app.utils import roles_required

jobs = Blueprint("jobs", __name__, url_prefix="/jobs")

@jobs.route("/create", methods=["GET", "POST"])
@login_required
@roles_required("recruiter")
def create():
    if not current_user.company or not current_user.address:
        flash("Vous devez compléter votre profil avant de pouvoir publier une annonce.", "warning")
        return redirect(url_for("main.home"))
    form = CreateJobForm()
    if form.validate_on_submit():
        print(form.working_hours.data)
        job = Job(title=form.title.data.strip(), 
                  salary=form.salary.data, 
                  place=form.place.data.strip(), 
                  working_hours=form.working_hours.data,
                  description=form.description.data.strip(),
                  recruiter=current_user)
        db.session.add(job)
        db.session.commit()
        flash("Votre annonce a été créée.", "success")
        return redirect(url_for("main.home"))
    return render_template("jobs/create.html", form=form)


@jobs.route("/<int:id>")
def show(id):
    job = Job.query.get_or_404(id)
    if not job.is_active and (current_user.is_anonymous or current_user.is_authenticated and current_user.role == "candidate"):
        return abort(403)
    # application = Application.query.filter_by(job_id=job.id, user_id=current_user.id).first()
    return render_template("jobs/show.html", job=job)


@jobs.route("/<int:id>/apply", methods=["POST"])
@login_required
@roles_required("candidate")
def apply(id):
    if not current_user.resume_file or not current_user.first_name or not current_user.last_name:
        flash("Vous devez compléter votre profil avant de pouvoir postuler à une annonce.", "warning")
        return redirect(url_for("account.informations"))
    job = Job.query.get_or_404(id)
    application = Application.query.filter_by(job_id=job.id, user_id=current_user.id).first()
    if application:
        flash("Vous avez déjà postulé à cette annonce.", "error")
        return redirect(url_for("jobs.show", id=job.id))
    new_application = Application(job_id=job.id, user_id=current_user.id)
    db.session.add(new_application)
    db.session.commit()
    flash("Votre candidature a été soumise.", "success")
    return redirect(url_for("jobs.show", id=job.id))