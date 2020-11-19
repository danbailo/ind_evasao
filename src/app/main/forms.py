from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


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
