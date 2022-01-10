from flask_wtf import FlaskForm
from wtforms.fields import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class CreateUserForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField("Confirmation mot de passe", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Créer")