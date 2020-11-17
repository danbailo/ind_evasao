from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired("Esse campo é necessário!")])
    password = PasswordField("Senha", validators=[DataRequired("Esse campo é necessário!")])
    remember_me = BooleanField("Lembrar de Mim")
    submit = SubmitField("Entrar")

class RegisterForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired("Esse campo é necessário!")])
    username = StringField("Usuário", validators=[DataRequired("Esse campo é necessário!")])
    email = StringField("Email", validators=[DataRequired("Esse campo é necessário!"), Email()])
    password = PasswordField("Senha", validators=[DataRequired("Esse campo é necessário!")])
    repeat_password = PasswordField(
        "Repetir Senha", validators=[DataRequired("Esse campo é necessário!"), EqualTo("password")])
    submit = SubmitField("Registrar")

    # when validate_<> pattern is used in methods with a name of a field
    # thats was used in class, it will link the methods like as validator
    # and call it automatically in your respectively form

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Por favor, escolha um nome de usuário diferente!")    

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Por favor, escolha um nome de email diferente!")

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Esse campo é necessário!"), Email()])
    submit = SubmitField('Solicitar Redefinição de Senha')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Senha', validators=[DataRequired("Esse campo é necessário!")])
    repeat_password = PasswordField(
        'Repetir Senha', validators=[DataRequired("Esse campo é necessário!"), EqualTo('password')])
    submit = SubmitField('Solicitar Redefinição de Senha')

class AnswersForm(FlaskForm):
    answer_1 = BooleanField("Campus não fornece RU (Restaurante Universitário)")
    answer_2 = BooleanField("Problemas psicológicos")
    answer_3 = BooleanField("Questões familiares (ex: algum familiar com problema de saúde, etc)")
    answer_4 = BooleanField("Problemas financeiros")
    answer_5 = BooleanField("Saudades de casa")
    answer_6 = BooleanField("Transporte (ex: movimentação na cidade, ir para faculdade, etc)")
    answer_7 = BooleanField("Infraestrutura da cidade (ex: internet, aluguel, etc)")
    answer_8 = BooleanField("Segurança (ex: não se sente seguro na faculdade ou nas redondezas da mesma)")
    answer_9 = BooleanField("Comprometimento com o curso (ex: não leva o mesmo a sério e com o tempo se cria uma bola de neve)")
    answer_10 = BooleanField("Insatisfação com o curso (ex: não está se sentindo pessoalmente realizado com o curso)")
    answer_11 = BooleanField("Não se adaptou as diferenças regionais")
    submit = SubmitField('Submeter Formulário')
