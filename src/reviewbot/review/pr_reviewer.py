"""Automated pull request code review."""

import logging
from typing import Any

from reviewbot.ai.adapters import get_backend
from reviewbot.ai.prompts import PR_REVIEW_SYSTEM, PR_REVIEW_USER
from reviewbot.github.app import get_github_client

logger = logging.getLogger(__name__)


async def handle_pr_event(payload: dict[str, Any]) -> None:
    """Process a pull_request webhook event and generate a review."""
    action = payload.get("action", "")
    if action not in ("opened", "synchronize", "reopened"):
        logger.debug("Ignoring PR action: %s", action)
        return

    repo_full_name = payload["repository"]["full_name"]
    pr_number = payload["pull_request"]["number"]
    pr_title = payload["pull_request"]["title"]
    pr_body = payload.get("pull_request", {}).get("body", "") or ""
    installation_id = payload["installation"]["id"]

    logger.info(
        "Reviewing PR #%d in %s (action=%s)",
        pr_number,
        repo_full_name,
        action,
    )

    gh = get_github_client(installation_id)
    repo = gh.get_repo(repo_full_name)
    pull_request = repo.get_pull(pr_number)

    # Get the diff
    diff_content = ""
    files = pull_request.get_files()
    file_list: list[str] = []
    for f in files:
        file_list.append(f.filename)
        if f.patch:
            diff_content += f"\n--- {f.filename} ---\n{f.patch}\n"

    if not diff_content.strip():
        logger.info("No diff content to review for PR #%d", pr_number)
        return

    # Limit diff size
    diff_lines = diff_content.split("\n")
    if len(diff_lines) > 3000:
        diff_content = "\n".join(diff_lines[:3000]) + "\n... (truncated)"

    # Generate review using AI
    backend = get_backend()
    files_str = ", ".join(file_list[:20])
    if len(file_list) > 20:
        files_str += f" ... and {len(file_list) - 20} more"

    try:
        review = await backend.chat(
            system_prompt=PR_REVIEW_SYSTEM,
            user_prompt=PR_REVIEW_USER.format(
                repo_name=repo_full_name,
                pr_title=pr_title,
                pr_description=pr_body or "(none)",
                files_changed=files_str,
                diff_content=diff_content,
            ),
        )
    except Exception as exc:
        logger.error("AI review failed for PR #%d: %s", pr_number, exc)
        return

    # Post review comment
    review_body = f"""## 🤖 ReviewBot — AI Code Review

{review}

---
*This is an automated review. A human maintainer should still verify critical findings.*"""

    pull_request.create_issue_comment(review_body)
    logger.info("Posted review for PR #%d in %s", pr_number, repo_full_name)