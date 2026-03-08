# 🤖 Artificial Scrum Master

**Agentic AI for monitoring Kanban boards** — Automatically scans open GitHub issues for staleness and GenAI-related roadblocks, then posts intelligent comments to keep your agile team moving at high velocity.

This bot acts as a virtual Scrum Master, detecting stalled tasks, flagging technical debt, and prompting updates—all while integrating seamlessly with your CI/CD pipelines.

---

## 🌟 Features

* 🔍 **Stale Issue Detection** – Identifies issues inactive for a configurable number of days.
* 🚧 **Roadblock Keyword Monitoring** – Flags comments/descriptions containing predefined risk terms (e.g., "data access", "rate limit").
* 💬 **Idempotent Commenting** – Uses hidden HTML markers to prevent duplicate bot messages.
* 📊 **Enterprise-Grade Logging** – Detailed logs for traceability in GitHub Actions runs.
* ⚙️ **Fully Configurable** – Set staleness threshold and roadblock keywords via environment variables.

---

## 🛠 How It Works

The Artificial Scrum Master follows a precise logic gate to ensure it only interacts when necessary, maintaining a high signal-to-noise ratio.



1.  **Data Retrieval:** The script fetches all open issues (excluding PRs) from the target repository.
2.  **Staleness Check:** It calculates the delta between the last update and the current timestamp.
3.  **Heuristic Scanning:** It scans the issue body and comments for specific roadblock keywords.
4.  **Idempotency Validation:** Before posting, it checks for hidden HTML markers (``) to ensure it doesn't spam the thread.

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.10+** (Recommended)
* **PyGithub** library
* **GitHub Personal Access Token (classic)** with `repo` scope.

### Installation & Usage

#### 1. As a GitHub Action (Recommended)
Add the following step to your `.github/workflows/scrum-master.yml`:

```yaml
- name: Run Artificial Scrum Master
  uses: your-username/artificial-scrum-master@v1
  with:
    days_stale: 2
    roadblocks: 'data access,rate limit,api latency,hallucination'
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

2. Local Execution
 * Clone the repository:
   git clone [https://github.com/your-username/artificial-scrum-master.git](https://github.com/your-username/artificial-scrum-master.git)
cd artificial-scrum-master

 * Install dependencies:
   pip install PyGithub

 * Set environment variables and run:
   export GITHUB_TOKEN=your_token
export GITHUB_REPOSITORY=owner/repo
export INPUT_DAYS_STALE=2
export INPUT_ROADBLOCKS="data access,rate limit,api latency,hallucination"
python scrum_master.py
```

⚙️ Configuration
The bot is highly customizable via environment variables:

| Variable | Description | Required | Default |
| :--- | :--- | :---: | :--- |
| `GITHUB_TOKEN` | GitHub token with repo access | ✅ | – |
| `GITHUB_REPOSITORY` | Repository name in `owner/repo` format | ✅ | – |
| `INPUT_DAYS_STALE` | Number of days after which an issue is considered stale | ❌ | `2` |
| `INPUT_ROADBLOCKS` | Comma-separated keywords that signal a GenAI roadblock | ❌ | `data access,rate limit,api latency,hallucination` |

```
📅 Example Workflow
Create .github/workflows/scrum-master-daily.yml to automate your daily standup checks:
name: Scrum Master Daily Scan

on:
  schedule:
    - cron: '0 9 * * *'   # Runs every day at 09:00 UTC
  workflow_dispatch:      # Allows manual trigger

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install PyGithub

      - name: Run Artificial Scrum Master
        run: python scrum_master.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
          INPUT_DAYS_STALE: 2
          INPUT_ROADBLOCKS: 'data access,rate limit,api latency,hallucination'
```
---
## ​🧩 Core Repository Components
* ​The Predictive Kanban Dashboard (index.html)
A zero-dependency, standalone interactive visual interface that maps GenAI use cases across a strict maturation lifecycle. It enforces a mandatory "Human-in-the-Loop (HITL)" review phase to monitor factual consistency and prevent model drift before scaling to production.
​
* The Agentic Scrum Master (ai_scrum_master.py)
An automated Python agent designed to run in your GitHub Actions pipeline. It continuously scans board activity, programmatically detecting stalled velocity and keyword-based technical debt (e.g., "API Latency", "Rate Limits"). It alerts the Chief AI Officer before a sprint fails.

* ​Governance Templates (.github/ISSUE_TEMPLATE/)
Standardized markdown templates that mandate AI Risk Assessments (Explainability, Data Privacy, Bias Audits) at the inception of every user story, turning compliance from an afterthought into a prerequisite.
---
## 🤝 Contributing
Contributions are welcome! Please follow these steps:
 * Fork the Project.
 * Create your Feature Branch (git checkout -b feature/AmazingFeature).
 * Commit your Changes (git commit -m 'Add some AmazingFeature').
 * Push to the Branch (git push origin feature/AmazingFeature).
 * Open a Pull Request.
---
📄 License
Distributed under the MIT License. See LICENSE for more information.
Built for agile teams that embrace AI-assisted development.
---
