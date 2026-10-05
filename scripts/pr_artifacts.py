"""Layout and integrity of pull-request shader artifacts.

An artifact bundle is the directory `artifacts/prs/<slug>/PR-<number>/`:

    shaders.patch     the shader-file patches of the pull request
    PROVENANCE.yaml   where each patch came from and its sha256

`shaders.patch` is a unified diff. Its hunks are the verbatim `patch` text
GitHub returns for each changed file; the three header lines in front of each
file (`diff --git`, `---`, `+++`) are written by this module so that standard
tools can read the file. `PROVENANCE.yaml` records the sha256 of each file's
verbatim hunk text, which makes the bundle checkable offline.

The upstream licence text is kept once per repository at
`artifacts/prs/<slug>/LICENSE`.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from _yaml_compat import yaml
from _wiki_root import WIKI_ROOT

ARTIFACTS_ROOT = "artifacts/prs"
PATCH_NAME = "shaders.patch"
PROVENANCE_NAME = "PROVENANCE.yaml"
LICENSE_NAME = "LICENSE"
_HEADER_RE = re.compile(r"^diff --git a/(.+) b/\1$")


def bundle_rel(slug: str, number: int) -> str:
    return f"{ARTIFACTS_ROOT}/{slug}/PR-{int(number)}"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render_patch(files: list) -> str:
    """Unified diff of `files`: [{filename, status, patch}] with a patch."""
    parts = []
    for item in files:
        path = item["filename"]
        old = "/dev/null" if item["status"] == "added" else f"a/{path}"
        new = "/dev/null" if item["status"] in {"removed", "deleted"} else f"b/{path}"
        parts.append(f"diff --git a/{path} b/{path}\n--- {old}\n+++ {new}\n{item['patch']}\n")
    return "".join(parts)


def split_patch(text: str) -> dict:
    """Inverse of render_patch: {path: verbatim hunk text}."""
    out, path, lines = {}, None, []

    def flush():
        if path is not None:
            out[path] = "\n".join(lines[2:])  # drop the '---' and '+++' lines

    for line in text.split("\n"):
        header = _HEADER_RE.match(line)
        if header:
            flush()
            path, lines = header.group(1), []
        elif path is not None:
            lines.append(line)
    if lines and lines[-1] == "":
        lines.pop()  # the newline render_patch adds after the last hunk
    flush()
    return out


def bundle_errors(rel: str, root: Path = WIKI_ROOT) -> list:
    """Offline integrity check of one bundle. Returns error strings."""
    directory = Path(root) / rel
    provenance_path = directory / PROVENANCE_NAME
    if not provenance_path.is_file():
        return [f"{rel}: missing {PROVENANCE_NAME}"]
    try:
        provenance = yaml.safe_load(provenance_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return [f"{rel}/{PROVENANCE_NAME}: unreadable ({exc})"]
    errors = []
    for field in ("repo", "pr", "url", "merge_sha", "license", "retrieved_at", "files"):
        if not provenance.get(field):
            errors.append(f"{rel}/{PROVENANCE_NAME}: missing '{field}'")
    if not (directory.parent / LICENSE_NAME).is_file():
        errors.append(f"{rel}: missing upstream licence text at {directory.parent.name}/{LICENSE_NAME}")
    patch_path = directory / PATCH_NAME
    if not patch_path.is_file():
        return errors + [f"{rel}: missing {PATCH_NAME}"]
    hunks = split_patch(patch_path.read_text(encoding="utf-8"))
    listed = {}
    for entry in provenance.get("files") or []:
        if not isinstance(entry, dict) or not entry.get("path"):
            errors.append(f"{rel}/{PROVENANCE_NAME}: a files entry lacks 'path'")
            continue
        listed[entry["path"]] = entry
        if entry.get("sha256") is None:
            continue  # recorded as carrying no patch (pure rename)
        if entry["path"] not in hunks:
            errors.append(f"{rel}: {PATCH_NAME} has no diff for '{entry['path']}'")
        elif sha256_text(hunks[entry["path"]]) != entry["sha256"]:
            errors.append(f"{rel}: patch text of '{entry['path']}' does not match its recorded sha256")
    for path in hunks:
        if path not in listed:
            errors.append(f"{rel}: {PATCH_NAME} contains '{path}', which {PROVENANCE_NAME} does not list")
    return errors
