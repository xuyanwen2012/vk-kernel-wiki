#!/usr/bin/env python3
"""Record which included merge requests a given upstream release contains.

For every `decision: include` row of a GitLab ledger, asks the forge which
tags contain the merge request's landed commit (the `merge_sha` of its page)
and writes the answer for one release tag to `data/release-membership.yaml`.

The check is by commit id. A change that reached the release through a
cherry-pick has a different commit id there and is reported as not
contained, so `not_contained` means "not contained under this commit id".

Usage:
    check_release_membership.py --repos <slug> --tag <tag> [--jobs N]
"""

from __future__ import annotations

import argparse
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pr_evidence  # noqa: E402
from _yaml_compat import yaml  # noqa: E402
from _wiki_root import WIKI_ROOT  # noqa: E402

OUTPUT = WIKI_ROOT / "data" / "release-membership.yaml"
HEADER = (
    "## Which included merge requests a release tag contains, by commit id.\n"
    "## Written by scripts/check_release_membership.py. A change that entered the\n"
    "## release by cherry-pick has another commit id and is listed as not contained.\n"
)


def tags_containing(ledger: dict, sha: str) -> set:
    project = urllib.parse.quote(ledger["repo"], safe="")
    url = f"{ledger['gitlab_api'].rstrip('/')}/projects/{project}/repository/commits/{sha}/refs?type=tag"
    return {str(ref.get("name")) for ref in pr_evidence._gitlab_pages(url)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--repos", required=True, help="one ledger slug")
    parser.add_argument("--tag", required=True, help="release tag to test, as the forge names it")
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--cache-dir")
    args = parser.parse_args()

    slug = args.repos
    try:
        ledger = pr_evidence.load_ledger(pr_evidence.CANDIDATES_DIR / f"{slug}.yaml")
        if pr_evidence.forge_of(ledger) != "gitlab":
            raise pr_evidence.EvidenceError("release membership is implemented for gitlab ledgers only")
    except (OSError, pr_evidence.EvidenceError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    numbers = [int(r["number"]) for r in ledger["prs"] if isinstance(r, dict) and r.get("decision") == "include"]

    def check(number):
        try:
            sha = pr_evidence.get(ledger, slug, number, args.cache_dir)["pr"]["merge_commit_sha"]
            return number, args.tag in tags_containing(ledger, sha)
        except pr_evidence.EvidenceError as exc:
            print(f"WARN: {slug} {number}: {exc}", file=sys.stderr)
            return number, None

    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        results = dict(pool.map(check, numbers))
    record = {
        "ledger": slug,
        "repo": ledger["repo"],
        "tag": args.tag,
        "checked_at": date.today().isoformat(),
        "method": "tags containing the landed commit of each merge request (GitLab commits/<sha>/refs?type=tag)",
        "contained": [f"pr-{slug}-{n}" for n in sorted(results) if results[n] is True],
        "not_contained": [f"pr-{slug}-{n}" for n in sorted(results) if results[n] is False],
        "unknown": [f"pr-{slug}-{n}" for n in sorted(results) if results[n] is None],
    }
    data = (yaml.safe_load(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.is_file() else None) or {}
    checks = [c for c in data.get("checks") or [] if (c.get("ledger"), c.get("tag")) != (slug, args.tag)]
    checks.append(record)
    checks.sort(key=lambda c: (c["ledger"], c["tag"]))
    OUTPUT.write_text(HEADER + pr_evidence.dump_yaml({"checks": checks}), encoding="utf-8")
    print(f"{slug} @ {args.tag}: {len(record['contained'])} contained, "
          f"{len(record['not_contained'])} not contained, {len(record['unknown'])} unknown")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
