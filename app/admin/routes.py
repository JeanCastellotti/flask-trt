from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Candidate, Recruiter, Consultant, Administrator, Job
from app import db, bcrypt
from .forms import CreateUserForm

admin = Blueprint("admin", __name__, url_prefix="/admin")

def roles_required(*args):
    if not current_user.role in args:
        return abort(403)

@admin.route("/")
@admin.route("/candidates")
@login_required
def candidates():
    roles_required("consultant", "administrator")
    candidates = Candidate.query.order_by(User.id.desc()).all()
    return render_template("admin/candidates.html", candidates=candidates)


@admin.route("/recruiters")
@login_required
def recruiters():
    roles_required("consultant", "administrator")
    recruiters = Recruiter.query.order_by(User.id.desc()).all()
    return render_template("admin/recruiters.html", recruiters=recruiters)


@admin.route("/consultants")
@login_required
def consultants():
    roles_required("administrator")
    consultants = Consultant.query.order_by(User.id.desc()).all()
    return render_template("admin/consultants.html", consultants=consultants)


@admin.route("/jobs")
@login_required
def jobs():
    roles_required("consultant", "administrator")
    jobs = Job.query.order_by(Job.id.desc()).all()
    return render_template("admin/jobs.html", jobs=jobs)


@admin.route("/activate/users/<int:id>", methods=["POST"])
@login_required
def activate_user(id):
    roles_required("consultant", "administrator")
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


@admin.route("/deactivate/users/<int:id>", methods=["POST"])
@login_required
def deactivate_user(id):
    roles_required("consultant", "administrator")
    user = User.query.get_or_404(id)
    if not user.is_active:
        flash("Le compte de cet utilisateur a déjà été désactivé.", "warning")
        return redirect(url_for("admin.candidates"))
    user.is_active = False
    db.session.commit()
    if user.role == "candidate":
        role = "candidat"
        next_page = "admin.candidates"
    else:
        role = "recruteur"
        next_page = "admin.recruiters"
    flash(f"Le {role} a bien été désactivé.", "success")
    return redirect(url_for(next_page))


@admin.route("/delete/users/<int:id>", methods=["POST"])
@login_required
def delete_user(id):
    roles_required("consultant", "administrator")
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
def activate_job(id):
    roles_required("consultant", "administrator")
    job = Job.query.get_or_404(id)
    if job.is_active:
        flash("Cette annonce a déjà été activée.", "warning")
        return redirect(url_for("admin.jobs"))
    job.is_active = True
    db.session.commit()
    flash(f"L'annonce a bien été activée.", "success")
    return redirect(url_for("admin.jobs"))


@admin.route("/deactivate/jobs/<int:id>", methods=["POST"])
@login_required
def deactivate_job(id):
    roles_required("consultant", "administrator")
    job = Job.query.get_or_404(id)
    if not job.is_active:
        flash("Cette annonce a déjà été désactivée.", "warning")
        return redirect(url_for("admin.jobs"))
    job.is_active = False
    db.session.commit()
    flash(f"L'annonce a bien été désactivée.", "success")
    return redirect(url_for("admin.jobs"))


@admin.route("/delete/jobs/<int:id>", methods=["POST"])
@login_required
def delete_job(id):
    roles_required("consultant", "administrator")
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash(f"L'annonce a bien été supprimée.", "success")
    return redirect(url_for("admin.jobs"))


@admin.route("/create/consultant", methods=["GET", "POST"])
@login_required
def create_consultant():
    roles_required("administrator")
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


# @admin.route("/create/<string:role>", methods=["GET", "POST"])
# def create_user(role):
#     if not role in ["consultant", "administrator"]:
#         return abort(400)
#     if role == "administrator":
#         admin = Administrator.query.first()
#         if admin:
#             flash("Un administrateur existe déjà.", "error")
#             return redirect(url_for("main.home"))
#     if role == "consultant" and (not current_user.is_authenticated or current_user.role != "administrator"):
#         return abort(403)
#     form = CreateUserForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
#         if role == "consultant":
#             new_user = Consultant(email=form.email.data, password=hashed_password)
#             message = "Le consultant a bien été créé."
#         elif role == "administrator":
#             new_user = Administrator(email=form.email.data, password=hashed_password)
#             message = "L'administrateur a bien été créé."
#         try:
#             db.session.add(new_user)
#             db.session.commit()
#         except:
#             flash("Un problème est survenu.", "error")
#             return redirect(url_for("users.create"))
#         flash(message, "success")
#         return redirect(url_for("main.home"))
#     return render_template("create-user.html", form=form, role=role)