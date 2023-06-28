from flask import Blueprint, render_template, request, session
from sqlalchemy import text
from .db import db
from .likes import likes

routes = Blueprint("routes", __name__)


@routes.route("/")
def homepage():
    return render_template("index.html")

@routes.route("/main")
def main():
    sql = text("SELECT P.id, P.content, U.username, P.posted_at, U.id FROM posts P, users U WHERE P.user_id=U.id ORDER BY P.id")
    recipes = db.session.execute(sql)
    post_list = recipes.fetchall()
    return render_template("main.html", count=len(post_list), recipes=post_list)

@routes.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    sql = text("SELECT P.content, P.ingredients, P.instructions, P.user_id, P.id FROM posts P, users U WHERE P.user_id=U.id AND P.id=:recipe_id")
    full_recipe = db.session.execute(sql, {"recipe_id":recipe_id})
    recipe = full_recipe.fetchone()

    if recipe is None:
        return render_template("error.html", message="Recipe not found")
    
    sql2 = text("SELECT user_id FROM likes WHERE post_id=:recipe_id")
    liked_users = db.session.execute(sql2, {"recipe_id": recipe_id}).fetchall()
    liked_users = [row.user_id for row in liked_users]

    sql3 = text("SELECT COUNT(*) FROM likes WHERE post_id=:recipe_id")
    result = db.session.execute(sql3, {"recipe_id": recipe_id})
    like_count = result.fetchone()[0]
    
    return render_template("recipe.html", recipe=recipe, like_count=like_count, liked_users=liked_users)

@routes.route("/search")
def search():
    query = request.args.get("query")
    sql = text("SELECT * FROM posts WHERE lower(content) LIKE '%' || lower(:query) || '%'")
    matching_posts = db.session.execute(sql, {"query": query}).fetchall()

    return render_template("search.html", query=query, posts=matching_posts, count=len(matching_posts))

@routes.route("/comments_list/<int:post_id>")
def comments_list(post_id):
    sql = text("SELECT U.username, C.content, C.post_id, C.sent_at, C.user_id, C.id FROM comments C, users U WHERE C.user_id = U.id AND C.post_id=:post_id ORDER BY C.id")
    comments_result = db.session.execute(sql, {"post_id":post_id})
    comments = comments_result.fetchall()

    return render_template("comments_list.html", comments=comments, post_id=post_id)

@routes.route("/show_cart")
def show_cart():
    user_id = session.get("user_id", 0)
    sql = text("SELECT C.ingredients, C.user_id, P.content, P.id, C.id FROM cart C, posts P WHERE C.user_id=:user_id AND P.id=C.post_id")
    result = db.session.execute(sql, {"user_id": user_id})
    ingredients = result.fetchall()

    return render_template("shopping_cart.html", ingredients=ingredients, user_id=user_id, count=len(ingredients))