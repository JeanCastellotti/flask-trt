from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, SubmitField
from flask_login import current_user
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models import User

class UpdateAccountForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Mettre à jour")

    def validate_email(self, email):
        if email.data == current_user.email: return
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Cette adresse email n'est pas disponible.")

class UpdateAccountCandidateForm(UpdateAccountForm):
    first_name = StringField("Prénom", validators=[Length(max=50)])
    last_name = StringField("Nom", validators=[Length(max=50)])
    resume_file = FileField("CV", validators=[FileAllowed(["pdf"])])

    def validate_first_name(self, first_name):
        if current_user.applications and not first_name.data:
            raise ValidationError("Ce champs est obligatoire.")

    def validate_last_name(self, last_name):
        if current_user.applications and not last_name.data:
            raise ValidationError("Ce champs est obligatoire.")


class UpdateAccountRecruiterForm(UpdateAccountForm):
    company = StringField("Société", validators=[Length(max=50)])
    address = StringField("Adresse", validators=[Length(max=150)])

    def validate_company(self, company):
        if current_user.jobs and not company.data:
            raise ValidationError("Ce champs est obligatoire.")

    def validate_address(self, address):
        if current_user.jobs and not address.data:
            raise ValidationError("Ce champs est oligaroire.")