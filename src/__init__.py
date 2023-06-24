from flask import Flask
from os import getenv

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")

    from .routes import routes
    from .auth import auth
    from .posts import posts
    from .comments import comments
    from .likes import likes
    from .shopping_cart import shopping_cart
    from .db import init_db

    app.register_blueprint(routes)
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.register_blueprint(comments)
    app.register_blueprint(likes)
    app.register_blueprint(shopping_cart)

    init_db(app)

    return app
