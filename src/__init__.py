from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "kjwdoaifho kesdklfn"

    from .routes import routes
    from .auth import auth
    from .db import init_db

    app.register_blueprint(routes)
    app.register_blueprint(auth)

    init_db(app)

    return app
