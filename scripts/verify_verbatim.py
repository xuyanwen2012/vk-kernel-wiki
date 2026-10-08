#!/usr/bin/env python3
"""Check that every pull-request artifact bundle is intact and verbatim.

Offline (default): each bundle under `artifacts/prs/` has its PROVENANCE.yaml,
its upstream licence text, and patch text whose sha256 matches the recorded
one; every `artifact_dir` named by a source-pr page exists, and every bundle
is named by a page.

With --against-cache: additionally compares each recorded sha256 with the
patch text in the evidence cache (`.cache/pr-evidence/`), which is what
GitHub returned. Bundles without cached evidence are reported and skipped.

Every bundle of complete kernel files under `artifacts/kernels/` is checked
the same way (PROVENANCE.yaml, licence text, sha256 per file).

Exit 0 when everything checks out, 1 otherwise.

Usage:
    verify_verbatim.py [--against-cache] [--cache-dir DIR]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pr_artifacts  # noqa: E402
import pr_evidence  # noqa: E402
from _yaml_compat import yaml  # noqa: E402
from _wiki_root import WIKI_ROOT  # noqa: E402


def page_artifact_dirs() -> dict:
    out = {}
    root = WIKI_ROOT / "sources" / "prs"
    for page in sorted(root.rglob("*.md")) if root.is_dir() else []:
        match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", page.read_text(encoding="utf-8"), re.DOTALL)
        fm = (yaml.safe_load(match.group(1)) or {}) if match else {}
        if isinstance(fm, dict) and fm.get("artifact_dir"):
            out[str(fm["artifact_dir"])] = page.relative_to(WIKI_ROOT).as_posix()
    return out


def cache_errors(rel: str, slug: str, cache_dir) -> tuple:
    provenance = yaml.safe_load((WIKI_ROOT / rel / pr_artifacts.PROVENANCE_NAME).read_text(encoding="utf-8"))
    evidence = pr_evidence.load_cached(slug, provenance["pr"], cache_dir)
    if evidence is None:
        return [], True
    upstream = {f["filename"]: f.get("patch") for f in evidence["files"]}
    errors = []
    for entry in provenance.get("files") or []:
        patch = upstream.get(entry["path"])
        expected = pr_artifacts.sha256_text(patch) if patch else None
        if expected != entry.get("sha256"):
            errors.append(f"{rel}: '{entry['path']}' differs from the cached upstream patch")
    return errors, False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--against-cache", action="store_true", help="also compare with cached upstream patches")
    parser.add_argument("--cache-dir", help="evidence cache directory (default: <root>/.cache/pr-evidence)")
    args = parser.parse_args()

    base = WIKI_ROOT / pr_artifacts.ARTIFACTS_ROOT
    bundles = sorted(
        p.parent.relative_to(WIKI_ROOT).as_posix() for p in base.glob(f"*/PR-*/{pr_artifacts.PROVENANCE_NAME}")
    ) if base.is_dir() else []
    bundles += sorted(
        p.relative_to(WIKI_ROOT).as_posix() for p in (base.glob("*/PR-*") if base.is_dir() else [])
        if p.is_dir() and p.relative_to(WIKI_ROOT).as_posix() not in bundles
    )
    named = page_artifact_dirs()
    errors, uncached = [], 0
    for rel in bundles:
        found = pr_artifacts.bundle_errors(rel)
        errors.extend(found)
        if rel not in named:
            errors.append(f"{rel}: no source-pr page names this bundle in artifact_dir")
        if args.against_cache and not found:
            more, missing = cache_errors(rel, Path(rel).parent.name, args.cache_dir)
            errors.extend(more)
            uncached += missing
    for rel, page in named.items():
        if rel not in bundles:
            errors.append(f"{page}: artifact_dir '{rel}' does not exist")
    kernels_base = WIKI_ROOT / pr_artifacts.KERNELS_ROOT
    kernel_bundles = sorted(
        p.relative_to(WIKI_ROOT).as_posix() for p in kernels_base.iterdir() if p.is_dir()
    ) if kernels_base.is_dir() else []
    for rel in kernel_bundles:
        errors.extend(pr_artifacts.kernel_bundle_errors(rel))
    for line in errors:
        print(f"ERROR: {line}")
    note = f", {uncached} without cached evidence" if args.against_cache else ""
    kernels = f", {len(kernel_bundles)} kernel bundle(s)" if kernel_bundles else ""
    print(f"Verified {len(bundles)} artifact bundle(s){note}{kernels}: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
