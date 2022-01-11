from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class UpdateAccountCandidateForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("Prénom", validators=[Length(max=50)])
    last_name = StringField("Nom", validators=[Length(max=50)])
    resume_file = FileField("CV", validators=[FileAllowed(["pdf"])])
    submit = SubmitField("Mettre à jour")


class UpdateAccountRecruiterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    company = StringField("Société", validators=[Length(max=50)])
    address = StringField("Adresse", validators=[Length(max=150)])
    submit = SubmitField("Mettre à jour")