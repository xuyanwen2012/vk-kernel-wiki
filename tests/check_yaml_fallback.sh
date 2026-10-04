#!/usr/bin/env bash
# Verify that the wiki scripts work with a Python interpreter that has no
# site-packages. `-S` disables the site directories, including any host
# PyYAML, so every YAML load must go through the copy bundled in
# scripts/_vendor (selected by scripts/_yaml_compat.py).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"
export PYTHONDONTWRITEBYTECODE=1
FIXTURE_ROOT="$REPO_ROOT/tests/fixtures/valid"

# 1. The bundled loader is the one in use, and it parses every real data file
#    and a fixture page's frontmatter.
python3 -S - <<'PY'
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from _yaml_compat import USING_BUNDLED, yaml

assert USING_BUNDLED, "fallback test unexpectedly imported host PyYAML"

data_files = sorted(Path("data").glob("*.yaml"))
assert data_files, "no data/*.yaml files found"
for path in data_files:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict), f"{path} did not parse to a mapping"

tags = yaml.safe_load(Path("data/tags.yaml").read_text(encoding="utf-8"))
assert "glsl" in tags["languages"]
tree = yaml.safe_load(Path("data/architectures.yaml").read_text(encoding="utf-8"))
assert isinstance(tree["architectures"], dict)

page = Path("tests/fixtures/valid/wiki/kernels/fixture-kernel.md").read_text(encoding="utf-8")
match = re.match(r"^---\s*\n(.*?)\n---", page, re.S)
fm = yaml.safe_load(match.group(1))
assert fm["id"] == "kernel-fixture-linear"
assert isinstance(fm["performance_claims"][0]["measured_at"], datetime.date)
assert isinstance(fm["performance_claims"][0]["value"], float)

round_trip = yaml.safe_load(yaml.safe_dump({"id": fm["id"], "tags": fm["tags"]}))
assert round_trip["tags"] == fm["tags"]
PY

# 2. Every script runs under -S against the real root.
python3 -S scripts/validate.py >/dev/null
python3 -S scripts/repo_status.py | grep -q "Corpus counts:"
python3 -S scripts/query.py --tag cooperative-matrix --compact >/dev/null
python3 -S scripts/grep_wiki.py fixture-pattern-that-matches-nothing --files-only >/dev/null || true

# 3. Every read path runs under -S against the valid fixture root.
export VK_KERNEL_WIKI_ROOT="$FIXTURE_ROOT"
python3 -S scripts/validate.py | grep -q "Validated 10 pages (4 source, 6 wiki): 0 error(s)"

query_output="$(python3 -S scripts/query.py --tag coopmat --type kernel --compact)"
grep -q "kernel-fixture-linear" <<<"$query_output"

page_output="$(python3 -S scripts/get_page.py kernel-fixture-linear --frontmatter-only)"
grep -q "id: kernel-fixture-linear" <<<"$page_output"

grep_output="$(python3 -S scripts/grep_wiki.py fixture_value --files-only)"
grep -q "wiki/kernels/fixture-kernel.md" <<<"$grep_output"

python3 -S scripts/repo_status.py | grep -q "Indexed source/wiki pages: 10"

echo "OK: wiki scripts work without host PyYAML"
