from .db import db
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            flash("User doesn't exist.")
            return redirect(url_for('auth.login'))
        
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for("routes.main"))
        
        flash("Incorrect username or password.")
        return redirect(url_for('auth.login'))

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

@auth.route("/register", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(username) < 2:
            flash("Username must be longer than 1 character.")
            return redirect(url_for('auth.sign_up'))
        if password1 != password2:
            flash("Passwords do not match.")
            return redirect(url_for('auth.sign_up'))
        if len(password1) < 7:
            flash("Password must be at least 7 characters.")
            return redirect(url_for('auth.sign_up'))

        hash_value = generate_password_hash(password1)
        new_user = User(username=username, password=hash_value)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("routes.homepage"))
        except IntegrityError:
            db.session.rollback()
            flash("Username already exists.")
            return redirect(url_for('auth.sign_up'))

    return render_template("register.html")
