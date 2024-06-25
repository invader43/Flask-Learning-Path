import os
import json

with open("/etc/config.json","r") as config_file:
    config = json.load(config_file)
    print(config)



class Config:
    SECRET_KEY = config.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USER_TLS = False
    MAIL_USER_SSL = True
    MAIL_USERNAME = config.get("EMAIL")
    MAIL_PASSWORD = config.get("PASSWORD")
