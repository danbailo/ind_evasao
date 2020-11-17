import uuid
from datetime import datetime
from time import time

import jwt
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db, login


class User(UserMixin, db.Document):
    _id = db.StringField(primary_key=True, required=True) #mongodb autoimplemnt this field
    name = db.StringField(required=True)
    username = db.StringField(unique=True, required=True)
    password_hash = db.StringField(required=True)
    email = db.EmailField(unique=True, required=True)
    answered = db.BooleanField(default=False, required=True)
    # activated

    def set_id(self, _id):
        self._id = _id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self._id, "exp": time() + expires_in},
            app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")

    def get_answer(self):
        return self.answered

    def set_answer(self, value):
        self.answered = value

    @staticmethod
    def verify_reset_password_token(token):
        try:
            _id = jwt.decode(token, app.config["SECRET_KEY"],
                            algorithms=["HS256"])["reset_password"]
        except:
            return None
        return User.objects(_id=_id).first()

    def __repr__(self):
        return f"<User {self.username}>"

@login.user_loader
def load_user(_id):
    return User.objects(_id=_id).first()


class Answer(db.Document):
    _id = db.StringField(primary_key=True, required=True) #mongodb autoimplemnt this field
    answer_1 = db.BooleanField(required=True)
    answer_2 = db.BooleanField(required=True)
    answer_3 = db.BooleanField(required=True)
    answer_4 = db.BooleanField(required=True)
    answer_5 = db.BooleanField(required=True)
    answer_6 = db.BooleanField(required=True)
    answer_7 = db.BooleanField(required=True)
    answer_8 = db.BooleanField(required=True)
    answer_9 = db.BooleanField(required=True)
    answer_10 = db.BooleanField(required=True)
    answer_11 = db.BooleanField(required=True)
    # timestamp = db.DateTimeField(default=datetime.utcnow, required=True)
    user_id = db.StringField(unique=True, required=True)

    @staticmethod
    def get_all_answers():
        all_answers = {}
        for answer in Answer.objects:
            for i in range(1, 12):
                if not all_answers.get(str(i)):
                    all_answers[str(i)] = 0
                if answer["answer_"+str(i)] == True:
                    all_answers[str(i)] += 1
        return all_answers