"""Configuration management for ReviewBot."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # GitHub App
    github_app_id: str = ""
    github_app_private_key: str = ""
    github_webhook_secret: str = ""

    # OpenAI
    openai_api_key: str = ""
    openai_org_id: str = ""

    # Alternative backends (optional)
    anthropic_api_key: str = ""
    google_api_key: str = ""

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"

    # AI defaults
    default_model: str = "codex"
    max_tokens: int = 4096
    review_max_diff_lines: int = 3000

    @property
    def github_private_key_path(self) -> Path:
        return Path(self.github_app_private_key)

    @property
    def github_private_key_content(self) -> str:
        if not self.github_app_private_key:
            return ""
        return self.github_private_key_path.read_text()


settings = Settings()