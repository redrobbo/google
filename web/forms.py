#-----------------------------------------------------------------------------------------------------------------------
# Script | forms.py
# Author | Jonathan Cox
# Date   | 18 / 3 / 18
#-----------------------------------------------------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------------------------------------------------

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from web.models import User

#-----------------------------------------------------------------------------------------------------------------------
# Main - User Forms
#-----------------------------------------------------------------------------------------------------------------------

class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Taken')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email In Use')

#-----------------------------------------------------------------------------------------------------------------------

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#-----------------------------------------------------------------------------------------------------------------------

class UpdateAccount(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png', 'gif'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username Taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email In Use')

#-----------------------------------------------------------------------------------------------------------------------

class RequestReset(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email Does Not Exist')

#-----------------------------------------------------------------------------------------------------------------------

class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')

#-----------------------------------------------------------------------------------------------------------------------
# Main - Post Forms
#-----------------------------------------------------------------------------------------------------------------------

class PostForm(FlaskForm):
    gender_choices = [('Male', 'Male'),('Female', 'Female'),('Neutered Male', 'Neutered Male'),('Spayed Female', 'Spayed Female'), ('Unaltered', 'Unaltered'), ('Unknown', 'Unknown'), ('Intact Male', 'Intact Male'), ('Intact Female', 'Intact Female')]
    animal_name = StringField('Animal Name', validators=[DataRequired()])
    animal_type = StringField('Animal Type', validators=[DataRequired()])
    animal_gender = SelectField('Animal Gender', validators=[DataRequired()], choices=gender_choices)
    animal_breed = StringField('Animal Breed', validators=[DataRequired()])
    animal_color = StringField('Animal Colour', validators=[DataRequired()])
    address = StringField('Address')
    animal_pic = FileField('Animal Pic', validators=[FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Info', validators=[DataRequired()])
    submit = SubmitField('Post')

#-----------------------------------------------------------------------------------------------------------------------

class Search(FlaskForm):
    gender_choices = [('', 'Gender'),('Male', 'Male'), ('Female', 'Female'), ('Neutered Male', 'Neutered Male'), ('Spayed Female', 'Spayed Female'), ('Unaltered', 'Unaltered'), ('Unknown', 'Unknown'), ('Intact Male', 'Intact Male'), ('Intact Female', 'Intact Female')]
    search_name = StringField('Search', render_kw={"placeholder": "Name"}, id='name_names')
    search_type = StringField('Search', render_kw={"placeholder": "Animal"}, id='animal_animals')
    search_gender = SelectField('Animal Gender', choices=gender_choices)
    search_breed = StringField('Search', render_kw={"placeholder": "Breed"}, id='breed_breeds')
    search_color = StringField('Search', render_kw={"placeholder": "Colour"}, id='color_colors')
    submit = SubmitField('Search')


#-----------------------------------------------------------------------------------------------------------------------
# Test
#-----------------------------------------------------------------------------------------------------------------------

class SearchForm(FlaskForm):
    autocomp = StringField('Insert Name', id='name_names')