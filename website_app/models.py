from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"


class PyTweet(db.Model):
    __tablename__ = 'py_tweets'
    id = db.Column(db.Integer, primary_key=True)
    tweet_text = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=func.now())
    username = db.Column(db.String(100), nullable=False)


class FlTweet(db.Model):
    __tablename__ = 'fl_tweets'
    id = db.Column(db.Integer, primary_key=True)
    tweet_text = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=func.now())
    username = db.Column(db.String(100), nullable=False)
