from .db import db
from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from sqlalchemy import text

comments = Blueprint("comments", __name__)

@comments.route("/comments_list")
def comments_list():
    return render_template("comments_list.html")