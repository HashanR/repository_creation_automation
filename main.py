from app.repository import create_repository, add_team_to_repository, add_branch_protection_rules, add_workflow_files_to_repository
from app.logging.logging_config import setup_logging

if __name__ == '__main__':
    setup_logging()
    
    
    # repo = create_repository()
    # if repo is not None:
    #    add_branch_protection_rules(repo)
    add_workflow_files_to_repository()
    #     add_team_to_repository(repo)