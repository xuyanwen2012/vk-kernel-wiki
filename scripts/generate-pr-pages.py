#!/usr/bin/env python3
"""Generate source-pr pages from candidate ledgers.

For every `decision: include` row of `candidates/<slug>.yaml`, writes
`sources/prs/<slug>/PR-<number>.md`: frontmatter derived by
scripts/pr_policy.py and a body holding a verbatim excerpt of the upstream
pull-request description with its locator. Nothing in the page is
model-written.

When the description is empty the excerpt is the pull-request title, and
the locator says so. A row that cannot become a valid page (no merge commit,
evidence unavailable) is recorded in data/pr-page-skipped.yaml
instead. An existing page is left alone unless --force is given.

Evidence is read from the cache written by refresh_candidate_ledger.py and
fetched through `gh` when missing; --offline forbids fetching.

Usage:
    generate-pr-pages.py [--repos slug,slug] [--max N] [--force] [--offline]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pr_artifacts  # noqa: E402
import pr_evidence  # noqa: E402
import pr_policy  # noqa: E402
from _yaml_compat import yaml  # noqa: E402
from _wiki_root import WIKI_ROOT  # noqa: E402

SKIPPED_PATH = WIKI_ROOT / "data" / "pr-page-skipped.yaml"
SKIPPED_HEADER = (
    "## Ledger rows with `decision: include` that have no source-pr page, and why.\n"
    "## Written by scripts/generate-pr-pages.py; rows sorted by (repo, pr).\n"
)
MAX_CHANGED_PATHS = 40


class Skip(Exception):
    pass


def build_page(repo: str, slug: str, row: dict, evidence: dict, vocab: dict, ledger: dict) -> str:
    pr, files = evidence["pr"], evidence["files"]
    number = int(pr["number"])
    title = str(pr.get("title") or "").strip()
    status = "merged" if pr.get("merged") or pr.get("merged_at") else str(pr.get("state") or "closed").lower()
    merge_sha = pr.get("merge_commit_sha")
    if status == "merged" and not merge_sha:
        raise Skip("merged pull request has no merge commit sha")
    if not title or not pr.get("author") or not pr.get("html_url"):
        raise Skip("pull request record lacks a title, author or url")

    excerpt, total_chars = pr_policy.upstream_excerpt(pr.get("body") or "")
    excerpt_of = "description"
    if pr_policy.excerpt_is_empty(excerpt):
        # Nothing to quote from the description: quote the title instead.
        excerpt, total_chars = pr_policy.upstream_excerpt(title)
        excerpt_of = "title"
        if pr_policy.excerpt_is_empty(excerpt):
            raise Skip("upstream description and title have no text to excerpt")

    metadata = pr_policy.derive_metadata(title, files, vocab, pr_policy.PathConfig.from_ledger(ledger))
    architectures, architecture_evidence = pr_policy.derive_architectures(
        title, files, ledger.get("architecture_code_markers") or {}
    )

    paths = [f["filename"] for f in pr_policy.normalize_files(files)]
    evidence_paths = [p for p in row.get("evidence_paths") or [] if p in paths]
    shown = list(dict.fromkeys([*evidence_paths, *paths]))[:max(MAX_CHANGED_PATHS, len(evidence_paths))]

    frontmatter = {
        "id": f"pr-{slug}-{number}",
        "repo": repo,
        "pr": number,
        "title": title,
        "author": str(pr["author"]),
        "date": str(pr.get("created_at") or "")[:10],
        "url": str(pr["html_url"]),
        "source_category": "upstream-code",
        "architectures": architectures,
        **({"architecture_evidence": architecture_evidence} if architecture_evidence else {}),
        "tags": metadata["tags"],
        "techniques": metadata["techniques"],
        "hardware_features": metadata["hardware_features"],
        "kernel_types": metadata["kernel_types"],
        "languages": metadata["languages"],
        "captured_at": str(evidence.get("fetched_at") or ""),
        "status": status,
    }
    if status == "merged":
        frontmatter["merge_sha"] = str(merge_sha)
    frontmatter["changed_paths"] = shown
    artifact_rel = pr_artifacts.bundle_rel(slug, number)
    if (WIKI_ROOT / artifact_rel / pr_artifacts.PROVENANCE_NAME).is_file():
        frontmatter["artifact_dir"] = artifact_rel
    frontmatter["inclusion_reason"] = (
        str(row.get("reason") or "") if len(shown) == len(paths)
        else f"{row.get('reason') or ''} ({len(paths)} changed files; {len(shown)} listed)"
    )
    return (
        "---\n" + pr_evidence.dump_yaml(frontmatter) + "---\n\n"
        + pr_policy.render_body(title, frontmatter["url"], excerpt, total_chars, excerpt_of)
    )


def load_skipped() -> dict:
    if not SKIPPED_PATH.is_file():
        return {}
    data = yaml.safe_load(SKIPPED_PATH.read_text(encoding="utf-8")) or {}
    return {(r["repo"], int(r["pr"])): r for r in data.get("rows") or []}


def write_skipped(skipped: dict) -> None:
    rows = [skipped[key] for key in sorted(skipped)]
    SKIPPED_PATH.write_text(SKIPPED_HEADER + pr_evidence.dump_yaml({"rows": rows}), encoding="utf-8")


def process(path: Path, vocab: dict, skipped: dict, args) -> tuple:
    slug = path.stem
    ledger = pr_evidence.load_ledger(path)
    repo = ledger["repo"]
    outdir = WIKI_ROOT / "sources" / "prs" / slug
    written = kept = 0
    for row in ledger["prs"]:
        if not isinstance(row, dict) or str(row.get("decision")) != "include":
            skipped.pop((repo, int(row.get("number", 0))), None) if isinstance(row, dict) else None
            continue
        number = int(row["number"])
        target = outdir / f"PR-{number}.md"
        if target.is_file() and not args.force:
            kept += 1
            continue
        if args.max is not None and written >= args.max:
            break
        try:
            evidence = pr_evidence.get(repo, slug, number, args.cache_dir, args.offline)
            content = build_page(repo, slug, row, evidence, vocab, ledger)
        except (Skip, pr_evidence.EvidenceError) as exc:
            skipped[(repo, number)] = {"repo": repo, "pr": number, "id": f"pr-{slug}-{number}", "reason": str(exc)}
            if target.is_file():
                target.unlink()
            # A bundle without a page would be unreachable; drop it.
            shutil.rmtree(WIKI_ROOT / pr_artifacts.bundle_rel(slug, number), ignore_errors=True)
            continue
        skipped.pop((repo, number), None)
        outdir.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written += 1
    return written, kept


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--repos", help="comma-separated ledger slugs (default: every ledger)")
    parser.add_argument("--max", type=int, help="stop after writing this many pages per ledger")
    parser.add_argument("--force", action="store_true", help="rewrite pages that already exist")
    parser.add_argument("--offline", action="store_true", help="use cached evidence only")
    parser.add_argument("--cache-dir", help="evidence cache directory (default: <root>/.cache/pr-evidence)")
    args = parser.parse_args()

    paths = pr_evidence.ledger_paths(args.repos.split(",") if args.repos else None)
    if not paths:
        print(f"ERROR: no ledger under {pr_evidence.CANDIDATES_DIR.relative_to(WIKI_ROOT)}/", file=sys.stderr)
        return 1
    vocab = yaml.safe_load((WIKI_ROOT / "data" / "tags.yaml").read_text(encoding="utf-8")) or {}
    skipped = load_skipped()
    before = dict(skipped)
    status = 0
    for path in paths:
        try:
            written, kept = process(path, vocab, skipped, args)
        except (OSError, pr_evidence.EvidenceError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            status = 1
            continue
        here = sum(1 for (repo, _), _row in skipped.items() if repo == pr_evidence.load_ledger(path)["repo"])
        print(f"{path.stem}: {written} page(s) written, {kept} already present, {here} skipped")
    if skipped != before or (skipped and not SKIPPED_PATH.is_file()):
        write_skipped(skipped)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
