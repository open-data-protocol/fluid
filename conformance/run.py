#!/usr/bin/env python3
"""The FLUID conformance runner.

Runs the vector corpus in ``tests/`` against a FLUID schema and reports which
cases an implementation gets right. FLUID's schemas are authored in forge-cli
and distributed here; this runner is what makes "FLUID-conformant" mean
something other than "the reference implementation did not crash".

    python3 conformance/run.py                      # every published version
    python3 conformance/run.py --version 0.7.5      # one version
    python3 conformance/run.py --junit report.xml   # for CI
    python3 conformance/run.py --list               # print test ids

Exit code is 0 only when every case behaves as the corpus says it must, and
every id in ``conformance/known-failures.txt`` still fails. A known failure
that starts passing is an error, not a quiet success: the corpus and the file
have to be updated together, or the record of what we cannot do yet rots.

Design borrowed (adapt-the-pattern) from prior art surveyed under
borrow-before-build:

* json-schema-org/JSON-Schema-Test-Suite (MIT) -- the corpus is data, grouped
  into per-topic files under a per-version directory, and requires only a JSON
  parser to consume. Its ``optional/`` split is ours too: ``tests/optional/``
  holds cases an implementation may legitimately not reach.
* protocolbuffers/protobuf (BSD-3-Clause) -- the failure-list file: one test id
  per line, ``#`` comments, kept sorted, so a suite can be strict without being
  merge-blocking on the day it lands.
* connectrpc/conformance (Apache-2.0) -- known-failing cases are still
  EXECUTED, so a fix flips them green loudly instead of silently.
* w3c/json-ld-api (W3C-20150513) -- asserting an expected *error code* rather
  than a message string, so the assertion survives rewording.
* flux-spec (Apache-2.0, same owner) -- the vectors envelope, and the
  meta-test discipline of proving a gate can actually fail.

Assertions are on JSON Schema keyword + RFC 6901 instance pointer, never on
message text, because message text is a rendering choice and every validator
words it differently. That is what keeps the corpus portable to ajv, to
check-jsonschema, and to an implementation in a language nobody has written
yet.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from xml.etree import ElementTree as ET

REPO = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO / "schema"
TESTS_DIR = REPO / "tests"
KNOWN_FAILURES = Path(__file__).resolve().parent / "known-failures.txt"

SCHEMA_URI_TEMPLATE = (
    "https://open-data-protocol.github.io/fluid/schema/fluid-schema-{version}.json"
)


class CorpusError(RuntimeError):
    """The corpus itself is malformed. Never a conformance failure."""


# --------------------------------------------------------------------------
# corpus loading
# --------------------------------------------------------------------------


def discover_versions() -> List[str]:
    """Corpus directories that have a matching published schema."""
    versions = []
    for child in sorted(TESTS_DIR.iterdir()):
        if not child.is_dir() or child.name == "optional":
            continue
        if (SCHEMA_DIR / f"fluid-schema-{child.name}.json").is_file():
            versions.append(child.name)
    return versions


def load_schema(version: str) -> Dict[str, Any]:
    path = SCHEMA_DIR / f"fluid-schema-{version}.json"
    if not path.is_file():
        raise CorpusError(f"no published schema for version {version}: {path}")
    return json.loads(path.read_text())


def _corpus_files(
    version: str, include_optional: bool, group: Optional[str] = None
) -> List[Tuple[Path, bool]]:
    pattern = f"{group}.json" if group else "*.json"
    files: List[Tuple[Path, bool]] = [
        (p, False) for p in sorted((TESTS_DIR / version).glob(pattern))
    ]
    optional_dir = TESTS_DIR / "optional" / version
    if include_optional and optional_dir.is_dir():
        files += [(p, True) for p in sorted(optional_dir.glob(pattern))]
    return files


def load_corpus(
    version: str, include_optional: bool, group: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Flatten every case for ``version`` into a list carrying its own id.

    A case id is ``<group>/<description>``. Descriptions are required to be
    unique inside a group so ids stay stable when cases are inserted -- an
    index-based id would renumber every downstream case on an insert and
    silently repoint every known-failure entry.
    """
    cases: List[Dict[str, Any]] = []
    for path, optional in _corpus_files(version, include_optional, group):
        doc = json.loads(path.read_text())
        # Deliberately not rebinding `group`: it is the file filter for the whole
        # loop, and a per-file label would clobber it on the second iteration.
        label = doc.get("group") or path.stem
        raw_cases = doc.get("cases")
        if not isinstance(raw_cases, list) or not raw_cases:
            raise CorpusError(f"{path}: 'cases' must be a non-empty array")

        seen: set = set()
        for case in raw_cases:
            desc = case.get("description")
            if not desc:
                raise CorpusError(f"{path}: every case needs a 'description'")
            if desc in seen:
                raise CorpusError(f"{path}: duplicate case description {desc!r}")
            seen.add(desc)
            if "contract" not in case:
                raise CorpusError(f"{path}: case {desc!r} has no 'contract'")
            if not isinstance(case.get("valid"), bool):
                raise CorpusError(f"{path}: case {desc!r} needs a boolean 'valid'")
            if case["valid"] and case.get("errors"):
                raise CorpusError(
                    f"{path}: case {desc!r} is valid but declares expected errors"
                )
            if not case["valid"] and not case.get("errors"):
                raise CorpusError(
                    f"{path}: case {desc!r} is invalid but declares no expected "
                    "errors -- an invalid case must say WHY, or it passes for "
                    "any reason at all"
                )
            cases.append(
                {
                    "id": f"{label}/{desc}",
                    "group": label,
                    "optional": optional,
                    "source": str(path.relative_to(REPO)),
                    **case,
                }
            )
    return cases


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------


def _build_validators(schema: Dict[str, Any]) -> Dict[bool, Any]:
    """One validator per tier, keyed by whether `format` is asserted.

    In JSON Schema 2020-12 `format` is an ANNOTATION by default, not an
    assertion: a conformant validator may accept "not-an-email" for
    {"format": "email"}. FLUID has never said which it wants, and its own
    reference implementation does not assert formats.

    So the core corpus is checked WITHOUT format assertion -- the weaker,
    universally-agreed reading -- and cases that depend on formats being
    assertive live in tests/optional/, exactly where JSON-Schema-Test-Suite
    puts its own format tests. That way the core corpus stays runnable by any
    conformant validator, and format behaviour is asserted where an
    implementation opts into it, rather than being silently assumed.
    """
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:  # pragma: no cover - environment problem, not a failure
        sys.exit(
            "conformance: the reference runner needs 'jsonschema'.\n"
            "  pip install jsonschema>=4.22\n"
            "An implementation in another language does not need this runner; "
            "the corpus under tests/ is plain JSON."
        )
    return {
        False: Draft202012Validator(schema),
        True: Draft202012Validator(schema, format_checker=FormatChecker()),
    }


def _pointer(error) -> str:
    """RFC 6901 pointer for the instance location that failed."""
    out = ""
    for part in error.absolute_path:
        out += "/" + str(part).replace("~", "~0").replace("/", "~1")
    return out


def _observed(error) -> Dict[str, Any]:
    obs = {"pointer": _pointer(error), "keyword": error.validator}
    # For 'required', the useful discriminator is WHICH property is missing.
    # jsonschema puts it in the message; the schema keeps it in validator_value
    # only as the full list, so recover it from the message deterministically.
    if error.validator == "required":
        msg = error.message
        if "'" in msg:
            obs["detail"] = msg.split("'")[1]
    elif error.validator == "additionalProperties":
        obs["detail"] = ", ".join(sorted(_extra_props(error)))
    return obs


def _extra_props(error) -> Iterable[str]:
    allowed = set()
    schema = error.schema or {}
    allowed |= set((schema.get("properties") or {}).keys())
    instance = error.instance if isinstance(error.instance, dict) else {}
    return sorted(set(instance.keys()) - allowed)


def _matches(expected: Dict[str, Any], observed: Sequence[Dict[str, Any]]) -> bool:
    """An expectation matches if some observed error agrees on every field it names.

    Expectations are deliberately partial: a case that says only
    ``{"keyword": "required", "detail": "fluidVersion"}`` should not break when
    a future schema change moves the pointer.
    """
    for obs in observed:
        if all(obs.get(k) == v for k, v in expected.items()):
            return True
    return False


def run_case(case: Dict[str, Any], validators: Dict[bool, Any]) -> Dict[str, Any]:
    validator = validators[bool(case.get("optional"))]
    errors = sorted(validator.iter_errors(case["contract"]), key=lambda e: str(e.path))
    observed = [_observed(e) for e in errors]
    actually_valid = not errors

    if case["valid"]:
        if actually_valid:
            return {"ok": True}
        return {
            "ok": False,
            "reason": "expected the contract to be VALID, but the schema rejected it",
            "observed": observed[:6],
        }

    if actually_valid:
        return {
            "ok": False,
            "reason": "expected the contract to be INVALID, but the schema accepted it",
            "observed": [],
        }

    unmet = [e for e in case["errors"] if not _matches(e, observed)]
    if unmet:
        return {
            "ok": False,
            "reason": "the contract was rejected, but not for the declared reason",
            "unmet": unmet,
            "observed": observed[:6],
        }
    return {"ok": True}


# --------------------------------------------------------------------------
# known failures
# --------------------------------------------------------------------------


def load_known_failures() -> List[str]:
    if not KNOWN_FAILURES.is_file():
        return []
    ids = []
    for line in KNOWN_FAILURES.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            ids.append(line)
    if ids != sorted(ids):
        raise CorpusError(
            f"{KNOWN_FAILURES.name} must be sorted so merges stay reviewable; "
            "run `sort -o conformance/known-failures.txt "
            "conformance/known-failures.txt`"
        )
    return ids


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------


def write_junit(path: Path, results: List[Dict[str, Any]]) -> None:
    suite = ET.Element(
        "testsuite",
        name="fluid-conformance",
        tests=str(len(results)),
        failures=str(sum(1 for r in results if r["status"] == "fail")),
        skipped=str(sum(1 for r in results if r["status"] == "knownfail")),
    )
    for r in results:
        case = ET.SubElement(
            suite, "testcase", classname=r["group"], name=r["id"], file=r["source"]
        )
        if r["status"] == "fail":
            failure = ET.SubElement(case, "failure", message=r["detail"][:200])
            failure.text = r["detail"]
        elif r["status"] == "knownfail":
            ET.SubElement(case, "skipped", message="known failure")
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(suite).write(path, encoding="utf-8", xml_declaration=True)


def _describe(outcome: Dict[str, Any]) -> str:
    parts = [outcome.get("reason", "failed")]
    for e in outcome.get("unmet", []):
        parts.append(f"  expected error not raised: {json.dumps(e, sort_keys=True)}")
    for o in outcome.get("observed", []):
        parts.append(f"  observed: {json.dumps(o, sort_keys=True)}")
    return "\n".join(parts)


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Run the FLUID conformance corpus against a published schema."
    )
    ap.add_argument("--version", action="append", dest="versions", metavar="X.Y.Z")
    ap.add_argument(
        "--group",
        metavar="NAME",
        help="run only one corpus file (its stem), e.g. --group agentpolicy. "
        "Other files are not even loaded, so a malformed sibling cannot mask "
        "or break the group under test.",
    )
    ap.add_argument("--junit", type=Path, metavar="PATH")
    ap.add_argument("--list", action="store_true", help="print test ids and exit")
    ap.add_argument(
        "--no-optional",
        action="store_true",
        help="skip tests/optional/, which asserts semantics beyond the schema",
    )
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args(argv)

    versions = args.versions or discover_versions()
    if not versions:
        print("conformance: no corpus directories found under tests/", file=sys.stderr)
        return 2

    try:
        known = set(load_known_failures())
    except CorpusError as exc:
        print(f"conformance: {exc}", file=sys.stderr)
        return 2

    results: List[Dict[str, Any]] = []
    for version in versions:
        try:
            cases = load_corpus(
                version,
                include_optional=not args.no_optional,
                group=args.group,
            )
            validators = _build_validators(load_schema(version))
        except CorpusError as exc:
            print(f"conformance: {exc}", file=sys.stderr)
            return 2

        for case in cases:
            test_id = f"{version}/{case['id']}"
            if args.list:
                print(test_id)
                continue
            outcome = run_case(case, validators)
            expected_fail = test_id in known
            if outcome["ok"]:
                status = "unexpectedpass" if expected_fail else "pass"
                detail = (
                    "listed in known-failures.txt but PASSED -- remove the entry"
                    if expected_fail
                    else ""
                )
            else:
                status = "knownfail" if expected_fail else "fail"
                detail = _describe(outcome)
            results.append(
                {
                    "id": test_id,
                    "group": f"{version}.{case['group']}",
                    "source": case["source"],
                    "status": status,
                    "detail": detail,
                }
            )

    if args.list:
        return 0

    ran = {r["id"] for r in results}
    stale = [] if args.group else sorted(known - ran)
    failed = [r for r in results if r["status"] == "fail"]
    unexpected = [r for r in results if r["status"] == "unexpectedpass"]
    knownfail = [r for r in results if r["status"] == "knownfail"]

    if not args.quiet:
        for r in failed + unexpected:
            marker = "FAIL" if r["status"] == "fail" else "UNEXPECTED PASS"
            print(f"\n{marker}  {r['id']}\n  ({r['source']})\n{r['detail']}")

    print(
        f"\nfluid conformance: {len(results)} cases, "
        f"{len(results) - len(failed) - len(unexpected) - len(knownfail)} passed, "
        f"{len(failed)} failed, {len(unexpected)} unexpectedly passed, "
        f"{len(knownfail)} known failures"
    )
    for entry in stale:
        print(f"  stale known-failure (no such test): {entry}", file=sys.stderr)

    if args.junit:
        write_junit(args.junit, results)
        print(f"  junit: {args.junit}")

    return 1 if (failed or unexpected or stale) else 0


if __name__ == "__main__":
    sys.exit(main())
