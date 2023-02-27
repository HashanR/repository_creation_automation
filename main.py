from app.repository import *
from app.logging.logging_config import setup_logging

if __name__ == '__main__':
    setup_logging()
    
    
    repo = create_repository()
    if repo is not None:
       add_readme_create_branches(repo)
       add_workflow_files_to_repository(repo)
       create_develop_branch(repo)
       add_branch_protection_rules(repo)
