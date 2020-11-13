from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object(Config())
db = MongoEngine(app)

from app import routes, models

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User, 'Form': models.Form}