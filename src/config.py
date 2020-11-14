import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGODB_SETTINGS = os.environ.get("DATABASE_URL") or\
    {
        'db': 'ind_evasao',
    }