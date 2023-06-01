from flask import Blueprint, render_template
from sqlalchemy import text
from .db import db

routes = Blueprint("routes", __name__)


@routes.route("/")
def homepage():
    return render_template("index.html")

@routes.route("/main")
def main():
    sql = text("SELECT P.content, U.username, P.posted_at FROM posts P, users U WHERE P.user_id = U.id ORDER BY P.id")
    result = db.session.execute(sql)
    return render_template("main.html", user=result)