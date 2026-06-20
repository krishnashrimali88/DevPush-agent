"""
main.py — DevMind CLI entry point.

Usage:
    python main.py --repo https://github.com/owner/repo
    python main.py --repo https://github.com/owner/repo --no-confirm
"""

import argparse
from config import GITHUB_TOKEN
from agents.orchestrator import OrchestratorAgent


def main():
    parser = argparse.ArgumentParser(
        description="DevMind: Autonomous multi-agent developer assistant"
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="GitHub repository URL (e.g. https://github.com/owner/repo)",
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Skip human-in-the-loop confirmation before opening PR",
    )
    args = parser.parse_args()

    # Validate URL
    if not args.repo.startswith("https://github.com/"):
        print("❌ Error: Please provide a full GitHub URL (https://github.com/owner/repo)")
        return

    orchestrator = OrchestratorAgent(
        github_token=GITHUB_TOKEN,
        repo_url=args.repo,
    )

    result = orchestrator.run(confirm_before_pr=not args.no_confirm)

    print("\n📊 Final Results:")
    print(f"   Issues found   : {len(result.get('review_results', []))}")
    print(f"   Docs generated : {'✅' if result.get('generated_docs') else '❌'}")
    print(f"   PR URL         : {result.get('pr_url') or 'Not created'}")


if __name__ == "__main__":
    main()
