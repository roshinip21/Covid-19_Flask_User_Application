from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .password2 import MAIL_PASSWORD
from flask_mail import Mail
from flask_avatars import Avatars
from datetime import date, datetime,timedelta
from .api import CoWinAPI
import geocoder
from geopy.geocoders import Nominatim
import pgeocode
import plotly.graph_objs as go
import pandas as pd

# init SQLAlchemy
db = SQLAlchemy()
# init flask_mail
mail= Mail()
cowin = CoWinAPI()
avatars = Avatars()

#This function is called for initializing the flask application
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'SJWIWHFIAS' #secret key used for sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = "bethelmv2@gmail.com"
    app.config['MAIL_PASSWORD'] = password2.MAIL_PASSWORD
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    db.init_app(app)
    mail.init_app(app)
    avatars.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app. Blueprint is a an object of the flask application
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
