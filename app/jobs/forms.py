from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateJobForm(FlaskForm):
    title = StringField("Titre", validators=[DataRequired(), Length(max=150)])
    place = StringField("Lieu", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Publier une annonce")