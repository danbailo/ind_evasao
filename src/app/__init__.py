import logging
from logging.handlers import SMTPHandler

from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object(Config())
db = MongoEngine(app)
login = LoginManager(app)
login.login_view = "login"

from app import errors, models, routes

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": models.User, "Form": models.Form}

# sent a message to admin email reporting a database error for example
if not app.debug:
    if app.config["MAIL_SERVER"]:
        auth = None
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr="no-reply@" + app.config["MAIL_SERVER"],
            toaddrs=app.config["ADMINS"], subject="Índice de Evasão - Falha no sistema!",
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
