import uuid

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.email import send_password_reset_email
from app.forms import (LoginForm, RegisterForm, ResetPasswordForm,
                       ResetPasswordRequestForm, AnswersForm)
from app.models import User, Answer


@app.route("/")
@app.route("/index")
def index():
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template("index.html", title="Home", login_form=login_form, register_form=register_form)


@app.route("/login", methods=["POST"]) # allow methods GET and POST to this view
def login():
    if current_user.is_authenticated: # if user try to navigates to /login
        return redirect(url_for("index"))
    register_form = RegisterForm()
    login_form = LoginForm()
    if login_form.is_submitted():
        user = User.objects(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Usuário ou senha inválidos')
            return redirect(url_for('index'))
        login_user(user, remember=login_form.remember_me.data)
        # when an user try to access a content that needs login
        # its necessary get the url content to redirect it to the next page
        next_page = request.args.get('next') 
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)        
    return render_template("index.html", login_form=login_form, register_form=register_form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    register_form = RegisterForm()
    login_form = LoginForm()
    if register_form.is_submitted():
        user = User(name=register_form.name.data,
                    username=register_form.username.data, 
                    email=register_form.email.data)
        user.set_password(register_form.password.data)
        user.set_id(uuid.uuid4().hex)
        user.save()
        flash('Parabéns, agora você é um usuário registrado!')
        return redirect(url_for('index'))
    return render_template("index.html", register_form=register_form, login_form=login_form)

@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm()
    if form.is_submitted():
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
    if form.is_submitted():
        user.set_password(form.password.data)
        user.save()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route("/answers", methods=["GET","POST"])
@login_required
def answers():
    answers_form = AnswersForm()
    if answers_form.is_submitted():
        answers = Answer(
            _id=uuid.uuid4().hex,
            answer_1=answers_form.answer_1.data, 
            answer_2=answers_form.answer_2.data,
            answer_3=answers_form.answer_3.data,
            answer_4=answers_form.answer_4.data,
            answer_5=answers_form.answer_5.data,
            answer_6=answers_form.answer_6.data,
            answer_7=answers_form.answer_7.data,
            answer_8=answers_form.answer_8.data,
            answer_9=answers_form.answer_9.data,
            answer_10=answers_form.answer_10.data,
            answer_11=answers_form.answer_11.data,
            user_id=current_user._id
        )
        answers.save()
        return redirect(url_for('index'))
    return render_template("answers.html", title="Formulário de Respostas", answers_form=answers_form)