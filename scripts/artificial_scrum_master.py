import os
import sys
import logging
from datetime import datetime, timedelta
from github import Github, GithubException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_env_var(name, default=None):
    value = os.getenv(name, default)
    if value is None:
        logger.error(f"Environment variable {name} is required.")
        sys.exit(1)
    return value

def parse_roadblocks(roadblocks_str):
    """Convert comma‑separated keywords into a list of lower‑cased strings."""
    if not roadblocks_str:
        return []
    return [r.strip().lower() for r in roadblocks_str.split(',') if r.strip()]

def main():
    # Configuration from environment (set by GitHub Actions or manually)
    token = get_env_var('GITHUB_TOKEN')
    repo_name = get_env_var('GITHUB_REPOSITORY')
    days_stale = int(os.getenv('INPUT_DAYS_STALE', '2'))
    roadblocks_str = os.getenv('INPUT_ROADBLOCKS',
                               'data access,rate limit,api latency,hallucination')
    roadblocks = parse_roadblocks(roadblocks_str)

    logger.info(f"Starting Artificial Scrum Master for {repo_name}")
    logger.info(f"Stale threshold: {days_stale} days | Roadblocks: {roadblocks}")

    # Connect to GitHub
    g = Github(token)
    try:
        repo = g.get_repo(repo_name)
    except GithubException as e:
        logger.error(f"Failed to access repository: {e}")
        sys.exit(1)

    stale_date = datetime.now() - timedelta(days=days_stale)
    open_issues = repo.get_issues(state='open')

    for issue in open_issues:
        # Skip pull requests
        if issue.pull_request:
            continue

        # Check if issue is stale (last updated before stale_date)
        if issue.updated_at.replace(tzinfo=None) < stale_date:
            comments = list(issue.get_comments())
            comment_bodies = [c.body.lower() for c in comments]

            # Combine issue body and all comments for keyword search
            issue_content = (issue.body or '').lower() + ' ' + ' '.join(comment_bodies)

            found_blockers = [r for r in roadblocks if r in issue_content]

            if found_blockers:
                alert_msg = (f"🚧 **AI Roadblock Detected**\n\n"
                             f"This issue appears to be stalled due to: {', '.join(found_blockers)}.\n\n"
                             f"@ChiefAIOfficer, @data-engineering team, please take a look.")
                # Avoid duplicate comments
                if not any(alert_msg.lower() in c for c in comment_bodies):
                    try:
                        issue.create_comment(alert_msg)
                        logger.info(f"Posted roadblock alert on #{issue.number}")
                    except GithubException as e:
                        logger.error(f"Failed to post comment on #{issue.number}: {e}")
            else:
                prompt_msg = (f"⏳ **Stale Issue Reminder**\n\n"
                              f"This issue has been inactive for {days_stale} days. "
                              f"Could you provide an update? Use AI as a strategy partner to pivot if needed.")
                if not any(prompt_msg.lower() in c for c in comment_bodies):
                    try:
                        issue.create_comment(prompt_msg)
                        logger.info(f"Posted stale reminder on #{issue.number}")
                    except GithubException as e:
                        logger.error(f"Failed to post comment on #{issue.number}: {e}")

if __name__ == "__main__":
    main()
