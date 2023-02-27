import json

def load_config(config_file_name):
 try:
    with open(config_file_name) as f:
        config = json.load(f)
    return config
 except(FileNotFoundError, json.JSONDecodeError):
    return {}

def load_workflow_config(workflow_config):
    # Load the list of files to copy from a JSON file
    try:
     with open(workflow_config, 'r') as f:
        files_to_copy = json.load(f)
        return files_to_copy
    except (FileNotFoundError, json.JSONDecodeError):
     return {}
