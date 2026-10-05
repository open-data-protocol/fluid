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
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
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

    # the default run covers every pair the promise covers, and passes
    default = run(sandbox_root, "scripts/check-compat.py")
    check(
        "the default run (every promised pair) passes as shipped",
        default.returncode == 0,
        f"exit={default.returncode} {default.stdout[-300:]}",
    )
    # ... while the pre-promise history it skips is a real break, so the floor is
    # what makes the default pass, not a gate that cannot fail
    history = run(sandbox_root, "scripts/check-compat.py", "--all-history")
    check(
        "--all-history still reports the pre-promise break",
        history.returncode == 1,
        f"exit={history.returncode}",
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


# --------------------------------------------------------------------------
# the schema drift check must fail when the vendored copy and the reference
# release disagree
# --------------------------------------------------------------------------


def _fake_release(root: Path) -> Tuple[Path, Path]:
    """A local stand-in for a forge-cli release that matches schema/ exactly."""
    record = json.loads((root / "scripts" / "schema-versions.json").read_text())
    release = Path(tempfile.mkdtemp(prefix="fluid-meta-release-"))
    for version in record["synced"]:
        name = f"fluid-schema-{version}.json"
        shutil.copy(root / "schema" / name, release / name)
    preview = ", ".join(f'"{v}"' for v in record.get("preview", []))
    manager = release / "schema_manager.py"
    manager.write_text(
        "class FluidSchemaManager:\n"
        f"    PREVIEW_VERSIONS: FrozenSet[str] = frozenset({{{preview}}})\n"
    )
    return release, manager


def drift_gate_is_load_bearing() -> None:
    print("\nschema drift check:")
    record = json.loads((REPO / "scripts" / "schema-versions.json").read_text())
    newest = max(record["synced"], key=lambda v: tuple(int(p) for p in v.split(".")))

    def drift(root: Path, release: Path, manager: Path) -> subprocess.CompletedProcess:
        return run(
            root, "scripts/check-schema-drift.py",
            "--source-dir", str(release), "--schema-manager", str(manager),
        )

    root = sandbox()
    release, manager = _fake_release(root)
    r = drift(root, release, manager)
    check("an identical release passes", r.returncode == 0, f"exit={r.returncode} {r.stderr[-300:]}")

    # 1. a byte of difference, even one that leaves the JSON equal
    target = release / f"fluid-schema-{newest}.json"
    target.write_bytes(target.read_bytes() + b"\n")
    r = drift(root, release, manager)
    check("catches a byte-level difference in a synced schema", r.returncode == 1, f"exit={r.returncode}")
    shutil.rmtree(release, ignore_errors=True)

    # 2. the release bundles a version this repo does not publish
    release, manager = _fake_release(root)
    major, minor, patch = newest.split(".")
    shutil.copy(release / f"fluid-schema-{newest}.json", release / f"fluid-schema-{major}.{minor}.{int(patch) + 1}.json")
    r = drift(root, release, manager)
    check("catches a bundled version that is not vendored here", r.returncode == 1, f"exit={r.returncode}")
    shutil.rmtree(release, ignore_errors=True)

    # 3. the release promoted its preview to stable
    release, manager = _fake_release(root)
    manager.write_text("PREVIEW_VERSIONS: FrozenSet[str] = frozenset({})\n")
    r = drift(root, release, manager)
    check("catches a preview promoted to stable upstream", r.returncode == 1, f"exit={r.returncode}")

    # 4. a schema manager it cannot read is an error, not a pass
    manager.write_text("PREVIEW = set()\n")
    r = drift(root, release, manager)
    check("refuses a release whose preview set it cannot read", r.returncode == 2, f"exit={r.returncode}")
    shutil.rmtree(release, ignore_errors=True)
    shutil.rmtree(root, ignore_errors=True)


# --------------------------------------------------------------------------
# the drift check is pinned: it fails closed on a malformed pin, never sends the
# token across a redirect, and a newer upstream release is advisory only
# --------------------------------------------------------------------------


def _load_drift_module():
    spec = importlib.util.spec_from_file_location(
        "check_schema_drift", REPO / "scripts" / "check-schema-drift.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def drift_pin_is_load_bearing() -> None:
    print("\nschema drift pin:")
    root = sandbox()
    versions = root / "scripts" / "schema-versions.json"
    pristine = versions.read_text()

    # Both of these are refused before any network access: a pin that is
    # missing or malformed must not fall back to "whatever is latest".
    for name, mutate in (
        ("a pin with no commit", lambda d: d["upstream"].pop("commit")),
        ("a pin with no ref", lambda d: d["upstream"].pop("ref")),
        ("a pin whose commit is not a full SHA", lambda d: d["upstream"].update(commit="93e78d4")),
        ("a pin whose ref is not a release tag", lambda d: d["upstream"].update(ref="main")),
        ("a pin whose ref could inject into a URL", lambda d: d["upstream"].update(ref="v0.18.1/../../x")),
    ):
        record = json.loads(pristine)
        mutate(record)
        versions.write_text(json.dumps(record, indent=2))
        r = run(root, "scripts/check-schema-drift.py")
        check(f"refuses {name}", r.returncode == 2, f"exit={r.returncode} {r.stderr[-200:]}")
    versions.write_text(pristine)

    for bad in ("main", "v1.2.3; echo pwned", "v1.2.3\n", "$(id)", "v1.2.3/../x"):
        r = run(root, "scripts/check-schema-drift.py", "--ref", bad)
        check(f"refuses --ref {bad!r}", r.returncode == 2, f"exit={r.returncode}")
    shutil.rmtree(root, ignore_errors=True)

    mod = _load_drift_module()
    check(
        "accepts a plain release tag, with and without the v",
        mod.validate_ref("v0.18.1", "t") == "v0.18.1" and mod.validate_ref("0.18.1", "t") == "0.18.1",
    )
    github = mod.GitHubRelease(
        "Agenticstiger/forge-cli", "fluid_build/schemas", "fluid_build/schema_manager.py",
        "v0.18.1", "93e78d4386c70b9e040283f9c5d98a89f901c986",
    )
    check(
        "a pinned run fetches by the commit, not the movable tag",
        "/93e78d4386c70b9e040283f9c5d98a89f901c986/" in github.url("0.7.5") and "v0.18.1" not in github.url("0.7.5"),
        github.url("0.7.5"),
    )

    # the token goes to api.github.com only, and never rides a redirect
    seen: List[urllib.request.Request] = []

    class _Response:
        def __enter__(self): return self
        def __exit__(self, *exc): return False
        def read(self): return b"{}"

    real_urlopen, real_token = urllib.request.urlopen, os.environ.get("GITHUB_TOKEN")
    urllib.request.urlopen = lambda req, timeout=None: seen.append(req) or _Response()
    os.environ["GITHUB_TOKEN"] = "meta-test-token"
    try:
        mod._get("https://api.github.com/repos/x/y/releases/latest")
        mod._get("https://raw.githubusercontent.com/x/y/z/file")
    finally:
        urllib.request.urlopen = real_urlopen
        if real_token is None:
            os.environ.pop("GITHUB_TOKEN", None)
        else:
            os.environ["GITHUB_TOKEN"] = real_token
    api, raw = seen
    check(
        "the token is sent unredirected: not among the headers a redirect copies",
        "Authorization" not in api.headers and api.unredirected_hdrs.get("Authorization") == "Bearer meta-test-token",
        f"headers={dict(api.headers)} unredirected={dict(api.unredirected_hdrs)}",
    )
    check(
        "the token is not sent to any other host",
        "Authorization" not in raw.headers and "Authorization" not in raw.unredirected_hdrs,
    )

    # --latest is advisory: exit 1 with the notice when a newer release exists,
    # exit 0 when the pin is the latest; the default (pinned) run never asks.
    root = sandbox()
    release, manager = _fake_release(root)
    record = json.loads((root / "scripts" / "schema-versions.json").read_text())
    pinned = record["upstream"]["ref"]
    mod.GitHubRelease = lambda *a, **k: mod.LocalDir(release, manager)
    try:
        mod.latest_release_tag = lambda repository: "v99.0.0"
        import contextlib, io
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = mod.run_latest(record)
        check(
            "--latest reports a newer release and exits 1",
            code == 1 and "a newer forge-cli release exists" in out.getvalue(),
            f"exit={code}",
        )
        mod.latest_release_tag = lambda repository: pinned
        with contextlib.redirect_stdout(io.StringIO()):
            code = mod.run_latest(record)
        check("--latest exits 0 when the pinned release is the latest", code == 0, f"exit={code}")
    finally:
        shutil.rmtree(release, ignore_errors=True)
        shutil.rmtree(root, ignore_errors=True)


# --------------------------------------------------------------------------
# generate-docs.py --check accounts for every file under schema/ and specs/
# --------------------------------------------------------------------------


def unaccounted_files_gate_is_load_bearing() -> None:
    print("\nfile inventory (generate-docs.py --check-files, the offline half of --check):")
    # specs/ is ~25 MB, so one copy is mutated and restored rather than one per case.
    root = Path(tempfile.mkdtemp(prefix="fluid-meta-specs-"))
    try:
        for sub in ("schema", "scripts", "specs"):
            shutil.copytree(REPO / sub, root / sub, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copy(REPO / "generate-docs.py", root / "generate-docs.py")

        def gate() -> subprocess.CompletedProcess:
            return run(root, "generate-docs.py", "--check-files")

        r = gate()
        check("a tree with every file accounted for passes", r.returncode == 0, f"exit={r.returncode} {r.stderr[-300:]}")

        # 1. a file beside the generated outputs of a synced version
        extra = root / "specs" / "0.7.6" / "extra.html"
        extra.write_text("<p>not generated</p>")
        r = gate()
        check(
            "rejects an extra file beside a synced version's generated pages",
            r.returncode == 1 and "specs/0.7.6/extra.html" in r.stderr,
            f"exit={r.returncode}",
        )
        extra.unlink()

        # 2. one byte appended to a frozen, non-synced page
        frozen_page = root / "specs" / "0.7.1" / "fluid-spec.html"
        original = frozen_page.read_bytes()
        frozen_page.write_bytes(original + b" ")
        r = gate()
        check(
            "rejects a one-byte change to a frozen page (specs/0.7.1)",
            r.returncode == 1 and "specs/0.7.1/fluid-spec.html" in r.stderr,
            f"exit={r.returncode}",
        )
        frozen_page.write_bytes(original)

        # 3. a frozen schema edited
        frozen_schema = root / "schema" / "fluid-schema-0.7.1.json"
        original = frozen_schema.read_bytes()
        frozen_schema.write_bytes(original + b"\n")
        r = gate()
        check("rejects a one-byte change to a frozen schema (0.7.1)", r.returncode == 1, f"exit={r.returncode}")
        frozen_schema.write_bytes(original)

        # 4. a frozen file deleted
        gone = root / "schema" / "fluid-schema-0.5.7.json"
        saved = gone.read_bytes()
        gone.unlink()
        r = gate()
        check("rejects a frozen file that has been deleted", r.returncode == 1, f"exit={r.returncode}")
        gone.write_bytes(saved)

        # 5. a schema that is neither synced nor frozen
        stray = root / "schema" / "fluid-schema-0.7.7.json"
        shutil.copy(root / "schema" / "fluid-schema-0.7.6.json", stray)
        r = gate()
        check(
            "rejects a schema that is neither synced nor frozen",
            r.returncode == 1 and "fluid-schema-0.7.7.json" in r.stderr,
            f"exit={r.returncode}",
        )
        stray.unlink()

        # 6. the hash-locked requirements and the pins people edit must agree
        pins = root / "scripts" / "requirements-docs.txt"
        saved = pins.read_text()
        pins.write_text(saved.replace("Jinja2==3.1.6", "Jinja2==3.1.5"))
        r = gate()
        check("rejects a pin the lock file does not match", r.returncode == 1 and "Jinja2" in r.stderr, f"exit={r.returncode}")
        pins.write_text(saved)

        r = gate()
        check("and passes again once everything is restored", r.returncode == 0, f"exit={r.returncode} {r.stderr[-300:]}")
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sandbox_root = sandbox()
    try:
        conformance_gate_is_load_bearing()
        compat_gate_is_load_bearing()
        drift_gate_is_load_bearing()
        drift_pin_is_load_bearing()
        unaccounted_files_gate_is_load_bearing()
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
