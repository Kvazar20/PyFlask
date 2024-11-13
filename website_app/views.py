from flask import Blueprint, render_template, url_for, request, redirect, session
from datetime import date
import math
import os
from config import ITEMS_PER_PAGE, ADMIN_PASSWORD
from .models import PyTweet, FlTweet, db

views = Blueprint('views', __name__)


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/python")
def python_index():
    page = request.args.get('page', default=1, type=int)

    offset = (page - 1) * ITEMS_PER_PAGE

    # Database query with an offset and a limit
    tweets = PyTweet.query.order_by(PyTweet.date.desc()).offset(offset).limit(ITEMS_PER_PAGE).all()
    total_pages_amount = 1 if PyTweet.query.count() == 0 else math.ceil(PyTweet.query.count() / 6)

    return render_template("python.html", tweets=tweets, pg=page, total_pg=total_pages_amount)


@views.route("/flask")
def flask_index():
    page = request.args.get('page', default=1, type=int)

    offset = (page - 1) * ITEMS_PER_PAGE

    # Database query with an offset and a limit
    tweets = FlTweet.query.order_by(FlTweet.date.desc()).offset(offset).limit(ITEMS_PER_PAGE).all()
    total_pages_amount = 1 if FlTweet.query.count() == 0 else math.ceil(FlTweet.query.count() / 6)

    return render_template("flask.html", tweets=tweets, pg=page, total_pg=total_pages_amount)


@views.route("/learn")
def learn_index():
    return render_template("learn.html")


@views.route('/admin_panel')
def admin_panel():
    if session.get('logged_in'):
        view_all = request.args.get('view_all', default='False') == 'True'
        error_message = request.args.get('error_message', 'False') == 'True'
        len_py_tweets = PyTweet.query.count()
        len_fl_tweets = FlTweet.query.count()

        if len_py_tweets >= 3 and not view_all:
            py_tweets = PyTweet.query.order_by(PyTweet.date.desc()).limit(3).all()
        else:
            py_tweets = PyTweet.query.order_by(PyTweet.date.desc()).all()

        if len_fl_tweets >= 3 and not view_all:
            fl_tweets = FlTweet.query.order_by(FlTweet.date.desc()).limit(3).all()
        else:
            fl_tweets = FlTweet.query.order_by(FlTweet.date.desc()).all()

        return render_template('admin_panel.html', py_tweets=py_tweets, fl_tweets=fl_tweets,
                                view_all=view_all, error_message=error_message, py_len=len_py_tweets, fl_len=len_fl_tweets)

    else:
        return redirect(url_for('views.signin'))


@views.route('/error')
def error():
    return render_template('error.html')


@views.route("/python/write_tweet/<int:page_num>", methods=["POST"])
def python_write_tweet(page_num):
    new_tweet = PyTweet(tweet_text=request.form['tweet'], username=request.form['username'])
    db.session.add(new_tweet)
    db.session.commit()
    return redirect(url_for('views.python_index', page=page_num))


@views.route("/flask/write_tweet/<int:page_num>", methods=["POST"])
def flask_write_tweet(page_num):
    new_tweet = FlTweet(tweet_text=request.form['tweet'], username=request.form['username'])
    db.session.add(new_tweet)
    db.session.commit()
    return redirect(url_for('views.flask_index', page=page_num))


@views.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html", error_message=False)
    else:
        if request.form["password"] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('views.admin_panel'))
        else:
            return render_template("signin.html", error_message=True)


@views.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('views.index'))


@views.route("/search", methods=["GET"])
def search():
    keyword = (request.args.get("search-input")).lower()
    searched_tweets = []

    # I used SQLAlchemy queries with ilike for case-insensitive search in the database
    py_searched_tweets = PyTweet.query.filter(
        (PyTweet.tweet_text.ilike(f"%{keyword}%")) |
        (PyTweet.date.ilike(f"%{keyword}%")) |
        (PyTweet.username.ilike(f"%{keyword}%"))
    ).all()

    fl_searched_tweets = FlTweet.query.filter(
        (FlTweet.tweet_text.ilike(f"%{keyword}%")) |
        (FlTweet.date.ilike(f"%{keyword}%")) |
        (FlTweet.username.ilike(f"%{keyword}%"))
    ).all()

    searched_tweets = py_searched_tweets + fl_searched_tweets
    error_message = True if not searched_tweets else False

    return render_template("searched_tweets.html", error_message=error_message, tweets=searched_tweets)


@views.route('/delete_tweet/<forum>/<int:tweet_id>', methods=["GET", "POST"])
def delete_tweet(forum, tweet_id):
    error_message = False
    if forum == "python":
        tweet_to_delete = PyTweet.query.get(tweet_id)
        if tweet_to_delete:
            db.session.delete(tweet_to_delete)
            db.session.commit()
            return redirect(url_for('views.admin_panel', view_all=True))
        else:
            return "Tweet not found", 404

    else:
        tweet_to_delete = FlTweet.query.get(tweet_id)
        if tweet_to_delete:
            db.session.delete(tweet_to_delete)
            db.session.commit()
            return redirect(url_for('views.admin_panel', view_all=True))
        else:
            return "Tweet not found", 404

