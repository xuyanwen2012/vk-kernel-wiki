#!/usr/bin/env python3
"""Offline test suite for the wiki scripts.

Run with:  python3 -S tests/test_wiki.py     (or: bash tests/run_all.sh)

Every script is started as a subprocess under `python3 -S` (no site-packages),
with VK_KERNEL_WIKI_ROOT selecting the root under test:

- the real repository root;
- a mini root under tests/fixtures/<case>/, whose `data` entry is a symlink to
  the tests/fixture-data/ directory, whose entries are symlinks to the real
  data/*.yaml files (so those are exercised) plus an empty claim registry;
- for the few cases that need a changed data file or a writable queries/
  directory, a temporary root assembled under tests/.tmp/ (removed afterwards);
- for the mutation cases, a temporary copy of the valid fixture root with one
  named defect applied to it.

All fixture pages are synthetic. Their titles start with "FIXTURE" and their
values are fake.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
SCRIPTS = REPO_ROOT / "scripts"
FIXTURES = TESTS_DIR / "fixtures"
REAL_DATA = REPO_ROOT / "data"
# What fixture roots see as data/: the real files, except an empty claim registry.
FIXTURE_DATA = TESTS_DIR / "fixture-data"
TMP_PARENT = Path(os.environ.get("VK_KERNEL_WIKI_TEST_TMPDIR") or TESTS_DIR / ".tmp")

INDEX_FILES = [
    "by-architecture.md", "by-device.md", "by-problem.md", "by-technique.md",
    "by-hardware-feature.md", "by-repo.md", "by-kernel-type.md", "by-language.md",
]

sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True
from _yaml_compat import yaml  # noqa: E402


def run_script(script, *args, root=None, scripts_dir=SCRIPTS, cwd=REPO_ROOT):
    """Run scripts/<script> under `python3 -S`. Returns CompletedProcess."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    env.pop("VK_KERNEL_WIKI_ROOT", None)
    if root is not None:
        env["VK_KERNEL_WIKI_ROOT"] = str(root)
    return subprocess.run(
        [sys.executable, "-S", str(Path(scripts_dir) / script), *args],
        env=env, cwd=str(cwd), capture_output=True, text=True, timeout=120,
    )


def error_lines(stdout):
    return sorted(line.strip() for line in stdout.splitlines() if line.strip().startswith("ERROR:"))


def summary_line(stdout):
    lines = [line for line in stdout.splitlines() if line.strip()]
    return lines[-1] if lines else ""


class TempRoots(unittest.TestCase):
    """Base class that can assemble throwaway wiki roots under tests/.tmp/."""

    def setUp(self):
        self._tmp_dirs = []

    def tearDown(self):
        for path in self._tmp_dirs:
            shutil.rmtree(path, ignore_errors=True)
        try:
            TMP_PARENT.rmdir()  # only succeeds when empty
        except OSError:
            pass

    def assemble_root(self, pages_from, data_overrides=None):
        """Build a temp root: wiki/ and sources/ come from `pages_from`
        (symlinked), data/ holds the real data files (symlinked) except for
        `data_overrides` ({filename: text}), and queries/ is a fresh directory."""
        TMP_PARENT.mkdir(parents=True, exist_ok=True)
        root = Path(tempfile.mkdtemp(prefix="root-", dir=str(TMP_PARENT)))
        self._tmp_dirs.append(root)
        for sub in ("wiki", "sources"):
            src = Path(pages_from) / sub
            if src.is_dir():
                os.symlink(src.resolve(), root / sub)
            else:
                (root / sub).mkdir()
        (root / "queries").mkdir()
        if not data_overrides:
            os.symlink(FIXTURE_DATA.resolve(), root / "data")
        else:
            (root / "data").mkdir()
            for path in sorted(FIXTURE_DATA.iterdir()):
                if path.name not in data_overrides:
                    os.symlink(path.resolve(), root / "data" / path.name)
            for name, text in data_overrides.items():
                if text is not None:  # None removes the data file from the root
                    (root / "data" / name).write_text(text, encoding="utf-8")
        return root

    def copy_root(self, pages_from, data_overrides=None):
        """Like assemble_root, but wiki/ and sources/ are real copies, so a test
        may change the pages."""
        root = self.assemble_root(TESTS_DIR / "no-such-pages", data_overrides)
        for sub in ("wiki", "sources"):
            src = Path(pages_from) / sub
            if src.is_dir():
                (root / sub).rmdir()
                shutil.copytree(src, root / sub)
        return root

    def scratch_dir(self):
        TMP_PARENT.mkdir(parents=True, exist_ok=True)
        path = Path(tempfile.mkdtemp(prefix="scratch-", dir=str(TMP_PARENT)))
        self._tmp_dirs.append(path)
        return path


# ---------------------------------------------------------------------------
# 1. The real repository
# ---------------------------------------------------------------------------

class RealRepoTest(TempRoots):
    def test_real_repo_validates(self):
        proc = run_script("validate.py")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(error_lines(proc.stdout), [])
        self.assertRegex(summary_line(proc.stdout), r"^Validated \d+ pages \(\d+ source, \d+ wiki\): 0 error\(s\)$")

    def test_real_repo_generates_every_index(self):
        # Mirror root: real data/, wiki/ and sources/, but a private queries/
        # directory so the test never rewrites files in the repository.
        root = self.assemble_root(REPO_ROOT)
        proc = run_script("generate-indices.py", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        produced = sorted(p.name for p in (root / "queries").glob("*.md"))
        self.assertEqual(produced, sorted(INDEX_FILES))
        for name in INDEX_FILES:
            self.assertTrue((root / "queries" / name).read_text(encoding="utf-8").strip(), name)

    def test_real_repo_status_runs(self):
        proc = run_script("repo_status.py")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("Corpus counts:", proc.stdout)
        self.assertIn("Architecture nodes:", proc.stdout)

    def test_real_data_files_match_contract(self):
        tags = yaml.safe_load((REAL_DATA / "tags.yaml").read_text(encoding="utf-8"))
        self.assertNotIn("architectures", tags)
        for group in ("techniques", "hardware_features", "kernel_types", "languages"):
            self.assertTrue(tags.get(group), group)
        self.assertLessEqual({"glsl", "spirv", "cpp", "python"}, set(tags["languages"]))
        self.assertEqual(tags["confidence"], ["verified", "source-reported", "inferred", "experimental"])
        self.assertEqual(tags["reproducibility"], ["concept", "pseudocode", "snippet", "runnable", "benchmarked"])
        self.assertEqual(
            set(tags["source_categories"]),
            {"official-doc", "upstream-code", "paper", "benchmark-blog", "community-note", "measurement"},
        )
        self.assertEqual(
            set(tags["evidence_types"]),
            {"official-doc", "upstream-code", "paper", "benchmark", "measurement", "inference"},
        )
        claims = yaml.safe_load((REAL_DATA / "version-claims.yaml").read_text(encoding="utf-8"))
        self.assertIsInstance(claims["claims"], list)
        schemas = yaml.safe_load((REAL_DATA / "schemas.yaml").read_text(encoding="utf-8"))
        for page_type in (
            "wiki-hardware", "wiki-technique", "wiki-pattern", "wiki-kernel", "wiki-language",
            "wiki-migration", "source-pr", "source-doc", "source-blog", "source-measurement",
        ):
            self.assertIn(page_type, schemas)

    def test_invalid_root_is_a_hard_error(self):
        proc = run_script("validate.py", root=TESTS_DIR)  # no data/tags.yaml, no wiki/
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("VK_KERNEL_WIKI_ROOT", proc.stderr)

    def test_committed_indices_are_up_to_date(self):
        # queries/*.md is committed; it must equal what the generator produces.
        root = self.assemble_root(REPO_ROOT)
        proc = run_script("generate-indices.py", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        committed = sorted(p.name for p in (REPO_ROOT / "queries").glob("*.md"))
        self.assertEqual(committed, sorted(INDEX_FILES))
        for name in INDEX_FILES:
            self.assertEqual(
                (REPO_ROOT / "queries" / name).read_text(encoding="utf-8"),
                (root / "queries" / name).read_text(encoding="utf-8"),
                f"queries/{name} is stale; run python3 -S scripts/generate-indices.py",
            )

    def test_page_directories_survive_a_clone(self):
        # git does not track empty directories, so each one holds a .gitkeep.
        for rel in (
            "wiki/hardware", "wiki/techniques", "wiki/patterns", "wiki/kernels",
            "wiki/languages", "wiki/migration",
            "sources/prs", "sources/docs", "sources/blogs", "sources/measurements",
        ):
            directory = REPO_ROOT / rel
            self.assertTrue(directory.is_dir(), rel)
            self.assertTrue(any(p.is_file() for p in directory.rglob("*")), f"{rel} holds no file")

    def test_scripts_run_in_a_clone_like_copy(self):
        # Rebuild the repository from exactly the files git would hand to a
        # clone (tracked plus not-ignored untracked files; no empty
        # directories) and run every script from inside that copy.
        try:
            listing = subprocess.run(
                ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                cwd=str(REPO_ROOT), capture_output=True, timeout=60,
            )
        except OSError:
            self.skipTest("git is not available")
        if listing.returncode != 0:
            self.skipTest("not a git work tree")
        clone = self.scratch_dir()
        for rel in filter(None, listing.stdout.decode("utf-8").split("\0")):
            src, dst = REPO_ROOT / rel, clone / rel
            if not (src.is_symlink() or src.is_file()):
                continue  # listed by git but deleted in the work tree
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_symlink():
                os.symlink(os.readlink(src), dst)
            else:
                shutil.copyfile(src, dst)
        self.assertTrue((clone / "data" / "tags.yaml").is_file())
        for script, args in (
            ("validate.py", []),
            ("repo_status.py", []),
            ("query.py", ["--architecture", "rdna3", "--compact"]),
            ("grep_wiki.py", ["fixture-pattern-that-matches-nothing", "--files-only"]),
            ("generate-indices.py", []),
        ):
            with self.subTest(script=script):
                proc = run_script(script, *args, scripts_dir=clone / "scripts", cwd=clone)
                self.assertIn(proc.returncode, (0, 1) if script == "grep_wiki.py" else (0,),
                              proc.stdout + proc.stderr)
                self.assertNotIn("Could not locate the wiki root", proc.stderr)
        # The copy validated itself, not the work tree it was made from.
        proc = run_script("repo_status.py", scripts_dir=clone / "scripts", cwd=clone)
        self.assertIn("Query indices: 8", proc.stdout)
        proc = run_script("validate.py", root=clone / "tests" / "fixtures" / "valid",
                          scripts_dir=clone / "scripts", cwd=clone)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(summary_line(proc.stdout), "Validated 10 pages (4 source, 6 wiki): 0 error(s)")


# ---------------------------------------------------------------------------
# 2. The valid fixture root: one page of each of the ten page types
# ---------------------------------------------------------------------------

VALID = FIXTURES / "valid"
VALID_IDS = {
    "source-pr": "pr-fixture-example-1",
    "source-doc": "doc-fixture-spec",
    "source-blog": "blog-fixture-note",
    "source-measurement": "meas-fixture-radeon-780m",
    "wiki-hardware": "hw-fixture-coopmat",
    "wiki-technique": "technique-fixture-double-buffering",
    "wiki-pattern": "pattern-fixture-slow-kernel",
    "wiki-kernel": "kernel-fixture-linear",
    "wiki-language": "lang-fixture-glsl",
    "wiki-migration": "migration-fixture-rdna3-to-xe2",
}


def load_frontmatter(path):
    text = Path(path).read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---\n", 2)[1])


class ValidRootTest(TempRoots):
    def test_fixture_root_uses_real_data(self):
        self.assertTrue((VALID / "data").is_symlink())
        self.assertEqual((VALID / "data").resolve(), FIXTURE_DATA.resolve())
        # Every data file the validator reads is the real one, except the claim
        # registry: real claims name real pages, which fixture roots lack.
        names = sorted(p.name for p in FIXTURE_DATA.iterdir())
        self.assertEqual(names, ["aliases.yaml", "architectures.yaml", "schemas.yaml", "tags.yaml",
                                 "version-claims.yaml"])
        for name in names:
            path = FIXTURE_DATA / name
            if name == "version-claims.yaml":
                self.assertFalse(path.is_symlink())
                self.assertEqual(yaml.safe_load(path.read_text(encoding="utf-8")), {"claims": []})
            else:
                self.assertEqual(path.resolve(), (REAL_DATA / name).resolve())

    def test_valid_root_validates(self):
        proc = run_script("validate.py", root=VALID)
        self.assertEqual(error_lines(proc.stdout), [])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(summary_line(proc.stdout), "Validated 10 pages (4 source, 6 wiki): 0 error(s)")

    def test_valid_root_has_all_ten_page_types(self):
        proc = run_script("query.py", "--limit", "100", "--compact", root=VALID)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        for page_type, page_id in VALID_IDS.items():
            self.assertIn(f"[{page_type}] {page_id}:", proc.stdout)

    def test_verified_kernel_page_is_backed_by_a_measurement_page(self):
        kernel = load_frontmatter(VALID / "wiki/kernels/fixture-kernel.md")
        meas = load_frontmatter(VALID / "sources/measurements/fixture-measurement.md")
        self.assertEqual(kernel["confidence"], "verified")
        self.assertEqual([e["evidence_type"] for e in kernel["evidence_basis"]], ["measurement"])
        self.assertEqual(kernel["evidence_basis"][0]["source_id"], meas["id"])
        self.assertIn(meas["id"], kernel["sources"])
        claim = kernel["performance_claims"][0]
        for field in ("gpu", "driver", "dtype", "shape", "metric", "value",
                      "measured_at", "source_id", "source_locator"):
            self.assertIn(field, claim)
        self.assertEqual(claim["source_id"], meas["id"])

    def test_fixture_titles_are_marked(self):
        # Only wiki/ and sources/ hold pages; a fixture root may also contain
        # generated queries/*.md, which have no frontmatter.
        pages = [
            p for case in sorted(FIXTURES.iterdir()) if case.is_dir()
            for sub in ("wiki", "sources") for p in sorted((case / sub).rglob("*.md"))
        ]
        self.assertTrue(pages)
        for page in pages:
            self.assertTrue(str(load_frontmatter(page)["title"]).startswith("FIXTURE"), page)

    def test_indices_for_valid_root(self):
        root = self.assemble_root(VALID)
        proc = run_script("generate-indices.py", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        for name in INDEX_FILES:
            self.assertTrue((root / "queries" / name).is_file(), name)
        by_device = (root / "queries" / "by-device.md").read_text(encoding="utf-8")
        self.assertIn("`radeon-780m`", by_device)
        self.assertIn("FIXTURE-DRIVER 0.0.0", by_device)
        self.assertIn("fixture-measurement.md", by_device)
        by_arch = (root / "queries" / "by-architecture.md").read_text(encoding="utf-8")
        for rel in ("fixture-doc.md", "fixture-kernel.md", "fixture-technique.md"):
            self.assertIn(rel, by_arch)
        self.assertIn("example-org/example-repo", (root / "queries" / "by-repo.md").read_text(encoding="utf-8"))

    def test_repo_status_counts_valid_root(self):
        proc = run_script("repo_status.py", root=VALID)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("Indexed source/wiki pages: 10", proc.stdout)
        self.assertIn("sources/measurements: 1", proc.stdout)
        self.assertIn("radeon-780m: 1", proc.stdout)

    def test_get_page_and_grep(self):
        proc = run_script("get_page.py", "kernel-fixture-linear", "--frontmatter-only", root=VALID)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("id: kernel-fixture-linear", proc.stdout)
        proc = run_script("get_page.py", "kernel-fixture-missing", root=VALID)
        self.assertEqual(proc.returncode, 1)
        proc = run_script("grep_wiki.py", "fixture_value", "--files-only", root=VALID)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("wiki/kernels/fixture-kernel.md", proc.stdout)


# ---------------------------------------------------------------------------
# 3. One fixture root per validation rule
# ---------------------------------------------------------------------------

_DOC = "sources/docs/fixture-doc.md"
_MEAS = "sources/measurements/fixture-measurement.md"
_HW = "wiki/hardware/fixture-hardware.md"
_KERNEL = "wiki/kernels/fixture-kernel.md"
_TECH = "wiki/techniques/fixture-technique.md"
_PR = "sources/prs/example-org-example-repo"
_NEEDS = "['first-party-measurement', 'official-doc-plus-upstream-code']"

# fixture directory -> the exact, complete list of expected error messages.
NEGATIVE_CASES = {
    "unknown-tag": [f"{_DOC}: 'fixture-not-a-tag' is not a valid tags value"],
    "unknown-architecture": [f"{_DOC}: unknown architecture 'fixture-unknown-gpu'"],
    "architecture-alias-not-a-node": [f"{_DOC}: unknown architecture '780M'"],
    "missing-required-field": [f"{_DOC}: missing required field 'url'"],
    "unknown-field": [f"{_DOC}: unknown field 'fixture_extra_field' for source-doc"],
    "wrong-id-prefix": [f"{_DOC}: id 'fixture-spec' must start with 'doc-'"],
    "duplicate-id": [
        "sources/docs/fixture-doc-b.md: duplicate id 'doc-fixture-spec' (also in sources/docs/fixture-doc-a.md)",
    ],
    "unresolved-source-id": [f"{_HW}: references unknown source id 'doc-fixture-missing'"],
    "verified-no-evidence-basis": [
        f"{_HW}: confidence 'verified' requires a non-empty 'evidence_basis' list",
    ],
    "verified-insufficient-evidence": [
        f"{_HW}: confidence 'verified' is not supported by evidence_basis: needs one of "
        f"{_NEEDS} (found evidence types: ['official-doc'])",
    ],
    "verified-measurement-evidence-not-measurement-page": [
        f"{_HW}: evidence_basis[0]: evidence_type 'measurement' requires source_id "
        "'doc-fixture-spec' to be a source-measurement page (it is source-doc)",
        f"{_HW}: confidence 'verified' is not supported by evidence_basis: needs one of "
        f"{_NEEDS} (found evidence types: ['measurement'])",
    ],
    "verified-evidence-not-in-sources": [
        f"{_HW}: evidence_basis[0].source_id 'meas-fixture-radeon-780m' is not listed in the page's 'sources'",
    ],
    "claim-missing-driver": [f"{_KERNEL}: performance_claims[0] missing 'driver'"],
    "claim-missing-measured-at": [f"{_KERNEL}: performance_claims[0] missing 'measured_at'"],
    "claim-non-numeric-value": [
        f"{_KERNEL}: performance_claims[0].value must be numeric, got str: fixture-fast",
    ],
    "claim-unknown-source-id": [
        f"{_KERNEL}: performance_claims[0].source_id 'meas-fixture-missing' not found in source corpus",
    ],
    "claim-empty-source-locator": [
        f"{_KERNEL}: performance_claims[0].source_locator must be a non-empty string",
    ],
    "measurement-missing-driver": [f"{_MEAS}: missing required field 'driver'"],
    "measurement-empty-driver": [f"{_MEAS}: driver must be a non-empty string"],
    "measurement-empty-raw-data": [f"{_MEAS}: raw_data must contain at least 1 entry"],
    "measurement-raw-data-missing-locator": [f"{_MEAS}: raw_data[0] missing 'locator'"],
    "measurement-device-not-leaf": [
        f"{_MEAS}: device 'rdna3' is not a device node in data/architectures.yaml",
    ],
    "measurement-wrong-source-category": [
        f"{_MEAS}: source_category 'benchmark-blog' not in allowed ['measurement']",
    ],
    "pr-without-excerpt-markers": [
        f"{_PR}/pr-1.md: body is missing the excerpt marker '<!-- upstream-excerpt-start -->'",
        f"{_PR}/pr-1.md: body is missing the excerpt marker '<!-- upstream-excerpt-end -->'",
    ],
    "pr-merged-without-merge-sha": [
        f"{_PR}/pr-1.md: merged PR requires a full 40-hex merge_sha",
        f"{_PR}/pr-2.md: merge_sha 'abc1234' must be a full 40-hex commit sha",
    ],
    "technique-snippet-without-code": [
        f"{_TECH}: wiki-technique page must contain fenced code block (reproducibility >= snippet)",
    ],
    "version-sensitive-unresolved": [
        f"{_HW}: version_sensitive id 'vs-fixture-missing' does not resolve to data/version-claims.yaml",
    ],
    # These two bring their own registry (version-claims.yaml in the case directory).
    "version-claim-page-not-in-applies-to": [
        "wiki/hardware/fixture-hardware-second.md: version_sensitive id 'vs-fixture-claim' resolves, "
        "but that claim's applies_to in data/version-claims.yaml does not list this page",
    ],
    "version-claim-empty-fields": [
        "data/version-claims.yaml: claim 'vs-fixture-claim'.claim_valid_for must be a non-empty string",
        "data/version-claims.yaml: claim 'vs-fixture-claim'.last_verified_release must be a non-empty string",
    ],
}

# Fixture directories that are not plain negative roots.
OTHER_CASES = {
    "valid", "glsl-snippet-passes", "alias-collision",
    "version-claim-roundtrip", "version-claim-missing-pointer",
}


class RuleTest(TempRoots):
    def assert_rejected(self, root, expected):
        proc = run_script("validate.py", root=root)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertEqual(error_lines(proc.stdout), sorted(f"ERROR: {msg}" for msg in expected))
        self.assertTrue(summary_line(proc.stdout).endswith(f": {len(expected)} error(s)"), proc.stdout)

    def test_every_fixture_directory_is_covered(self):
        on_disk = {p.name for p in FIXTURES.iterdir() if p.is_dir()}
        self.assertEqual(on_disk, set(NEGATIVE_CASES) | OTHER_CASES)

    def test_negative_fixtures(self):
        for case, expected in NEGATIVE_CASES.items():
            with self.subTest(case=case):
                root = FIXTURES / case
                registry = root / "version-claims.yaml"
                if registry.is_file():  # the case brings its own claim registry
                    root = self.assemble_root(
                        root, {"version-claims.yaml": registry.read_text(encoding="utf-8")}
                    )
                self.assert_rejected(root, expected)

    def test_glsl_snippet_page_passes(self):
        proc = run_script("validate.py", root=FIXTURES / "glsl-snippet-passes")
        self.assertEqual(error_lines(proc.stdout), [])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(summary_line(proc.stdout), "Validated 2 pages (1 source, 1 wiki): 0 error(s)")

    def test_alias_collision(self):
        # The real aliases.yaml plus one alias that already belongs to another node.
        case = FIXTURES / "alias-collision"
        aliases = yaml.safe_load((REAL_DATA / "aliases.yaml").read_text(encoding="utf-8"))
        extra = yaml.safe_load((case / "collision.yaml").read_text(encoding="utf-8"))
        for canonical, variants in extra.items():
            aliases[canonical] = list(aliases.get(canonical) or []) + list(variants)
        root = self.assemble_root(case, {"aliases.yaml": yaml.safe_dump(aliases, sort_keys=False)})
        self.assert_rejected(root, ["data/aliases.yaml: alias '780M' maps to both 'radeon-780m' and 'rx-7600'"])

    def test_real_aliases_have_no_collision(self):
        root = self.assemble_root(FIXTURES / "alias-collision")
        proc = run_script("validate.py", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_version_claim_roundtrip(self):
        case = FIXTURES / "version-claim-roundtrip"
        registry = (case / "version-claims.yaml").read_text(encoding="utf-8")
        root = self.assemble_root(case, {"version-claims.yaml": registry})
        proc = run_script("validate.py", root=root)
        self.assertEqual(error_lines(proc.stdout), [])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_version_claim_target_without_pointer(self):
        case = FIXTURES / "version-claim-missing-pointer"
        registry = (case / "version-claims.yaml").read_text(encoding="utf-8")
        root = self.assemble_root(case, {"version-claims.yaml": registry})
        self.assert_rejected(root, [
            "data/version-claims.yaml: claim 'vs-fixture-claim' applies_to "
            "'wiki/hardware/fixture-hardware.md' carries version_sensitive id None, expected 'vs-fixture-claim'",
        ])


# ---------------------------------------------------------------------------
# 3b. Mutation cases: the valid fixture root with exactly one defect
# ---------------------------------------------------------------------------

_BLOG = "sources/blogs/fixture-blog.md"
_PR1 = f"{_PR}/pr-1.md"
_PATTERN = "wiki/patterns/fixture-pattern.md"
_MIGRATION = "wiki/migration/fixture-migration.md"
_CLAIM = "performance_claims[0]"
_DRIVER_HINT = "(name the driver and its version, e.g. 'RADV Mesa 25.2.7')"
_UNKNOWN_TYPE = (
    "unknown page type (pages must live in sources/{prs,docs,blogs,measurements}/ or "
    "wiki/{hardware,techniques,patterns,kernels,languages,migration}/)"
)
_EXCERPT = "FIXTURE synthetic excerpt text; not copied from any real repository."
_EXCERPT_EMPTY = "body excerpt between the upstream-excerpt markers is empty"
_RAW_LOCATOR = "locator: sources/measurements/fixture-measurement.md#row-0"
_EXT_REPO = "https://example.invalid/fixture/repo"
_EXT_COMMIT = "0123456789abcdef0123456789abcdef01234567"
_EXT_BOTH = "(an external-repository entry needs repo and commit)"
_EXT_REPO_HINT = "(an https URL of the git repository, e.g. 'https://example.org/owner/name')"
_EXT_COMMIT_HINT = "(exactly 40 lowercase hex characters; quote a sha that is all digits)"


def _external(repo=_EXT_REPO, commit=_EXT_COMMIT, locator="fixture/not-in-the-wiki/run.log"):
    """Replacement for _RAW_LOCATOR: a raw_data entry in the external-repository form."""
    return f"repo: {repo}\n  commit: {commit}\n  locator: {locator}"


_CLAIMS_BLOCK = re.compile(r"^performance_claims:\n(?:[ -] .*\n)+", re.MULTILINE)
_FENCE_BLOCK = re.compile(r"^```glsl\n.*?^```\n", re.MULTILINE | re.DOTALL)
_NOT_VERIFIED = (
    f"confidence 'verified' is not supported by evidence_basis: needs one of {_NEEDS} "
)


def sub(rel, old, new):
    """Mutation: replace the single occurrence of `old` (str or regex) in a page."""
    def apply(root):
        path = root / rel
        text = path.read_text(encoding="utf-8")
        if isinstance(old, str):
            assert text.count(old) == 1, (rel, old, text.count(old))
            text = text.replace(old, new)
        else:
            text, count = old.subn(new, text)
            assert count == 1, (rel, old.pattern, count)
        path.write_text(text, encoding="utf-8")
    return apply


def move(rel, new_rel):
    def apply(root):
        (root / new_rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).rename(root / new_rel)
    return apply


def write(rel, text):
    def apply(root):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    return apply


def append_bytes(rel, data):
    def apply(root):
        with open(root / rel, "ab") as handle:
            handle.write(data)
    return apply


def claim(old, new):
    return sub(_KERNEL, old, new)


# case name -> (mutations applied to a copy of the valid root, exact expected errors)
MUTATION_CASES = {
    # --- performance claims -------------------------------------------------
    "claim-empty-driver": (
        [claim("  driver: FIXTURE-DRIVER 0.0.0", "  driver: ''")],
        [f"{_KERNEL}: {_CLAIM}.driver must be a non-empty string"],
    ),
    "claim-driver-without-version": (
        [claim("  driver: FIXTURE-DRIVER 0.0.0", "  driver: FIXTURE-DRIVER")],
        [f"{_KERNEL}: {_CLAIM}.driver 'FIXTURE-DRIVER' is not acceptable {_DRIVER_HINT}"],
    ),
    "claim-empty-gpu": (
        [claim("- gpu: radeon-780m", "- gpu: ''")],
        [f"{_KERNEL}: {_CLAIM}.gpu must be a non-empty string"],
    ),
    "claim-gpu-not-a-node": (
        [claim("- gpu: radeon-780m", "- gpu: fixture-not-a-node")],
        [f"{_KERNEL}: {_CLAIM}.gpu 'fixture-not-a-node' is not a device node in data/architectures.yaml"],
    ),
    "claim-gpu-is-a-generation": (
        [claim("- gpu: radeon-780m", "- gpu: rdna3")],
        [f"{_KERNEL}: {_CLAIM}.gpu 'rdna3' is not a device node in data/architectures.yaml"],
    ),
    "claim-gpu-is-an-alias": (
        [claim("- gpu: radeon-780m", "- gpu: 780M")],
        [f"{_KERNEL}: {_CLAIM}.gpu '780M' is not a device node in data/architectures.yaml"],
    ),
    "claim-empty-dtype-shape-metric": (
        [claim("dtype: fixture-dtype", "dtype: ''"), claim("shape: FIXTURE 1x1x1", "shape: ''"),
         claim("metric: fixture-units", "metric: ''")],
        [f"{_KERNEL}: {_CLAIM}.{field} must be a non-empty string" for field in ("dtype", "shape", "metric")],
    ),
    "claim-value-nan": (
        [claim("value: 999999.0", "value: .nan")],
        [f"{_KERNEL}: {_CLAIM}.value must be a finite number, got float: nan"],
    ),
    "claim-value-infinity": (
        [claim("value: 999999.0", "value: .inf")],
        [f"{_KERNEL}: {_CLAIM}.value must be a finite number, got float: inf"],
    ),
    "claim-value-bool": (
        [claim("value: 999999.0", "value: true")],
        [f"{_KERNEL}: {_CLAIM}.value must be numeric, got bool: True"],
    ),
    "claim-measured-at-timestamp": (
        [claim("  measured_at: 2000-01-01", "  measured_at: 2000-01-01 10:00:00")],
        [f"{_KERNEL}: {_CLAIM}.measured_at must be an ISO date (YYYY-MM-DD), "
         "got datetime.datetime(2000, 1, 1, 10, 0)"],
    ),
    "claim-source-id-is-a-list": (
        [claim("  source_id: meas-fixture-radeon-780m\n  source_locator",
               "  source_id: [meas-fixture-radeon-780m]\n  source_locator")],
        [f"{_KERNEL}: {_CLAIM}.source_id '['meas-fixture-radeon-780m']' not found in source corpus"],
    ),
    "claims-not-a-list": (
        [sub(_KERNEL, _CLAIMS_BLOCK, "performance_claims: {gpu: radeon-780m}\n")],
        [f"{_KERNEL}: performance_claims must be a list, got dict"],
    ),
    "claims-entry-not-a-mapping": (
        [sub(_KERNEL, _CLAIMS_BLOCK, "performance_claims:\n- fixture-not-a-mapping\n")],
        [f"{_KERNEL}: {_CLAIM} must be a mapping, got str"],
    ),
    # --- page location and type --------------------------------------------
    "wiki-page-in-unknown-directory": (
        [move(_KERNEL, "wiki/misc/fixture-kernel.md")],
        [f"wiki/misc/fixture-kernel.md: {_UNKNOWN_TYPE}"],
    ),
    "wiki-page-at-wiki-root": (
        [move(_MIGRATION, "wiki/fixture-migration.md")],
        [f"wiki/fixture-migration.md: {_UNKNOWN_TYPE}"],
    ),
    "source-page-in-unknown-directory": (
        [move(_BLOG, "sources/misc/fixture-blog.md")],
        # The page is no longer a source page, so its id stops resolving as one.
        [f"sources/misc/fixture-blog.md: {_UNKNOWN_TYPE}",
         f"{_PATTERN}: references unknown source id 'blog-fixture-note'",
         f"{_TECH}: references unknown source id 'blog-fixture-note'"],
    ),
    "page-in-wrong-directory": (
        [move(_MIGRATION, "wiki/hardware/fixture-migration.md")],
        [f"wiki/hardware/fixture-migration.md: {msg}" for msg in (
            "missing required field 'architectures'",
            "missing required field 'confidence'",
            "missing required field 'aliases'",
            "unknown field 'from_arch' for wiki-hardware",
            "unknown field 'to_arch' for wiki-hardware",
            "id 'migration-fixture-rdna3-to-xe2' must start with 'hw-'",
            "type 'migration' does not match expected 'hardware' for wiki-hardware",
        )],
    ),
    "type-mismatch": (
        [sub(_HW, "type: hardware", "type: technique")],
        [f"{_HW}: type 'technique' does not match expected 'hardware' for wiki-hardware"],
    ),
    "uppercase-extension": (
        [move(_MIGRATION, "wiki/migration/fixture-migration.MD")],
        ["wiki/migration/fixture-migration.MD: page file extension must be lowercase '.md'"],
    ),
    # --- frontmatter shape --------------------------------------------------
    "frontmatter-missing": (
        [write(_MIGRATION, "# FIXTURE page without frontmatter\n")],
        [f"{_MIGRATION}: missing YAML frontmatter"],
    ),
    "frontmatter-is-a-list": (
        [write(_MIGRATION, "---\n- FIXTURE\n- list\n---\n\n# FIXTURE page\n")],
        [f"{_MIGRATION}: frontmatter must be a YAML mapping, got list"],
    ),
    "frontmatter-invalid-yaml": (
        [write(_MIGRATION, "---\ntitle: [FIXTURE unclosed\n---\n\n# FIXTURE page\n")],
        None,  # exact parser wording is not pinned; see test_mutation_cases
    ),
    "page-not-utf8": (
        [append_bytes(_MIGRATION, b"\xff")],
        [f"{_MIGRATION}: not valid UTF-8"],
    ),
    "scalar-fields-hold-lists": (
        [sub(_HW, "confidence: source-reported", "confidence: [source-reported]"),
         sub(_TECH, "reproducibility: snippet", "reproducibility: [snippet]"),
         sub(_BLOG, "source_category: community-note", "source_category: [community-note]"),
         sub(_MIGRATION, "from_arch: rdna3", "from_arch: [rdna3]"),
         sub(_MIGRATION, "to_arch: xe2", "to_arch: {node: xe2}"),
         sub(_PR1, "status: merged", "status: [merged]")],
        [f"{_HW}: field 'confidence' must be a string, got list",
         f"{_TECH}: field 'reproducibility' must be a string, got list",
         f"{_BLOG}: field 'source_category' must be a string, got list",
         f"{_MIGRATION}: field 'from_arch' must be a string, got list",
         f"{_MIGRATION}: field 'to_arch' must be a string, got dict",
         f"{_PR1}: field 'status' must be a string, got list"],
    ),
    "malformed-page-does-not-hide-other-errors": (
        [sub(_HW, "confidence: source-reported", "confidence: [verified]"),
         sub(_MEAS, "device: radeon-780m", "device: [radeon-780m]"),
         sub(_BLOG, "url: https://example.invalid/fixture/note\n", "")],
        [f"{_HW}: field 'confidence' must be a string, got list",
         f"{_MEAS}: field 'device' must be a string, got list",
         f"{_BLOG}: missing required field 'url'"],
    ),
    # --- vocabulary and cross references -----------------------------------
    "architecture-name-in-tags": (
        [sub(_HW, "tags:\n- cooperative-matrix", "tags:\n- cooperative-matrix\n- amd")],
        [f"{_HW}: 'amd' is not a valid tags value"],
    ),
    "hardware-feature-tag-not-in-hardware-features": (
        [sub(_PR1, "hardware_features:\n- cooperative-matrix", "hardware_features: []")],
        [f"{_PR1}: tags contain hardware features ['cooperative-matrix'] not in hardware_features field"],
    ),
    "candidate-techniques-non-remedy-prefix": (
        [sub(_PATTERN, "candidate_techniques:\n- technique-fixture-double-buffering",
             "candidate_techniques:\n- lang-fixture-glsl")],
        [f"{_PATTERN}: candidate_techniques entry 'lang-fixture-glsl' must use one of "
         "('technique-', 'hw-', 'migration-') prefixes"],
    ),
    "candidate-techniques-unresolved": (
        [sub(_PATTERN, "candidate_techniques:\n- technique-fixture-double-buffering",
             "candidate_techniques:\n- technique-fixture-missing")],
        [f"{_PATTERN}: candidate_techniques entry 'technique-fixture-missing' does not resolve "
         "to an existing page id"],
    ),
    "related-unresolved": (
        [sub(_PATTERN, "related:\n- kernel-fixture-linear", "related:\n- kernel-fixture-missing")],
        [f"{_PATTERN}: related entry 'kernel-fixture-missing' does not resolve to an existing page id"],
    ),
    "pr-directory-with-two-repos": (
        [lambda root: (root / _PR / "pr-2.md").write_text(
            (root / _PR1).read_text(encoding="utf-8")
            .replace("id: pr-fixture-example-1", "id: pr-fixture-example-2")
            .replace("repo: example-org/example-repo", "repo: example-org/other-repo"),
            encoding="utf-8")],
        [f"{_PR}: expected one repo identity across PR pages, found "
         "['example-org/example-repo', 'example-org/other-repo']"],
    ),
    # --- 'verified' evidence ------------------------------------------------
    "evidence-official-doc-label-on-a-blog": (
        [sub(_TECH, "- evidence_type: official-doc\n  source_id: doc-fixture-spec",
             "- evidence_type: official-doc\n  source_id: blog-fixture-note")],
        [f"{_TECH}: evidence_basis[0]: evidence_type 'official-doc' requires source_id "
         "'blog-fixture-note' to have source_category 'official-doc' (it has 'community-note')",
         f"{_TECH}: {_NOT_VERIFIED}(found evidence types: ['official-doc', 'upstream-code'])"],
    ),
    "evidence-upstream-code-label-on-a-blog": (
        [sub(_TECH, "- evidence_type: upstream-code\n  source_id: pr-fixture-example-1",
             "- evidence_type: upstream-code\n  source_id: blog-fixture-note")],
        [f"{_TECH}: evidence_basis[1]: evidence_type 'upstream-code' requires source_id "
         "'blog-fixture-note' to be a source-pr page (it is source-blog)",
         f"{_TECH}: {_NOT_VERIFIED}(found evidence types: ['official-doc', 'upstream-code'])"],
    ),
    "evidence-entry-missing-evidence-type": (
        [sub(_KERNEL, "- evidence_type: measurement\n  source_id", "- source_id")],
        [f"{_KERNEL}: evidence_basis[0] missing 'evidence_type'",
         f"{_KERNEL}: {_NOT_VERIFIED}(found evidence types: ['None'])"],
    ),
    "evidence-type-is-a-list": (
        [sub(_KERNEL, "- evidence_type: measurement", "- evidence_type: [measurement]")],
        [f"{_KERNEL}: evidence_basis[0] missing 'evidence_type'",
         f"{_KERNEL}: {_NOT_VERIFIED}(found evidence types: [\"['measurement']\"])"],
    ),
    # --- measurement pages --------------------------------------------------
    "measurement-driver-without-version": (
        [sub(_MEAS, "driver: FIXTURE-DRIVER 0.0.0", "driver: FIXTURE-DRIVER")],
        [f"{_MEAS}: driver 'FIXTURE-DRIVER' is not acceptable {_DRIVER_HINT}"],
    ),
    "measurement-device-not-in-architectures": (
        [sub(_MEAS, "device: radeon-780m", "device: arc-b580")],
        [f"{_MEAS}: device 'arc-b580' must also be listed in 'architectures'"],
    ),
    "measurement-device-only-under-ancestor": (
        [sub(_MEAS, "architectures:\n- radeon-780m", "architectures:\n- rdna3")],
        [f"{_MEAS}: device 'radeon-780m' must also be listed in 'architectures'"],
    ),
    "measurement-measured-at-timestamp": (
        [sub(_MEAS, "measured_at: &id001 2000-01-01", "measured_at: &id001 2000-01-01 10:00:00")],
        [f"{_MEAS}: {field} must be an ISO date (YYYY-MM-DD), got datetime.datetime(2000, 1, 1, 10, 0)"
         for field in ("measured_at", "captured_at")],
    ),
    "raw-data-locator-absolute": (
        [sub(_MEAS, _RAW_LOCATOR, "locator: /fixture/absolute/run.log")],
        [f"{_MEAS}: raw_data[0].locator '/fixture/absolute/run.log' must be repo-relative, "
         "not an absolute or home path"],
    ),
    "raw-data-locator-home": (
        [sub(_MEAS, _RAW_LOCATOR, "locator: '~/fixture/run.log'")],
        [f"{_MEAS}: raw_data[0].locator '~/fixture/run.log' must be repo-relative, "
         "not an absolute or home path"],
    ),
    "raw-data-locator-parent": (
        [sub(_MEAS, _RAW_LOCATOR, "locator: sources/../../fixture/run.log")],
        [f"{_MEAS}: raw_data[0].locator 'sources/../../fixture/run.log' must not contain '..'"],
    ),
    "raw-data-locator-missing-file": (
        [sub(_MEAS, _RAW_LOCATOR, "locator: sources/measurements/fixture-missing.csv")],
        [f"{_MEAS}: raw_data[0].locator 'sources/measurements/fixture-missing.csv' names "
         "'sources/measurements/fixture-missing.csv', which is not a file in the repository"],
    ),
    "raw-data-locator-file-url": (
        [sub(_MEAS, _RAW_LOCATOR, "locator: file:///fixture/run.log")],
        [f"{_MEAS}: raw_data[0].locator 'file:///fixture/run.log' must be an http(s) URL "
         "or a repo-relative path"],
    ),
    # --- raw_data: external-repository form (repo + commit) -----------------
    "raw-data-external-repo-without-commit": (
        [sub(_MEAS, _RAW_LOCATOR, f"repo: {_EXT_REPO}\n  locator: fixture/run.log")],
        [f"{_MEAS}: raw_data[0] has 'repo' but is missing 'commit' {_EXT_BOTH}"],
    ),
    "raw-data-external-commit-without-repo": (
        [sub(_MEAS, _RAW_LOCATOR, f"commit: {_EXT_COMMIT}\n  {_RAW_LOCATOR}")],
        [f"{_MEAS}: raw_data[0] has 'commit' but is missing 'repo' {_EXT_BOTH}"],
    ),
    "raw-data-external-commit-short": (
        [sub(_MEAS, _RAW_LOCATOR, _external(commit="0123abc"))],
        [f"{_MEAS}: raw_data[0].commit '0123abc' is not acceptable {_EXT_COMMIT_HINT}"],
    ),
    "raw-data-external-commit-41-hex": (
        [sub(_MEAS, _RAW_LOCATOR, _external(commit=_EXT_COMMIT + "0"))],
        [f"{_MEAS}: raw_data[0].commit '{_EXT_COMMIT}0' is not acceptable {_EXT_COMMIT_HINT}"],
    ),
    "raw-data-external-commit-not-hex": (
        [sub(_MEAS, _RAW_LOCATOR, _external(commit="g" * 40))],
        [f"{_MEAS}: raw_data[0].commit '{'g' * 40}' is not acceptable {_EXT_COMMIT_HINT}"],
    ),
    "raw-data-external-commit-unquoted-digits": (
        [sub(_MEAS, _RAW_LOCATOR, _external(commit="1" * 40))],
        [f"{_MEAS}: raw_data[0].commit must be a string, got int: {'1' * 40} {_EXT_COMMIT_HINT}"],
    ),
    "raw-data-external-repo-not-https": (
        [sub(_MEAS, _RAW_LOCATOR, _external(repo="http://example.invalid/fixture/repo"))],
        [f"{_MEAS}: raw_data[0].repo 'http://example.invalid/fixture/repo' is not acceptable "
         f"{_EXT_REPO_HINT}"],
    ),
    "raw-data-external-repo-local-path": (
        [sub(_MEAS, _RAW_LOCATOR, _external(repo="fixture/local/checkout"))],
        [f"{_MEAS}: raw_data[0].repo 'fixture/local/checkout' is not acceptable {_EXT_REPO_HINT}"],
    ),
    "raw-data-external-locator-absolute": (
        [sub(_MEAS, _RAW_LOCATOR, _external(locator="/fixture/run.log"))],
        [f"{_MEAS}: raw_data[0].locator '/fixture/run.log' must be repo-relative, "
         "not an absolute or home path"],
    ),
    "raw-data-external-locator-home": (
        [sub(_MEAS, _RAW_LOCATOR, _external(locator="'~/fixture/run.log'"))],
        [f"{_MEAS}: raw_data[0].locator '~/fixture/run.log' must be repo-relative, "
         "not an absolute or home path"],
    ),
    "raw-data-external-locator-parent": (
        [sub(_MEAS, _RAW_LOCATOR, _external(locator="fixture/../run.log"))],
        [f"{_MEAS}: raw_data[0].locator 'fixture/../run.log' must not contain '..'"],
    ),
    "raw-data-external-locator-url": (
        [sub(_MEAS, _RAW_LOCATOR, _external(locator="https://example.invalid/fixture/run.log"))],
        [f"{_MEAS}: raw_data[0].locator 'https://example.invalid/fixture/run.log' must be a path "
         "relative to the external repository root, not a URL"],
    ),
    "raw-data-external-locator-only-a-fragment": (
        [sub(_MEAS, _RAW_LOCATOR, _external(locator="'#row-0'"))],
        [f"{_MEAS}: raw_data[0].locator '#row-0' must name a file before '#'"],
    ),
    # --- PR excerpt ---------------------------------------------------------
    "pr-excerpt-empty": (
        [sub(_PR1, _EXCERPT + "\n", "\n")], [f"{_PR1}: {_EXCERPT_EMPTY}"],
    ),
    "pr-excerpt-only-a-comment": (
        [sub(_PR1, _EXCERPT, "<!-- FIXTURE nothing -->")], [f"{_PR1}: {_EXCERPT_EMPTY}"],
    ),
    "pr-excerpt-only-an-empty-fence": (
        [sub(_PR1, _EXCERPT, "```glsl\n```")], [f"{_PR1}: {_EXCERPT_EMPTY}"],
    ),
    "pr-excerpt-markers-reversed": (
        [sub(_PR1, "<!-- upstream-excerpt-start -->\n", ""),
         sub(_PR1, "<!-- upstream-excerpt-end -->\n",
             "<!-- upstream-excerpt-end -->\n<!-- upstream-excerpt-start -->\n")],
        [f"{_PR1}: body excerpt end marker appears before the start marker"],
    ),
    # --- code blocks --------------------------------------------------------
    "python-fence-with-prose": (
        [sub(_TECH, _FENCE_BLOCK,
             "```python\nFIXTURE prose: we return the value here.\nThen we return again, for the loop.\n```\n")],
        [f"{_TECH}: wiki-technique page must contain fenced code block (reproducibility >= snippet)"],
    ),
    "yaml-fence-with-prose": (
        [sub(_TECH, _FENCE_BLOCK,
             "```yaml\nFIXTURE prose with a void and an int in it.\nA second line of prose, return included.\n```\n")],
        [f"{_TECH}: wiki-technique page must contain fenced code block (reproducibility >= snippet)"],
    ),
}

# Changes to the valid root that must still validate cleanly.
ACCEPTED_MUTATIONS = {
    "kernel-page-without-claims": [sub(_KERNEL, _CLAIMS_BLOCK, "performance_claims: []\n")],
    "raw-data-locator-url": [
        sub(_MEAS, _RAW_LOCATOR, "locator: https://example.invalid/fixture/run.log#row-0"),
    ],
    # External form: the file is not looked up inside the wiki root.
    "raw-data-external-entry": [sub(_MEAS, _RAW_LOCATOR, _external())],
    "raw-data-external-entry-with-fragment": [
        sub(_MEAS, _RAW_LOCATOR, _external(locator="fixture/run.csv#row-0")),
    ],
    "raw-data-external-commit-quoted-digits": [
        sub(_MEAS, _RAW_LOCATOR, _external(commit="'" + "1" * 40 + "'")),
    ],
    "raw-data-external-and-in-repo-entries": [
        sub(_MEAS, _RAW_LOCATOR,
            _external() + "\n  description: FIXTURE external row\n- " + _RAW_LOCATOR),
    ],
    "pr-excerpt-inside-a-fence": [sub(_PR1, _EXCERPT, "```glsl\n" + _EXCERPT + "\n```")],
    "python-fence-with-code": [
        sub(_TECH, _FENCE_BLOCK,
            "```python\ndef fixture_function(value):\n    return value + 1\n```\n"),
    ],
    "shell-fence-with-commands": [
        sub(_TECH, _FENCE_BLOCK,
            "```bash\nglslc -fshader-stage=compute fixture.glsl -o fixture.spv\nspirv-val fixture.spv\n```\n"),
    ],
    "yaml-fence-with-data": [
        sub(_TECH, _FENCE_BLOCK, "```yaml\nfixture_key: fixture-value\nfixture_list:\n  - one\n```\n"),
    ],
    "non-page-file-next-to-pages": [
        write("sources/measurements/fixture-run/fixture-raw.csv", "fixture,units\n0,999999.0\n"),
        sub(_MEAS, _RAW_LOCATOR, "locator: sources/measurements/fixture-run/fixture-raw.csv"),
    ],
}


class MutationTest(RuleTest):
    def mutated_root(self, mutations, data_overrides=None):
        root = self.copy_root(VALID, data_overrides)
        for mutate in mutations:
            mutate(root)
        return root

    def test_mutation_cases(self):
        for case, (mutations, expected) in MUTATION_CASES.items():
            with self.subTest(case=case):
                root = self.mutated_root(mutations)
                if expected is not None:
                    self.assert_rejected(root, expected)
                    continue
                proc = run_script("validate.py", root=root)
                self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
                errors = error_lines(proc.stdout)
                self.assertEqual(len(errors), 1, errors)
                self.assertTrue(errors[0].startswith(f"ERROR: {_MIGRATION}: YAML parse error: "), errors)

    def test_accepted_mutations(self):
        for case, mutations in ACCEPTED_MUTATIONS.items():
            with self.subTest(case=case):
                proc = run_script("validate.py", root=self.mutated_root(mutations))
                self.assertEqual(error_lines(proc.stdout), [])
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_validator_never_prints_a_traceback(self):
        for case, (mutations, _expected) in MUTATION_CASES.items():
            with self.subTest(case=case):
                proc = run_script("validate.py", root=self.mutated_root(mutations))
                self.assertNotIn("Traceback", proc.stderr)
                self.assertTrue(summary_line(proc.stdout).startswith("Validated "), proc.stdout)

    def test_non_utf8_page_is_reported_by_the_index_generator(self):
        root = self.mutated_root([append_bytes(_MIGRATION, b"\xff")])
        proc = run_script("generate-indices.py", root=root)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(f"{_MIGRATION}: not valid UTF-8", proc.stdout)
        self.assertNotIn("Traceback", proc.stderr)


# ---------------------------------------------------------------------------
# 3b'. scripts/check_external_locators.py against a throwaway git repository
# ---------------------------------------------------------------------------

_FAKE_COMMIT = "f" * 40


class ExternalLocatorScriptTest(MutationTest):
    """The external checkout is a tiny git repository created under tests/.tmp;
    the real evidence checkout is never used. The wiki root is always a
    mutated copy of the valid fixture root."""

    def git(self, repo, *args):
        env = dict(
            os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
            GIT_AUTHOR_NAME="FIXTURE", GIT_AUTHOR_EMAIL="fixture@example.invalid",
            GIT_COMMITTER_NAME="FIXTURE", GIT_COMMITTER_EMAIL="fixture@example.invalid",
        )
        for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            env.pop(name, None)
        proc = subprocess.run(["git", "-C", str(repo), *args], env=env,
                              capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc.stdout.strip()

    def make_checkout(self):
        """A git repository with two commits. Returns (path, first sha, second sha):
        fixture/run.csv exists in both, fixture/later.csv only in the second."""
        repo = self.scratch_dir()
        self.git(repo, "init", "--quiet")
        (repo / "fixture").mkdir()
        (repo / "fixture" / "run.csv").write_text("fixture,units\n0,999999.0\n", encoding="utf-8")
        self.git(repo, "add", "fixture/run.csv")
        self.git(repo, "commit", "--quiet", "--no-gpg-sign", "-m", "FIXTURE first")
        first = self.git(repo, "rev-parse", "HEAD")
        (repo / "fixture" / "later.csv").write_text("fixture,units\n", encoding="utf-8")
        self.git(repo, "add", "fixture/later.csv")
        self.git(repo, "commit", "--quiet", "--no-gpg-sign", "-m", "FIXTURE second")
        return repo, first, self.git(repo, "rev-parse", "HEAD")

    def wiki_root(self, *entries):
        """Valid fixture root whose measurement page carries `entries` as
        external raw_data entries (each an _external(...) string)."""
        block = "\n  description: FIXTURE external row\n- ".join(entries)
        return self.mutated_root([sub(_MEAS, _RAW_LOCATOR, block)])

    def check(self, root, checkout, *extra):
        proc = run_script("check_external_locators.py", "--checkout", str(checkout), *extra, root=root)
        self.assertNotIn("Traceback", proc.stderr)
        return proc

    def test_existing_files_pass(self):
        checkout, first, second = self.make_checkout()
        root = self.wiki_root(
            _external(commit=first, locator="fixture/run.csv"),
            _external(commit=second, locator="fixture/later.csv#row-0"),
        )
        self.assertEqual(run_script("validate.py", root=root).returncode, 0)
        proc = self.check(root, checkout)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(proc.stdout.strip(),
                         "Checked 2 external locator(s) (0 skipped for another repo): 0 failure(s)")

    def test_missing_file_fails_with_one_line_per_failure(self):
        checkout, first, second = self.make_checkout()
        root = self.wiki_root(
            _external(commit=second, locator="fixture/missing.csv#row-0"),
            _external(commit=second, locator="fixture/run.csv"),
            # Exists in the second commit only: the check is per commit.
            _external(commit=first, locator="fixture/later.csv"),
            # A directory is not a file.
            _external(commit=second, locator="fixture"),
        )
        proc = self.check(root, checkout)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertEqual(proc.stdout.splitlines(), [
            f"FAIL: {_MEAS}: raw_data[0]: 'fixture/missing.csv' does not exist at {second} in {_EXT_REPO}",
            f"FAIL: {_MEAS}: raw_data[2]: 'fixture/later.csv' does not exist at {first} in {_EXT_REPO}",
            f"FAIL: {_MEAS}: raw_data[3]: 'fixture' is not a file at {second} in {_EXT_REPO}",
            "Checked 4 external locator(s) (0 skipped for another repo): 3 failure(s)",
        ])

    def test_unknown_commit_is_exit_2(self):
        checkout, _first, _second = self.make_checkout()
        root = self.wiki_root(_external(commit=_FAKE_COMMIT, locator="fixture/run.csv"))
        proc = self.check(root, checkout)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn(f"does not contain commit(s) {_FAKE_COMMIT}", proc.stderr)
        self.assertEqual(proc.stdout, "")

    def test_repo_filter(self):
        checkout, first, _second = self.make_checkout()
        other = "https://example.invalid/fixture/other"
        root = self.wiki_root(
            _external(commit=first, locator="fixture/missing.csv"),
            # Another repository, and a commit this checkout does not have.
            _external(repo=other, commit=_FAKE_COMMIT, locator="fixture/run.csv"),
        )
        # Selected repo: its entry is checked, the other one is skipped.
        for url in (_EXT_REPO, _EXT_REPO + ".git", _EXT_REPO + "/"):
            with self.subTest(url=url):
                proc = self.check(root, checkout, "--repo", url)
                self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
                self.assertEqual(proc.stdout.splitlines(), [
                    f"FAIL: {_MEAS}: raw_data[0]: 'fixture/missing.csv' does not exist at {first} "
                    f"in {_EXT_REPO}",
                    "Checked 1 external locator(s) (1 skipped for another repo): 1 failure(s)",
                ])
        # A repo no entry uses: nothing is checked.
        proc = self.check(root, checkout, "--repo", "https://example.invalid/fixture/unused")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(proc.stdout.strip(),
                         "Checked 0 external locator(s) (2 skipped for another repo): 0 failure(s)")
        # The other repo: its commit is not in this checkout.
        self.assertEqual(self.check(root, checkout, "--repo", other).returncode, 2)
        # No filter: every external entry is checked, so the unknown commit stops the run.
        self.assertEqual(self.check(root, checkout).returncode, 2)

    def test_in_repo_entries_are_ignored(self):
        checkout, _first, _second = self.make_checkout()
        proc = self.check(VALID, checkout)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(proc.stdout.strip(),
                         "Checked 0 external locator(s) (0 skipped for another repo): 0 failure(s)")

    def test_malformed_entry_is_a_failure(self):
        checkout, first, _second = self.make_checkout()
        root = self.wiki_root(
            _external(commit=first, locator="../fixture/run.csv"),
            f"repo: {_EXT_REPO}\n  locator: fixture/run.csv",
        )
        proc = self.check(root, checkout)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertEqual(proc.stdout.splitlines(), [
            f"FAIL: {_MEAS}: raw_data[0]: malformed entry: raw_data[0].locator '../fixture/run.csv' "
            "must not contain '..'",
            f"FAIL: {_MEAS}: raw_data[1]: malformed entry: raw_data[1] has 'repo' but is missing "
            f"'commit' {_EXT_BOTH}",
            "Checked 2 external locator(s) (0 skipped for another repo): 2 failure(s)",
        ])

    def test_checkout_must_be_a_git_repository(self):
        root = self.wiki_root(_external())
        # A scratch directory outside any work tree would be ideal; tests/.tmp sits
        # inside the wiki repository, so point at a path that is not a directory
        # and at the filesystem root instead.
        proc = self.check(root, self.scratch_dir() / "no-such-checkout")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("is not a directory", proc.stderr)
        proc = run_script("check_external_locators.py", root=root)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("--checkout", proc.stderr)

    def test_invalid_wiki_root_is_a_hard_error(self):
        proc = self.check(TESTS_DIR, TESTS_DIR)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("does not point at a valid wiki root", proc.stderr)


# ---------------------------------------------------------------------------
# 3c. Data-file rules
# ---------------------------------------------------------------------------

_TREE_HEADER = "architectures:\n  amd:\n    kind: vendor\n    children:\n"
BAD_TREES = {
    "device-with-children": (
        _TREE_HEADER + "      radeon-780m:\n        kind: device\n        children:\n"
        "          fixture-sub:\n            kind: device\n",
        "data/architectures.yaml: device node 'radeon-780m' must not have children",
    ),
    "vendor-under-vendor": (
        _TREE_HEADER + "      fixture-sub:\n        kind: vendor\n",
        "data/architectures.yaml: node 'fixture-sub' of kind 'vendor' cannot be a child of "
        "'amd' of kind 'vendor'",
    ),
    "generation-under-generation": (
        _TREE_HEADER + "      rdna3:\n        kind: generation\n        children:\n"
        "          fixture-sub:\n            kind: generation\n",
        "data/architectures.yaml: node 'fixture-sub' of kind 'generation' cannot be a child of "
        "'rdna3' of kind 'generation'",
    ),
    "root-is-a-device": (
        "architectures:\n  fixture-root:\n    kind: device\n",
        "data/architectures.yaml: root node 'fixture-root' must be of kind 'vendor', got 'device'",
    ),
    "duplicate-node": (
        _TREE_HEADER + "      rdna3:\n        kind: generation\n        children:\n"
        "          amd:\n            kind: device\n",
        "data/architectures.yaml: duplicate node name 'amd'",
    ),
}
_EMPTY_PAGES = TESTS_DIR / "no-such-pages"  # assemble_root then creates empty wiki/ and sources/


class DataFileTest(RuleTest):
    def test_malformed_architecture_tree(self):
        for case, (tree, message) in BAD_TREES.items():
            with self.subTest(case=case):
                root = self.assemble_root(_EMPTY_PAGES, {"architectures.yaml": tree, "aliases.yaml": "{}\n"})
                self.assert_rejected(root, [message])
                for script, args in (("query.py", ["--architecture", "amd"]),
                                     ("generate-indices.py", []), ("repo_status.py", [])):
                    proc = run_script(script, *args, root=root)
                    self.assertEqual(proc.returncode, 2, script + proc.stdout + proc.stderr)
                    self.assertIn(message, proc.stderr)

    def test_missing_architecture_tree_is_an_error_everywhere(self):
        root = self.assemble_root(VALID, {"architectures.yaml": None})
        proc = run_script("validate.py", root=root)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("ERROR: data/architectures.yaml: missing (architecture tree is required)",
                      error_lines(proc.stdout))
        for script, args in (("query.py", ["--architecture", "amd"]),
                             ("generate-indices.py", []), ("repo_status.py", [])):
            with self.subTest(script=script):
                proc = run_script(script, *args, root=root)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn("data/architectures.yaml: missing", proc.stderr)
        self.assertEqual(list((root / "queries").iterdir()), [])

    def test_tags_yaml_must_not_define_architectures(self):
        tags = (REAL_DATA / "tags.yaml").read_text(encoding="utf-8") + "\narchitectures: [amd]\n"
        root = self.assemble_root(VALID, {"tags.yaml": tags})
        self.assert_rejected(root, [
            "data/tags.yaml: must not define 'architectures' "
            "(the architecture tree lives in data/architectures.yaml)",
        ])

    def test_version_claims_registry_needs_its_claims_key(self):
        root = self.assemble_root(VALID, {"version-claims.yaml": "fixture_other_key: []\n"})
        self.assert_rejected(root, ["data/version-claims.yaml: missing top-level key 'claims'"])

    def test_schema_keys_are_read_by_the_validator(self):
        # Every constraint key in data/schemas.yaml must appear in validate.py,
        # so the yaml file cannot grow keys that nothing enforces.
        schemas = yaml.safe_load((REAL_DATA / "schemas.yaml").read_text(encoding="utf-8"))
        source = (SCRIPTS / "validate.py").read_text(encoding="utf-8")
        keys = set()

        def walk(node, inside_constraints):
            if isinstance(node, dict):
                for key, value in node.items():
                    if inside_constraints:
                        keys.add(key)
                    walk(value, key == "constraints")

        walk(schemas, False)
        self.assertIn("candidate_techniques_id_prefixes", keys)
        for section in ("performance-claim", "verified_evidence_rule", "version-claims-registry"):
            keys.update(k for k in schemas[section] if k not in ("required", "optional", "constraints"))
        keys.update(("required", "optional", "raw_data_schema", "claim_schema"))
        # These two are looked up as f"{field}_required_min".
        dynamic = {"applies_to_required_min", "source_ids_required_min"}
        self.assertIn('f"{field}_required_min"', source)
        for key in sorted(keys - dynamic):
            self.assertIn(f'"{key}"', source, f"data/schemas.yaml key '{key}' is not read by validate.py")


# ---------------------------------------------------------------------------
# 3d. Command-line edge cases
# ---------------------------------------------------------------------------

class CommandLineTest(TempRoots):
    def test_empty_architecture_is_an_argument_error(self):
        for value in ("", "   "):
            with self.subTest(value=value):
                proc = run_script("query.py", "--architecture", value, "--paths-only", root=VALID)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertEqual(proc.stdout, "")
                self.assertIn("--architecture requires a non-empty node name or alias", proc.stderr)

    def test_get_page_stays_inside_the_root(self):
        outside = self.scratch_dir() / "fixture-outside.md"
        outside.write_text("FIXTURE-OUTSIDE-CONTENT\n", encoding="utf-8")
        relative = os.path.relpath(outside, VALID)
        self.assertTrue(relative.startswith(".."))
        for lookup in (relative, str(outside), "wiki/../../valid/../" + relative):
            with self.subTest(lookup=lookup):
                proc = run_script("get_page.py", lookup, root=VALID)
                self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
                self.assertNotIn("FIXTURE-OUTSIDE-CONTENT", proc.stdout)
        proc = run_script("get_page.py", _KERNEL, root=VALID)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("id: kernel-fixture-linear", proc.stdout)
        proc = run_script("get_page.py", "wiki/hardware/../kernels/fixture-kernel.md", root=VALID)
        self.assertEqual(proc.returncode, 0, proc.stderr)


# ---------------------------------------------------------------------------
# 4. Architecture-tree query semantics
# ---------------------------------------------------------------------------

# Architecture tags carried by the pages of the valid root.
TAGGED = {
    "amd": {_DOC, _HW},
    "rdna3": {"sources/blogs/fixture-blog.md", f"{_PR}/pr-1.md", _TECH},
    "radeon-780m": {_MEAS, _KERNEL},
    "rx-7600": {"wiki/patterns/fixture-pattern.md"},
    "arc-b580": {"wiki/languages/fixture-language.md"},
}


class ArchitectureQueryTest(unittest.TestCase):
    def query(self, *args):
        proc = run_script("query.py", *args, "--paths-only", "--limit", "100", root=VALID)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return set(proc.stdout.split()), proc.stderr

    def test_vendor_matches_all_descendants(self):
        paths, stderr = self.query("--architecture", "amd")
        self.assertEqual(paths, TAGGED["amd"] | TAGGED["rdna3"] | TAGGED["radeon-780m"] | TAGGED["rx-7600"])
        self.assertNotIn("excluded", stderr)

    def test_generation_excludes_vendor_only_pages(self):
        paths, stderr = self.query("--architecture", "rdna3")
        self.assertEqual(paths, TAGGED["rdna3"] | TAGGED["radeon-780m"] | TAGGED["rx-7600"])
        self.assertIn(
            "Architecture filter 'rdna3' excluded 2 page(s) tagged only with an ancestor (amd)", stderr
        )
        self.assertIn("use --architecture amd for the broader set", stderr)

    def test_no_broader_set_advice_when_nothing_was_excluded(self):
        _paths, stderr = self.query("--architecture", "xe2")
        self.assertIn("Architecture filter 'xe2' excluded 0 page(s) tagged only with an ancestor (intel).",
                      stderr)
        self.assertNotIn("broader set", stderr)

    def test_device_excludes_ancestor_only_pages(self):
        paths, stderr = self.query("--architecture", "radeon-780m")
        self.assertEqual(paths, TAGGED["radeon-780m"])
        self.assertIn(
            "Architecture filter 'radeon-780m' excluded 5 page(s) tagged only with an ancestor (rdna3, amd)",
            stderr,
        )

    def test_alias_resolves_before_matching(self):
        for alias in ("780M", "Phoenix"):
            with self.subTest(alias=alias):
                paths, stderr = self.query("--architecture", alias)
                self.assertEqual(paths, TAGGED["radeon-780m"])
                self.assertIn(f"Architecture '{alias}' resolved to 'radeon-780m'.", stderr)
                self.assertIn("excluded 5 page(s) tagged only with an ancestor (rdna3, amd)", stderr)

    def test_generation_alias(self):
        paths, stderr = self.query("--architecture", "Battlemage")
        self.assertEqual(paths, TAGGED["arc-b580"])
        self.assertIn("Architecture 'Battlemage' resolved to 'xe2'.", stderr)
        self.assertIn("excluded 0 page(s) tagged only with an ancestor (intel)", stderr)

    def test_exclusion_count_respects_other_filters(self):
        paths, stderr = self.query("--architecture", "780M", "--type", "measurement")
        self.assertEqual(paths, {_MEAS})
        self.assertIn("excluded 0 page(s)", stderr)

    def test_unknown_architecture_warns(self):
        paths, stderr = self.query("--architecture", "fixture-unknown-gpu")
        self.assertEqual(paths, set())
        self.assertIn("WARNING", stderr)

    def test_tree_helpers_on_real_tree(self):
        code = (
            "import json, sys; sys.path.insert(0, sys.argv[1]); import arch_policy as a; "
            "print(json.dumps({'anc': a.ancestors('radeon-780m'), 'desc': a.descendants('amd'), "
            "'devices': a.devices(), 'kinds': {n: k for n, _, k in a.tree_order()}, "
            "'childless': [n for n in a.all_nodes() if not a.children(n)]}))"
        )
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        env.pop("VK_KERNEL_WIKI_ROOT", None)
        proc = subprocess.run([sys.executable, "-S", "-c", code, str(SCRIPTS)],
                              env=env, capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        info = json.loads(proc.stdout)
        self.assertEqual(info["anc"], ["rdna3", "amd"])
        self.assertEqual(info["desc"], ["rdna3", "radeon-780m", "rx-7900-xtx", "rx-7600"])
        self.assertEqual(sum(1 for k in info["kinds"].values() if k == "vendor"), 6)
        # A vendor without children is a reserved node, never a device.
        reserved = [n for n in info["childless"] if info["kinds"][n] == "vendor"]
        self.assertEqual(len(reserved), 1)
        self.assertNotIn(reserved[0], info["devices"])
        for node in info["childless"]:
            if node not in reserved:
                self.assertEqual(info["kinds"][node], "device")


# ---------------------------------------------------------------------------
# 5. Pull-request intake: policy, ledger refresh and page generation (offline)
# ---------------------------------------------------------------------------

FIXTURE_REPO = "example-org/example-repo"
FIXTURE_LEDGER = (
    f"repo: {FIXTURE_REPO}\n"
    "keywords_used:\n- fixture in:title\n"
    "license: MIT\n"
    "shader_path_markers:\n- fixture-shaders/\n"
    "host_path_markers:\n- fixture-backend\n"
    "prs: []\n"
)


def fixture_evidence(number, title, filenames, body="FIXTURE synthetic description.", removed=()):
    return {
        "repo": FIXTURE_REPO,
        "fetched_at": "2000-01-02",
        "pr": {
            "number": number, "title": title, "body": body, "author": "fixture-author",
            "html_url": f"https://example.invalid/{FIXTURE_REPO}/pull/{number}",
            "state": "closed", "merged": True, "merged_at": "2000-01-01T00:00:00Z",
            "created_at": "2000-01-01T00:00:00Z", "closed_at": "2000-01-01T00:00:00Z",
            "merge_commit_sha": "0123456789abcdef0123456789abcdef01234567",
            "changed_files": len(filenames),
        },
        "files": [
            {"filename": name, "status": "removed" if name in removed else "modified", "patch": "+x"}
            for name in filenames
        ],
    }


class PrPolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import pr_policy
        cls.policy = pr_policy
        cls.vocab = yaml.safe_load((REAL_DATA / "tags.yaml").read_text(encoding="utf-8"))
        cls.config = pr_policy.PathConfig(("fixture-shaders/",), ("fixture_embedded.py",), ("fixture-backend",))

    def scope(self, *names, removed=()):
        files = [{"filename": n, "status": "removed" if n in removed else "modified"} for n in names]
        return self.policy.classify_scope(files, self.config)

    def test_shader_source_is_included(self):
        decision = self.scope("src/fixture-shaders/a.comp", "src/fixture-backend.cpp")
        self.assertEqual((decision.decision, decision.rule), ("include", "glsl-shader-source"))
        self.assertEqual(decision.evidence_paths, ("src/fixture-shaders/a.comp",))

    def test_embedded_shader_source_is_included(self):
        decision = self.scope("tools/fixture_embedded.py", "src/fixture-backend.cpp")
        self.assertEqual(decision.decision, "include")
        self.assertEqual(decision.evidence_paths, ("tools/fixture_embedded.py",))

    def test_kernel_type_patterns(self):
        for name, expected in (
            ("ssm_conv.comp", []), ("conv2d_mm.comp", ["convolution"]), ("rope_norm.comp", ["rope"]),
            ("rms_norm.comp", ["normalization"]), ("topk_moe.comp", ["moe", "topk-sort"]),
            ("dequant_q4_k.comp", ["dequantize"]), ("add.comp", ["elementwise"]), ("copy.comp", ["tensor-copy"]),
        ):
            with self.subTest(name=name):
                files = [{"filename": f"src/fixture-shaders/{name}"}]
                meta = self.policy.derive_metadata("FIXTURE", files, self.vocab, self.config)
                self.assertEqual(meta["kernel_types"], expected)

    def test_techniques_only_from_explicit_wording(self):
        def techniques(title, *names):
            files = [{"filename": f"src/fixture-shaders/{n}"} for n in names] or [{"filename": "src/fixture-shaders/x.comp"}]
            return self.policy.derive_metadata(title, files, self.vocab, self.config)["techniques"]
        self.assertEqual(techniques("FIXTURE change"), [])
        self.assertEqual(techniques("FIXTURE: tune matmul tile for a device"), ["workgroup-tile-sizing", "device-specific-tuning"])
        self.assertEqual(techniques("FIXTURE", "mul_mat_split_k_reduce.comp"), ["split-k-reduction"])
        self.assertEqual(techniques("FIXTURE workaround for a compiler bug"), ["driver-workaround"])
        self.assertEqual(techniques("FIXTURE", "convolution_pack4_3x3s1d1_winograd_gemm.comp"),
                         ["winograd-convolution", "channel-packing"])
        self.assertEqual(techniques("FIXTURE confused fortune textiles"), [])

    def test_host_source_only_is_deferred(self):
        decision = self.scope("src/fixture-backend.cpp", "docs/readme.md")
        self.assertEqual((decision.decision, decision.rule), ("defer", "backend-host-source-only"))

    def test_everything_else_is_excluded(self):
        for names, removed in (
            (("docs/readme.md",), ()),
            (("other/dir/a.comp",), ()),                         # shader outside the marked path
            (("src/fixture-backend/CMakeLists.txt",), ()),       # build file, not host source
            (("src/fixture-shaders/a.comp",), ("src/fixture-shaders/a.comp",)),  # removal only
        ):
            with self.subTest(names=names):
                self.assertEqual(self.scope(*names, removed=removed).decision, "exclude")

    def test_architectures_come_from_the_title(self):
        nodes, evidence = self.policy.derive_architectures("FIXTURE kernel for AMD RDNA3 and Intel")
        self.assertEqual(nodes, ["rdna3", "intel"])  # tree order; 'amd' dropped for its descendant
        self.assertEqual([row["locator"] for row in evidence], ["title", "title"])
        self.assertEqual(self.policy.derive_architectures("FIXTURE alarm64 charm")[0], [])

    def test_architectures_from_code_markers(self):
        markers = {"FIXTURE_ID_AMD": "amd", "FIXTURE_ARCH_RDNA3": "rdna3", "FIXTURE_ID_NONE": "fixture-unknown-node"}
        added = [{"filename": "src/a.cpp", "patch": "@@ -1 +1,2 @@\n ctx\n+if (id == FIXTURE_ID_AMD) {}"}]
        self.assertEqual(
            self.policy.derive_architectures("FIXTURE change", added, markers),
            (["amd"], [{"node": "amd", "locator": "added-patch:src/a.cpp", "matched": "FIXTURE_ID_AMD"}]),
        )
        # Code that is only moved adds and removes the marker equally often.
        moved = [
            {"filename": "src/a.cpp", "patch": "@@\n-if (id == FIXTURE_ID_AMD) {}"},
            {"filename": "src/b.cpp", "patch": "@@\n+if (id == FIXTURE_ID_AMD) {}"},
        ]
        self.assertEqual(self.policy.derive_architectures("FIXTURE change", moved, markers)[0], [])
        # A marker inside a longer identifier, or mapped to a name that is not a node, never counts.
        other = [{"filename": "src/a.cpp", "patch": "@@\n+X_FIXTURE_ID_AMD_2 FIXTURE_ID_NONE"}]
        self.assertEqual(self.policy.derive_architectures("FIXTURE change", other, markers)[0], [])
        # The title and the code agree on a descendant: the ancestor is dropped.
        both = [{"filename": "src/a.cpp", "patch": "@@\n+FIXTURE_ID_AMD FIXTURE_ARCH_RDNA3"}]
        self.assertEqual(self.policy.derive_architectures("FIXTURE for AMD", both, markers)[0], ["rdna3"])

    def test_driver_mode_needs_topic_and_driver_path(self):
        config = self.policy.PathConfig.from_ledger({
            "scope_mode": "driver",
            "driver_path_markers": ["src/fixture-driver/"],
            "topic_patterns": ["fixture[ -]topic"],
        })
        files = [{"filename": "src/fixture-driver/a.c"}, {"filename": "src/other/b.c"}]
        hit = self.policy.classify_scope(files, config, "FIXTURE topic change")
        self.assertEqual((hit.decision, hit.rule), ("include", "driver-source-on-topic"))
        self.assertEqual(hit.evidence_paths, ("src/fixture-driver/a.c",))
        self.assertEqual(self.policy.classify_scope(files, config, "FIXTURE other change").rule, "no-topic-in-title")
        self.assertEqual(self.policy.classify_scope(files[1:], config, "FIXTURE topic change").rule, "no-driver-path")
        # In driver mode the saved files are the ones under the driver paths.
        self.assertEqual([f["filename"] for f in self.policy.shader_files(files, config)], ["src/fixture-driver/a.c"])
        with self.assertRaises(ValueError):
            self.policy.PathConfig.from_ledger({"scope_mode": "fixture"})

    def test_architectures_from_changed_paths(self):
        files = [{"filename": "src/fixture-amd/a.c"}, {"filename": "src/gone/b.c", "status": "removed"}]
        markers = {"src/fixture-amd/": "amd", "src/gone/": "intel", "src/absent/": "nvidia"}
        self.assertEqual(
            self.policy.derive_architectures("FIXTURE", files, path_markers=markers),
            (["amd"], [{"node": "amd", "locator": "changed-path:src/fixture-amd/a.c", "matched": "src/fixture-amd/"}]),
        )

    def test_c_and_header_languages(self):
        def languages(*names):
            files = [{"filename": n} for n in names]
            return self.policy.derive_metadata("FIXTURE", files, self.vocab, self.config)["languages"]
        self.assertEqual(languages("a.c", "a.h"), ["c"])
        self.assertEqual(languages("a.cpp", "a.h"), ["cpp"])
        self.assertEqual(languages("a.h"), ["cpp"])

    def test_gitlab_merge_request_is_normalized(self):
        import pr_evidence
        mr = {
            "iid": 7, "title": "FIXTURE merge request", "description": "FIXTURE text", "state": "merged",
            "web_url": "https://example.invalid/g/p/-/merge_requests/7", "merged_at": "2000-01-03T00:00:00Z",
            "created_at": "2000-01-01T00:00:00Z", "merge_commit_sha": None, "squash_commit_sha": None,
            "sha": "0123456789abcdef0123456789abcdef01234567", "author": {"username": "fixture-author"},
        }
        diffs = [
            {"new_path": "a.c", "old_path": "a.c", "diff": "@@ -1 +1 @@\n-x\n+y\n"},
            {"new_path": "b.c", "old_path": "b.c", "new_file": True, "diff": "@@ -0,0 +1 @@\n+z\n"},
            {"new_path": "d.c", "old_path": "c.c", "renamed_file": True, "diff": ""},
        ]
        evidence = pr_evidence.normalize_gitlab("g/p", mr, diffs, "2000-01-04")
        self.assertEqual(evidence["pr"]["number"], 7)
        self.assertTrue(evidence["pr"]["merged"])
        self.assertEqual(evidence["pr"]["merge_commit_sha"], mr["sha"])  # fast-forward merge: the head commit
        self.assertEqual(evidence["pr"]["author"], "fixture-author")
        self.assertEqual(
            [(f["filename"], f["status"], f["patch"]) for f in evidence["files"]],
            [("a.c", "modified", "@@ -1 +1 @@\n-x\n+y"), ("b.c", "added", "@@ -0,0 +1 @@\n+z"), ("d.c", "renamed", None)],
        )
        self.assertEqual(pr_evidence.request_noun({"forge": "gitlab", "gitlab_api": "https://example.invalid/api/v4"}),
                         "merge request")
        with self.assertRaises(pr_evidence.EvidenceError):
            pr_evidence.forge_of({"forge": "gitlab"})
        with self.assertRaises(pr_evidence.EvidenceError):
            pr_evidence.forge_of({"forge": "fixture"})

    def test_reserved_vendor_is_never_emitted(self):
        import arch_policy
        reserved = [
            n for n in arch_policy.all_nodes()
            if arch_policy.node_kind(n) == "vendor" and not arch_policy.children(n)
        ]
        self.assertTrue(reserved)
        self.assertEqual(self.policy.derive_architectures(f"FIXTURE {reserved[0]} tile")[0], [])

    def test_metadata_only_uses_the_vocabulary(self):
        files = [{"filename": "src/fixture-shaders/mul_mm_cm2.comp"}, {"filename": "src/fixture-backend.cpp"}]
        meta = self.policy.derive_metadata("FIXTURE change", files, self.vocab, self.config)
        self.assertEqual(meta["hardware_features"], ["cooperative-matrix", "cooperative-matrix2"])
        self.assertEqual(meta["kernel_types"], ["gemm"])
        self.assertEqual(meta["languages"], ["glsl", "cpp"])
        self.assertEqual(meta["techniques"], [])
        self.assertEqual(meta["tags"], ["cooperative-matrix", "cooperative-matrix2", "gemm", "glsl", "cpp"])
        bare = self.policy.derive_metadata("FIXTURE change", files, {"languages": ["glsl"]}, self.config)
        self.assertEqual(bare["tags"], ["glsl"])

    def test_excerpt_is_a_bounded_verbatim_prefix(self):
        body = "line one\r\n" + "x" * 2000
        excerpt, total = self.policy.upstream_excerpt(body)
        self.assertEqual(total, len("line one\n") + 2000)
        self.assertEqual(len(excerpt), self.policy.UPSTREAM_EXCERPT_LIMIT)
        self.assertTrue(body.replace("\r\n", "\n").startswith(excerpt))
        forged, _ = self.policy.upstream_excerpt("a <!-- upstream-excerpt-end --> b")
        self.assertNotIn(self.policy.EXCERPT_END, forged)
        self.assertTrue(self.policy.excerpt_is_empty("<!-- template -->\n```\n```"))


class PrPipelineTest(TempRoots):
    """refresh_candidate_ledger.py --offline and generate-pr-pages.py --offline
    against a temporary root with a synthetic ledger and evidence cache."""

    def make_root(self):
        root = self.assemble_root(TESTS_DIR / "no-such-pages", {"pr-page-skipped.yaml": None})
        (root / "candidates").mkdir()
        (root / "candidates" / "fixture-repo.yaml").write_text(
            FIXTURE_LEDGER.replace("prs: []\n", "prs:\n" + "".join(f"- number: {n}\n" for n in (1, 2, 3, 4))),
            encoding="utf-8",
        )
        cache = root / ".cache" / "pr-evidence" / "fixture-repo"
        cache.mkdir(parents=True)
        for evidence in (
            fixture_evidence(1, "FIXTURE coopmat kernel for RDNA3", ["src/fixture-shaders/mul_mm_cm2.comp"]),
            fixture_evidence(2, "FIXTURE host change", ["src/fixture-backend.cpp"]),
            fixture_evidence(3, "FIXTURE docs", ["docs/readme.md"]),
            fixture_evidence(4, "FIXTURE shader without description", ["src/fixture-shaders/b.comp"], body=""),
        ):
            (cache / f"{evidence['pr']['number']}.json").write_text(json.dumps(evidence), encoding="utf-8")
        return root

    def test_offline_refresh_and_generation(self):
        root = self.make_root()
        proc = run_script("refresh_candidate_ledger.py", "--cutoff", "2000-01-31", "--offline",
                          "--reclassify", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        ledger = yaml.safe_load((root / "candidates" / "fixture-repo.yaml").read_text(encoding="utf-8"))
        self.assertEqual([row["decision"] for row in ledger["prs"]], ["include", "defer", "exclude", "include"])
        self.assertEqual((ledger["included"], ledger["deferred"], ledger["excluded"]), (2, 1, 1))
        self.assertEqual(list(ledger)[-1], "prs")

        (root / "artifacts" / "prs" / "fixture-repo").mkdir(parents=True)
        (root / "artifacts" / "prs" / "fixture-repo" / "LICENSE").write_text("FIXTURE licence text\n", encoding="utf-8")
        proc = run_script("fetch_pr_diff.py", "--offline", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        proc = run_script("generate-pr-pages.py", "--offline", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        pages = sorted(p.name for p in (root / "sources" / "prs" / "fixture-repo").glob("*.md"))
        self.assertEqual(pages, ["PR-1.md", "PR-4.md"])
        # An empty description is replaced by the title, and the locator says so.
        untitled = (root / "sources" / "prs" / "fixture-repo" / "PR-4.md").read_text(encoding="utf-8")
        self.assertIn("(pull request title, complete; the pull request description is empty)", untitled)
        self.assertIn("<!-- upstream-excerpt-start -->\nFIXTURE shader without description\n", untitled)
        fm = load_frontmatter(root / "sources" / "prs" / "fixture-repo" / "PR-1.md")
        self.assertEqual(fm["id"], "pr-fixture-repo-1")
        self.assertEqual(fm["architectures"], ["rdna3"])
        self.assertEqual(fm["architecture_evidence"], [{"node": "rdna3", "locator": "title", "matched": "RDNA3"}])
        self.assertEqual(fm["captured_at"], "2000-01-02")
        self.assertEqual(fm["artifact_dir"], "artifacts/prs/fixture-repo/PR-1")
        bundle = root / "artifacts" / "prs" / "fixture-repo"
        self.assertEqual(sorted(p.name for p in bundle.iterdir()), ["LICENSE", "PR-1", "PR-4"])
        patch = (bundle / "PR-1" / "shaders.patch").read_text(encoding="utf-8")
        self.assertEqual(patch.splitlines()[-1], "+x")
        proc = run_script("verify_verbatim.py", "--against-cache", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(summary_line(proc.stdout),
                         "Verified 2 artifact bundle(s), 0 without cached evidence: 0 error(s)")
        proc = run_script("grep_wiki.py", "^\\+x$", "--only", "artifacts", "--files-only", root=root)
        self.assertIn("PR-1/shaders.patch", proc.stdout)
        self.assertFalse((root / "data" / "pr-page-skipped.yaml").exists())

        proc = run_script("validate.py", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(summary_line(proc.stdout), "Validated 2 pages (2 source, 0 wiki): 0 error(s)")

        # A second run changes nothing; a manual decision survives --reclassify.
        before = (root / "sources" / "prs" / "fixture-repo" / "PR-1.md").read_bytes()
        proc = run_script("generate-pr-pages.py", "--offline", "--force", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual((root / "sources" / "prs" / "fixture-repo" / "PR-1.md").read_bytes(), before)
        ledger["prs"][1].update(decision="include", decision_source="manual")
        (root / "candidates" / "fixture-repo.yaml").write_text(yaml.safe_dump(ledger, sort_keys=False),
                                                              encoding="utf-8")
        run_script("refresh_candidate_ledger.py", "--cutoff", "2000-01-31", "--offline", "--reclassify", root=root)
        ledger = yaml.safe_load((root / "candidates" / "fixture-repo.yaml").read_text(encoding="utf-8"))
        self.assertEqual(ledger["prs"][1]["decision"], "include")

    def test_driver_ledger_writes_driver_patch(self):
        root = self.make_root()
        (root / "candidates" / "fixture-repo.yaml").unlink()
        (root / "candidates" / "fixture-driver.yaml").write_text(
            "repo: example-org/example-driver\nforge: gitlab\ngitlab_api: https://example.invalid/api/v4\n"
            "license: MIT\nlicense_path: LICENSE\nscope_mode: driver\nkeywords_used:\n- fixture\n"
            "driver_path_markers:\n- src/fixture-amd/\ntopic_patterns:\n- fixture topic\n"
            "architecture_path_markers:\n  src/fixture-amd/: amd\nprs:\n- number: 9\n", encoding="utf-8")
        cache = root / ".cache" / "pr-evidence" / "fixture-driver"
        cache.mkdir(parents=True)
        evidence = fixture_evidence(9, "FIXTURE topic in the driver", ["src/fixture-amd/a.c", "docs/readme.md"])
        (cache / "9.json").write_text(json.dumps(evidence), encoding="utf-8")
        (root / "artifacts" / "prs" / "fixture-driver").mkdir(parents=True)
        (root / "artifacts" / "prs" / "fixture-driver" / "LICENSE").write_text("FIXTURE\n", encoding="utf-8")
        for script in ("refresh_candidate_ledger.py --cutoff 2000-01-31 --reclassify", "fetch_pr_diff.py",
                       "generate-pr-pages.py"):
            name, *args = script.split()
            proc = run_script(name, *args, "--offline", root=root)
            self.assertEqual(proc.returncode, 0, script + proc.stdout + proc.stderr)
        bundle = root / "artifacts" / "prs" / "fixture-driver" / "PR-9"
        self.assertEqual(sorted(p.name for p in bundle.iterdir()), ["PROVENANCE.yaml", "driver.patch"])
        provenance = yaml.safe_load((bundle / "PROVENANCE.yaml").read_text(encoding="utf-8"))
        self.assertEqual(provenance["patch_file"], "driver.patch")
        self.assertEqual([f["path"] for f in provenance["files"]], ["src/fixture-amd/a.c"])
        self.assertIn("GitLab REST API", provenance["origin"])
        page = root / "sources" / "prs" / "fixture-driver" / "PR-9.md"
        fm = load_frontmatter(page)
        self.assertEqual((fm["architectures"], fm["languages"], fm["kernel_types"]), (["amd"], ["c"], []))
        self.assertIn("(merge request description, complete)", page.read_text(encoding="utf-8"))
        self.assertEqual(run_script("validate.py", root=root).returncode, 0)
        self.assertEqual(run_script("verify_verbatim.py", "--against-cache", root=root).returncode, 0)

    def test_tampered_or_missing_artifact_is_reported(self):
        root = self.make_root()
        (root / "artifacts" / "prs" / "fixture-repo").mkdir(parents=True)
        (root / "artifacts" / "prs" / "fixture-repo" / "LICENSE").write_text("FIXTURE\n", encoding="utf-8")
        for script in ("refresh_candidate_ledger.py --cutoff 2000-01-31 --reclassify", "fetch_pr_diff.py",
                       "generate-pr-pages.py"):
            name, *args = script.split()
            self.assertEqual(run_script(name, *args, "--offline", root=root).returncode, 0, script)
        patch = root / "artifacts" / "prs" / "fixture-repo" / "PR-1" / "shaders.patch"
        patch.write_text(patch.read_text(encoding="utf-8").replace("+x", "+y"), encoding="utf-8")
        proc = run_script("verify_verbatim.py", root=root)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("does not match its recorded sha256", proc.stdout)
        shutil.rmtree(patch.parent)
        proc = run_script("validate.py", root=root)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("artifact_dir 'artifacts/prs/fixture-repo/PR-1' has no PROVENANCE.yaml", proc.stdout)

    def test_kernel_bundle_integrity(self):
        import hashlib
        root = self.make_root()
        bundle = root / "artifacts" / "kernels" / "fixture-kernels"
        bundle.mkdir(parents=True)
        (root / "artifacts" / "prs" / "fixture-repo").mkdir(parents=True)
        (root / "artifacts" / "prs" / "fixture-repo" / "LICENSE").write_text("FIXTURE\n", encoding="utf-8")
        (bundle / "a.comp").write_text("FIXTURE shader text\n", encoding="utf-8")
        digest = hashlib.sha256(b"FIXTURE shader text\n").hexdigest()
        (bundle / "PROVENANCE.yaml").write_text(yaml.safe_dump({
            "repo": FIXTURE_REPO, "commit": "0123456789abcdef0123456789abcdef01234567", "license": "MIT",
            "license_file": "artifacts/prs/fixture-repo/LICENSE", "retrieved_at": "2000-01-02",
            "files": [{"path": "src/fixture-shaders/a.comp", "file": "a.comp", "sha256": digest}],
        }), encoding="utf-8")
        proc = run_script("verify_verbatim.py", root=root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(summary_line(proc.stdout), "Verified 0 artifact bundle(s), 1 kernel bundle(s): 0 error(s)")
        (bundle / "a.comp").write_text("FIXTURE changed\n", encoding="utf-8")
        (bundle / "stray.comp").write_text("FIXTURE\n", encoding="utf-8")
        proc = run_script("verify_verbatim.py", root=root)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("'a.comp' does not match its recorded sha256", proc.stdout)
        self.assertIn("'stray.comp' is not listed in PROVENANCE.yaml", proc.stdout)

    def test_real_artifacts_are_intact(self):
        proc = run_script("verify_verbatim.py")
        self.assertEqual(proc.returncode, 0, proc.stdout[-2000:] + proc.stderr)

    def test_missing_evidence_is_not_a_page(self):
        root = self.make_root()
        shutil.rmtree(root / ".cache")
        run_script("refresh_candidate_ledger.py", "--cutoff", "2000-01-31", "--offline", "--reclassify", root=root)
        ledger = yaml.safe_load((root / "candidates" / "fixture-repo.yaml").read_text(encoding="utf-8"))
        self.assertEqual({row["rule"] for row in ledger["prs"]}, {"evidence-unavailable"})
        self.assertEqual({row["decision"] for row in ledger["prs"]}, {"defer"})

    def test_real_ledgers_and_pages_agree(self):
        skipped_file = REAL_DATA / "pr-page-skipped.yaml"
        skipped = set()
        if skipped_file.is_file():
            rows = (yaml.safe_load(skipped_file.read_text(encoding="utf-8")) or {}).get("rows") or []
            skipped = {(row["repo"], row["pr"]) for row in rows}
        for path in sorted((REPO_ROOT / "candidates").glob("*.yaml")):
            ledger = yaml.safe_load(path.read_text(encoding="utf-8"))
            included = {row["number"] for row in ledger["prs"] if row["decision"] == "include"}
            pages = {
                int(p.stem.split("-")[1]) for p in (REPO_ROOT / "sources" / "prs" / path.stem).glob("PR-*.md")
            }
            without_page = {n for n in included if (ledger["repo"], n) in skipped}
            with self.subTest(ledger=path.name):
                self.assertEqual(pages, included - without_page)
                self.assertEqual(ledger["included"], len(included))
                self.assertEqual(ledger["total_candidates"], len(ledger["prs"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
