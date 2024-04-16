import json


def read_file_json(file_name):
    try:
        with open(file_name, 'r') as file:
            value = json.load(file)
        return value
    except Exception as e:
        print(e)
        raise Exception('Not open or read file')