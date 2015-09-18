import json
import os

config = {}

env = os.getenv('APP_MODE', "dev")

filename = 'conf/' + env + '.json'

if not os.path.isfile(filename):
    raise FileNotFoundError("No config file " + filename + " exists")

with open(filename) as file:
    config = json.load(file)