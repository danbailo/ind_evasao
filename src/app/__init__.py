from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config())
db = MongoEngine(app)
login = LoginManager(app)
login.login_view = "login"

from app import routes, models, errors

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User, 'Form': models.Form}