"""Fetch and cache pull-request evidence, and read candidate ledgers.

Shared by scripts/refresh_candidate_ledger.py and scripts/generate-pr-pages.py.

Evidence for one pull request is the GitHub pull-request record plus its
complete changed-file list (with patches where GitHub returns them). It is
fetched with the authenticated `gh` CLI and cached as JSON under
`<wiki-root>/.cache/pr-evidence/<slug>/<number>.json`. The cache is ignored
by git: it holds upstream content that this repository does not redistribute.
"""

from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path
from typing import Optional

from _yaml_compat import yaml
from _wiki_root import WIKI_ROOT

CANDIDATES_DIR = WIKI_ROOT / "candidates"
CACHE_DIR = WIKI_ROOT / ".cache" / "pr-evidence"
PR_FIELDS = (
    "number", "title", "body", "html_url", "state", "merged", "merged_at",
    "created_at", "closed_at", "merge_commit_sha", "changed_files",
)
MAX_FILE_PAGES = 30  # GitHub lists at most 3000 changed files per pull request


class EvidenceError(RuntimeError):
    pass


def gh_json(*args: str, timeout: int = 60):
    """Run `gh api ...` and return the parsed JSON, or raise EvidenceError."""
    try:
        proc = subprocess.run(["gh", "api", *args], capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise EvidenceError(f"gh api {' '.join(args)}: {exc}") from exc
    if proc.returncode != 0:
        raise EvidenceError(f"gh api {' '.join(args)}: {proc.stderr.strip() or proc.returncode}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise EvidenceError(f"gh api {' '.join(args)}: invalid JSON") from exc


def cache_path(slug: str, number: int, cache_dir: Optional[Path] = None) -> Path:
    return Path(cache_dir or CACHE_DIR) / slug / f"{int(number)}.json"


def load_cached(slug: str, number: int, cache_dir: Optional[Path] = None) -> Optional[dict]:
    path = cache_path(slug, number, cache_dir)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) and "pr" in data and "files" in data else None


def fetch(repo: str, number: int) -> dict:
    """Fetch one pull request and its complete changed-file list."""
    pr = gh_json(f"repos/{repo}/pulls/{int(number)}")
    files = []
    for page in range(1, MAX_FILE_PAGES + 1):
        chunk = gh_json(f"repos/{repo}/pulls/{int(number)}/files?per_page=100&page={page}")
        if not isinstance(chunk, list):
            raise EvidenceError(f"{repo}#{number}: unexpected changed-file payload")
        files.extend(chunk)
        if len(chunk) < 100:
            break
    record = {field: pr.get(field) for field in PR_FIELDS}
    record["author"] = (pr.get("user") or {}).get("login")
    return {
        "repo": repo,
        "fetched_at": date.today().isoformat(),
        "pr": record,
        "files": [
            {"filename": f.get("filename"), "status": f.get("status"), "patch": f.get("patch")}
            for f in files if isinstance(f, dict)
        ],
    }


def get(repo: str, slug: str, number: int, cache_dir: Optional[Path] = None,
        offline: bool = False) -> dict:
    """Return cached evidence, fetching and caching it when allowed."""
    cached = load_cached(slug, number, cache_dir)
    if cached is not None:
        return cached
    if offline:
        raise EvidenceError(f"{repo}#{number}: no cached evidence and --offline was given")
    evidence = fetch(repo, number)
    path = cache_path(slug, number, cache_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return evidence


# ---------------------------------------------------------------------------
# Ledgers
# ---------------------------------------------------------------------------

def ledger_paths(slugs: Optional[list] = None) -> list:
    if slugs:
        return [CANDIDATES_DIR / f"{slug}.yaml" for slug in slugs]
    return sorted(CANDIDATES_DIR.glob("*.yaml")) if CANDIDATES_DIR.is_dir() else []


def load_ledger(path: Path) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("repo"), str) or "/" not in data["repo"]:
        raise EvidenceError(f"{path}: a ledger needs a top-level 'repo: <owner>/<name>'")
    data.setdefault("prs", [])
    if not isinstance(data["prs"], list):
        raise EvidenceError(f"{path}: 'prs' must be a list")
    return data


def dump_yaml(data) -> str:
    return yaml.safe_dump(data, sort_keys=False, default_flow_style=False, width=200, allow_unicode=True)
