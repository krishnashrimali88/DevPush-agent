# 🤖 DevPush — Autonomous Multi-Agent Developer Assistant

> DevPush reviews your code, generates documentation, and opens a GitHub PR — all without you lifting a finger.

---

## ✨ Features

- 🔍 **Automated Code Review** — Detects unused imports, missing type hints, hardcoded values, and anti-patterns
- 📝 **Documentation Generation** — Writes a professional README and suggests docstrings for undocumented functions
- 🚀 **Autonomous PR Creation** — Commits changes to a branch and opens a GitHub Pull Request via MCP
- 🧠 **Multi-Agent Pipeline** — Orchestrator + 3 specialist agents, each with their own Agent Skill
- 🔒 **Human-in-the-Loop** — Pauses for your confirmation before writing to GitHub

---

## 🏗️ Architecture

```
User provides GitHub repo URL
        ↓
OrchestratorAgent
        ↓
CodeReviewAgent ──→ code_review_skill ──→ GitHub MCP (read)
        ↓
DocGenAgent ──────→ doc_gen_skill ────→ Gemini 2.0 Flash
        ↓
[Human confirmation]
        ↓
PRAgent ──────────→ pr_skill ─────────→ GitHub MCP (write)
        ↓
Returns PR URL
```

### Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Multi-agent system | OrchestratorAgent + 3 specialist agents |
| Agent Skills | `SKILL.md` files with YAML frontmatter + progressive disclosure |
| MCP server | GitHub MCP via `tools/github_mcp.py` |
| Security | Human-in-the-loop, scoped tokens, input validation |
| Progressive disclosure | Skills load only when triggered, keeping context small |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/devmind-agent
cd devmind-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_pat_here
```

> Get a Gemini API key at [aistudio.google.com](https://aistudio.google.com)
> Get a GitHub PAT at Settings → Developer Settings → Personal Access Tokens

### 4. Run DevMind

```bash
python main.py --repo https://github.com/yourusername/your-repo
```

With auto-confirm (skips human confirmation prompt):

```bash
python main.py --repo https://github.com/yourusername/your-repo --no-confirm
```

---

## 📁 Project Structure

```
devmind/
├── main.py                          # CLI entry point
├── config.py                        # Environment variable loader
├── requirements.txt
├── agents/
│   ├── orchestrator.py              # Master pipeline coordinator
│   ├── code_review_agent.py         # Specialist: static analysis
│   ├── doc_gen_agent.py             # Specialist: documentation
│   └── pr_agent.py                  # Specialist: GitHub PR creation
├── skills/
│   ├── code_review_skill/
│   │   ├── SKILL.md                 # Agent Skill definition
│   │   └── code_review_skill.py     # Skill implementation
│   ├── doc_gen_skill/
│   │   ├── SKILL.md
│   │   └── doc_gen_skill.py
│   └── pr_skill/
│       ├── SKILL.md
│       └── pr_skill.py
└── tools/
    └── github_mcp.py                # GitHub MCP server wrapper
```

---

## 🧠 About Agent Skills

Each specialist in DevMind is backed by an **Agent Skill** — a `SKILL.md` file with YAML frontmatter that defines:

- **When to trigger** (description field = routing algorithm)
- **What it does** (workflow steps)
- **What it must not do** (anti-triggers + anti-patterns)
- **Security tier** (`read-only` or `action-allowed`)

---

## 🔒 Security Design

- GitHub tokens are scoped to `repo:write` on the target repo only
- PRAgent requires explicit human confirmation before writing to GitHub
- Repository URLs are validated before being passed to any MCP tool
- No secrets are hardcoded — all loaded from `.env`

---

## 📄 License

MIT © Krishna Shrimali
