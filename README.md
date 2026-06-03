# ReviewBot

> AI-powered code review and maintainer automation for open source projects.

ReviewBot is a GitHub App that helps open source maintainers automate the most time-consuming parts of their workflow: PR review, issue triage, release drafting, and security scanning. It integrates directly with GitHub via webhooks and supports multiple AI backends, with a primary focus on OpenAI Codex.

## Features

| Module | Description |
|--------|-------------|
| **PR Reviewer** | Automatic first-pass code review on pull requests — detects bugs, security issues, style violations, and suggests improvements |
| **Issue Triage** | Intelligent issue labeling, duplicate detection, and automatic linking to related PRs |
| **Release Drafter** | Generates structured release notes from merged PRs with categorized changelogs |
| **Security Scanner** | Dependency vulnerability detection and code-level security pattern matching |
| **Multi-Model** | Pluggable AI backend — Codex (default), Claude, Gemini, or local models |

## How It Works

```
GitHub Webhook → ReviewBot Server → AI Backend (Codex) → GitHub API (comment/label/review)
```

1. Install the GitHub App on your repository
2. ReviewBot receives webhook events for PRs, issues, and releases
3. AI analyzes the context and generates reviews, labels, or release notes
4. Results are posted back to GitHub as comments, reviews, or labels

## Quick Start

### Prerequisites

- Python 3.11+
- A GitHub App (create one at `Settings > Developer settings > GitHub Apps`)
- An OpenAI API key (or other supported AI provider)

### Installation

```bash
git clone https://github.com/your-username/reviewbot.git
cd reviewbot
pip install -e .
```

### Configuration

Copy the example config and fill in your credentials:

```bash
cp .env.example .env
```

Required environment variables:

| Variable | Description |
|----------|-------------|
| `GITHUB_APP_ID` | Your GitHub App ID |
| `GITHUB_APP_PRIVATE_KEY` | Path to your GitHub App private key |
| `GITHUB_WEBHOOK_SECRET` | Webhook secret for verifying payloads |
| `OPENAI_API_KEY` | OpenAI API key for Codex |
| `OPENAI_ORG_ID` | Your OpenAI organization ID |

### Running the Server

```bash
reviewbot server --port 8000
```

### Running via Docker

```bash
docker compose up -d
```

## Architecture

```
src/reviewbot/
├── ai/              # AI backend adapters and prompt templates
│   ├── codex.py     # OpenAI Codex integration
│   ├── adapters.py  # Multi-model adapter layer
│   └── prompts.py   # Prompt templates for each module
├── github/          # GitHub integration
│   ├── app.py       # GitHub App authentication & API client
│   └── webhooks.py  # Webhook event routing
├── review/          # PR review module
│   ├── pr_reviewer.py
│   └── security_scanner.py
├── triage/          # Issue triage module
│   └── issue_triage.py
├── release/         # Release drafting module
│   └── release_drafter.py
├── config.py        # Configuration management
└── main.py          # FastAPI application entry point
cli/
└── commands.py      # CLI interface
```

## Why ReviewBot?

Open source maintainers are overwhelmed. The average popular project receives dozens of PRs and issues per week, and triaging them manually is unsustainable. ReviewBot acts as a tireless first responder, giving maintainers more time for the work that truly needs their expertise.

ReviewBot itself is built to benefit from — and showcase — the Codex for Open Source program. Every feature maps directly to a maintainer workflow that the program aims to support.

## License

MIT © ReviewBot Contributors