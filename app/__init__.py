from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_db'
db = SQLAlchemy(app)  # flask-sqlalchemy


from app import views
# from app import db_manager