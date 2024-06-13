from flask import Flask
from flask_caching import Cache
from routes import create_api


def create_app():
    app = Flask(__name__)

    cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
    cache.init_app(app)

    api = create_api(cache)
    app.register_blueprint(api, url_prefix="/api/carla")

    return app
