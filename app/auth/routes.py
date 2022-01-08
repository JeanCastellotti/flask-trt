from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import RegistrationForm
from app import models, bcrypt, db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.role.data == 'candidate':
            user = models.Candidate(email=form.email.data, password=hashed_password)
        else:
            user = models.Recruiter(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Votre compte a été créé', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)

