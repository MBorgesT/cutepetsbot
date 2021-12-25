import json
import os

dn = os.path.dirname(os.path.realpath(__file__))
with open(f'{dn}/paths.json', 'r') as f:
    paths = json.load(f)