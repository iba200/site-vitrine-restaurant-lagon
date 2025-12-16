from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField, TimeField, IntegerField, DecimalField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from .models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')

class ReservationForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Heure', validators=[DataRequired()])
    guests = IntegerField('Nombre de personnes', validators=[DataRequired(), NumberRange(min=1, max=20)])
    first_name = StringField('Prénom', validators=[DataRequired(), Length(1, 64)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    phone = StringField('Téléphone', validators=[DataRequired(), Length(1, 20)])
    special_requests = TextAreaField('Demandes particulières')
    submit = SubmitField('Réserver')

class ContactForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Envoyer')

class MenuItemForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(1, 150)])
    category_id = SelectField('Catégorie', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description')
    price = DecimalField('Prix', validators=[DataRequired()])
    image = FileField('Photo du plat')
    allergens = StringField('Allergènes')
    dietary_tags = StringField('Régimes (ex: vegan, sans-gluten)')
    is_available = BooleanField('Disponible')
    is_special = BooleanField('Spécialité')
    submit = SubmitField('Enregistrer')
