from flask import Blueprint, render_template

routes = Blueprint("routes", __name__)


@routes.route("/")
def homepage():
    return render_template("index.html")
