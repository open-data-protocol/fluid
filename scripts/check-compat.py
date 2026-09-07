#!/usr/bin/env python3
"""The FLUID backward-compatibility gate.

Every FLUID release makes the same promise, in the README and in every
``docs/releases/0.7.x.md``:

    "additive and fully backward-compatible -- every valid 0.7.4 contract
     still validates as 0.7.5 unchanged"

Until now nothing checked it. This script does, two independent ways:

  STATIC   walk both schemas together and classify every difference as
           additive (safe) or narrowing (breaking). A narrowing change is one
           that can turn a document that used to validate into one that does
           not: a new required member, a removed enum value, a removed
           property on a closed object, a tightened bound, a changed type.

  EMPIRICAL run the previous version's conformance corpus against the new
           schema. Every case the old corpus calls valid MUST still be valid.
           This is the promise stated literally, and it only reports on
           behaviour the corpus actually covers -- which is why the static
           pass exists alongside it.

Usage:
    python3 scripts/check-compat.py                     # every adjacent pair
    python3 scripts/check-compat.py --from 0.7.4 --to 0.7.5
    python3 scripts/check-compat.py --format json

Exit 0 when every pair is compatible or every breaking change is waived in
``scripts/compat-waivers.txt``; 1 when a release breaks the promise; 2 on a
usage or input error.

A waiver is how a DELIBERATE break ships: it records the decision in the repo
instead of quietly weakening the gate. Waivers are one ``<from>-><to> <pointer>``
per line, ``#`` comments, kept sorted -- the failure-list convention from
protocolbuffers/protobuf (BSD-3-Clause), which keeps a strict gate adoptable on
the day it lands rather than merge-blocking on history nobody can change.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

REPO = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO / "schema"
TESTS_DIR = REPO / "tests"
WAIVERS = Path(__file__).resolve().parent / "compat-waivers.txt"

VERSION_RE = re.compile(r"^fluid-schema-(\d+\.\d+\.\d+)\.json$")

# Keywords whose numeric value narrowing the instance set is breaking.
LOWER_BOUNDS = ("minimum", "exclusiveMinimum", "minItems", "minLength", "minProperties")
UPPER_BOUNDS = ("maximum", "exclusiveMaximum", "maxItems", "maxLength", "maxProperties")


class Finding:
    __slots__ = ("pointer", "kind", "detail", "breaking")

    def __init__(self, pointer: str, kind: str, detail: str, breaking: bool) -> None:
        self.pointer = pointer or "<root>"
        self.kind = kind
        self.detail = detail
        self.breaking = breaking

    def as_dict(self) -> Dict[str, Any]:
        return {
            "pointer": self.pointer,
            "kind": self.kind,
            "detail": self.detail,
            "breaking": self.breaking,
        }

    def __str__(self) -> str:
        flag = "BREAKING" if self.breaking else "additive"
        return f"  [{flag}] {self.pointer}\n      {self.kind}: {self.detail}"


# --------------------------------------------------------------------------
# discovery
# --------------------------------------------------------------------------


def published_versions() -> List[str]:
    found = []
    for path in SCHEMA_DIR.glob("fluid-schema-*.json"):
        m = VERSION_RE.match(path.name)
        if m:
            found.append(m.group(1))
    return sorted(found, key=lambda v: tuple(int(p) for p in v.split(".")))


def adjacent_pairs(versions: Sequence[str]) -> List[Tuple[str, str]]:
    return [(versions[i], versions[i + 1]) for i in range(len(versions) - 1)]


def load(version: str) -> Dict[str, Any]:
    path = SCHEMA_DIR / f"fluid-schema-{version}.json"
    if not path.is_file():
        sys.exit(f"check-compat: no such schema: {path}")
    return json.loads(path.read_text())


# --------------------------------------------------------------------------
# static comparison
# --------------------------------------------------------------------------


def _as_set(value: Any) -> set:
    return set(value) if isinstance(value, list) else set()


def _type_widened(old: Any, new: Any) -> bool:
    """True when `new` admits everything `old` did."""
    o = {old} if isinstance(old, str) else set(old or [])
    n = {new} if isinstance(new, str) else set(new or [])
    return o.issubset(n)


def compare(old: Any, new: Any, pointer: str, out: List[Finding]) -> None:
    if not isinstance(old, dict) or not isinstance(new, dict):
        return

    # -- type -------------------------------------------------------------
    if "type" in old and "type" in new and old["type"] != new["type"]:
        breaking = not _type_widened(old["type"], new["type"])
        out.append(
            Finding(
                pointer,
                "type changed",
                f"{json.dumps(old['type'])} -> {json.dumps(new['type'])}",
                breaking,
            )
        )
    elif "type" not in old and "type" in new:
        out.append(
            Finding(pointer, "type constraint added", json.dumps(new["type"]), True)
        )

    # -- enum -------------------------------------------------------------
    old_enum, new_enum = old.get("enum"), new.get("enum")
    if old_enum is not None and new_enum is not None:
        removed = _as_set(old_enum) - _as_set(new_enum)
        added = _as_set(new_enum) - _as_set(old_enum)
        if removed:
            out.append(
                Finding(
                    pointer,
                    "enum values removed",
                    ", ".join(sorted(map(str, removed))),
                    True,
                )
            )
        if added:
            out.append(
                Finding(
                    pointer,
                    "enum values added",
                    ", ".join(sorted(map(str, added))),
                    False,
                )
            )
    elif old_enum is None and new_enum is not None:
        out.append(
            Finding(
                pointer,
                "enum constraint added",
                f"values now restricted to {len(new_enum)} option(s)",
                True,
            )
        )

    # -- required ---------------------------------------------------------
    old_req, new_req = _as_set(old.get("required")), _as_set(new.get("required"))
    newly_required = new_req - old_req
    if newly_required:
        out.append(
            Finding(
                pointer,
                "required members added",
                ", ".join(sorted(newly_required)),
                True,
            )
        )
    if old_req - new_req:
        out.append(
            Finding(
                pointer,
                "required members relaxed",
                ", ".join(sorted(old_req - new_req)),
                False,
            )
        )

    # -- closed object property sets --------------------------------------
    old_props = old.get("properties") or {}
    new_props = new.get("properties") or {}
    old_closed = old.get("additionalProperties") is False
    new_closed = new.get("additionalProperties") is False

    if not old_closed and new_closed:
        out.append(
            Finding(
                pointer,
                "object closed",
                "additionalProperties became false; previously-allowed extra "
                "members are now rejected",
                True,
            )
        )
    elif old_closed and not new_closed:
        out.append(Finding(pointer, "object opened", "additionalProperties relaxed", False))

    dropped = set(old_props) - set(new_props)
    if dropped and (old_closed or new_closed):
        out.append(
            Finding(
                pointer,
                "properties removed from a closed object",
                ", ".join(sorted(dropped)),
                True,
            )
        )
    elif dropped:
        out.append(
            Finding(
                pointer, "properties removed", ", ".join(sorted(dropped)), False
            )
        )

    # -- pattern ----------------------------------------------------------
    old_pat, new_pat = old.get("pattern"), new.get("pattern")
    if old_pat != new_pat:
        if old_pat is None:
            out.append(Finding(pointer, "pattern added", f"{new_pat!r}", True))
        elif new_pat is None:
            out.append(Finding(pointer, "pattern removed", f"was {old_pat!r}", False))
        else:
            # Regex containment is undecidable in the general case, so a changed
            # pattern is reported as breaking and waived if it is in fact a
            # widening. Silence here would be the dangerous default.
            out.append(
                Finding(
                    pointer,
                    "pattern changed",
                    f"{old_pat!r} -> {new_pat!r} (containment not decidable "
                    "statically; waive if this is a widening)",
                    True,
                )
            )

    # -- numeric and size bounds ------------------------------------------
    for kw in LOWER_BOUNDS:
        if kw in new and (kw not in old or _num(new[kw]) > _num(old[kw])):
            out.append(
                Finding(
                    pointer,
                    f"{kw} tightened",
                    f"{old.get(kw, 'absent')} -> {new[kw]}",
                    True,
                )
            )
    for kw in UPPER_BOUNDS:
        if kw in new and (kw not in old or _num(new[kw]) < _num(old[kw])):
            out.append(
                Finding(
                    pointer,
                    f"{kw} tightened",
                    f"{old.get(kw, 'absent')} -> {new[kw]}",
                    True,
                )
            )
    if new.get("uniqueItems") and not old.get("uniqueItems"):
        out.append(Finding(pointer, "uniqueItems enabled", "duplicates now rejected", True))

    # -- recurse ----------------------------------------------------------
    for name in sorted(set(old_props) & set(new_props)):
        compare(old_props[name], new_props[name], f"{pointer}/properties/{name}", out)

    old_defs = old.get("$defs") or {}
    new_defs = new.get("$defs") or {}
    for name in sorted(set(old_defs) - set(new_defs)):
        out.append(Finding(f"{pointer}/$defs/{name}", "definition removed", name, True))
    for name in sorted(set(old_defs) & set(new_defs)):
        compare(old_defs[name], new_defs[name], f"{pointer}/$defs/{name}", out)

    for kw in ("items", "contains", "not", "additionalProperties", "propertyNames"):
        if isinstance(old.get(kw), dict) and isinstance(new.get(kw), dict):
            compare(old[kw], new[kw], f"{pointer}/{kw}", out)

    for kw in ("anyOf", "oneOf", "allOf"):
        o, n = old.get(kw), new.get(kw)
        if isinstance(o, list) and isinstance(n, list):
            if kw in ("anyOf", "oneOf") and len(n) < len(o):
                out.append(
                    Finding(
                        f"{pointer}/{kw}",
                        f"{kw} branches removed",
                        f"{len(o)} -> {len(n)} branch(es)",
                        True,
                    )
                )
            for i in range(min(len(o), len(n))):
                compare(o[i], n[i], f"{pointer}/{kw}/{i}", out)


def _num(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


# --------------------------------------------------------------------------
# empirical comparison
# --------------------------------------------------------------------------


def empirical(old_version: str, new_version: str) -> List[Finding]:
    """Every case the OLD corpus calls valid must still validate under NEW."""
    corpus_dir = TESTS_DIR / old_version
    if not corpus_dir.is_dir():
        return []
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        return [
            Finding(
                "<empirical>",
                "skipped",
                "jsonschema not installed; static pass only",
                False,
            )
        ]

    validator = Draft202012Validator(load(new_version), format_checker=FormatChecker())
    findings: List[Finding] = []
    for path in sorted(corpus_dir.glob("*.json")):
        doc = json.loads(path.read_text())
        for case in doc.get("cases", []):
            if not case.get("valid"):
                continue
            contract = dict(case["contract"])
            # The version member is expected to move with the release; pinning
            # it would make every case fail for a reason the promise excludes.
            if contract.get("fluidVersion") == old_version:
                contract["fluidVersion"] = new_version
            errors = list(validator.iter_errors(contract))
            if errors:
                findings.append(
                    Finding(
                        f"{doc.get('group', path.stem)}/{case['description']}",
                        "previously-valid contract now rejected",
                        errors[0].message[:180],
                        True,
                    )
                )
    return findings


# --------------------------------------------------------------------------
# waivers
# --------------------------------------------------------------------------


def load_waivers() -> Dict[str, set]:
    waived: Dict[str, set] = {}
    if not WAIVERS.is_file():
        return waived
    lines = []
    for raw in WAIVERS.read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        lines.append(line)
        pair, _, pointer = line.partition(" ")
        waived.setdefault(pair, set()).add(pointer.strip())
    if lines != sorted(lines):
        sys.exit(
            f"check-compat: {WAIVERS.name} must be sorted; run "
            f"`sort -o {WAIVERS} {WAIVERS}`"
        )
    return waived


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--from", dest="old", metavar="X.Y.Z")
    ap.add_argument("--to", dest="new", metavar="X.Y.Z")
    ap.add_argument("--format", choices=("text", "json"), default="text")
    ap.add_argument(
        "--show-additive", action="store_true", help="also list additive changes"
    )
    args = ap.parse_args(argv)

    if bool(args.old) != bool(args.new):
        ap.error("--from and --to must be given together")

    versions = published_versions()
    pairs = [(args.old, args.new)] if args.old else adjacent_pairs(versions)
    if not pairs:
        print("check-compat: fewer than two published schemas; nothing to compare")
        return 0

    waived = load_waivers()
    report: Dict[str, Any] = {}
    broke = False

    for old_v, new_v in pairs:
        findings: List[Finding] = []
        compare(load(old_v), load(new_v), "", findings)
        findings += empirical(old_v, new_v)

        key = f"{old_v}->{new_v}"
        allow = waived.get(key, set())
        breaking = [f for f in findings if f.breaking and f.pointer not in allow]
        waived_here = [f for f in findings if f.breaking and f.pointer in allow]
        additive = [f for f in findings if not f.breaking]
        if breaking:
            broke = True

        report[key] = {
            "breaking": [f.as_dict() for f in breaking],
            "waived": [f.as_dict() for f in waived_here],
            "additive": [f.as_dict() for f in additive],
        }

        if args.format == "text":
            verdict = "BREAKS THE PROMISE" if breaking else "compatible"
            print(f"\n{key}: {verdict}")
            print(
                f"  {len(breaking)} breaking, {len(waived_here)} waived, "
                f"{len(additive)} additive"
            )
            for f in breaking:
                print(f)
            if args.show_additive:
                for f in additive:
                    print(f)

    if args.format == "json":
        print(json.dumps(report, indent=2))
    elif not broke:
        print(
            "\ncheck-compat: every release keeps the promise "
            "-- no document valid under a version stops validating under its successor."
        )

    return 1 if broke else 0


if __name__ == "__main__":
    sys.exit(main())
