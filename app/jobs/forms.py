from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length


class CreateJobForm(FlaskForm):
    title = StringField("Titre", validators=[DataRequired("Ce champ est obligatoire."), Length(max=150, message="Le titre doit faire moins de 150 caractères.")])
    place = StringField("Lieu", validators=[DataRequired("Ce champ est obligatoire."), Length(max=50, message="La ville doit faire moins de caractères.")])
    salary = IntegerField("Salaire", validators=[DataRequired("Ce champ est obligatoire.")])
    working_hours = SelectMultipleField("Horaires de travail", 
                                        validators=[DataRequired("Ce champ est obligatoire.")], 
                                        choices=[
                                            ("week", "Du lundi au vendredi"),
                                            ("week-end", "Le week-end"),
                                            ("evening", "Le soir")
                                        ])
    description = TextAreaField("Description", validators=[DataRequired("Ce champ est obligatoire.")])
    submit = SubmitField("Publier une annonce")