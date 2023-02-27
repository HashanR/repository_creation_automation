import logging.config
import json
import os


log_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.json')

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def setup_logging():
    # Load logging configuration from file
    with open(log_config_path, "r") as f:
        config = json.load(f)
        
    # Configure logging using the loaded configuration
        logging.config.dictConfig(config)
        
def get_logger(name):
    # Get logger instance
    return logging.getLogger(name)