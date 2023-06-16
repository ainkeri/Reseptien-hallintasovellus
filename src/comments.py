from .db import db
from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import text

comments = Blueprint("comments", __name__)

@comments.route("/new_comment")
def new_comment():
    return render_template("new_comment.html")

@comments.route("/send_comment", methods=["POST"])
def send_comment():
    content = request.form.get("content")
    post_id = request.form.get("post_id")
    user_id = session.get("user_id", 0)


    sql = text("INSERT INTO comments (content, user_id, post_id, sent_at) VALUES (:content, :user_id, :post_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id, "post_id":post_id})
    db.session.commit()
    return redirect(url_for("routes.comments_list", recipe_id=post_id))

