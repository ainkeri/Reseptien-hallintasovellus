from . import db
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return "<p>Logout</p>"

@auth.route("/register", methods=["GET", "POST"])
def sign_up():
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
            new_user = "INSERT INTO users (username, password) VALUES (:username, :hash_value)"
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("routes.homepage"))

    if request.method == "GET":
        return render_template("register.html")
