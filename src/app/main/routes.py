import base64
import io
import uuid

import matplotlib.pyplot as plt
from app import db
from app.auth.email import send_password_reset_email
from app.main import bp
from app.main.forms import AnswersForm
from app.models import Answer, User
from flask import (current_app, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@bp.route("/index")
@bp.route("/")
@login_required
def index():
    answers_form = AnswersForm()
    return render_template("index.html",
                           title="Início",
                           answers_form=answers_form)


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
    # return render_template("index.html", title="Formulário de Respostas", answers_form=answers_form)

@bp.route("/about")
def about():
    pass

def build_plot():
    # colors = ['red', 'green', 'blue', 'purple', 'darkorange', 'brown', 'yellow', 'gray', 'cyan', 'olive', 'chocolate']
    all_answers = Answer.get_all_answers()

    img = io.BytesIO()

    x = list(all_answers.keys())
    y = list(all_answers.values()) #height
    plt.figure(figsize=(12, 8))
    bar_list = plt.bar(x,y, zorder=3, color="purple", width=0.5)
    plt.grid(axis="both")
    # for i, color in enumerate(colors):
        # bar_list[i].set_color(color)    
    plt.xticks(fontsize=15)
    max_y_value = max(y)
    int_yticks = list(range(0, max_y_value+1))
    plt.yticks(int_yticks, fontsize=15)
    plt.xlabel("Respostas", fontsize=15)
    plt.ylabel("Quantidade", fontsize=15)    
    plt.savefig(img, format='jpg')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

# @app.context_processor
# def build_plot_decorator():
#     return dict(image=build_plot())

# @app.context_processor
# def get_n_answers():
#     return dict(n_answers=Answer.objects.count())
