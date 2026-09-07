#!/usr/bin/env python3
"""Mutation coverage: which schema constraints does the corpus actually pin?

Counting cases measures effort, not coverage. The question that matters is:
*if someone weakened this schema, would anything go red?* A constraint no case
catches is a promise the standard makes and cannot keep.

So this deletes one constraint at a time and re-runs the corpus:

    constraint deleted  ->  some case fails   ->  COVERED
    constraint deleted  ->  corpus still green ->  UNCOVERED

An UNCOVERED constraint is not necessarily a bug. Some are unreachable, some
are genuinely not worth a case. But each one should be a decision rather than
an accident, which is what this report makes possible.

    python3 conformance/mutation_coverage.py
    python3 conformance/mutation_coverage.py --version 0.7.5 --format json
    python3 conformance/mutation_coverage.py --min-coverage 80   # gate mode

Mutation testing as a coverage measure is standard practice (Stryker, mutmut,
PIT); what is specific here is mutating the SCHEMA rather than the code, since
the schema is the artefact under test and the corpus is the test suite.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run import (  # noqa: E402
    CorpusError,
    _build_validators,
    discover_versions,
    load_corpus,
    load_schema,
    run_case,
)

Mutation = Tuple[str, str, Callable[[Dict[str, Any]], None]]


def _walk(node: Any, pointer: str, out: List[Mutation]) -> None:
    """Collect one mutation per constraint the schema expresses."""
    if isinstance(node, dict):
        if isinstance(node.get("required"), list):
            for name in list(node["required"]):
                out.append(
                    (
                        f"{pointer}/required",
                        f"drop required member {name!r}",
                        _dropper(pointer, "required", name),
                    )
                )
        for keyword in (
            "enum",
            "pattern",
            "minItems",
            "maxItems",
            "minLength",
            "maxLength",
            "minimum",
            "maximum",
            "exclusiveMinimum",
            "exclusiveMaximum",
            "uniqueItems",
            "minProperties",
            "maxProperties",
            "const",
        ):
            if keyword in node:
                out.append(
                    (
                        f"{pointer}/{keyword}",
                        f"delete {keyword}",
                        _deleter(pointer, keyword),
                    )
                )
        if node.get("additionalProperties") is False:
            out.append(
                (
                    f"{pointer}/additionalProperties",
                    "open the object (additionalProperties -> true)",
                    _setter(pointer, "additionalProperties", True),
                )
            )
        if "type" in node and pointer:
            out.append(
                (f"{pointer}/type", "delete type", _deleter(pointer, "type"))
            )

        for key, value in node.items():
            if key in ("enum", "required", "const", "examples", "description"):
                continue
            _walk(value, f"{pointer}/{key}", out)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            _walk(value, f"{pointer}/{i}", out)


def _resolve(schema: Dict[str, Any], pointer: str) -> Any:
    node: Any = schema
    for part in pointer.split("/"):
        if part == "":
            continue
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def _deleter(pointer: str, keyword: str) -> Callable[[Dict[str, Any]], None]:
    def apply(schema: Dict[str, Any]) -> None:
        _resolve(schema, pointer).pop(keyword, None)

    return apply


def _setter(pointer: str, keyword: str, value: Any) -> Callable[[Dict[str, Any]], None]:
    def apply(schema: Dict[str, Any]) -> None:
        _resolve(schema, pointer)[keyword] = value

    return apply


def _dropper(pointer: str, keyword: str, item: Any) -> Callable[[Dict[str, Any]], None]:
    def apply(schema: Dict[str, Any]) -> None:
        node = _resolve(schema, pointer)
        if item in node.get(keyword, []):
            node[keyword] = [x for x in node[keyword] if x != item]

    return apply


def is_unfalsifiable(node: Dict[str, Any], keyword: str) -> bool:
    """True when deleting `keyword` cannot change which documents validate.

    The common case: a node carries both an ``enum`` and a narrower-looking
    companion constraint (``pattern``, ``minLength``, ``type``, ``format``).
    The enum already restricts the instance to a fixed set, so if every member
    of that set satisfies the companion, the companion is dead weight -- and
    NO test case could ever catch its removal.

    Reporting that as "uncovered" would be crying wolf: it blames the corpus
    for a gap the corpus cannot close. It is a finding about the *schema*
    instead, so it gets its own bucket.
    """
    enum = node.get("enum")
    if not isinstance(enum, list) or not enum or keyword == "enum":
        return False
    try:
        from jsonschema import Draft202012Validator
    except ImportError:  # pragma: no cover
        return False
    with_kw = {k: v for k, v in node.items() if k != "enum"}
    if keyword not in with_kw:
        return False
    without_kw = {k: v for k, v in with_kw.items() if k != keyword}
    a = Draft202012Validator(with_kw)
    b = Draft202012Validator(without_kw)
    return all(a.is_valid(v) == b.is_valid(v) for v in enum)


def corpus_is_red(cases: List[Dict[str, Any]], schema: Dict[str, Any]) -> bool:
    """True when at least one case fails against this (mutated) schema."""
    validators = _build_validators(schema)
    for case in cases:
        if not run_case(case, validators)["ok"]:
            return True
    return False


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--version", action="append", dest="versions", metavar="X.Y.Z")
    ap.add_argument("--format", choices=("text", "json"), default="text")
    ap.add_argument(
        "--min-coverage",
        type=float,
        default=None,
        metavar="PCT",
        help="exit non-zero if coverage falls below this percentage",
    )
    ap.add_argument("--limit", type=int, default=None, help="sample N mutations")
    ap.add_argument(
        "--group",
        metavar="NAME",
        help="measure only one corpus file's cases (its stem). Answers 'does "
        "THIS group pin these constraints', which is what you want while "
        "authoring one group -- and it isolates you from a sibling group that "
        "is mid-edit.",
    )
    ap.add_argument(
        "--pointer-filter",
        metavar="SUBSTR",
        help="only report constraints whose pointer contains SUBSTR",
    )
    args = ap.parse_args(argv)

    report: Dict[str, Any] = {}
    worst = 100.0

    for version in args.versions or discover_versions():
        try:
            cases = load_corpus(version, include_optional=True, group=args.group)
        except CorpusError as exc:
            print(f"mutation-coverage: {exc}", file=sys.stderr)
            return 2
        schema = load_schema(version)

        mutations: List[Mutation] = []
        _walk(schema, "", mutations)
        if args.pointer_filter:
            mutations = [m for m in mutations if args.pointer_filter in m[0]]
        if args.limit:
            mutations = mutations[: args.limit]

        # Sanity: the corpus must be green before anything is mutated, or every
        # mutation trivially "fails" and the whole report is meaningless.
        if corpus_is_red(cases, copy.deepcopy(schema)):
            print(
                f"mutation-coverage: the {version} corpus"
                + (f" (group {args.group})" if args.group else "")
                + " is not green against the unmutated schema; fix that first -- "
                "otherwise every constraint reads as covered.",
                file=sys.stderr,
            )
            return 2

        covered: List[str] = []
        uncovered: List[Tuple[str, str]] = []
        redundant: List[Tuple[str, str]] = []
        for pointer, label, apply in mutations:
            mutated = copy.deepcopy(schema)
            try:
                apply(mutated)
            except (KeyError, IndexError, TypeError):
                continue
            if mutated == schema:
                continue
            if corpus_is_red(cases, mutated):
                covered.append(f"{pointer}: {label}")
                continue
            # Before blaming the corpus, ask whether ANY case could have caught
            # this. A constraint the schema makes unfalsifiable is not a
            # coverage gap.
            keyword = label.replace("delete ", "").split()[0]
            node_ptr = pointer.rsplit("/", 1)[0]
            try:
                node = _resolve(schema, node_ptr)
            except (KeyError, IndexError, TypeError):
                node = None
            if isinstance(node, dict) and is_unfalsifiable(node, keyword):
                redundant.append((pointer, label))
            else:
                uncovered.append((pointer, label))

        total = len(covered) + len(uncovered)
        pct = (100.0 * len(covered) / total) if total else 100.0
        worst = min(worst, pct)
        report[version] = {
            "cases": len(cases),
            "mutations": total,
            "covered": len(covered),
            "uncovered": [{"pointer": p, "mutation": m} for p, m in uncovered],
            "redundant": [{"pointer": p, "mutation": m} for p, m in redundant],
            "coveragePct": round(pct, 1),
        }

        if args.format == "text":
            print(f"\n{version}: {len(cases)} cases vs {total} falsifiable constraints")
            print(f"  covered   {len(covered):4}  ({pct:.1f}%)")
            print(f"  UNCOVERED {len(uncovered):4}")
            if redundant:
                print(
                    f"  redundant {len(redundant):4}  (schema findings, not corpus "
                    "gaps: an enum already makes these unfalsifiable)"
                )
                for pointer, label in redundant[:10]:
                    print(f"    {pointer}  --  {label}")
            for pointer, label in uncovered[:40]:
                print(f"    {pointer}  --  {label}")
            if len(uncovered) > 40:
                print(f"    ... and {len(uncovered) - 40} more (use --format json)")

    if args.format == "json":
        print(json.dumps(report, indent=2))

    if args.min_coverage is not None and worst < args.min_coverage:
        print(
            f"\nmutation-coverage: {worst:.1f}% is below the required "
            f"{args.min_coverage:.1f}%",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
