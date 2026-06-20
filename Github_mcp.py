"""
github_mcp.py — GitHub MCP tool wrapper for DevMind agents.
Wraps GitHub REST API calls to simulate MCP server tool use.
"""

import base64
import requests


class GitHubMCP:
    """
    Wrapper around GitHub REST API acting as the MCP server.
    Provides list_files, read_file, create_branch, create_or_update_file,
    and create_pull_request tools.
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def list_files(self, owner: str, repo: str, extension: str = ".py", path: str = "") -> list[str]:
        """
        Lists all files in a repo with a given extension (recursive).

        Args:
            owner: Repo owner username.
            repo: Repo name.
            extension: File extension to filter by (e.g. '.py').
            path: Sub-directory path (default: root).

        Returns:
            List of file paths matching the extension.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        tree = response.json().get("tree", [])
        return [
            item["path"]
            for item in tree
            if item["type"] == "blob" and item["path"].endswith(extension)
        ]

    def read_file(self, owner: str, repo: str, path: str) -> str | None:
        """
        Reads and returns the decoded content of a file from GitHub.

        Args:
            owner: Repo owner username.
            repo: Repo name.
            path: File path within the repo.

        Returns:
            Decoded file content as a string, or None on failure.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"   ⚠️ Could not read {path}: {response.status_code}")
            return None

        content_b64 = response.json().get("content", "")
        return base64.b64decode(content_b64).decode("utf-8", errors="replace")

    def get_default_branch_sha(self, owner: str, repo: str) -> str:
        """Gets the SHA of the HEAD commit on the default branch."""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/git/ref/heads/main"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["object"]["sha"]

    def create_branch(self, owner: str, repo: str, branch_name: str) -> None:
        """
        Creates a new branch from HEAD of main.

        Args:
            owner: Repo owner username.
            repo: Repo name.
            branch_name: Name of the new branch.
        """
        sha = self.get_default_branch_sha(owner, repo)
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/git/refs"
        payload = {"ref": f"refs/heads/{branch_name}", "sha": sha}
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 422:
            print(f"   ℹ️ Branch '{branch_name}' already exists, continuing...")
        else:
            response.raise_for_status()

    def create_or_update_file(
        self,
        owner: str,
        repo: str,
        branch: str,
        path: str,
        content: str,
        message: str,
    ) -> None:
        """
        Creates or updates a file in a branch.

        Args:
            owner: Repo owner.
            repo: Repo name.
            branch: Target branch.
            path: File path to create/update.
            content: File content as a string.
            message: Commit message.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}"

        # Check if file exists (to get its SHA for update)
        existing = requests.get(url, headers=self.headers, params={"ref": branch})
        sha = existing.json().get("sha") if existing.status_code == 200 else None

        payload = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "branch": branch,
        }
        if sha:
            payload["sha"] = sha

        response = requests.put(url, headers=self.headers, json=payload)
        response.raise_for_status()

    def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str = "main",
    ) -> str:
        """
        Opens a Pull Request on GitHub.

        Args:
            owner: Repo owner.
            repo: Repo name.
            title: PR title.
            body: PR description (markdown).
            head: Source branch.
            base: Target branch (default: main).

        Returns:
            HTML URL of the created PR.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls"
        payload = {"title": title, "body": body, "head": head, "base": base}
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()["html_url"]
