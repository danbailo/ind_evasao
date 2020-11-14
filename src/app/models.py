from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime
import uuid
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Document):
    # _id = db.StringField(primary_key=True,required=True) #mongodb autoimplemnt this field
    name = db.StringField(max_length=128, min_length=4, required=True)
    username = db.StringField(max_length=64, min_length=4, unique=True, required=True)
    password_hash = db.StringField(max_length=64, min_length=4, required=True)
    email = db.EmailField(max_length=128, min_length=4, unique=True, required=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

@login.user_loader
def load_user(id):
    return User.objects(id=id).first()


class Form(db.Document):
    _id = db.StringField(primary_key=True, default=uuid.uuid4().hex, required=True) #mongodb autoimplemnt this field
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
    timestamp = db.DateTimeField(default=datetime.utcnow, required=True)
    user_id = db.StringField(unique=True, required=True)
