#!/usr/bin/env python3
"""Run the corpus against the reference implementation, not just the schema.

``conformance/run.py`` checks the corpus against the published JSON Schema
using a generic validator. That proves the corpus is right about the schema.
It does not prove the *reference implementation* agrees -- and forge-cli does
more than schema validation, so the two can drift.

This is the check that matters most, because the FLUID contract already has
more than one first-party reader:

  * ``fluid_build.schema_manager.FluidSchemaManager`` (forge-cli)
  * ``flux_engine.seam`` (the FLUX engine, which resolves and compiles a
    referenced FLUID contract with its own type parser)
  * the Command Center

Nothing has ever proved those agree about what a FLUID contract means. A
shared corpus is how they are held to one answer. This script covers the
first; the others plug in the same way.

    pip install data-product-forge
    python3 conformance/check_reference.py
    python3 conformance/check_reference.py --junit reference.xml

Exit 0 when the implementation's verdict matches the corpus on every case,
1 on any disagreement, 2 if the implementation is not installed.

A disagreement is not automatically an implementation bug. It can equally mean
the corpus is wrong, or that the implementation deliberately applies semantic
rules the schema cannot express. The first two must be fixed; the third belongs
in ``tests/optional/`` where it is asserted rather than tolerated.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run import (  # noqa: E402
    CorpusError,
    discover_versions,
    load_corpus,
    write_junit,
)


def load_reference():
    try:
        from fluid_build.schema_manager import FluidSchemaManager
    except ImportError:
        print(
            "check_reference: the reference implementation is not installed.\n"
            "  pip install data-product-forge\n"
            "This check is skipped rather than failed when forge-cli is absent, "
            "so the corpus stays runnable on its own.",
            file=sys.stderr,
        )
        return None
    return FluidSchemaManager()


def verdict(manager, contract: Dict[str, Any], version: str) -> Dict[str, Any]:
    """Normalise the implementation's answer to valid/invalid plus a reason."""
    try:
        result = manager.validate_contract(contract, schema_version=version)
    except Exception as exc:  # an exception is a verdict of 'invalid', loudly
        return {"valid": False, "reason": f"{type(exc).__name__}: {exc}", "raised": True}

    errors = list(getattr(result, "errors", []) or [])
    is_valid = getattr(result, "is_valid", None)
    if is_valid is None:
        is_valid = not errors
    return {
        "valid": bool(is_valid),
        "reason": "; ".join(str(e) for e in errors[:3]),
        "raised": False,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--version", action="append", dest="versions", metavar="X.Y.Z")
    ap.add_argument("--junit", type=Path, metavar="PATH")
    args = ap.parse_args(argv)

    manager = load_reference()
    if manager is None:
        return 2

    versions = args.versions or discover_versions()
    results: List[Dict[str, Any]] = []
    disagreements: List[str] = []
    unimplemented: List[str] = []

    for version in versions:
        try:
            # optional/ asserts semantics beyond the schema, which is exactly
            # what an implementation MAY implement -- include it here.
            cases = load_corpus(version, include_optional=True)
        except CorpusError as exc:
            print(f"check_reference: {exc}", file=sys.stderr)
            return 2

        for case in cases:
            test_id = f"{version}/{case['id']}"
            got = verdict(manager, case["contract"], version)
            agrees = got["valid"] == case["valid"]
            optional = bool(case.get("optional"))
            detail = ""
            if not agrees and optional:
                # The optional tier asserts behaviour the specification permits
                # but does not require. An implementation that does not do it is
                # still conformant, so this is reported, never failed.
                unimplemented.append(test_id)
                results.append(
                    {
                        "id": test_id,
                        "group": f"{version}.{case['group']}",
                        "source": case["source"],
                        "status": "skip",
                        "detail": "optional behaviour not implemented",
                    }
                )
                continue
            if not agrees:
                expected = "VALID" if case["valid"] else "INVALID"
                actual = "VALID" if got["valid"] else "INVALID"
                detail = (
                    f"corpus says {expected}, {version} reference implementation "
                    f"says {actual}"
                )
                if got["reason"]:
                    detail += f"\n  implementation said: {got['reason'][:300]}"
                disagreements.append(test_id)
            results.append(
                {
                    "id": test_id,
                    "group": f"{version}.{case['group']}",
                    "source": case["source"],
                    "status": "pass" if agrees else "fail",
                    "detail": detail,
                }
            )

    for r in results:
        if r["status"] == "fail":
            print(f"\nDISAGREEMENT  {r['id']}\n  ({r['source']})\n  {r['detail']}")

    for test_id in unimplemented:
        print(f"\noptional, not implemented  {test_id}")

    print(
        f"\nreference implementation vs corpus: {len(results)} cases, "
        f"{len(results) - len(disagreements) - len(unimplemented)} agree, "
        f"{len(disagreements)} disagree, "
        f"{len(unimplemented)} optional behaviour(s) not implemented"
    )

    if args.junit:
        write_junit(args.junit, results)
        print(f"  junit: {args.junit}")

    return 1 if disagreements else 0


if __name__ == "__main__":
    sys.exit(main())
