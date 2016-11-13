import json

DEBUG = True
TESTING = True

CACHE_TYPE = 'simple'

SECRET_KEY = "change me"

DATA_FILE = "sites.json"
DATA = []
with open(DATA_FILE, "r") as f:
    DATA = json.load(f)
