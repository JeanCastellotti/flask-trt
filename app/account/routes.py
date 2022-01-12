from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import UpdateAccountCandidateForm, UpdateAccountRecruiterForm
from app import db
from app.utils import save_file, delete_file, roles_required

account = Blueprint("account", __name__, url_prefix="/account")


@account.route("/informations", methods=["GET", "POST"])
@login_required
@roles_required("candidate", "recruiter")
def informations():
    if current_user.role == "candidate":
        form = UpdateAccountCandidateForm()
    else:
        form = UpdateAccountRecruiterForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        if current_user.role == "candidate":
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            if form.resume_file.data:
                current_user.resume_file = save_file(form.resume_file.data)                
        else:
            current_user.company = form.company.data
            current_user.address = form.address.data
        db.session.commit()
        flash("Votre compte a bien été mis à jour", "success")
        return redirect(url_for("account.informations"))
    if request.method == "GET":
        form.email.data = current_user.email
        if current_user.role == "candidate":
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
        else:
            form.company.data = current_user.company
            form.address.data = current_user.address
    return render_template("account/informations.html", form=form)


@account.route("/jobs")
@login_required
@roles_required("recruiter")
def jobs():
    return render_template("account/jobs.html")


@account.route("/applications")
@login_required
@roles_required("candidate")
def applications():
    return render_template("account/applications.html")


@account.route("/delete_resume", methods=["POST"])
@login_required
@roles_required("candidate")
def delete_resume():
    if not current_user.resume_file:
        flash("Vous n'avez pas téléchargé de CV.", "error")
        return redirect(url_for("account.informations"))
    delete_file(current_user.resume_file)
    current_user.resume_file = None
    db.session.commit()
    flash("Votre CV a bien été supprimé", "success")
    return redirect(url_for("account.informations"))