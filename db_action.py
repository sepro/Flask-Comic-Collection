from coagg import create_app, db
from coagg.models import Comic
from flask_script import Manager

import os.path

app = create_app('config')
manager = Manager(app)


@manager.command
def create():
    """
    function to create the initial database and migration information
    """
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
        path = os.path.dirname(os.path.realpath(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')))
        if not os.path.exists(path):
            os.makedirs(path)

    db.create_all(app=app)


@manager.command
def update():
    with app.app_context():
        Comic.update_all_links(app.config['DATA'])


if __name__ == "__main__":
    manager.run()
