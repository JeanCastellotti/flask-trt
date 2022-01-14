from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required
from app.models import User, Candidate, Recruiter, Consultant, Administrator, Job, Application
from app import db, bcrypt
from app.utils import roles_required, send_email
from .forms import CreateUserForm

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/candidates")
@login_required
@roles_required("consultant", "administrator")
def candidates():
    page = request.args.get("page", 1, type=int)
    candidates = Candidate.query.order_by(User.id.desc()).paginate(page=page, per_page=5)
    return render_template("admin/candidates.html", candidates=candidates)


@admin.route("/recruiters")
@login_required
@roles_required("consultant", "administrator")
def recruiters():
    page = request.args.get("page", 1, type=int)
    recruiters = Recruiter.query.order_by(User.id.desc()).paginate(page=page, per_page=5)
    return render_template("admin/recruiters.html", recruiters=recruiters)


@admin.route("/consultants")
@login_required
@roles_required("administrator")
def consultants():
    page = request.args.get("page", 1, type=int)
    consultants = Consultant.query.order_by(User.id.desc()).paginate(page=page, per_page=5)
    return render_template("admin/consultants.html", consultants=consultants)


@admin.route("/jobs")
@login_required
@roles_required("consultant", "administrator")
def jobs():
    page = request.args.get("page", 1, type=int)
    jobs = Job.query.order_by(Job.id.desc()).paginate(page=page, per_page=5)
    return render_template("admin/jobs.html", jobs=jobs)


@admin.route("/applications")
@login_required
@roles_required("consultant", "administrator")
def applications():
    page = request.args.get("page", 1, type=int)
    applications = Application.query.order_by(Application.created_at.desc()).paginate(page=page, per_page=5)
    return render_template("admin/applications.html", applications=applications)


@admin.route("/activate/users/<int:id>", methods=["POST"])
@login_required
@roles_required("consultant", "administrator")
def activate_user(id):
    user = User.query.get_or_404(id)
    if user.is_active:
        flash("Le compte de cet utilisateur a déjà été activé.", "warning")
        return redirect(url_for("admin.candidates"))
    user.is_active = True
    db.session.commit()
    if user.role == "candidate":
        role = "candidat"
        next_page = "admin.candidates"
    else:
        role = "recruteur"
        next_page = "admin.recruiters"
    flash(f"Le {role} a bien été activé.", "success")
    return redirect(url_for(next_page))


# @admin.route("/deactivate/users/<int:id>", methods=["POST"])
# @login_required
# @roles_required("consultant", "administrator")
# def deactivate_user(id):
#     user = User.query.get_or_404(id)
#     if not user.is_active:
#         flash("Le compte de cet utilisateur a déjà été désactivé.", "warning")
#         return redirect(url_for("admin.candidates"))
#     user.is_active = False
#     db.session.commit()
#     if user.role == "candidate":
#         role = "candidat"
#         next_page = "admin.candidates"
#     else:
#         role = "recruteur"
#         next_page = "admin.recruiters"
#     flash(f"Le {role} a bien été désactivé.", "success")
#     return redirect(url_for(next_page))


@admin.route("/delete/users/<int:id>", methods=["POST"])
@login_required
@roles_required("administrator")
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.role == "candidate":
        role = "candidat"
        next_page = "admin.candidates"
    elif user.role == "recruiter":
        role = "recruteur"
        next_page = "admin.recruiters"
    else:
        role = "consultant"
        next_page = "admin.consultants"
    db.session.delete(user)
    db.session.commit()
    flash(f"Le {role} a bien été supprimé.", "success")
    return redirect(url_for(next_page))


@admin.route("/activate/jobs/<int:id>", methods=["POST"])
@login_required
@roles_required("consultant", "administrator")
def activate_job(id):
    job = Job.query.get_or_404(id)
    if job.is_active:
        flash("Cette annonce a déjà été activée.", "warning")
        return redirect(url_for("admin.jobs"))
    job.is_active = True
    db.session.commit()
    flash(f"L'annonce a bien été activée.", "success")
    return redirect(url_for("admin.jobs"))


# @admin.route("/deactivate/jobs/<int:id>", methods=["POST"])
# @login_required
# @roles_required("consultant", "administrator")
# def deactivate_job(id):
#     job = Job.query.get_or_404(id)
#     if not job.is_active:
#         flash("Cette annonce a déjà été désactivée.", "warning")
#         return redirect(url_for("admin.jobs"))
#     job.is_active = False
#     db.session.commit()
#     flash(f"L'annonce a bien été désactivée.", "success")
#     return redirect(url_for("admin.jobs"))


@admin.route("/delete/jobs/<int:id>", methods=["POST"])
@login_required
@roles_required("administrator")
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash(f"L'annonce a bien été supprimée.", "success")
    return redirect(url_for("admin.jobs"))


@admin.route("/create/consultant", methods=["GET", "POST"])
@login_required
@roles_required("administrator")
def create_consultant():
    form = CreateUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        consultant = Consultant(email=form.email.data, password=hashed_password)
        try:
            db.session.add(consultant)
            db.session.commit()
        except:
            flash("Un problème est survenu.", "error")
            return redirect(url_for("admin.consultants"))
        flash("Le consultant a bien été créé.", "success")
        return redirect(url_for("admin.consultants"))
    return render_template("admin/create-consultant.html", form=form)


@admin.route("/create/administrator", methods=["GET", "POST"])
def create_administrator():
    admin = Administrator.query.first()
    if admin:
        flash("Un administrateur existe déjà")
        return redirect(url_for("main.home"))
    form = CreateUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        administrator = Administrator(email=form.email.data, password=hashed_password)
        db.session.add(administrator)
        db.session.commit()
        flash("L'administrateur a bien été créé", "success")
        return redirect("main.home")
    return render_template("admin/create-administrator.html", form=form)


@admin.route("/activate/applications/<int:job_id>/<int:user_id>", methods=["POST"])
@login_required
@roles_required("consultant", "administrator")
def activate_application(job_id, user_id):
    application = Application.query.filter_by(job_id=job_id, user_id=user_id).first_or_404()
    if application.is_active:
        flash("Cette candidature a déjà été activée.", "warning")
        return redirect(url_for("admin.applications"))
    application.is_active = True
    db.session.commit()
    send_email(application.job.recruiter.email, f"static/uploads/{application.candidate.resume_file}")
    flash(f"La candidature a bien été activée.", "success")
    return redirect(url_for("admin.applications"))


# @admin.route("/deactivate/applications/<int:job_id>/<int:user_id>", methods=["POST"])
# @login_required
# @roles_required("consultant", "administrator")
# def deactivate_application(job_id, user_id):
#     application = Application.query.filter_by(job_id=job_id, user_id=user_id).first_or_404()
#     if not application.is_active:
#         flash("Cette candidature a déjà été désactivée.", "warning")
#         return redirect(url_for("admin.applications"))
#     application.is_active = False
#     db.session.commit()
#     flash(f"La candidature a bien été désactivée.", "success")
#     return redirect(url_for("admin.applications"))


@admin.route("/delete/applications/<int:job_id>/<int:user_id>", methods=["POST"])
@login_required
@roles_required("administrator")
def delete_application(job_id, user_id):
    application = Application.query.filter_by(job_id=job_id, user_id=user_id).first_or_404()
    db.session.delete(application)
    db.session.commit()
    flash(f"La candidature a bien été supprimée.", "success")
    return redirect(url_for("admin.applications"))