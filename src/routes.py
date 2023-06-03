from flask import Blueprint, render_template, request
from sqlalchemy import text
from .db import db

routes = Blueprint("routes", __name__)


@routes.route("/")
def homepage():
    return render_template("index.html")

@routes.route("/main")
def main():
    sql = text("SELECT P.id, P.content, U.username, P.posted_at FROM posts P, users U WHERE P.user_id=U.id ORDER BY P.id")
    recipes = db.session.execute(sql)
    post_list = recipes.fetchall()
    return render_template("main.html", count=len(post_list), recipes=post_list)

@routes.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    sql = text("SELECT content, ingredients, instructions FROM posts WHERE id=:recipe_id")
    recipe = db.session.execute(sql, {"recipe_id":recipe_id}).fetchone()
    if recipe is None:
        return render_template("error.html", message="Recipe not found")
    return render_template("recipe.html", recipe=recipe)