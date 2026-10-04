"""Architecture tree policy: the data-driven vendor/generation/device hierarchy.

Everything here is derived from ``data/architectures.yaml`` (see that file's
header for the yaml shape). No vendor, generation or device name is hardcoded.

Query semantics
---------------
- Asking for a node matches pages tagged with that node OR any descendant.
- Asking for a node does NOT match pages tagged only with an ancestor of it.
  ``ancestor_only_exclusion_count`` reports how many pages were left out for
  that reason so callers can disclose it.
- Human-facing spellings are resolved to node names through
  ``data/aliases.yaml`` (``canonical: [alias, ...]``) before matching.

All functions are pure with respect to the loaded tree. The tree is read once
per wiki root and cached; call ``clear_cache()`` after editing the yaml files
in-process.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _yaml_compat import yaml  # noqa: E402
from _wiki_root import WIKI_ROOT  # noqa: E402

ARCHITECTURES_FILE = Path("data") / "architectures.yaml"
ALIASES_FILE = Path("data") / "aliases.yaml"
TREE_KEY = "architectures"
NODE_KINDS = ("vendor", "generation", "device")
_NODE_KEYS = {"kind", "children"}


class ArchitectureTreeError(ValueError):
    """Raised when data/architectures.yaml is structurally invalid."""


class _Index:
    """Flattened view of the tree: order, parent, children and kind per node."""

    def __init__(self) -> None:
        self.order: List[str] = []
        self.parent: Dict[str, Optional[str]] = {}
        self.children: Dict[str, List[str]] = {}
        self.kind: Dict[str, str] = {}
        self.depth: Dict[str, int] = {}


_TREE_CACHE: Dict[Path, Dict[str, Any]] = {}
_INDEX_CACHE: Dict[Path, _Index] = {}
_ALIAS_CACHE: Dict[Path, Dict[str, str]] = {}


def clear_cache() -> None:
    """Forget every cached tree and alias map."""
    _TREE_CACHE.clear()
    _INDEX_CACHE.clear()
    _ALIAS_CACHE.clear()


def _root(root: Optional[Path]) -> Path:
    return Path(root).resolve() if root is not None else WIKI_ROOT


def normalize(name: Any) -> str:
    """Canonical spelling used for comparisons: stripped and lowercased."""
    return str(name).strip().lower()


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_tree(root: Optional[Path] = None) -> Dict[str, Any]:
    """Return the nested mapping under the top-level ``architectures`` key.

    Shape: ``{node: {"kind": str, "children": {node: {...}}}}``. A missing or
    malformed file raises ArchitectureTreeError: the tree is required, and an
    empty tree would silently turn every architecture filter into a literal
    match.
    """
    base = _root(root)
    if base in _TREE_CACHE:
        return _TREE_CACHE[base]
    path = base / ARCHITECTURES_FILE
    if not path.is_file():
        raise ArchitectureTreeError(
            f"{ARCHITECTURES_FILE}: missing (architecture tree is required)"
        )
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, UnicodeDecodeError) as exc:
        raise ArchitectureTreeError(f"{ARCHITECTURES_FILE}: invalid yaml: {exc}") from exc
    if not isinstance(raw, dict) or not isinstance(raw.get(TREE_KEY, {}), dict):
        raise ArchitectureTreeError(
            f"{ARCHITECTURES_FILE}: expected a top-level '{TREE_KEY}' mapping"
        )
    tree = raw.get(TREE_KEY) or {}
    _build_index(tree)  # validate eagerly; raises on structural problems
    _TREE_CACHE[base] = tree
    return tree


def _build_index(tree: Mapping[str, Any]) -> _Index:
    index = _Index()

    def walk(mapping: Mapping[str, Any], parent: Optional[str], depth: int) -> None:
        for raw_name, spec in mapping.items():
            if not isinstance(raw_name, str) or not raw_name.strip():
                raise ArchitectureTreeError(
                    f"{ARCHITECTURES_FILE}: node name {raw_name!r} must be a non-empty string"
                )
            name = raw_name
            if name != normalize(name):
                raise ArchitectureTreeError(
                    f"{ARCHITECTURES_FILE}: node name {name!r} must be lowercase without padding"
                )
            if name in index.parent:
                raise ArchitectureTreeError(
                    f"{ARCHITECTURES_FILE}: duplicate node name {name!r}"
                )
            if spec is None:
                spec = {}
            if not isinstance(spec, dict):
                raise ArchitectureTreeError(
                    f"{ARCHITECTURES_FILE}: node {name!r} must be a mapping"
                )
            unknown = set(spec) - _NODE_KEYS
            if unknown:
                raise ArchitectureTreeError(
                    f"{ARCHITECTURES_FILE}: node {name!r} has unknown keys {sorted(unknown)}"
                )
            kids = spec.get("children") or {}
            if not isinstance(kids, dict):
                raise ArchitectureTreeError(
                    f"{ARCHITECTURES_FILE}: node {name!r}: 'children' must be a mapping"
                )
            kind = spec.get("kind")
            if kind is None:
                kind = "vendor" if parent is None else ("generation" if kids else "device")
            if kind not in NODE_KINDS:
                raise ArchitectureTreeError(
                    f"{ARCHITECTURES_FILE}: node {name!r} has invalid kind {kind!r}; "
                    f"expected one of {list(NODE_KINDS)}"
                )
            # Levels only go down: vendor > generation > device. Roots are
            # vendors, and a device is always a leaf.
            rank = NODE_KINDS.index(kind)
            if parent is None and kind != "vendor":
                raise ArchitectureTreeError(
                    f"{ARCHITECTURES_FILE}: root node {name!r} must be of kind 'vendor', got {kind!r}"
                )
            if parent is not None and rank <= NODE_KINDS.index(index.kind[parent]):
                raise ArchitectureTreeError(
                    f"{ARCHITECTURES_FILE}: node {name!r} of kind {kind!r} cannot be a child of "
                    f"{parent!r} of kind {index.kind[parent]!r}"
                )
            if kind == "device" and kids:
                raise ArchitectureTreeError(
                    f"{ARCHITECTURES_FILE}: device node {name!r} must not have children"
                )
            index.order.append(name)
            index.parent[name] = parent
            index.children[name] = list(kids.keys())
            index.kind[name] = kind
            index.depth[name] = depth
            walk(kids, name, depth + 1)

    walk(tree, None, 0)
    return index


def _index(root: Optional[Path] = None) -> _Index:
    base = _root(root)
    if base not in _INDEX_CACHE:
        _INDEX_CACHE[base] = _build_index(load_tree(base))
    return _INDEX_CACHE[base]


def load_aliases(root: Optional[Path] = None) -> Dict[str, str]:
    """Return ``{lowercased alias: canonical}`` from data/aliases.yaml.

    Each canonical term also maps to itself. A missing or unreadable file
    yields an empty mapping.
    """
    base = _root(root)
    if base in _ALIAS_CACHE:
        return _ALIAS_CACHE[base]
    out: Dict[str, str] = {}
    try:
        raw = yaml.safe_load((base / ALIASES_FILE).read_text(encoding="utf-8")) or {}
    except Exception:
        raw = {}
    if isinstance(raw, dict):
        for canonical, variants in raw.items():
            if not isinstance(canonical, str):
                continue
            out.setdefault(canonical.lower(), canonical)
            if isinstance(variants, str):
                variants = [variants]
            for variant in variants or []:
                if isinstance(variant, (str, int, float)):
                    out.setdefault(str(variant).lower(), canonical)
    _ALIAS_CACHE[base] = out
    return out


# ---------------------------------------------------------------------------
# Tree navigation
# ---------------------------------------------------------------------------

def all_nodes(root: Optional[Path] = None) -> List[str]:
    """Every node name in tree (pre-order, yaml) order."""
    return list(_index(root).order)


def is_known(node: Any, root: Optional[Path] = None) -> bool:
    """True when ``node`` names a node of the tree (case-insensitive)."""
    return normalize(node) in _index(root).parent


def node_kind(node: Any, root: Optional[Path] = None) -> Optional[str]:
    """'vendor', 'generation' or 'device'; None for an unknown node."""
    return _index(root).kind.get(normalize(node))


def node_depth(node: Any, root: Optional[Path] = None) -> Optional[int]:
    """0 for a root node, 1 for its children, ...; None for an unknown node."""
    return _index(root).depth.get(normalize(node))


def parent(node: Any, root: Optional[Path] = None) -> Optional[str]:
    """Direct parent name, or None for a root or unknown node."""
    return _index(root).parent.get(normalize(node))


def children(node: Any, root: Optional[Path] = None) -> List[str]:
    """Direct children in yaml order; empty for a leaf or unknown node."""
    return list(_index(root).children.get(normalize(node), []))


def descendants(node: Any, root: Optional[Path] = None) -> List[str]:
    """All strict descendants in tree order; empty for a leaf or unknown node."""
    index = _index(root)
    out: List[str] = []
    stack = list(reversed(index.children.get(normalize(node), [])))
    while stack:
        current = stack.pop()
        out.append(current)
        stack.extend(reversed(index.children.get(current, [])))
    return out


def ancestors(node: Any, root: Optional[Path] = None) -> List[str]:
    """All strict ancestors, nearest first; empty for a root or unknown node."""
    index = _index(root)
    out: List[str] = []
    current = index.parent.get(normalize(node))
    while current is not None:
        out.append(current)
        current = index.parent.get(current)
    return out


def is_leaf(node: Any, root: Optional[Path] = None) -> bool:
    """True when ``node`` is a known node without children."""
    index = _index(root)
    name = normalize(node)
    return name in index.parent and not index.children[name]


def devices(root: Optional[Path] = None) -> List[str]:
    """Every node of kind 'device', in tree order."""
    index = _index(root)
    return [name for name in index.order if index.kind[name] == "device"]


def tree_order(root: Optional[Path] = None) -> List[Tuple[str, int, str]]:
    """``(node, depth, kind)`` for every node in tree order."""
    index = _index(root)
    return [(name, index.depth[name], index.kind[name]) for name in index.order]


# ---------------------------------------------------------------------------
# Query semantics
# ---------------------------------------------------------------------------

def resolve_architecture(requested: Any, root: Optional[Path] = None) -> str:
    """Resolve a user-supplied architecture spelling to a node name.

    Order: exact node name (case-insensitive, '_' treated as '-'), then
    data/aliases.yaml. An unresolvable value is returned normalized so the
    caller can still do a literal comparison and report it as unknown.
    """
    index = _index(root)
    name = normalize(requested)
    for candidate in (name, name.replace("_", "-")):
        if candidate in index.parent:
            return candidate
    aliases = load_aliases(root)
    for candidate in (name, name.replace("_", "-")):
        canonical = aliases.get(candidate)
        if canonical is not None and normalize(canonical) in index.parent:
            return normalize(canonical)
    return name


def _page_architectures(page_archs: Any) -> set:
    if page_archs is None:
        return set()
    if isinstance(page_archs, (str, bytes)):
        page_archs = [page_archs]
    return {normalize(value) for value in page_archs}


def architecture_matches_filter(
    page_archs: Optional[Iterable[Any]],
    requested: Any,
    root: Optional[Path] = None,
) -> bool:
    """True when a page tagged ``page_archs`` answers a query for ``requested``.

    Matches when the page carries the requested node itself or any descendant
    of it. A page carrying only ancestors of the requested node does not match.
    ``requested`` is alias-resolved first; an unknown value falls back to a
    literal comparison against the page's values.
    """
    archs = _page_architectures(page_archs)
    if not archs:
        return False
    node = resolve_architecture(requested, root)
    if node in archs:
        return True
    return any(name in archs for name in descendants(node, root))


def _archs_of(page: Any) -> Any:
    """Accept a query.py page ({'fm': {...}}), a frontmatter dict, or a list."""
    if isinstance(page, Mapping):
        fm = page.get("fm") if isinstance(page.get("fm"), Mapping) else page
        return fm.get("architectures")
    return page


def ancestor_only_exclusion_count(
    pages: Iterable[Any],
    requested: Any,
    root: Optional[Path] = None,
) -> int:
    """Count pages excluded from a ``requested`` query only for being too broad.

    A page counts when it does not match ``requested`` but is tagged with at
    least one ancestor of it. Always 0 for a root or unknown node. Each item of
    ``pages`` may be a ``{'fm': frontmatter}`` dict, a frontmatter dict, or a
    plain list of architecture values.
    """
    node = resolve_architecture(requested, root)
    above = set(ancestors(node, root))
    if not above:
        return 0
    count = 0
    for page in pages:
        archs = _page_architectures(_archs_of(page))
        if archs & above and not architecture_matches_filter(archs, node, root):
            count += 1
    return count


__all__ = [
    "ArchitectureTreeError",
    "NODE_KINDS",
    "all_nodes",
    "ancestor_only_exclusion_count",
    "ancestors",
    "architecture_matches_filter",
    "children",
    "clear_cache",
    "descendants",
    "devices",
    "is_known",
    "is_leaf",
    "load_aliases",
    "load_tree",
    "node_depth",
    "node_kind",
    "normalize",
    "parent",
    "resolve_architecture",
    "tree_order",
]
