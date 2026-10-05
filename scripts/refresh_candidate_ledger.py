#!/usr/bin/env python3
"""Refresh candidate ledgers from upstream pull requests.

For each ledger `candidates/<slug>.yaml`, runs every query in its
`keywords_used` list against merged pull requests of its `repo`, fetches the
changed files of each new hit, and appends one row per pull request with an
include / defer / exclude decision from scripts/pr_policy.py.

Existing rows are never changed, so a decision edited by hand survives a
refresh. Pass --reclassify to recompute every row that does not carry
`decision_source: manual`.

A ledger starts as a header written by hand:

    repo: <owner>/<name>
    keywords_used:            # GitHub search terms; qualifiers are allowed
      - "<term> in:title"
    shader_path_markers:      # a shader path must contain one of these
      - <substring>
    embedded_shader_path_markers:   # optional: non-GLSL files holding GLSL text
      - <substring>
    host_path_markers:        # backend host source; these PRs are deferred
      - <substring>
    prs: []

This script calls the GitHub API through the `gh` CLI. It is a refresh-time
utility: scripts/validate.py and the test suite stay offline.

Usage:
    refresh_candidate_ledger.py --cutoff YYYY-MM-DD [--repos slug,slug]
                                [--reclassify] [--dry-run] [--jobs N]
"""

from __future__ import annotations

import argparse
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pr_evidence  # noqa: E402
import pr_policy  # noqa: E402
from _wiki_root import WIKI_ROOT  # noqa: E402

SEARCH_RESULT_CAP = 1000  # GitHub returns at most 1000 results per search query
SEARCH_PAUSE_SECONDS = 2.5  # the search API allows 30 requests per minute


def search_merged_prs(repo: str, keyword: str, cutoff: date) -> list:
    """Return [{number, title, closed}] for merged PRs matching one query."""
    query = f"repo:{repo} is:pr is:merged merged:<={cutoff.isoformat()} {keyword}"
    hits, page = [], 1
    while True:
        payload = pr_evidence.gh_json(
            "-X", "GET", "search/issues", "-f", f"q={query}",
            "-f", "per_page=100", "-f", f"page={page}", "-f", "sort=created", "-f", "order=asc",
        )
        items = payload.get("items") or []
        total = int(payload.get("total_count") or 0)
        hits.extend(
            {"number": int(i["number"]), "title": i.get("title") or "", "closed": (i.get("closed_at") or "")[:10]}
            for i in items
        )
        time.sleep(SEARCH_PAUSE_SECONDS)
        if not items or len(hits) >= min(total, SEARCH_RESULT_CAP):
            if total > SEARCH_RESULT_CAP:
                print(
                    f"WARN: {repo} query {keyword!r} has {total} results; only the first "
                    f"{SEARCH_RESULT_CAP} are reachable. Split the query.", file=sys.stderr,
                )
            return hits
        page += 1


def build_row(ledger: dict, slug: str, number: int, cache_dir=None, offline=False) -> dict:
    """Fetch evidence for one pull request and classify it."""
    try:
        evidence = pr_evidence.get(ledger["repo"], slug, number, cache_dir, offline)
    except pr_evidence.EvidenceError as exc:
        return {
            "number": number, "decision": "defer", "rule": "evidence-unavailable",
            "reason": f"defer: pull request evidence unavailable ({exc})",
        }
    pr = evidence["pr"]
    scope = pr_policy.classify_scope(evidence["files"], pr_policy.PathConfig.from_ledger(ledger))
    return {
        "number": number,
        "title": pr.get("title") or "",
        "author": pr.get("author") or "",
        "merged_at": (pr.get("merged_at") or "")[:10],
        "url": pr.get("html_url") or "",
        "decision": scope.decision,
        "rule": scope.rule,
        "reason": scope.reason,
        "evidence_paths": list(scope.evidence_paths),
    }


def refresh(path: Path, cutoff: date, reclassify: bool, dry_run: bool, jobs: int,
            cache_dir=None, offline=False) -> Counter:
    slug = path.stem
    ledger = pr_evidence.load_ledger(path)
    rows = {int(r["number"]): r for r in ledger["prs"] if isinstance(r, dict) and "number" in r}

    seen = set()
    if not offline:
        for keyword in ledger.get("keywords_used") or []:
            hits = search_merged_prs(ledger["repo"], str(keyword), cutoff)
            print(f"  {slug}: {len(hits)} merged pull request(s) for {keyword!r}")
            seen.update(h["number"] for h in hits)

    todo = sorted(n for n in seen if n not in rows)
    if reclassify:
        todo = sorted(set(todo) | {n for n, r in rows.items() if r.get("decision_source") != "manual"})
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        for row in pool.map(lambda n: build_row(ledger, slug, n, cache_dir, offline), todo):
            rows[row["number"]] = row

    ledger["prs"] = [rows[n] for n in sorted(rows)]
    counts = Counter(str(r.get("decision")) for r in ledger["prs"])
    ledger["searched_at"] = date.today().isoformat()
    ledger["cutoff_date"] = cutoff.isoformat()
    ledger["total_candidates"] = len(ledger["prs"])
    for key, decision in (("included", "include"), ("deferred", "defer"), ("excluded", "exclude")):
        ledger[key] = counts[decision]
    ledger["prs"] = ledger.pop("prs")  # keep the rows last in the file

    print(
        f"  {slug}: {len(todo)} row(s) classified; ledger now has {len(rows)} "
        f"({counts['include']} include, {counts['defer']} defer, {counts['exclude']} exclude)"
    )
    if not dry_run:
        path.write_text(pr_evidence.dump_yaml(ledger), encoding="utf-8")
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--cutoff", required=True, help="only pull requests merged on or before this date")
    parser.add_argument("--repos", help="comma-separated ledger slugs (default: every ledger)")
    parser.add_argument("--reclassify", action="store_true", help="recompute rows not marked manual")
    parser.add_argument("--dry-run", action="store_true", help="do not write the ledger")
    parser.add_argument("--offline", action="store_true", help="no search; classify from cached evidence only")
    parser.add_argument("--cache-dir", help="evidence cache directory (default: <root>/.cache/pr-evidence)")
    parser.add_argument("--jobs", type=int, default=6, help="parallel evidence fetches")
    args = parser.parse_args()

    try:
        cutoff = date.fromisoformat(args.cutoff)
    except ValueError:
        parser.error(f"--cutoff must be YYYY-MM-DD, got {args.cutoff!r}")
    paths = pr_evidence.ledger_paths(args.repos.split(",") if args.repos else None)
    if not paths:
        print(f"ERROR: no ledger under {pr_evidence.CANDIDATES_DIR.relative_to(WIKI_ROOT)}/", file=sys.stderr)
        return 1
    status = 0
    for path in paths:
        try:
            refresh(path, cutoff, args.reclassify, args.dry_run, args.jobs, args.cache_dir, args.offline)
        except (OSError, pr_evidence.EvidenceError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            status = 1
    return status


if __name__ == "__main__":
    raise SystemExit(main())
