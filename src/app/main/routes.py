import uuid

from app import db
from app.auth.email import send_password_reset_email
from app.auth.forms import LoginForm, RegisterForm
from app.main import bp
from app.main.forms import AnswersForm
from app.models import Answer
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required


@bp.route("/index")
@bp.route("/")
def index():
    answers_form = AnswersForm()
    register_form = RegisterForm()
    login_form = LoginForm()
    return render_template("index.html",
                           title="Início",
                           answers_form=answers_form,
                           register_form=register_form,
                           login_form=login_form)


@bp.route("/answers", methods=["GET","POST"])
@login_required
def answers():
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
    return redirect(url_for('main.index'))

@bp.route("/about")
def about():
    pass
