"""Shared wiki-root resolution for the wiki scripts.

The repository is flat: data/, wiki/, sources/, queries/ and scripts/ all live
at the same root. By default the wiki root is this file's grandparent
directory:

    <wiki-root>/scripts/_wiki_root.py  ->  <wiki-root>

No environment variable is required for the common case. The optional
VK_KERNEL_WIKI_ROOT override points every script at another root (used by the
tests and by setups where the scripts run from a separate checkout). Any
detected root is validated; a misconfiguration is a hard error rather than a
silently wrong result.

A root is recognised by `data/tags.yaml`. The `wiki/` and `sources/`
directories are not required: git does not track empty directories, so a
fresh clone of an empty wiki may lack them, and every script treats a missing
page directory as "no pages".
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ENV_VAR = "VK_KERNEL_WIKI_ROOT"


def _looks_like_wiki_root(p: Path) -> bool:
    return (p / "data" / "tags.yaml").is_file()


def _error(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def resolve_wiki_root() -> Path:
    # 1. explicit env override
    env = os.environ.get(ENV_VAR)
    if env:
        p = Path(env).expanduser().resolve()
        if _looks_like_wiki_root(p):
            return p
        _error(
            f"{ENV_VAR}={env!r} does not point at a valid wiki root "
            f"(missing data/tags.yaml)."
        )

    # 2. default: script-file grandparent == wiki root
    default_root = Path(__file__).resolve().parent.parent
    if _looks_like_wiki_root(default_root):
        return default_root

    # 3. fallback: walk up from the script location and from cwd
    seen = set()
    for start in (Path(__file__).resolve().parent, Path.cwd().resolve()):
        for candidate in [start, *start.parents]:
            if candidate in seen:
                continue
            seen.add(candidate)
            if _looks_like_wiki_root(candidate):
                return candidate

    _error(
        "Could not locate the wiki root.\n"
        "       Expected a directory containing `data/tags.yaml`.\n"
        "       Fix: run the scripts from inside the repository checkout, or\n"
        f"       set {ENV_VAR} to its absolute path."
    )
    return Path()  # unreachable


WIKI_ROOT = resolve_wiki_root()
