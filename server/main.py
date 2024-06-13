from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from routes import create_api


"""Main entry point for the server application."""


app = Flask(__name__)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(app)
api = create_api(cache)
app.register_blueprint(api, url_prefix="/api/carla")
cors = CORS(app, resources={r"/api/carla/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run()
