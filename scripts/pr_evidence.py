"""Fetch and cache pull-request evidence, and read candidate ledgers.

Shared by scripts/refresh_candidate_ledger.py and scripts/generate-pr-pages.py.

Evidence for one pull request is its record plus its complete changed-file
list (with patches where the forge returns them), in one shape for every
forge. A ledger selects the forge:

    forge: github            # default; fetched with the authenticated `gh` CLI
    forge: gitlab            # merge requests, fetched over the public REST API
    gitlab_api: https://<host>/api/v4

For GitLab a merge request is stored under the same keys as a GitHub pull
request (`number` is the merge-request iid). Projects that merge by
fast-forward have no merge commit; `merge_commit_sha` then holds the head
commit of the merge request, which is the commit that landed on the target
branch. Evidence is cached as JSON under
`<wiki-root>/.cache/pr-evidence/<slug>/<number>.json`. The cache is ignored
by git: it holds upstream content that this repository does not redistribute.
"""

from __future__ import annotations

import json
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
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
SEARCH_RESULT_CAP = 1000  # GitHub returns at most 1000 results per search query
SEARCH_PAUSE_SECONDS = 2.5  # the GitHub search API allows 30 requests per minute


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


def http_json(url: str, timeout: int = 60, attempts: int = 4):
    """GET a JSON document, retrying transient failures."""
    last = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "vk-kernel-wiki"})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504):
                raise EvidenceError(f"GET {url}: HTTP {exc.code}") from exc
            last = exc
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            last = exc
        time.sleep(2 * (attempt + 1))
    raise EvidenceError(f"GET {url}: {last}")


def forge_of(ledger: dict) -> str:
    forge = str(ledger.get("forge") or "github")
    if forge not in ("github", "gitlab"):
        raise EvidenceError(f"unknown forge {forge!r} (expected github or gitlab)")
    if forge == "gitlab" and not str(ledger.get("gitlab_api") or "").startswith("https://"):
        raise EvidenceError("a gitlab ledger needs 'gitlab_api: https://<host>/api/v4'")
    return forge


def request_noun(ledger: dict) -> str:
    return "merge request" if forge_of(ledger) == "gitlab" else "pull request"


def _gitlab_project(ledger: dict) -> str:
    return f"{ledger['gitlab_api'].rstrip('/')}/projects/{urllib.parse.quote(ledger['repo'], safe='')}"


def _gitlab_pages(url: str) -> list:
    out, page = [], 1
    while True:
        chunk = http_json(f"{url}{'&' if '?' in url else '?'}per_page=100&page={page}")
        if not isinstance(chunk, list):
            raise EvidenceError(f"GET {url}: unexpected payload")
        out.extend(chunk)
        if len(chunk) < 100:
            return out
        page += 1


def normalize_gitlab(repo: str, mr: dict, diffs: list, fetched_at: str) -> dict:
    """Put a GitLab merge request and its diffs into the evidence shape."""
    def status(item):
        for flag, name in (("new_file", "added"), ("deleted_file", "removed"), ("renamed_file", "renamed")):
            if item.get(flag):
                return name
        return "modified"

    def patch(item):
        text = item.get("diff") or ""
        if text.endswith("\n"):
            text = text[:-1]  # the evidence shape carries no final newline
        return text or None

    merged = mr.get("state") == "merged"
    return {
        "repo": repo,
        "fetched_at": fetched_at,
        "pr": {
            "number": mr.get("iid"),
            "title": mr.get("title"),
            "body": mr.get("description"),
            "html_url": mr.get("web_url"),
            "state": mr.get("state"),
            "merged": merged,
            "merged_at": mr.get("merged_at"),
            "created_at": mr.get("created_at"),
            "closed_at": mr.get("closed_at") or mr.get("merged_at"),
            "merge_commit_sha": mr.get("merge_commit_sha") or mr.get("squash_commit_sha") or mr.get("sha"),
            "changed_files": len(diffs),
            "author": (mr.get("author") or {}).get("username"),
        },
        "files": [
            {"filename": d.get("new_path") or d.get("old_path"), "status": status(d), "patch": patch(d)}
            for d in diffs if isinstance(d, dict)
        ],
    }


def fetch_gitlab(ledger: dict, number: int) -> dict:
    base = f"{_gitlab_project(ledger)}/merge_requests/{int(number)}"
    mr = http_json(base)
    if not isinstance(mr, dict) or mr.get("iid") is None:
        raise EvidenceError(f"{ledger['repo']}!{number}: unexpected merge-request payload")
    return normalize_gitlab(ledger["repo"], mr, _gitlab_pages(f"{base}/diffs"), date.today().isoformat())


def search_merged(ledger: dict, keyword: str, cutoff: date) -> list:
    """Numbers of merged pull requests whose title matches `keyword`."""
    if forge_of(ledger) == "gitlab":
        url = (f"{_gitlab_project(ledger)}/merge_requests?state=merged&in=title&order_by=created_at&sort=asc"
               f"&search={urllib.parse.quote(keyword)}")
        return sorted(
            int(mr["iid"]) for mr in _gitlab_pages(url)
            if (mr.get("merged_at") or "")[:10] and (mr.get("merged_at") or "")[:10] <= cutoff.isoformat()
        )
    query = f"repo:{ledger['repo']} is:pr is:merged merged:<={cutoff.isoformat()} {keyword}"
    numbers, page = [], 1
    while True:
        payload = gh_json(
            "-X", "GET", "search/issues", "-f", f"q={query}",
            "-f", "per_page=100", "-f", f"page={page}", "-f", "sort=created", "-f", "order=asc",
        )
        items = payload.get("items") or []
        total = int(payload.get("total_count") or 0)
        numbers.extend(int(i["number"]) for i in items)
        time.sleep(SEARCH_PAUSE_SECONDS)
        if not items or len(numbers) >= min(total, SEARCH_RESULT_CAP):
            if total > SEARCH_RESULT_CAP:
                raise EvidenceError(
                    f"{ledger['repo']} query {keyword!r} has {total} results; only the first "
                    f"{SEARCH_RESULT_CAP} are reachable. Split the query."
                )
            return sorted(numbers)
        page += 1


def fetch_license_text(ledger: dict) -> bytes:
    """The upstream licence text.

    With `license_path` in the ledger that file is read from the default
    branch as the ledger owner's statement of the licence. Without it
    (GitHub only) the licence GitHub detects is used and must equal the
    ledger's `license`.
    """
    path = ledger.get("license_path")
    if forge_of(ledger) == "gitlab":
        if not path:
            raise EvidenceError("a gitlab ledger needs 'license_path: <file in the repository>'")
        project = http_json(_gitlab_project(ledger))
        url = (f"{_gitlab_project(ledger)}/repository/files/{urllib.parse.quote(path, safe='')}/raw"
               f"?ref={urllib.parse.quote(project.get('default_branch') or 'main')}")
        request = urllib.request.Request(url, headers={"User-Agent": "vk-kernel-wiki"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except (urllib.error.URLError, OSError) as exc:
            raise EvidenceError(f"GET {url}: {exc}") from exc
    import base64
    if path:
        return base64.b64decode(gh_json(f"repos/{ledger['repo']}/contents/{path}").get("content") or "")
    payload = gh_json(f"repos/{ledger['repo']}/license")
    reported = (payload.get("license") or {}).get("spdx_id")
    if reported != ledger.get("license"):
        raise EvidenceError(
            f"ledger says license {ledger.get('license')!r} but GitHub reports {reported!r} for "
            f"{ledger['repo']}; set 'license_path' to the licence file to state it yourself"
        )
    return base64.b64decode(payload.get("content") or "")


def fetch_github(repo: str, number: int) -> dict:
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


def get(ledger: dict, slug: str, number: int, cache_dir: Optional[Path] = None,
        offline: bool = False) -> dict:
    """Return cached evidence, fetching and caching it when allowed."""
    repo = ledger["repo"]
    cached = load_cached(slug, number, cache_dir)
    if cached is not None:
        return cached
    if offline:
        raise EvidenceError(f"{repo}#{number}: no cached evidence and --offline was given")
    evidence = fetch_gitlab(ledger, number) if forge_of(ledger) == "gitlab" else fetch_github(repo, number)
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
