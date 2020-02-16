import requests
from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")#change to 'Som3$ec5etK*y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cargill_db:password@localhost/krace_gennedy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#db.create_all()######

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.getenv("MAIL_PASSWORD")
}

app.config.update(mail_settings)

mail = Mail(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

from app import views, models