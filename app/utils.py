import json

def load_config(config_file_name):
 try:
    with open(config_file_name) as f:
        config = json.load(f)
    return config
 except(FileNotFoundError, json.JSONDecodeError):
    return {}

def load_workflow_config(worflow_config_file_name):
 try:
    with open(worflow_config_file_name) as f:
        workflow_list = json.load(f)
    return worflow_config_file_name
 except(FileNotFoundError, json.JSONDecodeError):
    return {}