from .db import db
from .auth import auth
from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import text

posts = Blueprint("posts", __name__)

@posts.route("/new")
def new():
    return render_template("new.html")

@posts.route("/send", methods=["POST"])
def send():
    content = request.form.get("content")
    user_id = session.get("user_id", 0)
    if user_id == 0:
        return render_template("error.html", message="Post failed")
    sql = text("INSERT INTO posts (content, user_id, posted_at) VALUES (:content, :user_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return render_template("main.html")