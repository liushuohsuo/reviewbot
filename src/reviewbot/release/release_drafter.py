"""Automated release notes generation from merged PRs."""

import logging
from typing import Any

from reviewbot.ai.adapters import get_backend
from reviewbot.ai.prompts import RELEASE_NOTES_SYSTEM, RELEASE_NOTES_USER
from reviewbot.github.app import get_github_client

logger = logging.getLogger(__name__)


async def handle_release_event(payload: dict[str, Any]) -> None:
    """Process a release webhook event and generate release notes."""
    action = payload.get("action", "")
    if action != "published":
        return

    repo_full_name = payload["repository"]["full_name"]
    release_tag = payload["release"]["tag_name"]
    release_id = payload["release"]["id"]
    installation_id = payload["installation"]["id"]

    logger.info("Drafting release notes for %s @ %s", repo_full_name, release_tag)

    gh = get_github_client(installation_id)
    repo = gh.get_repo(repo_full_name)

    # Find merged PRs since last release
    releases = list(repo.get_releases())
    previous_tag = releases[1].tag_name if len(releases) > 1 else None

    if previous_tag:
        comparison = repo.compare(previous_tag, release_tag)
        pr_list = _extract_prs_from_commits(comparison.commits)
    else:
        # First release — get recent merged PRs
        pulls = repo.get_pulls(state="closed", sort="updated", base=repo.default_branch)
        pr_list = []
        for pr in pulls[:50]:
            if pr.merged:
                pr_list.append(f"- #{pr.number} {pr.title} (@{pr.user.login})")

    if not pr_list:
        logger.info("No merged PRs found for release %s", release_tag)
        return

    backend = get_backend()
    try:
        notes = await backend.chat(
            system_prompt=RELEASE_NOTES_SYSTEM,
            user_prompt=RELEASE_NOTES_USER.format(
                version=release_tag,
                pr_list="\n".join(pr_list[:80]),
            ),
        )
    except Exception as exc:
        logger.error("Release notes generation failed: %s", exc)
        return

    # Update the release body
    release = repo.get_release(release_id)
    current_body = release.body or ""
    if current_body:
        full_body = f"{notes}\n\n---\n\n{current_body}"
    else:
        full_body = notes

    release.update_release(
        name=release_tag,
        message=full_body,
    )
    logger.info("Updated release notes for %s", release_tag)


def _extract_prs_from_commits(commits) -> list[str]:
    """Extract PR references from commit messages."""
    import re

    pr_list: list[str] = []
    seen: set[int] = set()
    pr_pattern = re.compile(r"#(\d+)")

    for commit in commits:
        message = commit.commit.message.split("\n")[0]
        match = pr_pattern.search(message)
        if match:
            pr_num = int(match.group(1))
            if pr_num not in seen:
                seen.add(pr_num)
                pr_list.append(f"- #{pr_num} {message}")

    return pr_list