#!/usr/bin/env python3
"""Validate wiki and source pages against data/schemas.yaml and the vocabulary.

Usage:
    python3 -S scripts/validate.py

Checks every Markdown page under wiki/ and sources/ plus the data files that
pages depend on (aliases, architecture tree, version-claims registry).
Exit code 0 when clean, 1 when at least one error was found. Each error is
printed as "  ERROR: <relpath>: <message>", followed by a one-line summary.

The wiki root is resolved by scripts/_wiki_root.py, so VK_KERNEL_WIKI_ROOT can
point the validator at another root. Derived from KernelWiki's validate.py.
"""

import datetime
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _yaml_compat import yaml  # noqa: E402
from _wiki_root import WIKI_ROOT  # noqa: E402
import arch_policy  # noqa: E402

REPO_ROOT = WIKI_ROOT
SOURCES_DIR = REPO_ROOT / "sources"
WIKI_DIR = REPO_ROOT / "wiki"
DATA_DIR = REPO_ROOT / "data"

REPRO_ORDER = ["concept", "pseudocode", "snippet", "runnable", "benchmarked"]
TOPICAL_GROUPS = ["hardware_features", "techniques", "kernel_types", "languages"]
LIST_FIELDS = [
    "tags", "techniques", "hardware_features", "kernel_types", "languages",
    "architectures", "related", "sources", "symptoms", "candidate_techniques",
    "prerequisites", "aliases", "changed_paths",
]
# Fields whose entries are page ids that must resolve to an existing page.
PAGE_ID_FIELDS = ["related", "prerequisites", "candidate_techniques"]
# Frontmatter fields that hold exactly one string.
SCALAR_STRING_FIELDS = [
    "id", "type", "confidence", "reproducibility", "source_category", "status",
    "device", "from_arch", "to_arch",
]
CODE_PAGE_TYPES = ("wiki-technique", "wiki-kernel", "wiki-language")

SOURCE_DIR_TYPES = {
    "prs": "source-pr",
    "docs": "source-doc",
    "blogs": "source-blog",
    "measurements": "source-measurement",
}
WIKI_DIR_TYPES = {
    "hardware": "wiki-hardware",
    "techniques": "wiki-technique",
    "patterns": "wiki-pattern",
    "kernels": "wiki-kernel",
    "languages": "wiki-language",
    "migration": "wiki-migration",
}

_FRONTMATTER_RE = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|\Z)", re.DOTALL)
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def load_yaml_file(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def rel_path(path):
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def split_page(filepath):
    """Return (frontmatter, body). Frontmatter is None when absent and
    {'_parse_error': ...} when it is not valid YAML."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"_read_error": "not valid UTF-8"}, ""
    except OSError as exc:
        return {"_read_error": f"unreadable ({exc.strerror or exc})"}, ""
    match = _FRONTMATTER_RE.match(content)
    if not match:
        return None, content
    try:
        fm = yaml.safe_load(match.group(1))
    except (yaml.YAMLError, ValueError) as exc:  # ValueError: impossible date
        fm = {"_parse_error": " ".join(str(exc).split())}
    return fm, content[match.end():]


def detect_page_type(filepath):
    """Detect the page type from the path alone (sources/<dir>, wiki/<dir>).

    A page outside the known directories is 'unknown'; the frontmatter 'type'
    field never decides the page type.
    """
    parts = filepath.relative_to(REPO_ROOT).parts
    subdir = parts[1] if len(parts) > 2 else ""
    if parts[0] == "sources":
        return SOURCE_DIR_TYPES.get(subdir, "unknown")
    if parts[0] == "wiki":
        return WIKI_DIR_TYPES.get(subdir, "unknown")
    return "unknown"


def is_iso_date(value):
    if isinstance(value, datetime.datetime):
        return False  # a timestamp is not a date
    if isinstance(value, datetime.date):
        return True
    if isinstance(value, str) and _ISO_DATE_RE.match(value):
        try:
            datetime.date.fromisoformat(value)
            return True
        except ValueError:
            return False
    return False


def is_number(value):
    """A finite int or float (bool, NaN and infinity are rejected)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value)


def hashable_in(value, collection):
    """Membership test that treats unhashable values (lists, mappings) as absent."""
    try:
        return value in collection
    except TypeError:
        return False


_URL_RE = re.compile(r"^https?://\S+$")


def locator_error(value, root):
    """Why `value` is not an acceptable raw-data locator, or None when it is.

    Accepted: an http(s) URL, or a path relative to the wiki root (optionally
    followed by '#fragment') that names an existing file inside the root.
    """
    if _URL_RE.match(value):
        return None
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return "must be an http(s) URL or a repo-relative path"
    problem, path = relative_locator_error(value)
    if problem:
        return problem
    if not (root / path).is_file():
        return f"names '{path}', which is not a file in the repository"
    return None


def relative_locator_error(value):
    """Why `value` is not a relative path locator (optionally followed by
    '#fragment'), or None when it is. Returns (problem, path)."""
    path = value.split("#", 1)[0].strip()
    if not path:
        return "must name a file before '#'", path
    if path.startswith(("/", "~", "\\")):
        return "must be repo-relative, not an absolute or home path", path
    if ".." in path.replace("\\", "/").split("/"):
        return "must not contain '..'", path
    return None, path


def external_locator_error(value):
    """Why `value` is not an acceptable locator inside an external repository
    (an entry that carries 'repo' and 'commit'), or None when it is.

    Accepted: a path relative to that repository's root, optionally followed
    by '#fragment'. Whether the file exists at the commit is not checked here;
    scripts/check_external_locators.py does that against a local checkout.
    """
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return "must be a path relative to the external repository root, not a URL"
    return relative_locator_error(value)[0]


def external_entry_errors(entry, label, spec):
    """constraints.external_locator: the fields in together_fields are all
    present or all absent, and each matches its pattern. Returns
    (is_external, errors)."""
    fields = spec.get("together_fields") or []
    present = [f for f in fields if f in entry]
    if not present:
        return False, []
    errors = []
    for field in fields:
        if field not in entry:
            errors.append(
                f"{label} has '{present[0]}' but is missing '{field}' "
                f"(an external-repository entry needs {' and '.join(fields)})"
            )
    for field, pspec in (spec.get("pattern_fields") or {}).items():
        if field not in entry:
            continue
        pspec = pspec if isinstance(pspec, dict) else {"pattern": pspec}
        hint = f" ({pspec['hint']})" if pspec.get("hint") else ""
        value = entry[field]
        if not isinstance(value, str):
            errors.append(
                f"{label}.{field} must be a string, got {type(value).__name__}: {value!r}{hint}"
            )
        elif not re.search(str(pspec.get("pattern", "")), value):
            errors.append(f"{label}.{field} '{value}' is not acceptable{hint}")
    return True, errors


def non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def repro_at_least(level, minimum):
    if level not in REPRO_ORDER or minimum not in REPRO_ORDER:
        return False
    return REPRO_ORDER.index(level) >= REPRO_ORDER.index(minimum)


def pointer_id(value):
    """A version_sensitive pointer is a bare id string or a mapping with 'id'."""
    return value.get("id") if isinstance(value, dict) else value


# ---------------------------------------------------------------------------
# Compilable-code check (reproducibility >= snippet)
# ---------------------------------------------------------------------------

_BASE_CODE_LANGS = {
    "glsl", "glslh", "comp", "spirv", "spvasm", "c", "c++", "cpp", "python",
    "py", "shell", "bash", "sh", "cmake", "yaml", "json",
}

# Patterns that indicate real code (not prose, pseudocode or ASCII diagrams),
# per fence-language family. A block must match the family of its own fence.
_GLSL_INDICATORS = (
    r"#version|#extension|\blayout\s*\(|\buniform\b|\bbuffer\b|void\s+main|"
    r"\b[iu]?vec[234]\b|\bf16vec[234]\b|\bmat[234]\b|\bcoopmat\b|"
    r"\bimageLoad\b|\bimageStore\b|\btexelFetch\b|\bshared\b|gl_\w+"
)
_C_INDICATORS = (
    r"#include|#define|#pragma|\bvoid\b|\bint\b|\buint\b|\bfloat\b|"
    r"\buint32_t\b|\buint64_t\b|\bstruct\b|\btypedef\b|\btemplate\b|"
    r"\bnamespace\b|\busing\b|\bauto\b|\bconstexpr\b|"
    r"\bfor\s*\(|\bwhile\s*\(|\bif\s*\(|return\s|"
    r"(?:\w+::)+\w+|\w+(?:\.|->)\w+\s*\("
)
# Line-anchored: a prose sentence that merely contains 'return' is not Python.
_PYTHON_INDICATORS = (
    r"^\s*(?:def\s+\w+\s*\(|class\s+\w+|import\s+\w+|from\s+[\w.]+\s+import\b|"
    r"for\s+\w+.*\bin\b.*:\s*$|(?:if|elif|while|with)\s+.+:\s*$|@\w+|"
    r"[A-Za-z_][\w.\[\]]*\s*[-+*/]?=\s*\S|[A-Za-z_][\w.]*\(.*\)\s*$)"
)
_SPIRV_INDICATORS = r"\bOp[A-Z]\w+"
_SHELL_INDICATORS = (
    r"^\s*(?:\$\s+)?(?:glslc|glslangValidator|spirv-\w+|cmake|python3?|bash|sh|"
    r"cd|export|make|ninja|git)(?:\s|$)|^\s*(?:\$\s+)?\./\S+|"
    r"^\s*[A-Za-z_]\w*=\S|^\s*\w+\s*\(|\s-{1,2}[A-Za-z]"
)
# yaml / json: a 'key: value' line or an opening bracket.
_DATA_INDICATORS = r"^\s*(?:-\s+)?[\"']?[\w.-]+[\"']?\s*:(?:\s|$)|^\s*[\[{]"

_FAMILY_PATTERNS = {
    "glsl": re.compile(f"{_GLSL_INDICATORS}|{_C_INDICATORS}", re.MULTILINE),
    "c": re.compile(_C_INDICATORS, re.MULTILINE),
    "python": re.compile(_PYTHON_INDICATORS, re.MULTILINE),
    "spirv": re.compile(_SPIRV_INDICATORS, re.MULTILINE),
    "shell": re.compile(_SHELL_INDICATORS, re.MULTILINE),
    "data": re.compile(_DATA_INDICATORS, re.MULTILINE),
}
_LANG_FAMILY = {
    "glsl": "glsl", "glslh": "glsl", "comp": "glsl",
    "c": "c", "c++": "c", "cpp": "c",
    "python": "python", "py": "python",
    "spirv": "spirv", "spvasm": "spirv",
    "shell": "shell", "bash": "shell", "sh": "shell", "cmake": "shell",
    "yaml": "data", "json": "data",
}
# A vocabulary language without a family of its own may match any family.
_ANY_INDICATORS = re.compile(
    "|".join(f"(?:{p})" for p in (
        _GLSL_INDICATORS, _C_INDICATORS, _PYTHON_INDICATORS, _SPIRV_INDICATORS,
        _SHELL_INDICATORS, _DATA_INDICATORS,
    )),
    re.MULTILINE,
)


def load_code_langs(vocab):
    return _BASE_CODE_LANGS | {str(v).lower() for v in vocab.get("languages") or []}


def has_compilable_code(body, code_langs):
    """True when the body has a fenced block in a known language that contains
    real code for that language and at least 2 non-blank, non-comment lines."""
    for m in re.finditer(r"^```(\S*)[^\n]*\n(.*?)\n```", body, re.MULTILINE | re.DOTALL):
        lang = m.group(1).lower()
        if lang not in code_langs:
            continue
        block = m.group(2)
        indicators = _FAMILY_PATTERNS.get(_LANG_FAMILY.get(lang), _ANY_INDICATORS)
        if not indicators.search(block):
            continue
        code_lines = [
            line for line in (raw.strip() for raw in block.split("\n"))
            if line and not line.startswith("//") and not line.startswith("#")
        ]
        if len(code_lines) >= 2:
            return True
    return False


# ---------------------------------------------------------------------------
# Generic schema-driven sub-checks
# ---------------------------------------------------------------------------

def pattern_field_errors(entry, label, constraints):
    """constraints.pattern_fields: {field: {pattern, hint}} on string fields."""
    errors = []
    for field, spec in (constraints.get("pattern_fields") or {}).items():
        value = entry.get(field)
        if not non_empty_string(value):
            continue  # absence / emptiness is reported by other checks
        spec = spec if isinstance(spec, dict) else {"pattern": spec}
        if not re.search(str(spec.get("pattern", "")), value):
            hint = f" ({spec['hint']})" if spec.get("hint") else ""
            errors.append(f"{label}{field} '{value}' is not acceptable{hint}")
    return errors


def mapping_errors(entry, label, schema, source_ids=None, device_nodes=None):
    """Check one mapping (performance claim, raw_data entry, registry claim)
    against a {required, optional, constraints} schema section."""
    errors = []
    constraints = schema.get("constraints") or {}
    required = schema.get("required") or []
    allowed = set(required) | set(schema.get("optional") or [])
    for field in required:
        if field not in entry or entry[field] is None:
            errors.append(f"{label} missing '{field}'")
    for field in entry:
        if field not in allowed:
            errors.append(f"{label} has unknown field '{field}'")
    for field in constraints.get("numeric_fields") or []:
        if entry.get(field) is not None and not is_number(entry[field]):
            what = "a finite number" if isinstance(entry[field], float) else "numeric"
            errors.append(
                f"{label}.{field} must be {what}, got "
                f"{type(entry[field]).__name__}: {entry[field]}"
            )
    for field in constraints.get("date_fields") or []:
        if entry.get(field) is not None and not is_iso_date(entry[field]):
            errors.append(f"{label}.{field} must be an ISO date (YYYY-MM-DD), got {entry[field]!r}")
    for field in constraints.get("non_empty_string_fields") or []:
        if entry.get(field) is not None and not non_empty_string(entry[field]):
            errors.append(f"{label}.{field} must be a non-empty string")
    errors.extend(pattern_field_errors(entry, f"{label}.", constraints))
    if device_nodes is not None:
        for field in constraints.get("device_node_fields") or []:
            value = entry.get(field)
            if non_empty_string(value) and value not in device_nodes:
                errors.append(
                    f"{label}.{field} '{value}' is not a device node in data/architectures.yaml"
                )
    # An entry carrying the external_locator fields points into another git
    # repository: its locator is checked for form only, not for existence here.
    external_spec = constraints.get("external_locator") or {}
    is_external, external_errors = external_entry_errors(entry, label, external_spec)
    errors.extend(external_errors)
    unchecked = external_spec.get("skip_exists_check_fields") or [] if is_external else []
    for field in constraints.get("locator_fields") or []:
        if non_empty_string(entry.get(field)):
            if field in unchecked:
                problem = external_locator_error(entry[field])
            else:
                problem = locator_error(entry[field], REPO_ROOT)
            if problem:
                errors.append(f"{label}.{field} '{entry[field]}' {problem}")
    if constraints.get("source_id_must_resolve") and source_ids is not None:
        sid = entry.get("source_id")
        if sid is not None and not hashable_in(sid, source_ids):
            errors.append(f"{label}.source_id '{sid}' not found in source corpus")
    return errors


def list_of_mappings_errors(value, field, schema, source_ids=None, minimum=0, device_nodes=None):
    if not isinstance(value, list):
        return [f"{field} must be a list, got {type(value).__name__}"]
    errors = []
    if len(value) < minimum:
        errors.append(f"{field} must contain at least {minimum} entry")
    for i, entry in enumerate(value):
        if not isinstance(entry, dict):
            errors.append(f"{field}[{i}] must be a mapping, got {type(entry).__name__}")
            continue
        errors.extend(mapping_errors(entry, f"{field}[{i}]", schema, source_ids, device_nodes))
    return errors


def evidence_errors(fm, rule, vocab, id_types, id_categories):
    """evidence_basis structure plus the 'verified' confidence rule."""
    errors = []
    field = rule.get("evidence_field", "evidence_basis")
    when = rule.get("applies_when") or {}
    applies = fm.get(when.get("field", "confidence")) == when.get("value", "verified")
    eb = fm.get(field)
    if eb is None and not applies:
        return errors
    minimum = rule.get("evidence_required_min", 1)
    if not isinstance(eb, list) or (applies and len(eb) < minimum):
        if applies:
            return [f"confidence 'verified' requires a non-empty '{field}' list"]
        return [f"field '{field}' must be a YAML list, got {type(eb).__name__}"]

    valid_types = set(vocab.get("evidence_types") or [])
    sources_field = rule.get("source_id_must_be_in", "sources")
    page_sources = fm.get(sources_field)
    page_sources = set(s for s in page_sources if isinstance(s, str)) if isinstance(page_sources, list) else set()
    allowed = set(rule.get("entry_required") or []) | set(rule.get("entry_optional") or [])
    alternatives = rule.get("any_of") or []
    # evidence_type -> what the cited source page must be (page type and/or
    # source_category), as demanded by the rule's alternatives.
    bound = {
        req["evidence_type"]: req
        for alt in alternatives for req in alt.get("require") or []
        if req.get("source_page_type") or req.get("source_category")
    }

    def binding_problem(req, sid):
        """Why source `sid` cannot back an entry of this requirement, or None."""
        want_type, want_cat = req.get("source_page_type"), req.get("source_category")
        if want_type and id_types.get(sid) != want_type:
            return f"to be a {want_type} page (it is {id_types.get(sid)})"
        if want_cat and id_categories.get(sid) != want_cat:
            return f"to have source_category '{want_cat}' (it has {id_categories.get(sid)!r})"
        return None
    entries = []
    for i, entry in enumerate(eb):
        label = f"{field}[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be a mapping, got {type(entry).__name__}")
            continue
        entries.append(entry)
        for req in rule.get("entry_required") or []:
            if not non_empty_string(entry.get(req)):
                errors.append(f"{label} missing '{req}'")
        for key in entry:
            if key not in allowed:
                errors.append(f"{label} has unknown field '{key}'")
        etype, sid = entry.get("evidence_type"), entry.get("source_id")
        if not isinstance(etype, str) or not isinstance(sid, str):
            continue  # already reported as missing
        if etype not in valid_types:
            errors.append(f"{label}.evidence_type '{etype}' is not a valid evidence type")
        if sid not in page_sources:
            errors.append(f"{label}.source_id '{sid}' is not listed in the page's '{sources_field}'")
        if etype in bound and sid in id_types:
            problem = binding_problem(bound[etype], sid)
            if problem:
                errors.append(
                    f"{label}: evidence_type '{etype}' requires source_id '{sid}' {problem}"
                )

    if not applies:
        return errors

    def satisfied(req):
        count = sum(
            1 for e in entries
            if e.get("evidence_type") == req.get("evidence_type")
            and isinstance(e.get("source_id"), str)
            and binding_problem(req, e["source_id"]) is None
        )
        return count >= req.get("min_count", 1)

    if alternatives and not any(
        all(satisfied(req) for req in alt.get("require") or []) for alt in alternatives
    ):
        names = [alt.get("name", "?") for alt in alternatives]
        found = sorted({str(e.get("evidence_type")) for e in entries})
        errors.append(
            f"confidence 'verified' is not supported by {field}: needs one of "
            f"{names} (found evidence types: {found})"
        )
    return errors


def excerpt_text(excerpt):
    """The excerpt with HTML comments and code-fence delimiter lines removed."""
    text = re.sub(r"<!--.*?-->", "", excerpt, flags=re.DOTALL)
    text = re.sub(r"^[ \t]*(?:```|~~~)[^\n]*$", "", text, flags=re.MULTILINE)
    return text.strip()


def source_pr_errors(fm, body, constraints):
    errors = []
    pattern = constraints.get("merge_sha_pattern", "^[0-9a-f]{40}$")
    when = str(constraints.get("merge_sha_required_when", "status == merged"))
    when_field, _, when_value = (part.strip() for part in when.partition("=="))
    merge_sha = fm.get("merge_sha")
    if fm.get(when_field) == when_value and merge_sha is None:
        errors.append("merged PR requires a full 40-hex merge_sha")
    elif merge_sha is not None and not re.fullmatch(pattern, str(merge_sha)):
        errors.append(f"merge_sha '{merge_sha}' must be a full 40-hex commit sha")

    if constraints.get("body_excerpt_required"):
        start = constraints.get("body_excerpt_start_marker", "<!-- upstream-excerpt-start -->")
        end = constraints.get("body_excerpt_end_marker", "<!-- upstream-excerpt-end -->")
        s, e = body.find(start), body.find(end)
        if s < 0:
            errors.append(f"body is missing the excerpt marker '{start}'")
        if e < 0:
            errors.append(f"body is missing the excerpt marker '{end}'")
        if s >= 0 and e >= 0:
            if e < s:
                errors.append("body excerpt end marker appears before the start marker")
            elif not excerpt_text(body[s + len(start):e]):
                errors.append("body excerpt between the upstream-excerpt markers is empty")
    return errors


# ---------------------------------------------------------------------------
# Per-page validation
# ---------------------------------------------------------------------------

def validate_page(page, ctx):
    """Validate one page. Returns messages without the '<relpath>: ' prefix."""
    fm, body, page_type = page["fm"], page["body"], page["type"]
    schemas, vocab = ctx["schemas"], ctx["vocab"]
    errors = []

    if page_type == "unknown":
        return [
            "unknown page type (pages must live in sources/{"
            + ",".join(SOURCE_DIR_TYPES) + "}/ or wiki/{" + ",".join(WIKI_DIR_TYPES) + "}/)"
        ]
    schema = schemas.get(page_type)
    if not schema:
        return [f"no schema defined for type '{page_type}'"]
    constraints = schema.get("constraints") or {}
    required = schema.get("required") or []

    for field in required:
        if field not in fm or fm[field] is None:
            errors.append(f"missing required field '{field}'")
    declared = set(required) | set(schema.get("optional") or [])
    for field in fm:
        if field not in declared:
            errors.append(f"unknown field '{field}' for {page_type}")

    # Scalar fields must be strings. A wrongly typed one is reported once and
    # then ignored, so the remaining checks still run on the rest of the page.
    fm = dict(fm)
    for field in SCALAR_STRING_FIELDS:
        if fm.get(field) is not None and not isinstance(fm[field], str):
            errors.append(f"field '{field}' must be a string, got {type(fm[field]).__name__}")
            del fm[field]

    id_prefix = constraints.get("id_prefix")
    if id_prefix and "id" in fm and not str(fm["id"]).startswith(id_prefix):
        errors.append(f"id '{fm['id']}' must start with '{id_prefix}'")

    # List type, string entries and uniqueness for every list-valued field.
    lists = {}
    for field in LIST_FIELDS:
        if fm.get(field) is None:
            continue
        value = fm[field]
        if not isinstance(value, list):
            errors.append(f"field '{field}' must be a YAML list, got {type(value).__name__}")
            continue
        seen, clean = set(), []
        for item in value:
            if not isinstance(item, str):
                errors.append(f"field '{field}' entries must be strings, got {type(item).__name__}: {item}")
                continue
            if item in seen:
                errors.append(f"duplicate value '{item}' in field '{field}'")
            seen.add(item)
            clean.append(item)
        lists[field] = clean

    # Per-field vocabulary. 'tags' accepts any topical term.
    field_vocab = {group: set(vocab.get(group) or []) for group in TOPICAL_GROUPS}
    field_vocab["tags"] = set().union(*field_vocab.values())
    for field in ["tags", *TOPICAL_GROUPS]:
        for value in lists.get(field, []):
            if value not in field_vocab[field]:
                errors.append(f"'{value}' is not a valid {field} value")

    if "hardware_features" in lists:
        missing_hw = (set(lists.get("tags", [])) & field_vocab["hardware_features"]) - set(lists["hardware_features"])
        if missing_hw:
            errors.append(
                f"tags contain hardware features {sorted(missing_hw)} not in hardware_features field"
            )

    remedy_prefixes = tuple(constraints.get("candidate_techniques_id_prefixes") or ())
    for ct in lists.get("candidate_techniques", []) if remedy_prefixes else []:
        if not ct.startswith(remedy_prefixes):
            errors.append(
                f"candidate_techniques entry '{ct}' must use one of {remedy_prefixes} prefixes"
            )

    # Architecture nodes (data/architectures.yaml).
    for arch in lists.get("architectures", []):
        if arch not in ctx["arch_nodes"]:
            errors.append(f"unknown architecture '{arch}'")
    for field in constraints.get("architecture_node_fields") or []:
        if fm.get(field) is not None and fm[field] not in ctx["arch_nodes"]:
            errors.append(f"{field} '{fm[field]}' is not a known architecture")

    if "confidence" in fm and fm["confidence"] not in set(vocab.get("confidence") or []):
        errors.append(f"invalid confidence '{fm['confidence']}'")

    if "reproducibility" in fm:
        repro = fm["reproducibility"]
        repro_min = constraints.get("reproducibility_minimum")
        if repro not in set(vocab.get("reproducibility") or []):
            errors.append(f"invalid reproducibility '{repro}'")
        elif repro_min and not repro_at_least(repro, repro_min):
            errors.append(f"reproducibility '{repro}' below minimum '{repro_min}' for {page_type}")

    if "source_category" in fm:
        cat = fm["source_category"]
        allowed = as_list(constraints.get("source_category"))
        if cat not in set(vocab.get("source_categories") or []):
            errors.append(f"invalid source_category '{cat}'")
        elif allowed and cat not in allowed:
            errors.append(f"source_category '{cat}' not in allowed {allowed}")

    allowed_status = as_list(constraints.get("status"))
    if allowed_status and "status" in fm and fm["status"] not in allowed_status:
        errors.append(f"status '{fm['status']}' not in {allowed_status}")

    if "type" in constraints and "type" in fm and fm["type"] != constraints["type"]:
        errors.append(
            f"type '{fm['type']}' does not match expected '{constraints['type']}' for {page_type}"
        )

    for field in constraints.get("date_fields") or []:
        if fm.get(field) is not None and not is_iso_date(fm[field]):
            errors.append(f"{field} must be an ISO date (YYYY-MM-DD), got {fm[field]!r}")
    for field in constraints.get("non_empty_string_fields") or []:
        if field in fm and fm[field] is not None and not non_empty_string(fm[field]):
            errors.append(f"{field} must be a non-empty string")
    errors.extend(pattern_field_errors(fm, "", constraints))

    if page_type == "source-pr":
        errors.extend(source_pr_errors(fm, body, constraints))

    if page_type == "source-measurement":
        if constraints.get("device_node_kind") and fm.get("device") is not None:
            kind = constraints["device_node_kind"]
            if fm["device"] not in ctx["arch_kinds"].get(kind, set()):
                errors.append(
                    f"device '{fm['device']}' is not a {kind} node in data/architectures.yaml"
                )
            elif (constraints.get("device_must_be_in")
                  and fm["device"] not in lists.get(constraints["device_must_be_in"], [])):
                errors.append(
                    f"device '{fm['device']}' must also be listed in "
                    f"'{constraints['device_must_be_in']}'"
                )
        if fm.get("raw_data") is not None:
            errors.extend(list_of_mappings_errors(
                fm["raw_data"], "raw_data", schema.get("raw_data_schema") or {},
                minimum=constraints.get("raw_data_required_min", 1),
            ))

    claim_schema = schemas.get("performance-claim") or {}
    claim_field = claim_schema.get("field", "performance_claims")
    if fm.get(claim_field) is not None:
        errors.extend(list_of_mappings_errors(
            fm[claim_field], claim_field, claim_schema, ctx["source_ids"],
            minimum=(claim_schema.get("constraints") or {}).get("required_min", 0),
            device_nodes=ctx["arch_kinds"].get("device", set()),
        ))

    rule = schemas.get("verified_evidence_rule") or {}
    if page_type.startswith(rule.get("applies_to_page_type_prefix", "wiki-")):
        for src_id in lists.get("sources", []):
            if src_id not in ctx["source_ids"]:
                errors.append(f"references unknown source id '{src_id}'")
        for field in PAGE_ID_FIELDS:
            for ref in lists.get(field, []):
                if ref not in ctx["id_types"]:
                    errors.append(f"{field} entry '{ref}' does not resolve to an existing page id")
        errors.extend(evidence_errors(fm, rule, vocab, ctx["id_types"], ctx["id_categories"]))

    if page_type in CODE_PAGE_TYPES and repro_at_least(fm.get("reproducibility", "concept"), "snippet"):
        if not has_compilable_code(body, ctx["code_langs"]):
            errors.append(f"{page_type} page must contain fenced code block (reproducibility >= snippet)")

    # version_sensitive pointer shape; resolution is checked against the registry.
    if fm.get("version_sensitive") is not None:
        vs = fm["version_sensitive"]
        ptr_schema = schemas.get("version-sensitive-pointer") or {}
        prefix = (ptr_schema.get("constraints") or {}).get("id_prefix", "vs-")
        ptr = pointer_id(vs)
        if isinstance(vs, dict):
            ptr_allowed = set(ptr_schema.get("required") or ["id"]) | set(ptr_schema.get("optional") or [])
            for key in vs:
                if key not in ptr_allowed:
                    errors.append(f"version_sensitive has unknown field '{key}'")
        if not non_empty_string(ptr):
            errors.append("version_sensitive block has no id")
        elif not ptr.startswith(prefix):
            errors.append(f"version_sensitive id '{ptr}' must start with '{prefix}'")
        elif ptr not in ctx["claims"]:
            errors.append(f"version_sensitive id '{ptr}' does not resolve to data/version-claims.yaml")
        else:
            targets = ctx["claims"][ptr].get("applies_to")
            if page["rel"] not in [str(t) for t in (targets if isinstance(targets, list) else [])]:
                errors.append(
                    f"version_sensitive id '{ptr}' resolves, but that claim's applies_to "
                    "in data/version-claims.yaml does not list this page"
                )
    return errors


# ---------------------------------------------------------------------------
# Repository-level checks (messages carry their own '<relpath>: ' prefix)
# ---------------------------------------------------------------------------

def validate_aliases(vocab, arch_nodes):
    """Reject aliases that resolve to two different canonical terms.

    Case variants under one canonical (and an alias equal to its own
    canonical) are fine; only a clash between DIFFERENT canonicals is an error.
    """
    name = "data/aliases.yaml"
    path = DATA_DIR / "aliases.yaml"
    if not path.is_file():
        return []
    try:
        raw = load_yaml_file(path) or {}
    except (OSError, yaml.YAMLError) as exc:
        return [f"{name}: could not load aliases ({' '.join(str(exc).split())})"]
    if not isinstance(raw, dict):
        return [f"{name}: top level must be a mapping"]

    known = set(arch_nodes)
    for group in TOPICAL_GROUPS:
        known.update(vocab.get(group) or [])
    resolved = {term.lower(): term for term in known}
    errors = []
    for canonical, variants in raw.items():
        if not non_empty_string(canonical):
            errors.append(f"{name}: canonical terms must be non-empty strings")
            continue
        if canonical not in known:
            errors.append(
                f"{name}: canonical '{canonical}' is not a vocabulary term or architecture node"
            )
        if variants is not None and not isinstance(variants, list):
            errors.append(f"{name}: aliases of '{canonical}' must be a list")
            continue
        for value in [canonical, *(variants or [])]:
            if not non_empty_string(value):
                errors.append(f"{name}: aliases of '{canonical}' must be non-empty strings")
                continue
            previous = resolved.setdefault(value.lower(), canonical)
            if previous != canonical:
                errors.append(f"{name}: alias '{value}' maps to both '{previous}' and '{canonical}'")
    return errors


def load_version_claims(schemas):
    """Return (claims_by_id, errors) for data/version-claims.yaml."""
    name = "data/version-claims.yaml"
    path = DATA_DIR / "version-claims.yaml"
    if not path.is_file():
        return {}, [f"{name}: missing (version-claims registry is required)"]
    try:
        data = load_yaml_file(path)
    except (OSError, yaml.YAMLError) as exc:
        return {}, [f"{name}: invalid YAML ({' '.join(str(exc).split())})"]
    registry = schemas.get("version-claims-registry") or {}
    if not isinstance(data, dict):
        return {}, [f"{name}: top level must be a mapping"]
    missing = [key for key in registry.get("required") or ["claims"] if data.get(key) is None]
    if missing:
        return {}, [f"{name}: missing top-level key '{key}'" for key in missing]
    claims = data.get("claims")
    if not isinstance(claims, list):
        return {}, [f"{name}: top-level 'claims' must be a list"]

    schema = registry.get("claim_schema") or {}
    constraints = schema.get("constraints") or {}
    errors, by_id = [], {}
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"{name}: claims[{i}] must be a mapping")
            continue
        cid = claim.get("id")
        if not non_empty_string(cid):
            errors.append(f"{name}: claims[{i}] missing 'id'")
            continue
        label = f"claim '{cid}'"
        if cid in by_id:
            errors.append(f"{name}: duplicate claim id '{cid}'")
            continue
        by_id[cid] = claim
        errors.extend(f"{name}: {msg}" for msg in mapping_errors(claim, label, schema))
        prefix = constraints.get("id_prefix")
        if prefix and not cid.startswith(prefix):
            errors.append(f"{name}: {label} id must start with '{prefix}'")
        tools = constraints.get("tool") or []
        if tools and claim.get("tool") is not None and claim["tool"] not in tools:
            errors.append(f"{name}: {label} tool '{claim['tool']}' not in {tools}")
        for field in ("applies_to", "source_ids"):
            value = claim.get(field)
            minimum = constraints.get(f"{field}_required_min", 1)
            if value is not None and (not isinstance(value, list) or len(value) < minimum):
                errors.append(f"{name}: {label} {field} must be a list with at least {minimum} entry")
    return by_id, errors


def validate_version_claims(claims, pages_by_rel, source_ids):
    """Registry -> page direction: sources resolve, targets exist and point back."""
    name = "data/version-claims.yaml"
    errors = []
    for cid, claim in claims.items():
        label = f"claim '{cid}'"
        for sid in claim.get("source_ids") if isinstance(claim.get("source_ids"), list) else []:
            if not hashable_in(sid, source_ids):
                errors.append(f"{name}: {label} source_id '{sid}' does not resolve")
        for target in claim.get("applies_to") if isinstance(claim.get("applies_to"), list) else []:
            page = pages_by_rel.get(str(target))
            if page is None:
                errors.append(f"{name}: {label} applies_to '{target}' is not an existing page")
                continue
            ptr = pointer_id(page["fm"].get("version_sensitive"))
            if ptr != cid:
                errors.append(
                    f"{name}: {label} applies_to '{target}' carries version_sensitive "
                    f"id {ptr!r}, expected '{cid}'"
                )
    return errors


def validate_discoverability(pages):
    """Each sources/prs/<dir>/ directory holds PR pages of exactly one repository."""
    errors = []
    by_dir = {}
    for page in pages:
        parts = page["rel"].split("/")
        if page["type"] == "source-pr" and len(parts) > 3 and page["fm"].get("repo"):
            by_dir.setdefault("/".join(parts[:3]), []).append(str(page["fm"]["repo"]))
    for directory, repos in sorted(by_dir.items()):
        if len(set(repos)) != 1:
            errors.append(
                f"{directory}: expected one repo identity across PR pages, found {sorted(set(repos))}"
            )
    return errors


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def load_data():
    """Load the data files every check depends on. Returns (ctx, errors)."""
    errors = []
    loaded = {}
    for key, filename in (("vocab", "tags.yaml"), ("schemas", "schemas.yaml")):
        path = DATA_DIR / filename
        try:
            loaded[key] = load_yaml_file(path)
        except OSError:
            errors.append(f"data/{filename}: missing")
        except yaml.YAMLError as exc:
            errors.append(f"data/{filename}: invalid YAML ({' '.join(str(exc).split())})")
        if not isinstance(loaded.get(key), dict):
            if key in loaded:
                errors.append(f"data/{filename}: top level must be a mapping")
            loaded[key] = {}
    if "architectures" in loaded["vocab"]:
        errors.append(
            "data/tags.yaml: must not define 'architectures' "
            "(the architecture tree lives in data/architectures.yaml)"
        )

    arch_nodes, arch_kinds = set(), {}
    if not (REPO_ROOT / arch_policy.ARCHITECTURES_FILE).is_file():
        errors.append("data/architectures.yaml: missing (architecture tree is required)")
    else:
        try:
            for node, _depth, kind in arch_policy.tree_order(REPO_ROOT):
                arch_nodes.add(node)
                arch_kinds.setdefault(kind, set()).add(node)
        except (ValueError, yaml.YAMLError) as exc:  # message names the file
            errors.append(" ".join(str(exc).split()))

    ctx = {
        "vocab": loaded["vocab"],
        "schemas": loaded["schemas"],
        "arch_nodes": arch_nodes,
        "arch_kinds": arch_kinds,
        "code_langs": load_code_langs(loaded["vocab"]),
    }
    return ctx, errors


def collect_pages():
    """Parse every page once. Returns (pages, errors)."""
    pages, errors = [], []
    for search_dir in (SOURCES_DIR, WIKI_DIR):
        if not search_dir.exists():
            continue
        for md_file in sorted(p for p in search_dir.rglob("*") if p.suffix.lower() == ".md" and p.is_file()):
            rel = rel_path(md_file)
            if md_file.suffix != ".md":
                # The other tools only see '*.md'; refuse a page they would miss.
                errors.append(f"{rel}: page file extension must be lowercase '.md'")
                continue
            fm, body = split_page(md_file)
            page = {"path": md_file, "rel": rel, "fm": {}, "body": body, "type": "unknown", "ok": False}
            pages.append(page)
            if fm is None:
                errors.append(f"{rel}: missing YAML frontmatter")
            elif not isinstance(fm, dict):
                errors.append(f"{rel}: frontmatter must be a YAML mapping, got {type(fm).__name__}")
            elif "_read_error" in fm:
                errors.append(f"{rel}: {fm['_read_error']}")
            elif "_parse_error" in fm:
                errors.append(f"{rel}: YAML parse error: {fm['_parse_error']}")
            else:
                page.update(fm=fm, type=detect_page_type(md_file), ok=True)
    return pages, errors


def main():
    ctx, all_errors = load_data()
    pages, page_errors = collect_pages()
    all_errors.extend(page_errors)

    # Pass 1: ids. A duplicate id is an error on every page after the first.
    id_types, id_categories, first_seen = {}, {}, {}
    for page in pages:
        fid = page["fm"].get("id")
        if not isinstance(fid, str):
            continue
        if fid in first_seen:
            all_errors.append(f"{page['rel']}: duplicate id '{fid}' (also in {first_seen[fid]})")
            continue
        first_seen[fid] = page["rel"]
        id_types[fid] = page["type"]
        category = page["fm"].get("source_category")
        id_categories[fid] = category if isinstance(category, str) else None
    source_ids = {fid for fid, ptype in id_types.items() if ptype.startswith("source-")}

    claims, claim_errors = load_version_claims(ctx["schemas"])
    ctx.update(id_types=id_types, id_categories=id_categories, source_ids=source_ids, claims=claims)

    # Pass 2: per-page validation.
    for page in pages:
        if not page["ok"]:
            continue
        try:
            messages = validate_page(page, ctx)
        except Exception as exc:  # a validator bug must not hide the other pages' errors
            messages = [f"internal validator error ({type(exc).__name__}: {exc})"]
        all_errors.extend(f"{page['rel']}: {msg}" for msg in messages)

    all_errors.extend(claim_errors)
    all_errors.extend(validate_version_claims(
        claims, {p["rel"]: p for p in pages if p["ok"]}, source_ids
    ))
    all_errors.extend(validate_aliases(ctx["vocab"], ctx["arch_nodes"]))
    all_errors.extend(validate_discoverability(pages))

    for err in all_errors:
        print(f"  ERROR: {err}")
    wiki_count = sum(1 for p in pages if p["rel"].startswith("wiki/"))
    print(
        f"Validated {len(pages)} pages ({len(pages) - wiki_count} source, {wiki_count} wiki): "
        f"{len(all_errors)} error(s)"
    )
    sys.exit(1 if all_errors else 0)


if __name__ == "__main__":
    main()
