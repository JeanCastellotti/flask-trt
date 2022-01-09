from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user
from .forms import RegistrationForm, LoginForm
from app import bcrypt, db
from app.models import User, Candidate, Recruiter
from app.utils import is_safe_url

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        if form.role.data == "candidate":
            user = Candidate(email=form.email.data, password=hashed_password)
        else:
            user = Recruiter(email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash("Un problème est survenu.", "error")
            return redirect(url_for("main.home"))
        flash("Votre compte a bien été créé.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if not user.is_active:
                flash("Votre compte n'a pas été activé.", "error")
                return redirect(url_for("auth.login"))
            login_user(user, remember=form.remember.data)
            flash("Vous êtes connecté.", "success")
            next_page = request.args.get("next")
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for("main.home"))
        flash("Vos identifiants sont incorrects", "error")
    return render_template("login.html", form=form)