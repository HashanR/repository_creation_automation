# import unittest
# from unittest.mock import patch, MagicMock
# from github import GithubException

# from src.create_repository import create_repository, add_team_to_repository


# class TestCreateRepository(unittest.TestCase):
#     @patch('src.create_repository.load_config')
#     @patch('src.create_repository.Github')
#     def test_create_repository_success(self, mock_github, mock_load_config):
#         # Arrange
#         repo_name = 'test-repo'
#         config = {'repository_name': repo_name}
#         mock_load_config.return_value = config
#         user_mock = MagicMock()
#         mock_github.return_value.get_user.return_value = user_mock
#         repo_mock = MagicMock()
#         user_mock.create_repo.return_value = repo_mock

#         # Act
#         result = create_repository()

#         # Assert
#         self.assertEqual(result, repo_mock)
#         user_mock.create_repo.assert_called()

#     @patch('src.create_repository.load_config')
#     @patch('src.create_repository.Github')
#     def test_create_repository_failure(self, mock_github, mock_load_config):
#         # Arrange
#         mock_load_config.return_value = {}
#         mock_github.return_value.get_user.side_effect = GithubException('Not Found')

#         # Act & Assert
#         with self.assertRaises(GithubException):
#             create_repository()

#     @patch('src.create_repository.load_config')
#     @patch('src.create_repository.Github')
#     def test_add_team_to_repository_success(self, mock_github, mock_load_config):
#         # Arrange
#         repo_mock = MagicMock()
#         team_slug = 'test-team'
#         config = {'team_slug': team_slug}
#         mock_load_config.return_value = config
#         org_mock = MagicMock()
#         mock_github.return_value.get_organization.return_value = org_mock
#         team_mock = MagicMock()
#         org_mock.get_team_by_slug.return_value = team_mock

#         # Act
#         add_team_to_repository(repo_mock)

#         # Assert
#         team_mock.add_to_repos.assert_called_once_with(repo_mock)

#     @patch('src.create_repository.load_config')
#     @patch('src.create_repository.Github')
#     def test_add_team_to_repository_failure(self, mock_github, mock_load_config):
#         # Arrange
#         repo_mock = MagicMock()
#         mock_load_config.return_value = {}
#         mock_github.return_value.get_organization.side_effect = GithubException('Not Found')

#         # Act & Assert
#         with self.assertRaises(GithubException):
#             add_team_to_repository(repo_mock)