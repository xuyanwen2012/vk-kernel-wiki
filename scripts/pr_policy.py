"""Shared intake policy for upstream pull requests.

Used by scripts/refresh_candidate_ledger.py (decide include / defer / exclude
for a search hit) and scripts/generate-pr-pages.py (derive the frontmatter of
a source-pr page). Everything here is offline and deterministic: the callers
fetch the pull request and its changed-file list and hand them in.

Policy
------
- Scope is decided from the changed files, never from the title alone:
    include  at least one GLSL shader source file was added or modified
    defer    no shader source changed, but backend host source did (kernel
             selection, tile choice, driver workarounds); needs manual triage
    exclude  neither
  Which paths count is configured per ledger (`shader_path_markers`,
  `embedded_shader_path_markers`, `host_path_markers`), so no repository
  layout is hardcoded here. An embedded-shader path is a file of another
  language that carries GLSL source as text (a generator script, for example);
  it counts as shader source.
- Frontmatter is derived from positive evidence only. A term is emitted when
  a pattern matches the PR title or a changed shader path; nothing is guessed
  from the description. `techniques` is always left empty: the technique
  vocabulary names specific shader constructs and assigning one needs a human
  or agent to read the diff.
- Architecture nodes come from two kinds of evidence. The PR title is
  matched against the node names and aliases of data/architectures.yaml and
  data/aliases.yaml. The patches are matched against the ledger's
  `architecture_code_markers` (identifier -> node): a marker counts when the
  pull request adds it on more lines than it removes, so code that is only
  moved does not count. An ancestor is dropped when one of its descendants
  also matched. Reserved vendor nodes (vendors without children) and names
  that are not nodes are never emitted.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Optional

import arch_policy

SHADER_SUFFIXES = (".comp", ".glsl")
HOST_LANGUAGE_SUFFIXES = {
    ".cpp": "cpp", ".cc": "cpp", ".cxx": "cpp", ".h": "cpp", ".hpp": "cpp",
    ".py": "python",
}
UPSTREAM_EXCERPT_LIMIT = 1200
EXCERPT_START = "<!-- upstream-excerpt-start -->"
EXCERPT_END = "<!-- upstream-excerpt-end -->"

DECISIONS = ("include", "defer", "exclude")


@dataclass(frozen=True)
class ScopeDecision:
    decision: str
    rule: str
    evidence_paths: tuple
    reason: str


def normalize_files(files: Iterable[Any]) -> list:
    """Reduce GitHub changed-file records to the fields the policy reads."""
    out = []
    for item in files or []:
        if not isinstance(item, dict) or not item.get("filename"):
            continue
        out.append({
            "filename": str(item["filename"]),
            "status": str(item.get("status") or "").lower(),
            "patch": item.get("patch"),
        })
    return out


def _has_marker(path: str, markers: Iterable[str]) -> bool:
    markers = [m for m in (markers or []) if m]
    return not markers or any(m in path for m in markers)


@dataclass(frozen=True)
class PathConfig:
    """The path markers of one ledger."""
    shader: tuple = ()
    embedded: tuple = ()
    host: tuple = ()

    @classmethod
    def from_ledger(cls, ledger: dict) -> "PathConfig":
        return cls(
            tuple(ledger.get("shader_path_markers") or ()),
            tuple(ledger.get("embedded_shader_path_markers") or ()),
            tuple(ledger.get("host_path_markers") or ()),
        )


def is_shader_path(path: str, config: PathConfig) -> bool:
    if config.embedded and any(marker in path for marker in config.embedded):
        return True
    return PurePosixPath(path).suffix.lower() in SHADER_SUFFIXES and _has_marker(path, config.shader)


def shader_files(files: Iterable[Any], config: PathConfig) -> list:
    """The changed-file records that carry shader source, removals included."""
    return [f for f in normalize_files(files) if is_shader_path(f["filename"], config)]


def classify_scope(files: Iterable[Any], config: PathConfig = PathConfig()) -> ScopeDecision:
    """Decide include / defer / exclude from the changed files."""
    normalized = normalize_files(files)
    host_markers = config.host
    shader_paths, host_paths = [], []
    for item in normalized:
        path = item["filename"]
        if item["status"] in {"removed", "deleted"}:
            continue
        if is_shader_path(path, config):
            shader_paths.append(path)
        elif (host_markers and _has_marker(path, host_markers)
              and PurePosixPath(path).suffix.lower() in HOST_LANGUAGE_SUFFIXES):
            host_paths.append(path)

    if shader_paths:
        paths = tuple(sorted(set(shader_paths)))
        return ScopeDecision(
            "include", "glsl-shader-source", paths,
            "include: GLSL shader source added or modified: " + ", ".join(paths),
        )
    if host_paths:
        paths = tuple(sorted(set(host_paths)))
        return ScopeDecision(
            "defer", "backend-host-source-only", paths,
            "defer: no GLSL shader source changed; backend host source changed: " + ", ".join(paths),
        )
    return ScopeDecision(
        "exclude", "no-shader-or-backend-source", (),
        f"exclude: no GLSL shader or backend host source in {len(normalized)} changed file(s)",
    )


# ---------------------------------------------------------------------------
# Architectures
# ---------------------------------------------------------------------------

def _spelling_pattern(spelling: str) -> re.Pattern:
    body = r"[\s_-]*".join(re.escape(part) for part in re.split(r"[\s_-]+", spelling) if part)
    return re.compile(rf"(?<![A-Za-z0-9]){body}(?![A-Za-z0-9])", re.IGNORECASE)


def _marker_hits(files: Iterable[Any], markers: dict) -> dict:
    """{marker: path of its first added line} for markers with a net addition."""
    patterns = {m: re.compile(rf"(?<![A-Za-z0-9_]){re.escape(str(m))}(?![A-Za-z0-9_])") for m in markers}
    net = dict.fromkeys(markers, 0)
    first = {}
    for item in normalize_files(files):
        for line in (item.get("patch") or "").split("\n"):
            sign = line[:1]
            if sign not in "+-" or line.startswith(("+++", "---")):
                continue
            for marker, pattern in patterns.items():
                count = len(pattern.findall(line))
                if count:
                    net[marker] += count if sign == "+" else -count
                    if sign == "+":
                        first.setdefault(marker, item["filename"])
    return {m: first[m] for m in markers if net[m] > 0 and m in first}


def derive_architectures(title: str, files: Iterable[Any] = (), code_markers: Optional[dict] = None,
                         root: Optional[Path] = None) -> tuple:
    """Return (nodes in tree order, evidence rows) for a pull request."""
    nodes = set(arch_policy.all_nodes(root))
    reserved = {
        n for n in nodes
        if arch_policy.node_kind(n, root) == "vendor" and not arch_policy.children(n, root)
    }
    matched = {}
    for spelling, canonical in sorted(arch_policy.load_aliases(root).items()):
        if canonical not in nodes or canonical in reserved or canonical in matched:
            continue
        hit = _spelling_pattern(spelling).search(title or "")
        if hit:
            matched[canonical] = {"node": canonical, "locator": "title", "matched": hit.group(0)}
    usable = {
        str(marker): node for marker, node in sorted((code_markers or {}).items())
        if node in nodes and node not in reserved
    }
    for marker, path in _marker_hits(files, usable).items():
        matched.setdefault(usable[marker], {
            "node": usable[marker], "locator": f"added-patch:{path}", "matched": marker,
        })
    for node in list(matched):
        if any(d in matched for d in arch_policy.descendants(node, root)):
            del matched[node]
    ordered = [n for n in arch_policy.all_nodes(root) if n in matched]
    return ordered, [matched[n] for n in ordered]


# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

_TOKEN = r"(?<![A-Za-z0-9]){}(?![A-Za-z0-9])"

_HARDWARE_PATTERNS = {
    "cooperative-matrix": r"coop[\s_-]?mat|cooperative[\s_-]matri|" + _TOKEN.format(r"cm[12]"),
    "cooperative-matrix2": r"coop[\s_-]?mat[\s_-]?2|cooperative[\s_-]matrix[\s_-]?2|" + _TOKEN.format("cm2"),
    "bfloat16-arithmetic": _TOKEN.format(r"bf16|bfloat16"),
    "int8-cooperative-matrix": r"int8[\s_-]coop[\s_-]?mat",
    "integer-dot-product": _TOKEN.format("dp4a") + r"|integer[\s_-]dot[\s_-]product|dotPacked",
    "subgroup-size": r"subgroup[\s_-]size",
    "shared-memory-limit": _TOKEN.format("shmem") + r"|shared[\s_-]memory",
    "fp16-arithmetic": _TOKEN.format(r"fp16|f16|float16"),
    "specialization-constants": r"spec(?:ialization)?[\s_-]constant",
}
_KERNEL_TYPE_PATTERNS = {
    "gemm": _TOKEN.format(r"mul_?mmq?|mmq|gemm") + r"|mat[\s_-]?mul|matrix[\s_-]matrix",
    "gemv": _TOKEN.format(r"mmvq?|gemv") + r"|mul_mat_vec|matrix[\s_-]vector",
    "sdpa": r"flash[\s_-]?att(?:entio)?n|scaled[\s_-]dot[\s_-]product[\s_-]attention|" + _TOKEN.format("sdpa"),
    "moe": _TOKEN.format(r"moe|mmid") + r"|mul_(?:mm|mat)_id|count_experts",
    "convolution": r"(?<![A-Za-z])(?<!ssm_)conv(?:[\s_-]?[123]d|_transpose|olution)?(?![A-Za-z])|im2col|col2im",
    "dequantize": r"dequant",
    "rope": _TOKEN.format("rope"),
    "normalization": r"(?m)(?:rms|l2|group)[ _-]?norm|^norm\.comp$",
    "softmax": r"soft[ _-]?max",
    "topk-sort": r"arg[ _-]?sort|arg[ _-]?max|top[ _-]?k",
    "gated-delta-net": r"gated[ _-]delta|" + _TOKEN.format("gdn"),
    "tensor-copy": (
        r"(?m)^(?:copy|contig_copy|copy_(?:to|from)_quant|copy_transpose\w*|[gs]et_rows\w*|"
        r"concat|repeat|pad|fill)\.comp$"
    ),
    "elementwise": (
        r"(?m)^(?:add|sub|mul|div|acc|scale|clamp|square|sqrt|exp|log|sin|cos|tanh|abs|neg|sgn|"
        r"step|ceil|floor|round|trunc|relu|leaky_relu|elu|xielu|sigmoid|softplus|silu|"
        r"gelu\w*|hard\w+|unary|multi_add|generic_(?:binary|unary)_head|\w*glu\w*)\.comp$"
    ),
}


def _matching_terms(patterns: dict, text: str, allowed: set) -> list:
    return [
        term for term, pattern in patterns.items()
        if term in allowed and re.search(pattern, text, re.IGNORECASE)
    ]


def derive_metadata(title: str, files: Iterable[Any], vocab: dict,
                    config: PathConfig = PathConfig()) -> dict:
    """Derive tags, hardware_features, kernel_types and languages.

    `vocab` is the parsed data/tags.yaml. A pattern whose term is not in the
    vocabulary is ignored, so the output always validates.
    """
    normalized = [f for f in normalize_files(files) if f["status"] not in {"removed", "deleted"}]
    shader_paths = [f["filename"] for f in normalized if is_shader_path(f["filename"], config)]
    text = "\n".join([title or "", *(PurePosixPath(p).name for p in shader_paths)])

    hardware = _matching_terms(_HARDWARE_PATTERNS, text, set(vocab.get("hardware_features") or []))
    if {"int8-cooperative-matrix", "cooperative-matrix2"} & set(hardware) and "cooperative-matrix" not in hardware:
        hardware.insert(0, "cooperative-matrix")
    kernel_types = _matching_terms(_KERNEL_TYPE_PATTERNS, text, set(vocab.get("kernel_types") or []))

    allowed_languages = set(vocab.get("languages") or [])
    languages = []
    if shader_paths and "glsl" in allowed_languages:
        languages.append("glsl")
    for item in normalized:
        language = HOST_LANGUAGE_SUFFIXES.get(PurePosixPath(item["filename"]).suffix.lower())
        if language and language in allowed_languages and language not in languages:
            languages.append(language)

    return {
        "tags": [*hardware, *kernel_types, *languages],
        "techniques": [],
        "hardware_features": hardware,
        "kernel_types": kernel_types,
        "languages": languages,
    }


# ---------------------------------------------------------------------------
# Page body
# ---------------------------------------------------------------------------

def upstream_excerpt(body: str, limit: int = UPSTREAM_EXCERPT_LIMIT) -> tuple:
    """Return (verbatim excerpt, total characters of the canonical description).

    The excerpt is a prefix of the description with line endings normalized
    and trailing whitespace removed. Lines that git would read as conflict
    markers are escaped with a backslash, and the page's own excerpt markers
    are HTML-escaped so a description cannot close the excerpt early.
    """
    lines = []
    for line in (body or "").replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = line.rstrip(" \t")
        if re.match(r"^(?:<{7}|={7}|>{7})(?: |$)", line):
            line = "\\" + line
        lines.append(line)
    canonical = "\n".join(lines).strip()
    excerpt = canonical[:limit].rstrip()
    for marker in (EXCERPT_START, EXCERPT_END):
        excerpt = excerpt.replace(marker, marker.replace("<", "&lt;").replace(">", "&gt;"))
    return excerpt, len(canonical)


def excerpt_is_empty(excerpt: str) -> bool:
    """Mirror of validate.py: comments and code-fence lines do not count."""
    text = re.sub(r"<!--.*?-->", "", excerpt, flags=re.DOTALL)
    text = re.sub(r"^[ \t]*(?:```|~~~)[^\n]*$", "", text, flags=re.MULTILINE)
    return not text.strip()


def render_body(title: str, url: str, excerpt: str, total_chars: int, what: str = "description") -> str:
    """Render the only body a generated source-pr page may have.

    `what` names the upstream text the excerpt was taken from: the
    description, or the title when the description is empty.
    """
    shown = len(excerpt)
    scope = "complete" if shown >= total_chars else f"first {shown} of {total_chars} characters"
    if what != "description":
        scope += "; the pull request description is empty"
    return "\n".join([
        f"# {title}",
        "",
        f"Locator: {url} (pull request {what}, {scope})",
        "",
        EXCERPT_START,
        excerpt,
        EXCERPT_END,
        "",
    ])
