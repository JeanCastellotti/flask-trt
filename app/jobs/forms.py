from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length


class CreateJobForm(FlaskForm):
    title = StringField("Titre", validators=[DataRequired(), Length(max=150)])
    place = StringField("Lieu", validators=[DataRequired(), Length(max=50)])
    salary = IntegerField("Salaire", validators=[DataRequired()])
    working_hours = SelectMultipleField("Horaires de travail", 
                                        validators=[DataRequired()], 
                                        choices=[
                                            ("week", "Du lundi au vendredi"),
                                            ("week-end", "Le week-end"),
                                            ("evening", "Le soir")
                                        ])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Publier une annonce")