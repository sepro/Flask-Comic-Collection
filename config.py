import json
import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TESTING = True

SECRET_KEY = "change me"

CACHE_TYPE = 'simple'

# Database settings, database location and path to migration scripts
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'comics.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

DATA_FILE = "sites.json"
DATA = []
with open(DATA_FILE, "r") as f:
    DATA = json.load(f)
