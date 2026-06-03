"""GitHub webhook event handling and routing."""

import hashlib
import hmac
import logging

from fastapi import APIRouter, Header, HTTPException, Request

from reviewbot.config import settings
from reviewbot.review.pr_reviewer import handle_pr_event
from reviewbot.review.security_scanner import handle_security_scan
from reviewbot.triage.issue_triage import handle_issue_event
from reviewbot.release.release_drafter import handle_release_event

logger = logging.getLogger(__name__)
router = APIRouter()


def _verify_signature(payload_body: bytes, signature_header: str | None) -> bool:
    """Verify the webhook payload against the HMAC signature."""
    if not signature_header or not settings.github_webhook_secret:
        return False
    expected = "sha256=" + hmac.new(
        key=settings.github_webhook_secret.encode(),
        msg=payload_body,
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)


@router.post("/")
async def webhook_handler(
    request: Request,
    x_github_event: str = Header(default=""),
    x_hub_signature_256: str = Header(default=""),
    x_github_delivery: str = Header(default=""),
):
    """Main webhook endpoint for GitHub events."""
    body = await request.body()

    if not _verify_signature(body, x_hub_signature_256):
        logger.warning("Webhook signature verification failed (delivery=%s)", x_github_delivery)
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    logger.info("Received webhook: event=%s delivery=%s", x_github_event, x_github_delivery)

    # Route to appropriate handler based on event type
    match x_github_event:
        case "pull_request":
            await handle_pr_event(payload)
        case "issues":
            await handle_issue_event(payload)
        case "release":
            await handle_release_event(payload)
        case "check_run" | "check_suite":
            # Security scanning triggered via GitHub Checks
            await handle_security_scan(payload)
        case "ping":
            logger.info("Ping received — webhook configured correctly")
        case _:
            logger.debug("Unhandled event type: %s", x_github_event)

    return {"status": "ok", "delivery": x_github_delivery}


@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}