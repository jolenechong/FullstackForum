from datetime import datetime, timedelta
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    # encrypt data with secret key
    app.config['SECRET_KEY'] = 'dbfduf2873b'
    # telling them where teh sqlite file should be
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # define schema in models.py

    # importing blueprints
    from .views import views
    from .auth import auth

    # register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # make sure the file runs by importing the databases
    from .models import User, Post, Like, Comment

    @app.template_filter()
    def format_datetime(value):
        current_time = datetime.utcnow()
        if current_time - timedelta(hours=1) < value:
            # posted less than an hour ago
            minutes_ago = int(current_time.strftime(format='%M')) - int(value.strftime(format='%M'))
            return minutes_ago,'minutes ago'
        elif current_time - timedelta(hours=24) < value:
            hours_left = int(current_time.strftime(format='%H')) - int(value.strftime(format='%H'))
            return hours_left,'hours ago'
        else:
            # return date if its over a day ago
            return 'on' ,value.strftime(format= "%d %b, %Y")

    create_database(app)

    login_manager = LoginManager()
    # where should flask redirect us if user is not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # tell flask which user we looking for, use this function to load user
        return User.query.get(int(id))

    return app

# connecting database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        # tell flask sqlalchemy which app to create database for
        print('Created Database!')
