import pprint
import json
import pprint

with open("to_city.json", "r") as f:
    data = json.load(f)

pp = pprint.PrettyPrinter(indent=2, width=30, compact=True)

pp.pprint(data)