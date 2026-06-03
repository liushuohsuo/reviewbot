"""GitHub App authentication and API client."""

from github import Auth, Github
from github.GithubIntegration import GithubIntegration

from reviewbot.config import settings


def get_github_client(installation_id: int) -> Github:
    """Get an authenticated GitHub client for a specific installation."""
    auth = Auth.AppAuth(
        app_id=settings.github_app_id,
        private_key=settings.github_private_key_content,
    )
    integration = GithubIntegration(auth=auth)
    installation_auth = integration.get_access_token(installation_id)
    return Github(auth=installation_auth)


def get_app_client() -> Github:
    """Get a GitHub client authenticated as the app itself."""
    auth = Auth.AppAuth(
        app_id=settings.github_app_id,
        private_key=settings.github_private_key_content,
    )
    return Github(auth=auth)