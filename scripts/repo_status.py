#!/usr/bin/env python3
"""Print current corpus counts.

Usage:
    repo_status.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _yaml_compat import yaml  # noqa: E402
from _wiki_root import WIKI_ROOT  # noqa: E402
import arch_policy  # noqa: E402

WIKI_SECTIONS = ("hardware", "techniques", "patterns", "kernels", "languages", "migration")
SOURCE_SECTIONS = ("prs", "docs", "blogs", "measurements")


def count_files(*parts: str, pattern: str = "*.md") -> int:
    root = WIKI_ROOT.joinpath(*parts)
    if not root.exists():
        return 0
    return sum(1 for p in root.rglob(pattern) if p.is_file())


def count_top_level_files(*parts: str, pattern: str = "*.md") -> int:
    root = WIKI_ROOT.joinpath(*parts)
    if not root.exists():
        return 0
    return sum(1 for p in root.glob(pattern) if p.is_file())


def load_frontmatter(path: Path) -> dict:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    match = re.match(r'^---\s*\r?\n(.*?)\r?\n---\s*\r?\n', content, re.DOTALL)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def count_prs_by_repo() -> Counter:
    counts: Counter = Counter()
    prs_root = WIKI_ROOT / "sources" / "prs"
    if not prs_root.exists():
        return counts
    for page in prs_root.rglob("*.md"):
        repo = load_frontmatter(page).get("repo")
        counts[str(repo) if repo else "(no repo field)"] += 1
    return counts


def count_measurements_by_device() -> Counter:
    counts: Counter = Counter()
    root = WIKI_ROOT / "sources" / "measurements"
    if not root.exists():
        return counts
    for page in root.rglob("*.md"):
        device = load_frontmatter(page).get("device")
        counts[arch_policy.normalize(device) if device else "(no device field)"] += 1
    return counts


def main() -> int:
    try:
        nodes = arch_policy.tree_order()
    except arch_policy.ArchitectureTreeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    source_pages = count_files("sources")
    wiki_pages = count_files("wiki")
    kinds = Counter(kind for _, _, kind in nodes)

    print("Corpus counts:")
    print(f"  Indexed source/wiki pages: {source_pages + wiki_pages}")
    print(f"  Wiki pages: {wiki_pages}")
    for section in WIKI_SECTIONS:
        print(f"    wiki/{section}: {count_files('wiki', section)}")
    print(f"  Source pages: {source_pages}")
    for section in SOURCE_SECTIONS:
        print(f"    sources/{section}: {count_files('sources', section)}")
    print(f"  Query indices: {count_top_level_files('queries')}")
    print(
        f"  Architecture nodes: {len(nodes)} "
        f"({', '.join(f'{kinds[k]} {k}' for k in arch_policy.NODE_KINDS)})"
    )

    pr_counts = count_prs_by_repo()
    if pr_counts:
        print()
        print("Source PR pages by repo:")
        for repo, count in sorted(pr_counts.items(), key=lambda item: item[0].lower()):
            print(f"  {repo}: {count}")

    device_counts = count_measurements_by_device()
    if device_counts:
        print()
        print("Measurement pages by device:")
        order = {name: i for i, name in enumerate(arch_policy.devices())}
        for device, count in sorted(
            device_counts.items(), key=lambda item: (order.get(item[0], len(order)), item[0])
        ):
            print(f"  {device}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
