#!/usr/bin/env python3
"""
Artificial Scrum Master – Agentic AI for monitoring Kanban boards.

Scans open issues in a GitHub repository for staleness and GenAI roadblocks,
then posts comments to alert the team or ask for updates. Engineered for 
high-velocity agile teams utilizing CI/CD pipelines.
"""

import os
import sys
import logging
from datetime import datetime, timedelta, timezone
from github import Github, GithubException

# Configure enterprise-grade logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Hidden HTML markers to ensure idempotency (prevents duplicate bot comments)
ROADBLOCK_MARKER = "<!-- AI_SCRUM_MASTER_ROADBLOCK -->"
STALE_MARKER = "<!-- AI_SCRUM_MASTER_STALE -->"

def get_env_var(name, default=None):
    """Safely retrieve environment variables, critical for CI/CD security."""
    value = os.getenv(name, default)
    if value is None:
        logger.error(f"FATAL: Environment variable {name} is required for execution.")
        sys.exit(1)
    return value

def parse_roadblocks(roadblocks_str):
    """Convert comma-separated keywords into a sanitized list of lowercase strings."""
    if not roadblocks_str:
        return []
    return [r.strip().lower() for r in roadblocks_str.split(',') if r.strip()]

def main():
    # 1. Configuration from environment (Set by GitHub Actions)
    token = get_env_var('GITHUB_TOKEN')
    repo_name = get_env_var('GITHUB_REPOSITORY')
    
    # Cast days_stale safely, defaulting to 2 days for high-velocity sprints
    try:
        days_stale = int(os.getenv('INPUT_DAYS_STALE', '2'))
    except ValueError:
        logger.warning("Invalid INPUT_DAYS_STALE provided. Defaulting to 2.")
        days_stale = 2
        
    roadblocks_str = os.getenv('INPUT_ROADBLOCKS', 'data access,rate limit,api latency,hallucination')
    roadblocks = parse_roadblocks(roadblocks_str)

    logger.info(f"Initiating Artificial Scrum Master for repository: {repo_name}")
    logger.info(f"Metrics -> Stale threshold: {days_stale} days | Tracking {len(roadblocks)} Risk Factors.")

    # 2. Authenticate & Connect to GitHub
    g = Github(token)
    try:
        repo = g.get_repo(repo_name)
    except GithubException as e:
        logger.error(f"API Authentication/Access Failure: {e}")
        sys.exit(1)

    # Use timezone-aware UTC datetimes for consistent comparison
    stale_date = datetime.now(timezone.utc) - timedelta(days=days_stale)
    
    try:
        open_issues = repo.get_issues(state='open')
    except GithubException as e:
        logger.error(f"Failed to fetch repository issues: {e}")
        sys.exit(1)

    # 3. Process Issues (The "Predictive Agile" Loop)
    for issue in open_issues:
        # Ignore pull requests; we only want to manage Agile task issues
        if issue.pull_request:
            continue

        # Ensure updated_at is timezone-aware (GitHub returns UTC, but we normalize)
        issue_updated = issue.updated_at
        if issue_updated.tzinfo is None:
            # Fallback: assume UTC if naive (should not happen, but safe)
            issue_updated = issue_updated.replace(tzinfo=timezone.utc)

        if issue_updated < stale_date:
            try:
                comments = list(issue.get_comments())
            except GithubException as e:
                logger.error(f"Failed to fetch comments for issue #{issue.number}: {e}")
                continue

            # Safely handle None bodies
            comment_bodies_lower = [(c.body or '').lower() for c in comments]
            raw_comment_bodies = [c.body or '' for c in comments]

            # Combine issue body and all comments for a holistic keyword search
            issue_content = (issue.body or '').lower() + ' ' + ' '.join(comment_bodies_lower)

            # Check for GenAI-specific technical debt or risks
            found_blockers = [r for r in roadblocks if r in issue_content]

            if found_blockers:
                # Use hidden HTML markers for robust idempotency
                if not any(ROADBLOCK_MARKER in c for c in raw_comment_bodies):
                    alert_msg = (f"{ROADBLOCK_MARKER}\n"
                                 f"🚧 **AI Roadblock Detected**\n\n"
                                 f"This task's velocity has dropped. It appears stalled due to: **{', '.join(found_blockers)}**.\n\n"
                                 f"@ChiefAIOfficer, @data-engineering team — Please review to unblock the pipeline and maintain sprint velocity.")
                    try:
                        issue.create_comment(alert_msg)
                        logger.info(f"Action Taken: Posted roadblock alert on Issue #{issue.number}")
                    except GithubException as e:
                        logger.error(f"Failed to post comment on #{issue.number}: {e}")
            else:
                # Standard stale issue ping
                if not any(STALE_MARKER in c for c in raw_comment_bodies):
                    prompt_msg = (f"{STALE_MARKER}\n"
                                  f"⏳ **Stale Issue Reminder**\n\n"
                                  f"This issue has been inactive for {days_stale} days, impacting our burndown rate. "
                                  f"Could the assignee provide an update? Remember to use Copilot or GenAI as a strategy partner to pivot if you are stuck.")
                    try:
                        issue.create_comment(prompt_msg)
                        logger.info(f"Action Taken: Posted stale reminder on Issue #{issue.number}")
                    except GithubException as e:
                        logger.error(f"Failed to post comment on #{issue.number}: {e}")

if __name__ == "__main__":
    main()