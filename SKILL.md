---
name: code-reviewing
description: |
  Analyzes Python source files for code quality issues and returns structured JSON feedback.
  Use this skill when the user wants to review, audit, lint, or find bugs in Python code.
  Triggers on: "review my code", "find issues", "check for bugs", "audit this repo".
  Do NOT use for generating documentation, creating PRs, or non-Python files.
version: 1.0.0
license: MIT
allowed-tools: Read
metadata:
  author: krishna-shrimali
  tier: read-only
---

# Code Review Skill

Reviews Python source files and returns a structured list of issues with severity ratings.

## When to use

- User asks to review, lint, or audit Python code
- User wants to find bugs, anti-patterns, or missing type hints
- Part of the DevMind pipeline after fetching repo files

## When NOT to use

- Generating documentation (use doc-generating skill)
- Opening PRs (use pr-opening skill)
- Reviewing non-Python files

## Workflow

1. Receive `file_path` and `source_code` as input
2. Send to Gemini with structured review prompt
3. Parse JSON response — strip markdown fences if present
4. Return list of issue dicts: `[{file, line, issue, severity}]`
5. On parse failure, return `[]` and log warning — never crash the pipeline

## Output format

```json
[
  {
    "file": "main.py",
    "line": 12,
    "issue": "Missing type hint on public function `run()`",
    "severity": "medium"
  }
]
```

## Severity levels

- `high` — Security issues, unhandled exceptions, hardcoded secrets
- `medium` — Missing type hints, missing docstrings, magic numbers
- `low` — Style issues, unused imports, naming conventions

## Anti-patterns to avoid

- Do NOT hallucinate line numbers — use `null` if unsure
- Do NOT return more than 30 issues per file chunk
- Do NOT include boilerplate issues the model already knows (e.g. "add comments")

## References

See `references/review_patterns.md` for common Python anti-pattern examples.
