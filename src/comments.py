from .db import db
from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from sqlalchemy import text

comments = Blueprint("comments", __name__)

@comments.route("/new_comment/<int:post_id>")
def new_comment(post_id):
    return render_template("new_comment.html", post_id=post_id)

@comments.route("/send_comment/<int:post_id>", methods=["POST"])
def send_comment(post_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    content = request.form.get("content")
    user_id = session.get("user_id", 0)

    if not post_id:
        return render_template("error.html", message="Invalid post ID.")

    sql = text("INSERT INTO comments (content, user_id, post_id, sent_at) VALUES (:content, :user_id, :post_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id, "post_id":post_id})
    db.session.commit()
    return redirect(url_for("routes.comments_list", post_id=post_id))

@comments.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    if request.method == "GET":
        sql = text("SELECT C.id, C.content, C.user_id, C.post_id FROM comments C, users U WHERE U.id=C.user_id AND C.id=:comment_id")
        edit_comment = db.session.execute(sql, {"comment_id": comment_id})
        edit_comment2 = edit_comment.fetchone()

        if edit_comment2 is None:
            return render_template("error.html", message="Comment not found.")

        return render_template("edit_your_comment.html", edit_comment2=edit_comment2)

    elif request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        content = request.form.get("content")
        post_id = request.form.get("post_id")

        sql = text("UPDATE comments SET content=:content WHERE id=:comment_id")
        db.session.execute(sql, {"content": content, "comment_id": comment_id})
        db.session.commit()

        sql = text("SELECT post_id FROM comments WHERE id=:comment_id")
        result = db.session.execute(sql, {"comment_id": comment_id})
        post_id = result.fetchone()[0]

        return redirect(url_for("routes.comments_list", post_id=post_id))


@comments.route("/delete_comment/<int:comment_id>", methods=["GET", "POST"])
def delete_comment(comment_id):
    sql = text("SELECT post_id FROM comments WHERE id=:comment_id")
    result = db.session.execute(sql, {"comment_id": comment_id})
    post_id = result.fetchone()[0]

    sql = text("DELETE FROM comments WHERE id=:comment_id")
    db.session.execute(sql, {"comment_id": comment_id})
    db.session.commit()

    return redirect(url_for("routes.comments_list", post_id=post_id))

 