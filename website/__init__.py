from .views import views
from flask import Flask
from secrets import token_urlsafe


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = token_urlsafe(16)

    app.register_blueprint(views, url_prefix="/")

    return app
