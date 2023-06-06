from flask import Flask
from os import getenv

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")

    from .routes import routes
    from .auth import auth
    from .posts import posts
    from .db import init_db

    app.register_blueprint(routes)
    app.register_blueprint(auth)
    app.register_blueprint(posts)

    init_db(app)

    return app
