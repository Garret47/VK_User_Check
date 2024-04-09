import json

FileName = './data/command_message.json'

with open(FileName, 'r') as f:
    dict_command = json.load(f)

start_message = dict_command['start_message']
help_message = dict_command['help_message']