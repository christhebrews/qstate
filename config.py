ENVIRONMENT = "dev"

###########################

import json
import os.path

config = {}

filename = 'env/' + ENVIRONMENT + '.json'

if not os.path.isfile(filename):
    raise FileNotFoundError("No config file " + filename + " exists")

with open(filename) as file:
    config = json.load(file)