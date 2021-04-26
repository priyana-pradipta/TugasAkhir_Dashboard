# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo, ValidationError, Length

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired(message="Harap Isi Bagian Ini!")])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired(message="Harap Isi Bagian Ini!")])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired("Harap Isi Bagian Ini!")])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(message="Harap Isi Bagian Ini!"), Email(message="Harap Isi dengan Email!")])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired(message="Harap Isi Bagian Ini!")])
    confirm_password = PasswordField('Confirm Password', id= 'pwd_confirm',
                                     validators=[DataRequired(message="Harap Isi Bagian Ini!"), EqualTo('password', message="Password Tidak Sama!")])
    submit = SubmitField('Daftar')

class RequestResetForm(FlaskForm):
    email = TextField('Email', id="email_forget", validators=[DataRequired(message="Harap Isi Bagian Ini!"), Email(message="Harap Isi dengan Email!")])
    submit = SubmitField('Kirim Email')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', id='pwd_new', validators=[DataRequired(message="Harap Isi Bagian Ini!")])
    confirm_password = PasswordField('Confirm Password', id= 'pwd_confim',
                                     validators=[DataRequired(), EqualTo('password', message="Password Tidak Sama!")])
    submit = SubmitField('Ganti Password')