import json

FileName = './data/command_message.json'

with open(FileName, 'r') as f:
    dict_command = json.load(f)