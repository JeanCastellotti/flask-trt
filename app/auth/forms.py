from flask_wtf import FlaskForm
from wtforms.fields import EmailField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirmation mot de passe', validators=[DataRequired(), EqualTo('password')])
    role = RadioField('Role', choices=[('candidate', 'Candidat'), ('recruiter', 'Recruteur')], default='candidate')
    submit = SubmitField('Créer mon compte')

