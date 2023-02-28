import logging
import requests
from github import Github, GithubException
from .config import *
from .utils import load_config, load_workflow_config
import json


##############################################################
## Create Repository                                        ##
##                                                          ## 
##############################################################
def create_repository():

    # Load configuration from file
    config = load_config(CONFIG_FILE_NAME)
    
    # Create Github API client
    github_api_client = Github(GITHUB_ACCESS_TOKEN)

    # Create new repository
    repo_name = REPOSITORY_NAME
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
## Add Readme File                                          ##
##                                                          ## 
##############################################################
def add_readme_create_branches(repo):
    
    try:
        # create README.md file
        repo.create_file("README.md", "Initial commit",
                         README_CONTENT, branch="master")
        
        
        logging.info(
            f"Successfully created branches and added README file to repository {repo}.")

    except GithubException as e:
        logging.error(f"Failed to create repository {repo}. Error: {e}")

    except Exception as e:
        logging.error(
            f"An error occurred while creating branches and adding README file to repository {repo}. Error: {e}")

    except GithubException as e:
        logging.exception(
            "Error occurred while creating branches and pushing to GitHub: %s", e)
        raise
    
##############################################################
## Add Teams to Repository                                  ##
##                                                          ##
##############################################################
def add_team_to_repository(repo):
  
  # Load configuration from file  
  config = load_config(CONFIG_FILE_NAME)
  
  # Create Github API client
  github_api_client = Github(GITHUB_ACCESS_TOKEN)
  
  
  # Add team to repository
  team_slug = TEAM_NAME
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
    
##############################################################
## Add Workflow files to Repository                         ##
##                                                          ##
##############################################################

def add_workflow_files_to_repository(repo):

    github_api_client = Github(GITHUB_ACCESS_TOKEN)

    files_to_copy = load_workflow_config(WORKFLOW_CONFIG_FILE_NAME)

    src_repo = github_api_client.get_repo(WORKFLOW_COPY_FROM_REPOSITORY)
    dst_repo = repo

    # Define the directory to copy
    dir_to_copy = DIR_TO_COPY

    # Copy the files from the source repository to the destination repository
    for file_path in files_to_copy:
        # Get the contents of the file from the source repository
        file_contents = src_repo.get_contents(
            f"{dir_to_copy}/{file_path}").decoded_content.decode()

        # Create the file in the destination repository
        dst_repo.create_file(f"{dir_to_copy}/{file_path}",
                             f"Copy {file_path} from {src_repo.name}", file_contents)

        # Copy the file to the master branch
        file_contents = dst_repo.get_contents(
            f"{dir_to_copy}/{file_path}", ref='master').decoded_content.decode()
        if file_contents != src_repo.get_contents(f"{dir_to_copy}/{file_path}").decoded_content.decode():
            dst_repo.create_file(f"{dir_to_copy}/{file_path}",
                                 f"Copy {file_path} from {src_repo.name} to master", file_contents, branch='master')


##############################################################
## Create Develop Branch from Master                        ##
##                                                          ##
##############################################################

def create_develop_branch(repo):
# get the reference object for the master branch
  master_ref = repo.get_git_ref('heads/master')

# create a new branch called develop
  repo.create_git_ref(ref='refs/heads/develop', sha=master_ref.object.sha)
    

##############################################################
## Add Branch Protection Rules                              ##
##                                                          ##
##############################################################
def add_branch_protection_rules(repo):

    repo = ORG + '/' + repo.name
       
    # Set the headers with your GitHub personal access token
    headers = {
        "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
        "Accept": "application/vnd.github.luke-cage-preview+json"
    }

    # Set the body with the desired protection rules
    body = {
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False
        },
        "enforce_admins": True,
        "required_status_checks": {
            "strict": True,
            "contexts": [
                "continuous-integration"
            ]
        },
        "restrictions": None
    }

    # Set the list of branches to which the protection rules should be added
    branches = ["master", "develop"]

    # Loop through the branches and add the protection rules
    for branch_name in branches:
        # Set the API endpoint for branch protection
        api_url = f"https://api.github.com/repos/{repo}/branches/{branch_name}/protection"
        try:
            # Send a PUT request to the API endpoint to add the protection rules
            response = requests.put(
                api_url, headers=headers, data=json.dumps(body))

            # Check the response status code
            if response.status_code == 200:
                logging.info(
                    f"Branch protection rules added successfully to {branch_name} branch.")
            else:
                logging.error(
                    f"Error adding branch protection rules to {branch_name} branch: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(
                f"Exception occurred while adding branch protection rules to {branch_name} branch: {str(e)}")
