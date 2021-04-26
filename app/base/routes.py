# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os, secrets
from flask import jsonify, render_template, redirect, request, url_for, abort
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager, mail, bcrypt
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm, RequestResetForm, ResetPasswordForm
from app.base.models import User
from flask_mail import Message
from app.base.util import verify_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if 'login' in request.form:
            
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
            
        # Check the password
        if user and bcrypt.check_password_hash(user.password, password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Username atau Password Salah', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    else: 
        return redirect(url_for('home_blueprint.home_index'))

    return redirect(url_for('home_blueprint.home_index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home_index'))

    #login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    #if 'register' in request.form:
    if create_account_form.validate_on_submit():
        username  = request.form['username']
        email     = request.form['email'   ]
        password  = request.form['password']

            # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
                return render_template( 'accounts/register.html', 
                                            msg='Username Sudah Digunakan !',
                                            success=False,
                                            form=create_account_form)

                # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
                return render_template( 'accounts/register.html', 
                                            msg='Email Sudah Digunakan !', 
                                            success=False,
                                            form=create_account_form)

                # else we can create the user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', 
                                        msg='User Sudah Terdaftar, Silahkan <a href="/login">Masuk</a>', 
                                        success=True,
                                        form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route("/forgot_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home_index'))

    request_reset_form = RequestResetForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    login_form = LoginForm(request.form)
    if request_reset_form.validate_on_submit():

        email     = request.form['email'   ]

        user = User.query.filter_by(email=email).first()
        if user is None:
            #raise ValidationError('There is no account with that email. You must register first.')
            return render_template( 'accounts/forgot-password.html', 
                                    msg='Email tidak terdaftar, Register Dahulu',
                                    success=False,
                                    form=request_reset_form)
        else :
            send_reset_email(user)
            #flash('An email has been sent with instructions to reset your password.', 'info')
            #return redirect(url_for('base_blueprint.login')) 
            return render_template( 'accounts/login.html', 
                                    msg='Email Reset Password Sudah Dikirim, Silahkan Cek Email',
                                    success=True,
                                    form=login_form)    
    else :
        return render_template('accounts/forgot-password.html', form=request_reset_form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='priyanapradipta@gmail.com',
                  recipients=[user.email])
    msg.html = render_template('reset_email.html', token=token)

    mail.send(msg)


@blueprint.route("/recover_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home_index'))
        
    user = User.verify_reset_token(token)
    request_reset_form = RequestResetForm(request.form)
    reset_password_form = ResetPasswordForm(request.form)
    if user is None:
        #flash('That is an invalid or expired token', 'warning')
        return render_template( 'accounts/forgot-password.html', 
                                msg='Token Salah atau Kadaluwarsa',
                                success=False,
                                form=request_reset_form)
    else :
        if reset_password_form.validate_on_submit():

            password     = request.form['password'   ]

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            #flash('Your password has been updated! You are now able to log in', 'success')
            return render_template( 'accounts/recover-password.html', 
                                    msg='Password Sudah Diganti, Silahkan <a href="/login">Masuk</a>', 
                                    success=True,
                                    form=reset_password_form)
        else :
            return render_template('accounts/recover-password.html', form=reset_password_form)

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
