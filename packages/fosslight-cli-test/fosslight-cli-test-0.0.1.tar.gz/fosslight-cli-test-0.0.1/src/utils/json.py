import json


def pretty_print_dict(data: dict):
    print(json.dumps(data, indent=4))
