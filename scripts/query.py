#!/usr/bin/env python3
"""Unified query tool for the Vulkan compute-shader kernel wiki.

Supports natural-language keyword queries, tag filters, repo filters, type
filters and architecture-tree filters.

Usage:
    query.py "quantized linear cooperative matrix"
    query.py --tag cooperative-matrix --type kernel
    query.py --architecture rdna3
    query.py --architecture 780M --type measurement
    query.py --language glsl --limit 20
    query.py --symptom "<exact symptom string>"

Architecture filters follow the tree in data/architectures.yaml: asking for a
node returns pages tagged with that node or any descendant, never pages tagged
only with an ancestor. Spellings listed in data/aliases.yaml are resolved
first. The number of ancestor-only pages left out is reported on stderr.

Returns a ranked list of matching pages with titles, paths, and key frontmatter fields.
"""

import argparse
import copy
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _yaml_compat import yaml  # noqa: E402
from _wiki_root import WIKI_ROOT  # noqa: E402
import arch_policy  # noqa: E402

VOCAB_FIELDS = ("tags", "techniques", "hardware_features", "kernel_types", "languages")

_ALIAS_CACHE = None


def load_alias_expansions():
    """Return a dict mapping lowercased alias -> canonical term, loaded from data/aliases.yaml.

    Each canonical is also mapped to itself, so lookups always return something
    sensible when the user already types the canonical form. A missing file
    yields an empty mapping.
    """
    global _ALIAS_CACHE
    if _ALIAS_CACHE is None:
        _ALIAS_CACHE = arch_policy.load_aliases()
    return _ALIAS_CACHE


def expand_keyword(kw):
    """Return a list of search variants for a keyword: the original plus any
    canonical term the alias map points to."""
    aliases = load_alias_expansions()
    canonical = aliases.get(kw.lower())
    if canonical and canonical.lower() != kw.lower():
        return [kw, canonical]
    return [kw]


def as_list(value):
    """Frontmatter list fields may be absent, null, or a bare scalar."""
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def load_frontmatter(path):
    """Parse YAML frontmatter from a markdown file. Returns (fm_dict, body_str) or (None, None)."""
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return None, None
    m = re.match(r'^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)', content, re.DOTALL)
    if not m:
        return None, None
    try:
        fm = yaml.safe_load(m.group(1))
        if not isinstance(fm, dict):
            return None, None
        return fm, m.group(2)
    except yaml.YAMLError:
        return None, None


def load_all_pages():
    """Load frontmatter + body for every sources/**/*.md and wiki/**/*.md file."""
    pages = []
    for subdir in ["sources", "wiki"]:
        base = WIKI_ROOT / subdir
        if not base.exists():
            continue
        for md in base.rglob("*.md"):
            fm, body = load_frontmatter(md)
            if fm is None:
                continue
            pages.append({
                "path": md.relative_to(WIKI_ROOT).as_posix(),
                "fm": fm,
                "body": body or "",
            })
    return pages


def detect_page_type(fm, path):
    """Return a page-type label for filtering: source-pr/source-measurement/..., wiki-hardware/..."""
    if "type" in fm:
        return f"wiki-{fm['type']}"
    parts = path.split("/")
    if parts[0] == "sources" and len(parts) > 1:
        return f"source-{parts[1].rstrip('s')}"  # prs -> source-pr, measurements -> source-measurement
    return "unknown"


def score_keyword_match(fm, body, keywords):
    """Score a page by keyword matches in title, tags, and body (title > tags > body).

    Each user keyword is expanded through the alias map, so a spelling listed
    in data/aliases.yaml also scores pages that use the canonical term.
    """
    score = 0
    title_text = str(fm.get("title", "")).lower()
    tag_text = " ".join(
        str(v)
        for k in VOCAB_FIELDS + ("architectures", "aliases", "symptoms")
        for v in as_list(fm.get(k))
    ).lower()
    body_lower = body.lower()
    for kw in keywords:
        best_variant_score = 0
        for variant in expand_keyword(kw):
            v_l = variant.lower()
            variant_score = 0
            if v_l in title_text:
                variant_score += 10
            if v_l in tag_text:
                variant_score += 5
            body_hits = body_lower.count(v_l)
            variant_score += min(body_hits, 3)
            if variant_score > best_variant_score:
                best_variant_score = variant_score
        score += best_variant_score
    return score


def filter_pages(pages, args):
    """Apply CLI filters to narrow the page set."""
    out = []
    for p in pages:
        fm = p["fm"]
        path = p["path"]
        ptype = detect_page_type(fm, path)
        p["_ptype"] = ptype

        if args.type and not ptype.endswith(args.type):
            # --type kernel matches wiki-kernel, --type pr matches source-pr
            if ptype != args.type:
                continue

        if args.tag:
            all_tags = set()
            for k in VOCAB_FIELDS:
                all_tags.update(str(v) for v in as_list(fm.get(k)))
            tag_variants = {v.lower() for v in expand_keyword(args.tag)}
            if not any(t.lower() in tag_variants for t in all_tags):
                continue

        if args.repo:
            repo = str(fm.get("repo", "")).lower()
            if args.repo.lower() not in repo:
                continue

        if args.language:
            langs = set(as_list(fm.get("languages")))
            tags = set(as_list(fm.get("tags")))
            if args.language not in langs and args.language not in tags:
                continue

        if args.architecture:
            if not arch_policy.architecture_matches_filter(
                as_list(fm.get("architectures")), args.architecture
            ):
                continue

        if args.symptom:
            symptoms = set(as_list(fm.get("symptoms")))
            if args.symptom not in symptoms:
                continue

        if args.confidence:
            if str(fm.get("confidence", "")) != args.confidence:
                continue

        out.append(p)
    return out


def report_architecture_filter(requested, eligible_pages):
    """Disclose on stderr how the architecture filter was interpreted."""
    node = arch_policy.resolve_architecture(requested)
    if node != arch_policy.normalize(requested):
        print(f"Architecture '{requested}' resolved to '{node}'.", file=sys.stderr)
    if not arch_policy.is_known(node):
        known = ", ".join(arch_policy.all_nodes()) or "(none; data/architectures.yaml defines no nodes)"
        print(
            f"WARNING: '{requested}' is not a node of data/architectures.yaml and not an "
            f"alias of one; matching the literal value only. Known nodes: {known}",
            file=sys.stderr,
        )
        return
    above = arch_policy.ancestors(node)
    if not above:
        return
    excluded = arch_policy.ancestor_only_exclusion_count(eligible_pages, node)
    message = (
        f"Architecture filter '{node}' excluded {excluded} page(s) tagged only with "
        f"an ancestor ({', '.join(above)})"
    )
    if excluded:
        broader = " or ".join(f"--architecture {name}" for name in above)
        message += f"; use {broader} for the broader set"
    print(message + ".", file=sys.stderr)


def format_result(page, compact=False):
    """Format a single page as a readable line."""
    fm = page["fm"]
    title = fm.get("title", "Untitled")
    path = page["path"]
    pid = fm.get("id", "")
    ptype = page.get("_ptype", "?")

    if compact:
        return f"  [{ptype}] {pid}: {title}  ({path})"

    # Rich: include key metadata
    lines = [f"## {title}"]
    lines.append(f"- **id**: `{pid}`")
    lines.append(f"- **type**: `{ptype}`")
    lines.append(f"- **path**: `{path}`")
    if "architectures" in fm:
        lines.append(f"- **architectures**: {fm['architectures']}")
    for k in ("device", "driver", "measured_at", "confidence", "reproducibility"):
        if k in fm:
            lines.append(f"- **{k}**: {fm[k]}")
    for k in VOCAB_FIELDS:
        v = fm.get(k)
        if v:
            lines.append(f"- **{k}**: {v}")
    if isinstance(fm.get("performance_claims"), list):
        for claim in fm["performance_claims"][:2]:
            if not isinstance(claim, dict):
                continue
            lines.append(
                f"- **perf**: {claim.get('value')} {claim.get('metric')} on {claim.get('gpu')} "
                f"/ {claim.get('driver')} ({claim.get('dtype')}, {claim.get('shape')})"
            )
    if fm.get("sources"):
        lines.append(f"- **sources**: {as_list(fm['sources'])[:5]}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Query the Vulkan compute-shader kernel wiki",
        epilog="Examples: query.py --tag cooperative-matrix --type kernel | "
               "query.py --architecture rdna3 | query.py --architecture 780M --type measurement",
    )
    parser.add_argument("query", nargs="*", help="Free-text keywords")
    parser.add_argument("--type", help="Filter by page type (kernel, technique, hardware, pattern, language, migration, pr, doc, blog, measurement)")
    parser.add_argument("--tag", help="Filter by tag (must appear in tags/techniques/hardware_features/kernel_types/languages), e.g. cooperative-matrix")
    parser.add_argument("--repo", help="Filter by source repo (partial match on the 'repo' field)")
    parser.add_argument("--language", help="Filter by language (glsl, spirv, cpp, python, ...)")
    parser.add_argument("--architecture", help="Filter by architecture-tree node or alias (vendor, generation or device, e.g. amd, rdna3, radeon-780m, 780M); matches the node and its descendants")
    parser.add_argument("--symptom", help="Filter by pattern symptom (exact, case-sensitive match of one 'symptoms' entry)")
    parser.add_argument("--confidence", help="Filter by confidence (verified, source-reported, inferred, experimental)")
    parser.add_argument("--limit", type=int, default=10, help="Max results (default 10)")
    parser.add_argument("--compact", action="store_true", help="Compact one-line-per-result output")
    parser.add_argument("--paths-only", action="store_true", help="Output only file paths, one per line")
    args = parser.parse_args()
    if args.architecture is not None and not args.architecture.strip():
        parser.error("--architecture requires a non-empty node name or alias")

    try:
        arch_policy.load_tree()
    except arch_policy.ArchitectureTreeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)

    all_pages = load_all_pages()
    if args.architecture:
        without_architecture = copy.copy(args)
        without_architecture.architecture = None
        eligible_pages = filter_pages(all_pages, without_architecture)
        pages = filter_pages(eligible_pages, args)
        report_architecture_filter(args.architecture, eligible_pages)
    else:
        pages = filter_pages(all_pages, args)

    # Score by keywords if any. Flatten multi-word quoted args into tokens so
    # `query.py "quantized linear"` behaves like `query.py quantized linear`.
    keywords = []
    for q in args.query:
        for tok in re.split(r"\s+", q.strip()):
            if tok:
                keywords.append(tok)
    if keywords:
        for p in pages:
            p["_score"] = score_keyword_match(p["fm"], p["body"], keywords)
        pages = [p for p in pages if p["_score"] > 0]
        pages.sort(key=lambda x: (-x["_score"], x["path"]))
    else:
        pages.sort(key=lambda x: x["path"])

    pages = pages[:args.limit]

    if args.paths_only:
        for p in pages:
            print(p["path"])
        return

    if not pages:
        print("No matching pages.")
        return

    print(f"# {len(pages)} result(s)")
    print()
    for p in pages:
        print(format_result(p, compact=args.compact))
        if not args.compact:
            print()


if __name__ == "__main__":
    main()
