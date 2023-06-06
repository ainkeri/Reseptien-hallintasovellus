from .db import db
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
    ingredients = request.form.get("ingredients")
    instructions = request.form.get("instructions")

    if user_id == 0:
        return render_template("error.html", message="Post failed")
    
    sql = text("INSERT INTO posts (content, user_id, posted_at, ingredients, instructions) VALUES (:content, :user_id, NOW(), :ingredients, :instructions)")
    db.session.execute(sql, {"content":content, "user_id":user_id, "ingredients":ingredients, "instructions":instructions})
    db.session.commit()
    return redirect(url_for("routes.main"))

@posts.route("/recipe")
def recipe():
    return render_template("recipe.html")

@posts.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit(recipe_id):
    if request.method == "GET":
        sql = text("SELECT P.content, P.ingredients, P.instructions, U.id FROM posts P, users U WHERE U.id=P.user_id AND P.id = :recipe_id")
        recipe = db.session.execute(sql, {"recipe_id": recipe_id}).fetchone()

        if recipe is None:
            return render_template("error.html", message="Recipe not found.")

        return render_template("edit_post.html", recipe=recipe)

    elif request.method == "POST":
        content = request.form.get("content")
        ingredients = request.form.get("ingredients")
        instructions = request.form.get("instructions")

        sql = text("UPDATE posts SET content = :content, ingredients = :ingredients, instructions = :instructions WHERE id = :recipe_id")
        db.session.execute(sql, {"content": content, "ingredients": ingredients, "instructions": instructions, "recipe_id": recipe_id})
        db.session.commit()

        return redirect(url_for("routes.recipe", recipe_id=recipe_id))
