import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    MONGODB_DB = os.environ.get("MONGODB_DB")
    MONGODB_HOST = os.environ.get("MONGODB_HOST")
    MONGODB_PORT = int(os.environ.get("MONGODB_PORT"))
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["danbailoufms@gmail.com"]