from flask_wtf import FlaskForm
from wtforms.fields import EmailField, PasswordField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired("Ce champ est obligatoire"), Email("L'adresse email est incorrecte.")])
    password = PasswordField("Mot de passe", validators=[DataRequired("Ce champ est obligatoire"), Length(min=8, message="Le mot de passe doit faire au minimum 8 caractères.")])
    password_confirm = PasswordField("Confirmation mot de passe", validators=[DataRequired("Ce champ est obligatoire"), EqualTo("password", message="Les mots de passe ne correspondent pas.")])
    role = RadioField("Role", choices=[("candidate", "Candidat"), ("recruiter", "Recruteur")], default="candidate")
    submit = SubmitField("Créer mon compte")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Cette adresse email n'est pas disponible.")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired("Ce champ est obligatoire"), Email("Cette adresse email est incorrecte.")])
    password = PasswordField("Mot de passe", validators=[DataRequired("Ce champ est obligatoire")])
    remember = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter")