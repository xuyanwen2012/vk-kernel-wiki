#!/usr/bin/env python3
"""Check external-repository raw_data locators against a local git checkout.

Usage:
    python3 -S scripts/check_external_locators.py --checkout <path> [--repo <url>]

A source-measurement raw_data entry that carries 'repo' and 'commit' points at
a file in another git repository. scripts/validate.py checks only the form of
such an entry. This script checks that the file really exists at that commit:
for every such entry it runs

    git -C <path> cat-file -e <commit>:<locator-without-fragment>

against a local checkout of the external repository. No network is used.

--checkout  a local git checkout (or bare repository) of the external repository
--repo      check only entries whose 'repo' is this URL (a trailing '/' or
            '.git' is ignored). Without it, every external entry is checked
            against the checkout.

Output: one "FAIL: ..." line per failing entry, then a one-line summary.
Exit code 0 when every checked entry resolves, 1 when at least one does not,
2 when the check could not be made (the checkout is not a git repository, git
is missing, or the checkout does not contain a cited commit).

The wiki root is resolved by scripts/_wiki_root.py, so VK_KERNEL_WIKI_ROOT can
point the script at another root.
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _wiki_root import WIKI_ROOT  # noqa: E402
import validate  # noqa: E402  (shares the page parser and the locator rules)


def fatal(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(2)


def normalize_repo(url):
    url = url.strip().rstrip("/")
    return url[:-4] if url.endswith(".git") else url


def git(checkout, *args):
    try:
        return subprocess.run(
            ["git", "-C", str(checkout), *args], capture_output=True, text=True, timeout=120,
        )
    except FileNotFoundError:
        fatal("git was not found on PATH")
    except subprocess.TimeoutExpired:
        fatal(f"git {' '.join(args)} timed out in {checkout}")


def external_entries(spec):
    """Yield (page rel path, entry label, entry) for every raw_data entry in
    the external-repository form, in page order."""
    fields = spec.get("together_fields") or []
    sources = WIKI_ROOT / "sources"
    if not sources.is_dir():
        return
    for path in sorted(p for p in sources.rglob("*.md") if p.is_file()):
        fm, _body = validate.split_page(path)
        if not isinstance(fm, dict) or not isinstance(fm.get("raw_data"), list):
            continue
        for i, entry in enumerate(fm["raw_data"]):
            if isinstance(entry, dict) and any(f in entry for f in fields):
                yield validate.rel_path(path), f"raw_data[{i}]", entry


def main():
    parser = argparse.ArgumentParser(
        description="Check external-repository raw_data locators against a local git checkout."
    )
    parser.add_argument("--checkout", required=True, help="local checkout of the external repository")
    parser.add_argument("--repo", help="check only entries whose 'repo' is this URL")
    args = parser.parse_args()

    checkout = Path(args.checkout).expanduser()
    if not checkout.is_dir():
        fatal(f"--checkout {args.checkout!r} is not a directory")
    if git(checkout, "rev-parse", "--git-dir").returncode != 0:
        fatal(f"--checkout {args.checkout!r} is not a git repository")
    wanted = normalize_repo(args.repo) if args.repo else None
    if args.repo and not wanted:
        fatal("--repo must not be empty")

    schemas = validate.load_yaml_file(WIKI_ROOT / "data" / "schemas.yaml") or {}
    raw_schema = (schemas.get("source-measurement") or {}).get("raw_data_schema") or {}
    spec = (raw_schema.get("constraints") or {}).get("external_locator") or {}
    if not spec.get("together_fields"):
        fatal("data/schemas.yaml defines no external_locator rule for raw_data entries")

    failures, todo, skipped = [], [], 0
    for rel, label, entry in external_entries(spec):
        repo = entry.get("repo")
        if wanted is not None and not (isinstance(repo, str) and normalize_repo(repo) == wanted):
            skipped += 1
            continue
        _is_external, problems = validate.external_entry_errors(entry, label, spec)
        locator = entry.get("locator")
        if not validate.non_empty_string(locator):
            problems.append(f"{label}.locator must be a non-empty string")
        else:
            problem = validate.external_locator_error(locator)
            if problem:
                problems.append(f"{label}.locator '{locator}' {problem}")
        if problems:
            failures.append(f"{rel}: {label}: malformed entry: {'; '.join(problems)}")
            continue
        todo.append((rel, label, entry["commit"], locator.split("#", 1)[0].strip(), repo))

    # The checkout must contain every cited commit before any file is looked up.
    missing = sorted(
        commit for commit in {item[2] for item in todo}
        if git(checkout, "cat-file", "-e", f"{commit}^{{commit}}").returncode != 0
    )
    if missing:
        fatal(
            f"checkout {args.checkout!r} does not contain commit(s) {', '.join(missing)}; "
            "fetch them, or pass --repo to select the entries that belong to this checkout"
        )

    for rel, label, commit, path, repo in todo:
        spec_arg = f"{commit}:{path}"
        if git(checkout, "cat-file", "-e", spec_arg).returncode != 0:
            failures.append(f"{rel}: {label}: '{path}' does not exist at {commit} in {repo}")
        elif git(checkout, "cat-file", "-t", spec_arg).stdout.strip() != "blob":
            failures.append(f"{rel}: {label}: '{path}' is not a file at {commit} in {repo}")

    for failure in failures:
        print(f"FAIL: {failure}")
    checked = len(todo) + sum(1 for f in failures if ": malformed entry: " in f)
    print(
        f"Checked {checked} external locator(s) ({skipped} skipped for another repo): "
        f"{len(failures)} failure(s)"
    )
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
