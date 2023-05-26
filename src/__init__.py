from flask import Flask
from .routes import routes
from .auth import auth

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "kjwdoaifho kesdklfn"

    app.register_blueprint(routes)
    app.register_blueprint(auth)

    return app