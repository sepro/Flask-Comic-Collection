from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.app = app
    db.init_app(app)

    from coagg.controllers import main
    from coagg.models import Comic, Message

    app.register_blueprint(main)

    @app.before_request
    def load_data():
        g.messages = Message.query.order_by(Message.created.desc()).limit(5)

        g.images = Comic.query.all()

        for i in g.images:
            cookie_url = request.cookies.get(str(i.id))
            if cookie_url != i.img_url:
                i.new = True

    return app
