from flask import Flask
from secrets import token_urlsafe
from website.views import views

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = token_urlsafe(16)

    app.register_blueprint(views, url_prefix="/")

    return app
