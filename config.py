import json
import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TESTING = True

SECRET_KEY = "change me"

# Database settings, database location and path to migration scripts
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'comics.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# Setting allow updates to True will add an Update button to the config panel, where the users can force
# the app to check for new comics
ALLOW_UPDATE = True

DATA_FILE = "sites.json"
DATA = []
with open(DATA_FILE, "r") as f:
    DATA = json.load(f)
