from .db import db
from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import text

posts = Blueprint("posts", __name__)

@posts.route("/new")
def new():
    return render_template("new.html")
