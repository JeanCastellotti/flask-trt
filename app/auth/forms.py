from flask_wtf import FlaskForm
from wtforms.fields import EmailField, PasswordField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

DATA_REQUIRED = "Ce champ est obligatoire."
EMAIL_INVALID = "Cette adresse email n'est pas valide."
EMAIL_NOT_AVAILABLE = "Cette adresse email n'est pas disponible."
PASSWORD_LENGTH = "Le mot de passe doit faire au minimum 8 caractères."
PASSWORD_NOT_EQUAL = "Les mots de passe ne correspondent pas."

class RegistrationForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(DATA_REQUIRED), Email(EMAIL_INVALID)])
    password = PasswordField("Mot de passe", validators=[DataRequired(DATA_REQUIRED), Length(min=8, message=PASSWORD_LENGTH)])
    password_confirm = PasswordField("Confirmation mot de passe", validators=[DataRequired(DATA_REQUIRED), EqualTo("password", message=PASSWORD_NOT_EQUAL)])
    role = RadioField("Role", choices=[("candidate", "Candidat"), ("recruiter", "Recruteur")], default="candidate")
    submit = SubmitField("Créer mon compte")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email address is not available.")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(DATA_REQUIRED), Email(EMAIL_INVALID)])
    password = PasswordField("Mot de passe", validators=[DataRequired(DATA_REQUIRED)])
    remember = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter")