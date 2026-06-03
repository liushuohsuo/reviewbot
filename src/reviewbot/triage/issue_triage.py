"""Intelligent GitHub issue triage and labeling."""

import logging
from typing import Any

from reviewbot.ai.adapters import get_backend
from reviewbot.ai.prompts import ISSUE_TRIAGE_SYSTEM, ISSUE_TRIAGE_USER
from reviewbot.github.app import get_github_client

logger = logging.getLogger(__name__)


async def handle_issue_event(payload: dict[str, Any]) -> None:
    """Process an issues webhook event and perform automated triage."""
    action = payload.get("action", "")
    if action not in ("opened", "edited"):
        return

    repo_full_name = payload["repository"]["full_name"]
    issue_number = payload["issue"]["number"]
    issue_title = payload["issue"]["title"]
    issue_body = payload["issue"].get("body", "") or ""
    installation_id = payload["installation"]["id"]

    logger.info("Triaging issue #%d in %s", issue_number, repo_full_name)

    gh = get_github_client(installation_id)
    repo = gh.get_repo(repo_full_name)
    issue = repo.get_issue(issue_number)

    # Get existing labels
    existing_labels = [label.name for label in issue.labels]

    backend = get_backend()
    try:
        triage = await backend.chat_json(
            system_prompt=ISSUE_TRIAGE_SYSTEM,
            user_prompt=ISSUE_TRIAGE_USER.format(
                issue_title=issue_title,
                issue_body=issue_body[:4000],
                existing_labels=", ".join(existing_labels) if existing_labels else "(none)",
            ),
        )
    except Exception as exc:
        logger.error("Issue triage failed: %s", exc)
        return

    # Apply suggested labels
    suggested_labels = triage.get("labels", [])
    priority = triage.get("priority", "")
    summary = triage.get("summary", "")

    labels_to_add: list[str] = []
    for label in suggested_labels:
        if label not in existing_labels:
            labels_to_add.append(label)
    if priority and priority not in existing_labels:
        labels_to_add.append(priority)

    if labels_to_add:
        try:
            issue.add_to_labels(*labels_to_add)
            logger.info("Added labels to issue #%d: %s", issue_number, labels_to_add)
        except Exception as exc:
            logger.error("Failed to add labels: %s", exc)

    # Post triage summary as comment
    if summary or labels_to_add:
        comment = "## 🤖 ReviewBot — Auto-Triage\n\n"
        if summary:
            comment += f"**Summary:** {summary}\n\n"
        if labels_to_add:
            comment += f"**Labels applied:** {', '.join(f'`{l}`' for l in labels_to_add)}\n"
        comment += "\n---\n*Labels are AI-suggested. Maintainers can adjust as needed.*"

        issue.create_comment(comment)
        logger.info("Posted triage comment on issue #%d", issue_number)