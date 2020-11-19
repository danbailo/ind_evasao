import uuid

from app import db
from app.auth import bp
from app.auth.email import send_password_reset_email
from app.auth.forms import (LoginForm, RegisterForm, ResetPasswordForm,
                            ResetPasswordRequestForm)
from app.models import User
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@bp.route("/login", methods=["GET", "POST"]) # allow methods GET and POST to this view
def login():
    if current_user.is_authenticated: # if user try to navigates to /login
        return redirect(url_for('main.index'))
    register_form = RegisterForm()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.objects(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Usuário ou senha inválidos!', "danger")
            return redirect(url_for('main.index'))
        login_user(user, remember=login_form.remember_me.data)
        # when an user try to access a content that needs login
        # its necessary get the url content to redirect it to the next page
        next_page = request.args.get('next') 
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)        
    return render_template("index.html", login_form=login_form, register_form=register_form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    register_form = RegisterForm()
    login_form = LoginForm()
    if register_form.validate_on_submit():
        user = User(name=register_form.name.data,
                    username=register_form.username.data, 
                    email=register_form.email.data)
        user.set_password(register_form.password.data)
        user.set_id(uuid.uuid4().hex)
        user.save()
        flash('Parabéns, agora você é um usuário registrado!', "success")
        return redirect(url_for('main.index'))
    return render_template("index.html", register_form=register_form, login_form=login_form)

@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            # I'm not doing the condition for verify if the email exists, because
            # if I do it, an anonymous user can verify if an user have an account in my system.            
        flash('Check your email for the instructions to reset your password', "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_request.html",
                           title="Reset Password", form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.save()
        flash('Your password has been reset.', "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
