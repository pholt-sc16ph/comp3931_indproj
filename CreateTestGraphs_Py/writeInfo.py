import json


def print_info(dictionary):
    print(json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': ')))