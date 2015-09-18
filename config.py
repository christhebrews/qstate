import json
import os

config = {}

env = os.getenv('APP_MODE', "dev")

filename = 'env/' + env + '.json'

if not os.path.isfile(filename):
    raise FileNotFoundError("No config file " + filename + " exists")

with open(filename) as file:
    config = json.load(file)