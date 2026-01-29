#!/usr/bin/env python3
"""
Iron Bank Container Dependency Tree Traversal Tool

This script analyzes Iron Bank container dependencies by parsing hardening_manifest.yaml
files and recursively traversing the base image chain.

Environment Variables:
    IRONBANK_REPO_URL: Base URL for Iron Bank repositories (default: https://repo1.dso.mil/dsop)

Usage:
    python ironbank_tree.py [manifest_path_or_repo]
    python ironbank_tree.py hardening_manifest.yaml
    python ironbank_tree.py opensource/xfce/xfce-openjdk21
"""

import os
import sys
import json
import yaml
import urllib.request
import urllib.error
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum


class ContainerStatus(Enum):
    CURRENT = "current"
    UPDATE_AVAILABLE = "update_available"
    DEPRECATED = "deprecated"
    NOT_FOUND = "not_found"
    ERROR = "error"


@dataclass
class ContainerNode:
    """Represents a container in the dependency tree."""
    name: str
    repository: str
    current_tag: str
    latest_tag: Optional[str] = None
    base_image: Optional[str] = None
    base_tag: Optional[str] = None
    status: ContainerStatus = ContainerStatus.CURRENT
    depth: int = 0
    manifest_data: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "repository": self.repository,
            "current_tag": self.current_tag,
            "latest_tag": self.latest_tag,
            "base_image": self.base_image,
            "base_tag": self.base_tag,
            "status": self.status.value,
            "depth": self.depth,
            "error_message": self.error_message
        }


@dataclass
class DependencyTree:
    """Represents the full container dependency tree."""
    root: Optional[ContainerNode] = None
    nodes: List[ContainerNode] = field(default_factory=list)
    edges: List[Dict[str, str]] = field(default_factory=list)
    max_depth: int = 0
    update_count: int = 0
    deprecated_count: int = 0
    error_count: int = 0

    def add_node(self, node: ContainerNode) -> None:
        """Add a node to the tree."""
        self.nodes.append(node)
        if node.depth > self.max_depth:
            self.max_depth = node.depth
        if node.status == ContainerStatus.UPDATE_AVAILABLE:
            self.update_count += 1
        elif node.status == ContainerStatus.DEPRECATED:
            self.deprecated_count += 1
        elif node.status in (ContainerStatus.NOT_FOUND, ContainerStatus.ERROR):
            self.error_count += 1

    def add_edge(self, from_repo: str, to_repo: str) -> None:
        """Add an edge between containers."""
        self.edges.append({"from": from_repo, "to": to_repo})

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "root": self.root.to_dict() if self.root else None,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": self.edges,
            "max_depth": self.max_depth,
            "update_count": self.update_count,
            "deprecated_count": self.deprecated_count,
            "error_count": self.error_count
        }


class IronBankTreeTraversal:
    """Main class for traversing Iron Bank container dependencies."""

    # Terminal base images that don't have further dependencies
    TERMINAL_BASES = [
        "ubi9", "ubi8", "ubi9-minimal", "ubi8-minimal",
        "ubi9-micro", "ubi8-micro", "scratch", "distroless"
    ]

    def __init__(self, repo_url: Optional[str] = None, raw_url: Optional[str] = None):
        """
        Initialize the traversal tool.

        Args:
            repo_url: Base URL for Iron Bank repositories
            raw_url: URL pattern for fetching raw manifest files (use {path} placeholder)
        """
        self.repo_url = repo_url or os.environ.get(
            "IRONBANK_REPO_URL",
            "https://repo1.dso.mil/dsop"
        )
        # IRONBANK_RAW_URL allows custom URL pattern for fetching raw files
        # Use {path} as placeholder for repo path
        # Default: construct from repo_url with GitLab raw file pattern
        self.raw_url = raw_url or os.environ.get("IRONBANK_RAW_URL")
        self.tree = DependencyTree()
        self.visited = set()  # Track visited repos to prevent cycles

    def parse_manifest(self, manifest_content: str) -> Dict[str, Any]:
        """
        Parse a hardening_manifest.yaml file.

        Args:
            manifest_content: YAML content of the manifest

        Returns:
            Parsed manifest data as dictionary
        """
        try:
            return yaml.safe_load(manifest_content)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML: {e}")

    def extract_base_info(self, manifest: Dict[str, Any]) -> tuple:
        """
        Extract base image information from manifest.

        Args:
            manifest: Parsed manifest dictionary

        Returns:
            Tuple of (base_image, base_tag, base_registry)
        """
        args = manifest.get("args", {})
        base_image = args.get("BASE_IMAGE", "")
        base_tag = args.get("BASE_TAG", "")
        base_registry = args.get("BASE_REGISTRY", "registry1.dso.mil")

        # Remove ironbank/ prefix if present
        if base_image.startswith("ironbank/"):
            base_image = base_image[len("ironbank/"):]

        return base_image, base_tag, base_registry

    def fetch_manifest_from_repo(self, repo_path: str, branch: str = "development") -> Optional[str]:
        """
        Fetch hardening_manifest.yaml from a GitLab repository.

        Uses IRONBANK_RAW_URL if set (with {path} placeholder replaced),
        otherwise falls back to constructing URL from IRONBANK_REPO_URL.

        Args:
            repo_path: Repository path (e.g., 'redhat/openjdk/openjdk21-ubi9')
            branch: Git branch to fetch from

        Returns:
            Manifest content as string, or None if not found
        """
        urls_to_try = []

        # If IRONBANK_RAW_URL is set, try it first
        if self.raw_url:
            custom_url = self.raw_url.replace("{path}", repo_path)
            urls_to_try.append(("IRONBANK_RAW_URL", custom_url))

        # Always include the default GitLab raw file URL as fallback
        default_url = f"{self.repo_url}/{repo_path}/-/raw/{branch}/hardening_manifest.yaml"
        urls_to_try.append(("IRONBANK_REPO_URL", default_url))

        last_error = None
        for url_source, url in urls_to_try:
            try:
                req = urllib.request.Request(url, headers={
                    "User-Agent": "IronBank-Tree-Traversal/1.0"
                })
                with urllib.request.urlopen(req, timeout=30) as response:
                    return response.read().decode('utf-8')
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    last_error = None  # 404 is expected, try next URL
                    continue
                last_error = e
            except urllib.error.URLError as e:
                last_error = e
                # Log and try next URL
                continue

        # If all URLs failed
        if last_error:
            raise ConnectionError(f"Failed to fetch manifest from {repo_path}: {last_error}")
        return None  # 404 from all sources

    def fetch_latest_tags(self, repo_path: str) -> Optional[List[str]]:
        """
        Fetch available tags from the GitLab repository.

        Args:
            repo_path: Repository path (e.g., 'redhat/openjdk/openjdk21-ubi9')

        Returns:
            List of tag names, or None if unable to fetch
        """
        # GitLab API endpoint for repository tags
        # URL encode the repo path for the API
        encoded_path = repo_path.replace("/", "%2F")
        url = f"{self.repo_url}/api/v4/projects/dsop%2F{encoded_path}/repository/tags"

        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "IronBank-Tree-Traversal/1.0"
            })
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                return [tag.get("name", "") for tag in data if tag.get("name")]
        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
            return None

    def populate_update_status(self, node: ContainerNode) -> None:
        """
        Populate latest_tag and status for a container node.

        Fetches available tags from the repository and determines if
        an update is available by comparing to current_tag.

        Args:
            node: ContainerNode to update with status information
        """
        if node.repository == "local":
            # Can't determine updates for local files without more context
            return

        tags = self.fetch_latest_tags(node.repository)

        if tags is None:
            # Could not fetch tags - status remains CURRENT (unknown)
            # We don't set ERROR here since the manifest was successfully parsed
            return

        if not tags:
            # Repository exists but has no tags - might be deprecated
            node.status = ContainerStatus.DEPRECATED
            return

        # Get the latest tag (first in list, typically most recent)
        latest = tags[0] if tags else None
        node.latest_tag = latest

        # Compare versions to determine if update is available
        if latest and latest != node.current_tag:
            # Simple comparison - if tags differ, update may be available
            # More sophisticated version comparison could be added here
            node.status = ContainerStatus.UPDATE_AVAILABLE

    def is_terminal_base(self, repo_path: str) -> bool:
        """
        Check if a repository is a terminal base (no further dependencies).

        Only matches when repo_name exactly equals a terminal base or has
        the terminal base as a distinct suffix with token boundary.
        e.g., "ubi9" matches, "foo-ubi9" matches, but "openjdk21-ubi9" does NOT
        match because we want to traverse into openjdk containers.

        Args:
            repo_path: Repository path to check

        Returns:
            True if this is a terminal base image
        """
        import re
        repo_name = repo_path.split("/")[-1].lower()

        for base in self.TERMINAL_BASES:
            # Match if repo_name exactly equals the base
            if repo_name == base:
                return True
            # Match if base appears at end with non-alphanumeric boundary
            # e.g., "9.x/ubi9" -> repo_name="ubi9" matches
            # but "openjdk21-ubi9" should NOT match (it's not a terminal)
            # Terminal bases are standalone repos like "ubi9", not suffixes
            pattern = rf'(^|[^a-z0-9]){re.escape(base)}$'
            if re.search(pattern, repo_name):
                # Additional check: exclude if there's a product name prefix
                # like "openjdk21-ubi9" or "nodejs18-ubi9"
                if re.match(rf'^[a-z]+\d+[-_]{re.escape(base)}$', repo_name):
                    continue  # This is a product container, not terminal
                return True

        return False

    def normalize_repo_path(self, base_image: str) -> str:
        """
        Normalize repository path for Iron Bank lookup.

        Args:
            base_image: Base image path from manifest

        Returns:
            Normalized repository path
        """
        # Handle common path variations
        path = base_image

        # Remove registry prefix if present
        if "/" in path and "." in path.split("/")[0]:
            path = "/".join(path.split("/")[1:])

        # Remove ironbank prefix
        if path.startswith("ironbank/"):
            path = path[len("ironbank/"):]

        return path

    def traverse(self, start_path: str, depth: int = 0) -> Optional[ContainerNode]:
        """
        Recursively traverse the container dependency tree.

        Args:
            start_path: Repository path or local manifest path
            depth: Current depth in the tree

        Returns:
            Root ContainerNode of the traversed tree
        """
        # Determine if start_path is a local file or repository and normalize
        # the path BEFORE cycle detection so we use canonical repo identifiers
        manifest_content = None

        if os.path.isfile(start_path):
            # For local files, use absolute path as canonical identifier
            repo_path = os.path.abspath(start_path)
        else:
            # Normalize repository path to canonical form
            repo_path = self.normalize_repo_path(start_path)

        # Check for cycles using normalized path
        if repo_path in self.visited:
            return None
        self.visited.add(repo_path)

        # Now fetch the manifest content
        if os.path.isfile(start_path):
            with open(start_path, 'r') as f:
                manifest_content = f.read()
            repo_path = "local"  # Reset for display purposes
        else:
            try:
                manifest_content = self.fetch_manifest_from_repo(repo_path)
            except Exception as e:
                node = ContainerNode(
                    name=repo_path.split("/")[-1],
                    repository=repo_path,
                    current_tag="unknown",
                    status=ContainerStatus.ERROR,
                    depth=depth,
                    error_message=str(e)
                )
                self.tree.add_node(node)
                return node

        if manifest_content is None:
            node = ContainerNode(
                name=repo_path.split("/")[-1],
                repository=repo_path,
                current_tag="unknown",
                status=ContainerStatus.NOT_FOUND,
                depth=depth,
                error_message="Manifest not found"
            )
            self.tree.add_node(node)
            return node

        # Parse the manifest
        try:
            manifest = self.parse_manifest(manifest_content)
        except ValueError as e:
            node = ContainerNode(
                name=repo_path.split("/")[-1],
                repository=repo_path,
                current_tag="unknown",
                status=ContainerStatus.ERROR,
                depth=depth,
                error_message=str(e)
            )
            self.tree.add_node(node)
            return node

        # Extract information
        name = manifest.get("name", repo_path.split("/")[-1])
        tags = manifest.get("tags", [])
        current_tag = tags[0] if tags else "latest"
        base_image, base_tag, base_registry = self.extract_base_info(manifest)

        # Create node
        node = ContainerNode(
            name=name,
            repository=repo_path,
            current_tag=current_tag,
            base_image=base_image,
            base_tag=base_tag,
            depth=depth,
            manifest_data=manifest
        )

        # Populate update status (latest_tag and status)
        self.populate_update_status(node)

        # Add to tree
        self.tree.add_node(node)
        if depth == 0:
            self.tree.root = node

        # Check if this is a terminal base
        if self.is_terminal_base(repo_path) or not base_image:
            return node

        # Recurse to parent
        if base_image:
            parent_node = self.traverse(base_image, depth + 1)
            if parent_node:
                self.tree.add_edge(repo_path, parent_node.repository)

        return node

    def generate_mermaid_diagram(self) -> str:
        """
        Generate a Mermaid diagram of the dependency tree.

        Returns:
            Mermaid diagram as string
        """
        lines = ["graph TD"]

        # Add nodes
        node_ids = {}
        for i, node in enumerate(self.tree.nodes):
            node_id = f"N{i}"
            node_ids[node.repository] = node_id
            label = f"{node.name}<br/>{node.current_tag}"
            lines.append(f'    {node_id}["{label}"]')

            # Add styling based on status
            if node.status == ContainerStatus.UPDATE_AVAILABLE:
                lines.append(f"    {node_id}:::update")
            elif node.status == ContainerStatus.DEPRECATED:
                lines.append(f"    {node_id}:::deprecated")
            elif node.status in (ContainerStatus.NOT_FOUND, ContainerStatus.ERROR):
                lines.append(f"    {node_id}:::error")

        # Add edges
        for edge in self.tree.edges:
            from_id = node_ids.get(edge["from"], "")
            to_id = node_ids.get(edge["to"], "")
            if from_id and to_id:
                lines.append(f"    {from_id} --> {to_id}")

        # Add legend
        lines.extend([
            "",
            "    classDef update fill:#ffeb3b,stroke:#f57f17",
            "    classDef deprecated fill:#ef5350,stroke:#c62828",
            "    classDef error fill:#9e9e9e,stroke:#616161"
        ])

        return "\n".join(lines)

    def generate_update_plan(self) -> str:
        """
        Generate an update task plan for the dependency tree.

        Returns:
            Markdown formatted update plan
        """
        lines = ["## Update Task Plan", ""]

        # Sort nodes by depth (deepest first for bottom-up updates)
        sorted_nodes = sorted(self.tree.nodes, key=lambda n: -n.depth)

        # Group by priority
        base_updates = []
        intermediate_updates = []
        app_updates = []

        for node in sorted_nodes:
            if node.status == ContainerStatus.UPDATE_AVAILABLE or node.latest_tag:
                if node.depth >= 2:
                    base_updates.append(node)
                elif node.depth == 1:
                    intermediate_updates.append(node)
                else:
                    app_updates.append(node)

        # Generate plan sections
        if base_updates:
            lines.append("### Priority 1: Base Image Updates (Bottom-Up)")
            for i, node in enumerate(base_updates, 1):
                lines.append(f"{i}. [ ] Update {node.name}: {node.current_tag} → {node.latest_tag or 'latest'}")
                lines.append(f"   - Repository: {node.repository}")
                lines.append(f"   - Impact: All dependent images")
                lines.append("")

        if intermediate_updates:
            lines.append("### Priority 2: Intermediate Images")
            for i, node in enumerate(intermediate_updates, len(base_updates) + 1):
                lines.append(f"{i}. [ ] Update {node.name}: {node.current_tag}")
                lines.append(f"   - Repository: {node.repository}")
                if node.base_image:
                    lines.append(f"   - Depends on: {node.base_image}")
                lines.append("")

        if app_updates:
            lines.append("### Priority 3: Application Images")
            for i, node in enumerate(app_updates, len(base_updates) + len(intermediate_updates) + 1):
                lines.append(f"{i}. [ ] Update {node.name}: {node.current_tag}")
                lines.append(f"   - Repository: {node.repository}")
                if node.base_image:
                    lines.append(f"   - Depends on: {node.base_image}")
                lines.append("")

        if not (base_updates or intermediate_updates or app_updates):
            lines.append("No updates required - all containers are current.")

        return "\n".join(lines)

    def generate_summary_table(self) -> str:
        """
        Generate a summary table of all containers.

        Returns:
            Markdown formatted table
        """
        lines = [
            "## Dependency Chain",
            "",
            "| Depth | Container | Repository | Current Tag | Base Image | Status |",
            "|-------|-----------|------------|-------------|------------|--------|"
        ]

        for node in sorted(self.tree.nodes, key=lambda n: n.depth):
            status_emoji = {
                ContainerStatus.CURRENT: "✅",
                ContainerStatus.UPDATE_AVAILABLE: "⚠️",
                ContainerStatus.DEPRECATED: "❌",
                ContainerStatus.NOT_FOUND: "❓",
                ContainerStatus.ERROR: "💥"
            }.get(node.status, "")

            base = node.base_image or "-"
            if len(base) > 30:
                base = "..." + base[-27:]

            lines.append(
                f"| {node.depth} | {node.name} | {node.repository[:40]} | "
                f"{node.current_tag[:25]} | {base} | {status_emoji} {node.status.value} |"
            )

        return "\n".join(lines)

    def generate_report(self) -> str:
        """
        Generate a full analysis report.

        Returns:
            Complete markdown report
        """
        root_name = self.tree.root.name if self.tree.root else "Unknown"

        report = [
            f"# Iron Bank Dependency Tree Analysis",
            "",
            f"## Container: {root_name}",
            "",
            f"**Total Layers**: {len(self.tree.nodes)}",
            f"**Max Depth**: {self.tree.max_depth}",
            f"**Updates Available**: {self.tree.update_count}",
            f"**Deprecated**: {self.tree.deprecated_count}",
            f"**Errors**: {self.tree.error_count}",
            "",
            self.generate_summary_table(),
            "",
            "## Dependency Diagram",
            "",
            "```mermaid",
            self.generate_mermaid_diagram(),
            "```",
            "",
            self.generate_update_plan()
        ]

        return "\n".join(report)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python ironbank_tree.py <manifest_path_or_repo>")
        print("Example: python ironbank_tree.py hardening_manifest.yaml")
        print("Example: python ironbank_tree.py opensource/xfce/xfce-openjdk21")
        sys.exit(1)

    start_path = sys.argv[1]

    traversal = IronBankTreeTraversal()

    try:
        traversal.traverse(start_path)
        report = traversal.generate_report()
        print(report)

        # Also output JSON for programmatic use
        if "--json" in sys.argv:
            print("\n---JSON OUTPUT---")
            print(json.dumps(traversal.tree.to_dict(), indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
