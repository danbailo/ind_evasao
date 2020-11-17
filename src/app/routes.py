import uuid

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.email import send_password_reset_email
from app.forms import (LoginForm, RegisterForm, ResetPasswordForm,
                       ResetPasswordRequestForm, AnswersForm)
from app.models import User, Answer
import io
import matplotlib.pyplot as plt
import base64

@app.route("/")
@app.route("/index")
def index():
    login_form = LoginForm()
    register_form = RegisterForm()
    answers_form = AnswersForm()
    return render_template("index.html",
                           title="Home", 
                           login_form=login_form, 
                           register_form=register_form,
                           answers_form=answers_form)


@app.route("/login", methods=["GET", "POST"]) # allow methods GET and POST to this view
def login():
    if current_user.is_authenticated: # if user try to navigates to /login
        return redirect(url_for("index"))
    register_form = RegisterForm()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.objects(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Usuário ou senha inválidos!', "danger")
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

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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
        return redirect(url_for('index'))
    return render_template("index.html", register_form=register_form, login_form=login_form)

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
        flash('Check your email for the instructions to reset your password', "success")
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
        flash('Your password has been reset.', "success")
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route("/answers", methods=["GET","POST"])
@login_required
def answers():
    if current_user.get_answer():

        img = io.BytesIO()

        y = [1,2,3,4,5]
        x = [0,2,1,3,4]
        plt.bar(x,y)
        plt.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template("index.html", image=plot_url)

    answers_form = AnswersForm()
    if answers_form.validate_on_submit():
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
        current_user.set_answer(True)
        current_user.save()
        answers.save()
        flash('Respota salva com sucesso!', "success")
        return redirect(url_for('index'))
    return render_template("answers.html", title="Formulário de Respostas", answers_form=answers_form)

@app.route("/about")
def about():
    pass

def build_plot():
    colors = ['red', 'green', 'blue', 'purple', 'darkorange', 'brown', 'yellow', 'gray', 'cyan', 'olive', 'chocolate']
    all_answers = Answer.get_all_answers()

    img = io.BytesIO()

    x = list(all_answers.keys())
    y = list(all_answers.values()) #height
    plt.figure(figsize=(12, 8))
    bar_list = plt.bar(x,y, zorder=3)
    plt.grid(axis="both")
    for i, color in enumerate(colors):
        bar_list[i].set_color(color)    
    plt.xticks(rotation=90)
    max_y_value = max(y)
    int_yticks = list(range(0, max_y_value+1))
    plt.yticks(int_yticks)
    plt.xlabel("Respostas em ordem")
    plt.ylabel("Quantidade")    
    plt.savefig(img, format='jpg')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

@app.context_processor
def build_plot_decorator():
    return dict(image=build_plot())