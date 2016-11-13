from flask import Flask
from flask_cache import Cache

cache = Cache()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    cache.init_app(app)

    from coagg.controllers import main

    app.register_blueprint(main)

    return app
