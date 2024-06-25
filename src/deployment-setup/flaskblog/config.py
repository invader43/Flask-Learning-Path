import os



class Config:
    SECRET_KEY = '03c846950425a22fc22fb6be5f12ef6d'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USER_TLS = False
    MAIL_USER_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('PASSWORD')