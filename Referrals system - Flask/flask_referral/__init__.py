from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'holaflask'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = 'Login Required to access this page.'
login_manager.login_message_category = 'danger'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flask_referral.routes import app