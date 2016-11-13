from flask import Flask
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cache = Cache()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.app = app
    db.init_app(app)

    cache.init_app(app)

    from coagg.controllers import main
    from coagg.models import Comic

    app.register_blueprint(main)

    return app
