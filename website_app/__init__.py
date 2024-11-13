from flask import Flask
from .views import views
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY
import math
from os import path
from .models import PyTweet, FlTweet, db, DB_NAME

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.register_blueprint(views, url_prefix='/')
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    create_database(app)

    @app.template_filter('ceil')
    def ceil_filter(value):
        return math.ceil(value)

    @app.template_filter('length')
    def length_filter(arr: list):
        return len(arr)

    return app


def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
