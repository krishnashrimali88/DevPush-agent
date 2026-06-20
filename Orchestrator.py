"""
DevMind Orchestrator Agent
Coordinates CodeReviewAgent, DocGenAgent, and PRAgent in sequence.
"""

import json
from agents.code_review_agent import CodeReviewAgent
from agents.doc_gen_agent import DocGenAgent
from agents.pr_agent import PRAgent


class OrchestratorAgent:
    """
    Master agent that manages the full DevMind pipeline:
    1. Code Review → 2. Doc Generation → 3. PR Creation
    """

    def __init__(self, github_token: str, repo_url: str):
        self.github_token = github_token
        self.repo_url = repo_url
        self.context = {
            "repo_url": repo_url,
            "review_results": None,
            "generated_docs": None,
            "pr_url": None,
        }

    def run(self, confirm_before_pr: bool = True) -> dict:
        """
        Run the full multi-agent pipeline.

        Args:
            confirm_before_pr: If True, pauses and asks user before opening a PR.

        Returns:
            dict with review results, generated docs, and PR URL.
        """
        print(f"\n🤖 DevMind starting pipeline for: {self.repo_url}\n")

        # Step 1: Code Review
        print("🔍 Step 1/3 — Running CodeReviewAgent...")
        reviewer = CodeReviewAgent(self.repo_url, self.github_token)
        self.context["review_results"] = reviewer.run()
        print(f"   ✅ Found {len(self.context['review_results'])} issue(s)\n")

        # Step 2: Doc Generation
        print("📝 Step 2/3 — Running DocGenAgent...")
        doc_gen = DocGenAgent(self.repo_url, self.github_token)
        self.context["generated_docs"] = doc_gen.run()
        print(f"   ✅ Generated README and docstrings\n")

        # Step 3: Human-in-the-loop confirmation
        if confirm_before_pr:
            print("=" * 50)
            print("📋 REVIEW SUMMARY BEFORE PR:")
            print(f"   Issues found: {len(self.context['review_results'])}")
            print(f"   Docs generated: README.md + inline docstrings")
            print("=" * 50)
            confirm = input("\n🚦 Open a Pull Request with these changes? (yes/no): ")
            if confirm.strip().lower() != "yes":
                print("❌ PR creation cancelled by user.")
                return self.context

        # Step 4: PR Creation
        print("\n🚀 Step 3/3 — Running PRAgent...")
        pr_agent = PRAgent(self.repo_url, self.github_token)
        self.context["pr_url"] = pr_agent.run(
            review_results=self.context["review_results"],
            generated_docs=self.context["generated_docs"],
        )
        print(f"   ✅ PR opened: {self.context['pr_url']}\n")

        print("🎉 DevMind pipeline complete!")
        return self.context
