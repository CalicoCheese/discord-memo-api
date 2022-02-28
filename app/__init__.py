from os import environ

from flask import Flask
from flask import redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # SQLAlchemy for Database
    __import__("app.models")
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    # CORS for API
    CORS(app=app)

    @app.get("/")
    def index():
        return redirect(
            location="https://github.com/CalicoCheese/discord-memo-api",
            code=301
        )

    from app import views
    for view in views.__all__:
        app.register_blueprint(
            blueprint=getattr(getattr(views, view), "bp")
        )

    from app.errors import emap
    for code in emap.keys():
        app.register_error_handler(
            code_or_exception=code,
            f=emap.get(code)
        )

    return app
