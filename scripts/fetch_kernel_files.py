#!/usr/bin/env python3
"""Save complete upstream kernel source files as reference bundles.

A pull-request bundle (scripts/fetch_pr_diff.py) holds a patch. This script
holds whole files, pinned to one upstream commit, so a kernel can be read
from top to bottom. The bundles are listed by hand in
`artifacts/kernels/MANIFEST.yaml`:

    bundles:
      - id: <bundle-id>            # directory name under artifacts/kernels/
        ledger: <slug>             # candidates/<slug>.yaml: repo, forge, licence
        commit: <40-hex commit>
        files:
          - <path in the upstream repository>

Each bundle directory receives the files (flat, by base name) and a
`PROVENANCE.yaml` with the repository, commit, licence and a sha256 per file.
The licence text is the one already kept at `artifacts/prs/<slug>/LICENSE`.

Usage:
    fetch_kernel_files.py [--only bundle-id,bundle-id] [--force]
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pr_artifacts  # noqa: E402
import pr_evidence  # noqa: E402
from _yaml_compat import yaml  # noqa: E402
from _wiki_root import WIKI_ROOT  # noqa: E402


def fetch_file(ledger: dict, commit: str, path: str) -> bytes:
    if pr_evidence.forge_of(ledger) == "gitlab":
        project = urllib.parse.quote(ledger["repo"], safe="")
        url = (f"{ledger['gitlab_api'].rstrip('/')}/projects/{project}/repository/files/"
               f"{urllib.parse.quote(path, safe='')}/raw?ref={commit}")
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "vk-kernel-wiki"})
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except OSError as exc:
            raise pr_evidence.EvidenceError(f"GET {url}: {exc}") from exc
    payload = pr_evidence.gh_json(f"repos/{ledger['repo']}/contents/{path}?ref={commit}")
    if payload.get("encoding") != "base64" or not payload.get("content"):
        raise pr_evidence.EvidenceError(f"{ledger['repo']}:{path}@{commit}: no inline content returned")
    return base64.b64decode(payload["content"])


def write_bundle(bundle: dict, force: bool) -> str:
    bundle_id, slug, commit = bundle["id"], bundle["ledger"], str(bundle["commit"])
    ledger = pr_evidence.load_ledger(pr_evidence.CANDIDATES_DIR / f"{slug}.yaml")
    license_rel = f"{pr_artifacts.ARTIFACTS_ROOT}/{slug}/{pr_artifacts.LICENSE_NAME}"
    if not (WIKI_ROOT / license_rel).is_file():
        raise pr_evidence.EvidenceError(f"{bundle_id}: {license_rel} is missing; run fetch_pr_diff.py --repos {slug}")
    directory = WIKI_ROOT / pr_artifacts.KERNELS_ROOT / bundle_id
    if (directory / pr_artifacts.PROVENANCE_NAME).is_file() and not force:
        return "already present"
    names = [PurePosixPath(p).name for p in bundle["files"]]
    if len(set(names)) != len(names):
        raise pr_evidence.EvidenceError(f"{bundle_id}: two files share a base name")
    directory.mkdir(parents=True, exist_ok=True)
    entries = []
    for path, name in zip(bundle["files"], names):
        content = fetch_file(ledger, commit, path)
        (directory / name).write_bytes(content)
        entries.append({"path": path, "file": name, "sha256": hashlib.sha256(content).hexdigest()})
    forge = pr_evidence.forge_of(ledger)
    host = ledger["gitlab_api"].split("/api/")[0] if forge == "gitlab" else "https://github.com"
    provenance = {
        "repo": ledger["repo"],
        "url": f"{host}/{ledger['repo']}",
        "commit": commit,
        "license": ledger.get("license"),
        "license_file": license_rel,
        "retrieved_at": date.today().isoformat(),
        "extraction": "complete files, byte for byte, at the commit above",
        "files": entries,
    }
    (directory / pr_artifacts.PROVENANCE_NAME).write_text(pr_evidence.dump_yaml(provenance), encoding="utf-8")
    return f"{len(entries)} file(s) written"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--only", help="comma-separated bundle ids (default: every bundle in the manifest)")
    parser.add_argument("--force", action="store_true", help="rewrite bundles that already exist")
    args = parser.parse_args()
    manifest_path = WIKI_ROOT / pr_artifacts.KERNELS_ROOT / pr_artifacts.MANIFEST_NAME
    if not manifest_path.is_file():
        print(f"ERROR: {manifest_path.relative_to(WIKI_ROOT)} does not exist", file=sys.stderr)
        return 1
    bundles = (yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}).get("bundles") or []
    wanted = set(args.only.split(",")) if args.only else None
    status = 0
    for bundle in bundles:
        if wanted is not None and bundle.get("id") not in wanted:
            continue
        try:
            print(f"{bundle['id']}: {write_bundle(bundle, args.force)}")
        except (KeyError, OSError, pr_evidence.EvidenceError) as exc:
            print(f"ERROR: {bundle.get('id')}: {exc}", file=sys.stderr)
            status = 1
    return status


if __name__ == "__main__":
    raise SystemExit(main())
