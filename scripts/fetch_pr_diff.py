#!/usr/bin/env python3
"""Save the shader patches of included pull requests as artifact bundles.

For every `decision: include` row of `candidates/<slug>.yaml` whose pull
request changed shader source, writes `artifacts/prs/<slug>/PR-<number>/`
(`shaders.patch` and `PROVENANCE.yaml`; see scripts/pr_artifacts.py) and the
upstream licence text at `artifacts/prs/<slug>/LICENSE`. Only shader-source
files are saved; backend host source is not.

A ledger must name the upstream licence before anything is saved:

    license: <SPDX id>      # checked against what GitHub reports for the repo

Evidence comes from the cache written by refresh_candidate_ledger.py and is
fetched through `gh` when missing; --offline forbids fetching (the licence
text must then already be present). Run generate-pr-pages.py afterwards so
the pages pick up `artifact_dir`.

Usage:
    fetch_pr_diff.py [--repos slug,slug] [--force] [--offline]
"""

from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pr_artifacts  # noqa: E402
import pr_evidence  # noqa: E402
import pr_policy  # noqa: E402
from _yaml_compat import yaml  # noqa: E402
from _wiki_root import WIKI_ROOT  # noqa: E402


def ensure_license(ledger: dict, slug: str, offline: bool) -> str:
    spdx = ledger.get("license")
    if not isinstance(spdx, str) or not spdx.strip():
        raise pr_evidence.EvidenceError(f"candidates/{slug}.yaml: add 'license: <SPDX id>' before saving upstream code")
    target = WIKI_ROOT / pr_artifacts.ARTIFACTS_ROOT / slug / pr_artifacts.LICENSE_NAME
    if target.is_file():
        return spdx
    if offline:
        raise pr_evidence.EvidenceError(f"{target.relative_to(WIKI_ROOT)} is missing and --offline was given")
    payload = pr_evidence.gh_json(f"repos/{ledger['repo']}/license")
    reported = (payload.get("license") or {}).get("spdx_id")
    if reported != spdx:
        raise pr_evidence.EvidenceError(
            f"candidates/{slug}.yaml says license {spdx!r} but GitHub reports {reported!r} for {ledger['repo']}"
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(base64.b64decode(payload.get("content") or ""))
    return spdx


def skipped_numbers(repo: str) -> set:
    """Pull requests listed in data/pr-page-skipped.yaml for `repo`."""
    path = WIKI_ROOT / "data" / "pr-page-skipped.yaml"
    if not path.is_file():
        return set()
    rows = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("rows") or []
    return {int(r["pr"]) for r in rows if isinstance(r, dict) and r.get("repo") == repo}


def write_bundle(ledger: dict, slug: str, evidence: dict, spdx: str) -> bool:
    """Write one bundle. Returns False when the PR has no shader patch."""
    config = pr_policy.PathConfig.from_ledger(ledger)
    files = pr_policy.shader_files(evidence["files"], config)
    with_patch = [f for f in files if f.get("patch")]
    if not with_patch:
        return False
    pr = evidence["pr"]
    directory = WIKI_ROOT / pr_artifacts.bundle_rel(slug, pr["number"])
    directory.mkdir(parents=True, exist_ok=True)
    (directory / pr_artifacts.PATCH_NAME).write_text(pr_artifacts.render_patch(with_patch), encoding="utf-8")
    provenance = {
        "repo": ledger["repo"],
        "pr": int(pr["number"]),
        "url": pr.get("html_url"),
        "merge_sha": pr.get("merge_commit_sha"),
        "license": spdx,
        "license_file": f"{pr_artifacts.ARTIFACTS_ROOT}/{slug}/{pr_artifacts.LICENSE_NAME}",
        "retrieved_at": evidence.get("fetched_at"),
        "origin": f"GitHub REST API, repos/{ledger['repo']}/pulls/{int(pr['number'])}/files, field 'patch'",
        "extraction": "verbatim patch text per file; the diff/---/+++ header lines are generated",
        "files": [
            {
                "path": f["filename"],
                "status": f["status"],
                "sha256": pr_artifacts.sha256_text(f["patch"]) if f.get("patch") else None,
            }
            for f in files
        ],
    }
    (directory / pr_artifacts.PROVENANCE_NAME).write_text(pr_evidence.dump_yaml(provenance), encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--repos", help="comma-separated ledger slugs (default: every ledger)")
    parser.add_argument("--force", action="store_true", help="rewrite bundles that already exist")
    parser.add_argument("--offline", action="store_true", help="use cached evidence only")
    parser.add_argument("--cache-dir", help="evidence cache directory (default: <root>/.cache/pr-evidence)")
    args = parser.parse_args()

    paths = pr_evidence.ledger_paths(args.repos.split(",") if args.repos else None)
    if not paths:
        print(f"ERROR: no ledger under {pr_evidence.CANDIDATES_DIR.relative_to(WIKI_ROOT)}/", file=sys.stderr)
        return 1
    status = 0
    for path in paths:
        slug = path.stem
        try:
            ledger = pr_evidence.load_ledger(path)
            spdx = ensure_license(ledger, slug, args.offline)
        except (OSError, pr_evidence.EvidenceError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            status = 1
            continue
        written = kept = without = failed = 0
        pageless = skipped_numbers(ledger["repo"])
        for row in ledger["prs"]:
            if not isinstance(row, dict) or str(row.get("decision")) != "include":
                continue
            number = int(row["number"])
            if number in pageless:
                continue  # generate-pr-pages.py could not write a page for it
            directory = WIKI_ROOT / pr_artifacts.bundle_rel(slug, number)
            if (directory / pr_artifacts.PROVENANCE_NAME).is_file() and not args.force:
                kept += 1
                continue
            try:
                evidence = pr_evidence.get(ledger["repo"], slug, number, args.cache_dir, args.offline)
            except pr_evidence.EvidenceError as exc:
                print(f"WARN: {exc}", file=sys.stderr)
                failed += 1
                continue
            if write_bundle(ledger, slug, evidence, spdx):
                written += 1
            else:
                without += 1
        print(f"{slug}: {written} bundle(s) written, {kept} already present, "
              f"{without} included row(s) without a shader patch, {failed} failed")
        status = status or (1 if failed else 0)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
