from .db import db
from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import text

comments = Blueprint("comments", __name__)

@comments.route("/new_comment/<int:post_id>")
def new_comment(post_id):
    post_id = request.form.get("post_id")
    return render_template("new_comment.html", post_id=post_id)

@comments.route("/send_comment/<int:post_id>", methods=["POST"])
def send_comment(post_id):
    content = request.form.get("content")
    post_id = request.form.get("post_id")
    user_id = session.get("user_id", 0)

    if not post_id:
        return render_template("error.html", message="Invalid post ID.")

    sql = text("INSERT INTO comments (content, user_id, post_id, sent_at) VALUES (:content, :user_id, :post_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id, "post_id":post_id})
    db.session.commit()
    return redirect(url_for("routes.comments_list", post_id=post_id))

 