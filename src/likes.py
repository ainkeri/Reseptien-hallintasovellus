from flask import Blueprint, redirect, request, url_for, session
from sqlalchemy import text
from .db import db

likes = Blueprint("likes", __name__)

@likes.route("/like", methods=["POST"])
def like():
    post_id = int(request.form.get("post_id"))
    user_id = session.get("user_id")

    sql = text("SELECT id FROM likes WHERE user_id = :user_id AND post_id = :post_id")
    result = db.session.execute(sql, {"user_id": user_id, "post_id": post_id})
    existing_like = result.fetchone()

    if existing_like:
        sql2 = text("DELETE FROM likes WHERE id=:like_id")
        db.session.execute(sql2, {"like_id": existing_like.id})
        db.session.commit()

        sql3 = text("UPDATE posts SET like_count = like_count - 1 WHERE id = :post_id")
        db.session.execute(sql3, {"post_id": post_id})
        db.session.commit()

        return redirect(url_for("routes.recipe", recipe_id=post_id))

    else:
        sql4 = text("INSERT INTO likes (user_id, post_id) VALUES (:user_id, :post_id)")
        db.session.execute(sql4, {"user_id": user_id, "post_id": post_id})
        db.session.commit()

        sql5 = text("UPDATE posts SET like_count = like_count + 1 WHERE id = :post_id")
        db.session.execute(sql5, {"post_id": post_id})
        db.session.commit()

        return redirect(url_for("routes.recipe", recipe_id=post_id))

