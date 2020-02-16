import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Som3$ec5etK*y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cargill_db:password@localhost/krace_gennedy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#db.create_all()######

mail = Mail(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

from app import views, models