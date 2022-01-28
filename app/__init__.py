from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # CORS for API
    CORS(app=app)

    from app import views
    for view in views.__all__:
        app.register_blueprint(
            blueprint=getattr(getattr(views, view), "bp")
        )

    return app
