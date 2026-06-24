# Workshop Setup Guide

Complete these steps **before** the workshop. The setup takes about 15–20 minutes. If you run into issues, bring your laptop to the workshop early — we'll help you troubleshoot.

## 1. Git

You need Git 2.20+ (for worktree support).

```bash
git --version
```

**Install if missing:**
- **macOS:** `xcode-select --install` (or `brew install git`)
- **Linux:** `sudo apt install git` / `sudo dnf install git`
- **Windows:** [git-scm.com](https://git-scm.com/downloads)

## 2. Python 3.11+

```bash
python3 --version
```

**Install if missing:**
- **macOS:** `brew install python@3.11`
- **Linux:** `sudo apt install python3.11` / `sudo dnf install python3.11`
- **Windows:** [python.org](https://www.python.org/downloads/)

## 3. uv (Python Package Manager)

We use `uv` instead of `pip` for faster, more reliable dependency management.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify
uv --version
```

**Windows:** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

## 4. Node.js 18+

Required for MCP servers (Context7).

```bash
node --version
```

**Install if missing:**
- **macOS:** `brew install node`
- **Linux:** [nodesource.com](https://github.com/nodesource/distributions)
- **Windows:** [nodejs.org](https://nodejs.org/)

## 5. Terraform 1.0+

Required for Lab 3 (Cloud deployment).

```bash
terraform --version
```

**Install if missing:**
- **macOS:** `brew install terraform`
- **Linux/Windows:** [developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install)

## 6. Google Cloud CLI

Required for Lab 3 (Cloud deployment).

```bash
gcloud --version
```

**Install if missing:** [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

You do **not** need to authenticate before the workshop — we'll provide project access on the day.

## 7. AI Tools

Install **one CLI tool** and **one IDE tool**:

### CLI Tool (for Labs 0 and 1)

**Option A — Claude Code** (recommended)

```bash
# Install
npm install -g @anthropic-ai/claude-code

# Verify
claude --version
```

**Option B — Antigravity CLI (for Labs 0 and 1)**

Install `agy` using the instructions on [https://antigravity.google/download#antigravity-cli](https://antigravity.google/download#antigravity-cli).

```bash
# Verify
agy --version
```

### IDE Tool (for Labs 2 and 3)

**Option A — Antigravity IDE** (recommended)

Download from [https://antigravity.google/download#antigravity-ide](https://antigravity.google/download#antigravity-ide). It is a VS Code-based editor with built-in AI capabilities.

**Option B — Cursor** (alternative)

Download from [cursor.sh](https://cursor.sh/)

## 8. Download the Starter Project

Download and extract the starter project to your own working directory. **Do not work inside the cloned workshop repo** — you need your own independent git repo for the worktree workflow.

```bash
# Option A: Download via git (then copy and discard the clone)
git clone https://github.com/<org>/ai-driven-data-engineering.git
cp -r ai-driven-data-engineering/starter ~/my-pokedex-project
rm -rf ai-driven-data-engineering
cd ~/my-pokedex-project

# Option B: Download just the starter folder (if provided as a zip)
# unzip starter.zip -d ~/my-pokedex-project
# cd ~/my-pokedex-project
```

## 9. Initialize Your Git Repo

Create your own local git repo. This is a **local-only repo** — no remote, no risk of pushing to the workshop repo.

```bash
cd ~/my-pokedex-project
git init
git checkout -b development
git add .
git commit -m "initial project scaffold"
```

## 10. Set Up the Python Environment

```bash
uv venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows

uv pip install -r requirements.txt
```

## 11. Verify Everything Works

Run through this checklist:

```bash
# Git
git --version                    # 2.20+

# Python
python3 --version                # 3.11+

# uv
uv --version

# Node.js
node --version                   # 18+

# Terraform
terraform --version              # 1.0+

# Your CLI tool
claude --version                 # or: agy --help

# Python environment
uv run python -c "import dlt; import duckdb; print('Ready!')"
```

If all commands succeed, you're ready for the workshop.

## What You'll Receive at the Workshop

- **GCP project access** — a pre-provisioned Google Cloud playground
- **AI model API keys** — for your CLI and IDE tools

You do **not** need to set these up in advance.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `uv` not found after install | Restart your terminal or run `source ~/.bashrc` / `source ~/.zshrc` |
| `npm install -g` permission error | Use `sudo npm install -g` or configure npm global prefix |
| Python version too old | Install 3.11+ alongside your existing Python — `uv` handles virtual environments |
| `import dlt` fails | Make sure the virtual environment is activated and you ran `uv pip install -r requirements.txt` |
| Terraform not found | Ensure it's in your PATH — try `which terraform` or reinstall |

## Questions?

Reach out to the workshop organizer before the event. It's much easier to debug setup issues when you're not under time pressure.
