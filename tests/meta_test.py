#!/usr/bin/env python3
"""Meta-test: prove the gates can actually fail.

A green gate is not evidence that the thing it guards is sound -- it is only
evidence that the gate said nothing. This file breaks things on purpose and
asserts that each gate goes red, so "conformance passed" and "compat passed"
carry information.

Every check runs against a disposable copy of the repo, so nothing here can
touch the real corpus, schemas or waivers.

    python3 tests/meta_test.py      (exit 0 = the gates are load-bearing)

Discipline borrowed from flux-spec's tests/test_regression.py (Apache-2.0,
same owner), which pairs its conformance vectors with a meta-test proving a
broken gate fails.
"""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

REPO = Path(__file__).resolve().parent.parent
PYTHON = sys.executable

RESULTS: List[Tuple[bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    RESULTS.append((condition, name if not detail else f"{name} -- {detail}"))
    print(f"  {'ok  ' if condition else 'FAIL'}  {name}")
    if not condition and detail:
        print(f"        {detail}")


def sandbox() -> Path:
    """A disposable copy of everything the gates read."""
    tmp = Path(tempfile.mkdtemp(prefix="fluid-meta-"))
    for sub in ("schema", "tests", "conformance", "scripts"):
        src = REPO / sub
        if src.is_dir():
            shutil.copytree(
                src, tmp / sub, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
            )
    return tmp


def run(root: Path, script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, str(root / script), *args],
        capture_output=True,
        text=True,
        cwd=root,
    )


def edit_json(path: Path, mutate: Callable[[Any], Any]) -> None:
    doc = json.loads(path.read_text())
    path.write_text(json.dumps(mutate(doc), indent=2))


# --------------------------------------------------------------------------
# the conformance runner must fail on a broken corpus
# --------------------------------------------------------------------------


def conformance_gate_is_load_bearing() -> None:
    print("\nconformance runner:")

    baseline = run(sandbox_root, "conformance/run.py", "-q")
    check(
        "clean corpus passes",
        baseline.returncode == 0,
        f"exit={baseline.returncode} {baseline.stdout[-300:]}",
    )

    # 1. a document that does not validate, asserted valid
    root = sandbox()
    envelope = root / "tests" / "0.7.5" / "envelope.json"
    edit_json(
        envelope,
        lambda d: {
            **d,
            "cases": d["cases"]
            + [
                {
                    "description": "META truly invalid asserted valid",
                    "contract": {"fluidVersion": "0.7.5"},
                    "valid": True,
                }
            ],
        },
    )
    r = run(root, "conformance/run.py", "-q")
    check("rejects an invalid document asserted valid", r.returncode == 1, f"exit={r.returncode}")
    shutil.rmtree(root, ignore_errors=True)

    # 2. a valid document asserted invalid
    root = sandbox()
    edit_json(
        root / "tests" / "0.7.5" / "envelope.json",
        lambda d: {
            **d,
            "cases": [
                {**c, "valid": False, "errors": [{"keyword": "required"}]}
                if c["description"].startswith("minimal document")
                else c
                for c in d["cases"]
            ],
        },
    )
    r = run(root, "conformance/run.py", "-q")
    check("rejects a valid document asserted invalid", r.returncode == 1, f"exit={r.returncode}")
    shutil.rmtree(root, ignore_errors=True)

    # 3. right verdict, wrong declared reason
    root = sandbox()
    edit_json(
        root / "tests" / "0.7.5" / "envelope.json",
        lambda d: {
            **d,
            "cases": [
                {**c, "errors": [{"pointer": "/nonexistent", "keyword": "maxLength"}]}
                if not c["valid"]
                else c
                for c in d["cases"]
            ],
        },
    )
    r = run(root, "conformance/run.py", "-q")
    check(
        "rejects a case that fails for a reason other than the declared one",
        r.returncode == 1,
        f"exit={r.returncode}",
    )
    shutil.rmtree(root, ignore_errors=True)

    # 4. an invalid case that declares no reason is a corpus error, not a pass
    root = sandbox()
    edit_json(
        root / "tests" / "0.7.5" / "envelope.json",
        lambda d: {
            **d,
            "cases": d["cases"]
            + [{"description": "META no reason", "contract": {}, "valid": False}],
        },
    )
    r = run(root, "conformance/run.py", "-q")
    check("refuses an invalid case with no declared reason", r.returncode == 2, f"exit={r.returncode}")
    shutil.rmtree(root, ignore_errors=True)

    # 5. a known-failure that starts passing must be reported, not silently absorbed
    root = sandbox()
    listing = run(root, "conformance/run.py", "--list")
    first_id = listing.stdout.splitlines()[0].strip()
    (root / "conformance" / "known-failures.txt").write_text(first_id + "\n")
    r = run(root, "conformance/run.py", "-q")
    check(
        "reports a known-failure that unexpectedly passes",
        r.returncode == 1,
        f"exit={r.returncode} for id {first_id!r}",
    )
    shutil.rmtree(root, ignore_errors=True)

    # 6. a known-failure naming no existing test is stale and must be reported
    root = sandbox()
    (root / "conformance" / "known-failures.txt").write_text("0.7.5/nosuch/case\n")
    r = run(root, "conformance/run.py", "-q")
    check("reports a stale known-failure entry", r.returncode == 1, f"exit={r.returncode}")
    shutil.rmtree(root, ignore_errors=True)

    # 7. an unsorted known-failures file is refused
    root = sandbox()
    (root / "conformance" / "known-failures.txt").write_text("z/case\na/case\n")
    r = run(root, "conformance/run.py", "-q")
    check("refuses an unsorted known-failures file", r.returncode == 2, f"exit={r.returncode}")
    shutil.rmtree(root, ignore_errors=True)


# --------------------------------------------------------------------------
# the compatibility gate must fail on each class of narrowing
# --------------------------------------------------------------------------


NARROWINGS: List[Tuple[str, Callable[[Dict[str, Any]], Dict[str, Any]]]] = [
    (
        "a newly required member",
        lambda s: {**s, "required": s["required"] + ["domain"]},
    ),
    (
        "a removed enum value",
        lambda s: _set_in(s, ["properties", "kind", "enum"], ["DataProduct"]),
    ),
    (
        "a removed property on a closed object",
        lambda s: _drop_in(s, ["properties", "metadata", "properties"], "layer"),
    ),
    (
        "a tightened lower bound",
        lambda s: _set_in(s, ["properties", "exposes", "minItems"], 2),
    ),
    (
        "a narrowed type",
        lambda s: _set_in(s, ["properties", "name", "type"], "null"),
    ),
    (
        "a removed $defs definition",
        lambda s: _drop_in(s, ["$defs"], "sovereignty"),
    ),
    (
        "an object becoming closed",
        lambda s: _set_in(s, ["$defs", "labels", "additionalProperties"], False),
    ),
]


def _set_in(schema: Dict[str, Any], path: List[str], value: Any) -> Dict[str, Any]:
    out = copy.deepcopy(schema)
    node = out
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    return out


def _drop_in(schema: Dict[str, Any], path: List[str], key: str) -> Dict[str, Any]:
    out = copy.deepcopy(schema)
    node = out
    for part in path:
        node = node[part]
    node.pop(key, None)
    return out


def compat_gate_is_load_bearing() -> None:
    print("\ncompatibility gate:")

    baseline = run(sandbox_root, "scripts/check-compat.py", "--from", "0.7.4", "--to", "0.7.5")
    check(
        "0.7.4 -> 0.7.5 passes as shipped",
        baseline.returncode == 0,
        f"exit={baseline.returncode}",
    )

    for name, mutate in NARROWINGS:
        root = sandbox()
        target = root / "schema" / "fluid-schema-0.7.5.json"
        target.write_text(json.dumps(mutate(json.loads(target.read_text())), indent=2))
        r = run(root, "scripts/check-compat.py", "--from", "0.7.4", "--to", "0.7.5")
        check(f"catches {name}", r.returncode == 1, f"exit={r.returncode}")
        shutil.rmtree(root, ignore_errors=True)

    # a waiver must silence exactly its own pointer and nothing else
    root = sandbox()
    target = root / "schema" / "fluid-schema-0.7.5.json"
    target.write_text(
        json.dumps(_set_in(json.loads(target.read_text()), ["properties", "exposes", "minItems"], 2), indent=2)
    )
    waivers = root / "scripts" / "compat-waivers.txt"
    waivers.write_text(waivers.read_text() + "0.7.4->0.7.5 /properties/exposes\n")
    r = run(root, "scripts/check-compat.py", "--from", "0.7.4", "--to", "0.7.5")
    check("a waiver silences its own pointer", r.returncode == 0, f"exit={r.returncode}")

    # ... but not a different narrowing elsewhere
    target.write_text(
        json.dumps(_set_in(json.loads(target.read_text()), ["properties", "kind", "enum"], ["DataProduct"]), indent=2)
    )
    r = run(root, "scripts/check-compat.py", "--from", "0.7.4", "--to", "0.7.5")
    check("a waiver does NOT silence an unrelated narrowing", r.returncode == 1, f"exit={r.returncode}")
    shutil.rmtree(root, ignore_errors=True)

    # the empirical pass must catch a narrowing the static pass would miss:
    # a pattern that rejects a value the corpus uses, with no structural change.
    root = sandbox()
    target = root / "schema" / "fluid-schema-0.7.5.json"
    schema = json.loads(target.read_text())
    schema["properties"]["name"]["pattern"] = "^ZZZ"
    target.write_text(json.dumps(schema, indent=2))
    (root / "tests" / "0.7.4").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        root / "tests" / "0.7.5" / "envelope.json", root / "tests" / "0.7.4" / "envelope.json"
    )
    r = run(root, "scripts/check-compat.py", "--from", "0.7.4", "--to", "0.7.5")
    check(
        "the empirical pass catches a previously-valid contract being rejected",
        r.returncode == 1 and "now rejected" in r.stdout,
        f"exit={r.returncode}",
    )
    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sandbox_root = sandbox()
    try:
        conformance_gate_is_load_bearing()
        compat_gate_is_load_bearing()
    finally:
        shutil.rmtree(sandbox_root, ignore_errors=True)

    failed = [name for ok, name in RESULTS if not ok]
    print(
        f"\nmeta-test: {len(RESULTS) - len(failed)}/{len(RESULTS)} checks passed"
    )
    if failed:
        print("\nThese gates are NOT load-bearing:")
        for name in failed:
            print(f"  - {name}")
    sys.exit(1 if failed else 0)
