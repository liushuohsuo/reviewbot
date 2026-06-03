"""Security-focused code scanning for pull requests."""

import logging
from typing import Any

from reviewbot.ai.adapters import get_backend
from reviewbot.ai.prompts import SECURITY_SCAN_SYSTEM, SECURITY_SCAN_USER
from reviewbot.github.app import get_github_client

logger = logging.getLogger(__name__)


async def handle_security_scan(payload: dict[str, Any]) -> None:
    """Process a check_run event for security scanning."""
    action = payload.get("action", "")
    if action != "created":
        return

    repo_full_name = payload["repository"]["full_name"]
    installation_id = payload["installation"]["id"]
    check_run = payload.get("check_run", {})

    # Only handle security-related check runs
    if "security" not in check_run.get("name", "").lower():
        return

    pr_number = check_run.get("pull_requests", [{}])[0].get("number")
    if not pr_number:
        logger.debug("No PR associated with security check run")
        return

    logger.info("Running security scan for PR #%d in %s", pr_number, repo_full_name)

    gh = get_github_client(installation_id)
    repo = gh.get_repo(repo_full_name)
    pull_request = repo.get_pull(pr_number)

    diff_content = ""
    for f in pull_request.get_files():
        if f.patch:
            diff_content += f"\n--- {f.filename} ---\n{f.patch}\n"

    if not diff_content.strip():
        return

    backend = get_backend()
    try:
        scan_result = await backend.chat(
            system_prompt=SECURITY_SCAN_SYSTEM,
            user_prompt=SECURITY_SCAN_USER.format(
                repo_name=repo_full_name,
                diff_content=diff_content[:12000],
            ),
        )
    except Exception as exc:
        logger.error("Security scan failed: %s", exc)
        return

    comment_body = f"""## 🔒 ReviewBot — Security Scan

{scan_result}

---
*ReviewBot identified potential security concerns. Please review carefully.*"""

    pull_request.create_issue_comment(comment_body)
    logger.info("Posted security scan for PR #%d", pr_number)