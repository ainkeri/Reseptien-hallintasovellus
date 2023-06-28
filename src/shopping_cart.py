from .db import db
from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from sqlalchemy import text

shopping_cart = Blueprint("shopping_cart", __name__)

@shopping_cart.route("/add_to_cart/<int:recipe_id>")
def add_to_cart(recipe_id):
    sql = text("SELECT ingredients FROM posts WHERE id=:recipe_id")
    result = db.session.execute(sql, {"recipe_id": recipe_id})
    recipe_ingredients = result.fetchone()

    if recipe_ingredients is None:
        return render_template("error.html", message="No ingredients found.")
        
    user_id = session.get("user_id", 0) 
    ingredients_text = recipe_ingredients[0]    

    sql2 = text("INSERT INTO cart (post_id, user_id, ingredients) VALUES (:post_id, :user_id, :ingredients)")
    db.session.execute(sql2, {"post_id":recipe_id, "user_id":user_id, "ingredients":ingredients_text})
    db.session.commit()

    return render_template("success.html", recipe_id=recipe_id)

@shopping_cart.route("/delete_cart/<int:item_id>", methods=["GET", "POST"])
def delete_cart(item_id):
    sql = text("DELETE FROM cart WHERE id=:item_id")
    result = db.session.execute(sql, {"item_id": item_id})
    db.session.commit()

    if result.rowcount == 0:
        abort(404)

    return redirect(url_for("routes.show_cart"))




