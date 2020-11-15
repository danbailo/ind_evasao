import uuid

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.email import send_password_reset_email
from app.forms import (LoginForm, RegisterForm, ResetPasswordForm,
                       ResetPasswordRequestForm)
from app.models import User


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")

@app.route("/login", methods=["GET", "POST"]) # allow methods GET and POST to this view
def login():
    if current_user.is_authenticated: # if user try to navigates to /login
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # when an user try to access a content that needs login
        # its necessary get the url content to redirect it to the next page
        next_page = request.args.get('next') 
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)        
    return render_template("login.html", title="Sign In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    username=form.username.data, 
                    email=form.email.data)
        user.set_password(form.password.data)
        user.set_id(uuid.uuid4().hex)
        user.save()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)

@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            # I'm not doing the condition for verify if the email exists, because
            # if I do it, an anonymous user can verify if an user have an account in my system.            
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for("login"))
    return render_template("reset_password_request.html",
                           title="Reset Password", form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.save()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)