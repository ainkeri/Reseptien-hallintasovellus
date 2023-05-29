from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "kjwdoaifho kesdklfn"

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes)
    app.register_blueprint(auth)

    return app
