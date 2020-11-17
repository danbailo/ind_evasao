from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember_me = BooleanField("Lembrar de Mim")
    submit = SubmitField("Entrar")

class RegisterForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired()])
    username = StringField("Usuário", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    repeat_password = PasswordField(
        "Repetir Senha", validators=[DataRequired(), EqualTo("password")])
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar Redefinição de Senha')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Senha', validators=[DataRequired()])
    repeat_password = PasswordField(
        'Repetir Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Solicitar Redefinição de Senha')    