from flask import Blueprint, render_template, request
from sqlalchemy import text
from .db import db

routes = Blueprint("routes", __name__)


@routes.route("/")
def homepage():
    return render_template("index.html")

@routes.route("/main")
def main():
    sql = text("SELECT P.content, U.username, P.posted_at FROM posts P, users U WHERE P.user_id=U.id ORDER BY P.id")
    recipes = db.session.execute(sql)
    post_list = recipes.fetchall()
    return render_template("main.html", count=len(post_list), recipes=post_list)