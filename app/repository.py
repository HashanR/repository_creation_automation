import logging
import requests
from github import Github, GithubException,InputGitTreeElement
from .config import GITHUB_ACCESS_TOKEN, CONFIG_FILE_NAME, WORKFLOW_CONFIG_FILE_NAME
from .utils import load_config, load_workflow_config



##############################################################
## Create Repository Method                                 ##
##                                                          ## 
##############################################################
def create_repository():

    # Load configuration from file
    config = load_config(CONFIG_FILE_NAME)
    
    # Create Github API client
    github_api_client = Github(GITHUB_ACCESS_TOKEN)

    # Create new repository
    repo_name = config.get('repository_name')
    if repo_name is None:
        logging.error('Repository name not found in config')
        return
    

    try:
       repo = github_api_client.get_user().create_repo(repo_name)
       
       # Log sucess
       
       logging.info(f"Repository '{repo_name}' created successfully")
       
       return repo
    except GithubException as e:
       # Log error
       logging.error(f"Failed to create repository: {e}") 
       raise




##############################################################
## Add Team to Repository Method                            ##
##                                                          ## 
##############################################################

def add_team_to_repository(repo):
  
  # Load configuration from file  
  config = load_config(CONFIG_FILE_NAME)
  
  # Create Github API client
  github_api_client = Github(GITHUB_ACCESS_TOKEN)
  
  
  # Add team to repository
  team_slug = config.get('team')
  if team_slug is None:
      logging.error('Team not found in config')

      return
  try:
     team = github_api_client.get_organization().get_team_by_slug(team_slug)
     team.add_to_repos(repo)
     
     # Log sucess
     logging.info(f"Team '{team_slug}' added to repository sucessfully")
     
  except GithubException as e:
      
      # Log error
      logging.error(f"Failed to add team to repository: {e}")
      raise   
    
     
def add_workflow_files_to_repository():
    
  github_api_client = Github(GITHUB_ACCESS_TOKEN)

  # Load configuration from file  
  config = load_workflow_config(WORKFLOW_CONFIG_FILE_NAME)
  
  
  
  source_repo = github_api_client.get_repo("HashanR/test_workflows")
  target_repo = github_api_client.get_repo("HashanR/test_ccc_aaaa")


  try:
     # Copy each workflow file in the list to the target repository's main and develop branches
     for file_name in config:
        # Get the contents of the file in the source repository
        file_content = source_repo.get_contents(f".github/workflows/{file_name}.yaml")
        if file_content is not None:
            file_content = file_content.decoded_content.decode("utf-8")
            # Copy the file to the target repository's main and develop branches
            target_repo.create_file(f".github/workflows/{file_name}.yaml", f"Copy {file_name}.yaml from {source_repo.full_name}", file_content, branch="main")
            target_repo.create_file(f".github/workflows/{file_name}.yaml", f"Copy {file_name}.yaml from {source_repo.full_name}", file_content, branch="develop")
        else:
         print(f"File .github/workflows/{file_name}.yml not found in {source_repo.full_name}. Skipping.")
         print("Workflow files copied successfully.")
  except GithubException as e:
        print(f"Error copying workflow files: {e}")
    
    
       


def add_branch_protection_rules(repo):
    try:
        branch_names = ['master', 'develop']
        for branch_name in branch_names:
            branch = repo.get_branch(branch_name)
            if not branch.protected:
                branch.edit_protection(strict=True, contexts=[])
                logging.info(f"Added branch protection rule to {branch_name}")
            else:
                logging.info(f"Branch protection rule already exists for {branch_name}")
    except Exception as e:
        logging.error(f"Error adding branch protection rules: {e}")
        