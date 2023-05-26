from flask import Blueprint

routes = Blueprint("routes", __name__)


@routes.route("/")
def homepage():
    return "<h1>Testi</h1>"