from .db import db
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return render_template("error.html", message="User doesn't exist.")
        else:
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                return redirect("/")
            else:
                return render_template("error.html", message="Incorrect username or password.")
    

@auth.route("/logout")
def logout():
    return "<p>Logout</p>"

@auth.route("/register", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(username) < 2:
            return render_template("error.html", message="Username must be longer than 1 character.")
        elif password1 != password2:
            return render_template("error.html", message="Passwords do not match.")
        elif len(password1) < 7:
            return render_template("error.html", message="Password must be at least 7 characters.")
        else:
            hash_value = generate_password_hash(password1)
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
            return redirect(url_for("routes.homepage"))

