from app import db
import uuid

class User(db.Document):
    _id = db.StringField(primary_key=True, required=True) #mongodb autoimplemnt this field
    username = db.StringField(max_length=64, min_length=4, required=True, unique=True)
    password_hash = db.StringField(max_length=64, min_length=4, required=True)
    email = db.EmailField(max_length=128, min_length=4, required=True, unique=True)

    def __repr__(self):
        return f"<User {self.username}>"

if __name__ == "__main__":
    user = User()
    user._id = uuid.uuid4().hex
    user.username = "Daniel"
    user.password_hash = "1234"
    user.email = "dan@email.com"
    user.save()