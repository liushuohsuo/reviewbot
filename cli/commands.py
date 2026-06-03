"""ReviewBot CLI — command-line interface for local use."""

import sys

import click
import uvicorn
from rich.console import Console
from rich.panel import Panel

from reviewbot.config import settings

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="reviewbot")
def main():
    """ReviewBot — AI-powered code review and maintainer automation."""


@main.command()
@click.option("--host", default=settings.host, help="Bind address")
@click.option("--port", default=settings.port, help="Bind port")
@click.option("--reload", is_flag=True, help="Enable auto-reload for development")
def server(host: str, port: int, reload: bool):
    """Start the ReviewBot webhook server."""
    console.print(
        Panel.fit(
            f"[bold green]ReviewBot v0.1.0[/]\n"
            f"Starting server on [cyan]{host}:{port}[/]\n"
            f"Webhook endpoint: [cyan]http://{host}:{port}/webhook/[/]",
            title="ReviewBot Server",
        )
    )
    uvicorn.run(
        "reviewbot.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=settings.log_level,
    )


@main.command()
@click.argument("repo_url")
@click.option("--pr", type=int, help="PR number to review locally")
def review(repo_url: str, pr: int | None):
    """Review a GitHub PR from the command line."""
    console.print("[yellow]Local PR review mode coming soon.[/]")


@main.command()
@click.argument("issue_url")
def triage(issue_url: str):
    """Triage a GitHub issue from the command line."""
    console.print("[yellow]Local issue triage mode coming soon.[/]")


@main.command()
def check():
    """Verify configuration and connectivity."""
    errors = []

    if not settings.github_app_id:
        errors.append("GITHUB_APP_ID is not set")
    if not settings.github_app_private_key:
        errors.append("GITHUB_APP_PRIVATE_KEY is not set")
    if not settings.github_webhook_secret:
        errors.append("GITHUB_WEBHOOK_SECRET is not set")
    if not settings.openai_api_key:
        errors.append("OPENAI_API_KEY is not set")

    if errors:
        console.print("[red]Configuration issues found:[/]")
        for e in errors:
            console.print(f"  [red]✗[/] {e}")
        sys.exit(1)

    console.print("[green]✓[/] Configuration looks good")
    console.print(f"  GitHub App ID: {settings.github_app_id}")
    console.print(f"  API Backend: {settings.default_model}")
    console.print(f"  Server: {settings.host}:{settings.port}")

    # Test OpenAI connectivity
    try:
        import asyncio

        from reviewbot.ai.codex import codex

        async def test():
            return await codex.chat(
                system_prompt="Reply with just 'ok'.",
                user_prompt="ping",
                max_tokens=10,
            )

        result = asyncio.run(test())
        if "ok" in result.lower():
            console.print("[green]✓[/] OpenAI API connection successful")
        else:
            console.print(f"[yellow]?[/] Unexpected API response: {result[:50]}")
    except Exception as exc:
        console.print(f"[red]✗[/] OpenAI API connection failed: {exc}")