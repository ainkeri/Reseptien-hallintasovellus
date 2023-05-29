from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "kjwdoaifho kesdklfn"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///inkeriahlstrom"
    db.init_app(app)

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes)
    app.register_blueprint(auth)

    return app
