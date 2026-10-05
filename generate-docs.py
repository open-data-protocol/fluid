#!/usr/bin/env python3
"""Render the HTML schema reference: specs/<version>/fluid-spec.html.

    python3 generate-docs.py                      # every synced version
    python3 generate-docs.py --all                # the same, spelled out
    python3 generate-docs.py --version 0.7.6      # one version (repeatable)
    python3 generate-docs.py --check              # render to a temp dir and
                                                  # fail if specs/ is stale, or
                                                  # holds a file it should not
    python3 generate-docs.py --check-files        # the offline half of --check
    python3 generate-docs.py --print-latest-stable

Which versions are "synced", and which one is the latest STABLE version, is
recorded once, in scripts/schema-versions.json. The latest stable version is
not the highest version number: a preview has the higher number and is never
"latest". This script used to render only the highest-numbered schema, so a
re-vendored older version kept its stale HTML, and vendoring a preview would
have made the preview the only page CI and the docs deploy ever refreshed.

The renderer is json-schema-for-humans, run in-process, with the exact
versions pinned in scripts/requirements-docs.txt (the file a person edits) and
installed from scripts/requirements-docs.lock (the same pins plus their
transitive closure, hash-locked, which is what CI installs). The output is
committed and --check compares it byte for byte, so the renderer version is
part of the input; the script refuses to run with any other installed version.
The footer timestamp is switched off so that the same schema and the same
renderer give the same bytes.

--check also accounts for every file under schema/ and specs/, offline. A file
is either generated (schema/fluid-schema-<synced>.json, which the drift check
compares with the reference implementation, and the OUTPUT_FILES of a synced
version under specs/) or "frozen": listed with its sha256 in
scripts/schema-versions.json. A file that is neither fails the check, as does a
frozen file whose bytes changed. Without this, only the synced versions'
outputs were compared, and the older pages and schemas -- and any extra file
dropped beside the generated ones -- could change with every gate green.
--check-files runs just this part and the lock check; it needs no renderer.
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, List

REPO = Path(__file__).resolve().parent
SCHEMA_DIR = REPO / "schema"
SPECS_DIR = REPO / "specs"
VERSIONS_FILE = REPO / "scripts" / "schema-versions.json"
REQUIREMENTS = REPO / "scripts" / "requirements-docs.txt"
LOCK = REPO / "scripts" / "requirements-docs.lock"
OUTPUT_FILES = ("fluid-spec.html", "schema_doc.css", "schema_doc.min.js")


def log(msg: str) -> None:
    print(f"[fluid-docs] {msg}")


def version_key(version: str):
    return tuple(int(p) for p in version.split("."))


def load_versions() -> Dict:
    data = json.loads(VERSIONS_FILE.read_text())
    stable = data["latestStable"]
    preview = set(data.get("preview", []))
    synced = data["synced"]
    if stable in preview:
        sys.exit(f"{VERSIONS_FILE.name}: latestStable {stable} is also listed as preview")
    if stable not in synced:
        sys.exit(f"{VERSIONS_FILE.name}: latestStable {stable} is not in synced")
    highest_stable = max((v for v in synced if v not in preview), key=version_key)
    if highest_stable != stable:
        sys.exit(
            f"{VERSIONS_FILE.name}: latestStable is {stable}, but {highest_stable} "
            "is a higher synced version that is not a preview"
        )
    return data


def check_renderer_pins() -> None:
    """Refuse to render with anything but the pinned renderer."""
    from importlib.metadata import PackageNotFoundError, version

    pins = {}
    for line in REQUIREMENTS.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        m = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^\s]+)", line)
        if m:
            pins[m.group(1)] = m.group(2)
    wrong = []
    for name, wanted in pins.items():
        try:
            got = version(name)
        except PackageNotFoundError:
            got = "not installed"
        if got != wanted:
            wrong.append(f"{name}: need {wanted}, found {got}")
    if wrong:
        sys.exit(
            "generate-docs: the HTML renderer does not match its pins:\n  "
            + "\n  ".join(wrong)
            + f"\nInstall them with:  pip install --require-hashes -r {LOCK.relative_to(REPO)}"
        )


def _normalise(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def check_lock() -> List[str]:
    """requirements-docs.txt (edited) and requirements-docs.lock (installed) pin the same versions."""
    if not LOCK.is_file():
        return [f"{LOCK.relative_to(REPO)} is missing (pip-compile --generate-hashes; see its sibling .txt)"]
    locked = {}
    for line in LOCK.read_text().splitlines():
        m = re.match(r"([A-Za-z0-9_.-]+)==(\S+?)\s*\\?\s*$", line)
        if m:
            locked[_normalise(m.group(1))] = m.group(2)
    problems = []
    for line in REQUIREMENTS.read_text().splitlines():
        m = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^\s]+)", line.split("#", 1)[0].strip())
        if not m:
            continue
        name, wanted = m.groups()
        got = locked.get(_normalise(name))
        if got != wanted:
            problems.append(
                f"{REQUIREMENTS.name} pins {name}=={wanted}, but {LOCK.name} has "
                f"{'no entry' if got is None else got}; recompile the lock"
            )
    return problems


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_inventory(data: Dict) -> List[str]:
    """Every file under schema/ and specs/ is generated output of a synced version, or frozen.

    The synced versions' outputs are compared with a fresh render and the synced
    schemas with the reference implementation, so they are not hashed here. All
    other files are hashed against the "frozen" map in scripts/schema-versions.json.
    """
    synced = data["synced"]
    frozen = data.get("frozen")
    if not isinstance(frozen, dict):
        return [f'{VERSIONS_FILE.name} has no "frozen" map, so nothing under schema/ or specs/ outside the synced versions can be accounted for']

    generated = {f"specs/{v}/{name}" for v in synced for name in OUTPUT_FILES}
    synced_schemas = {f"schema/fluid-schema-{v}.json" for v in synced}
    problems: List[str] = []

    for rel, digest in sorted(frozen.items()):
        if rel in generated or rel in synced_schemas:
            problems.append(f"{rel}: listed in \"frozen\", but it belongs to a synced version, which is compared instead")
            continue
        if not rel.startswith(("schema/", "specs/")) or ".." in rel.split("/"):
            problems.append(f"{rel}: \"frozen\" lists only files under schema/ and specs/")
            continue
        path = REPO / rel
        if path.is_symlink() or not path.is_file():
            problems.append(f"{rel}: listed in \"frozen\", but the file is missing")
        elif sha256_of(path) != digest:
            problems.append(f"{rel}: differs from its frozen sha256 (a frozen file is never edited; changing one is a deliberate edit to \"frozen\")")

    for root in (SCHEMA_DIR, SPECS_DIR):
        for path in sorted(root.rglob("*")):
            if path.is_dir() and not path.is_symlink():
                continue
            rel = path.relative_to(REPO).as_posix()
            if path.is_symlink():
                problems.append(f"{rel}: a symbolic link; schema/ and specs/ hold regular files only")
            elif rel not in generated and rel not in synced_schemas and rel not in frozen:
                problems.append(
                    f"{rel}: neither generated output of a synced version nor listed in \"frozen\" "
                    f"in scripts/{VERSIONS_FILE.name}"
                )
    return problems


def render(version: str, out_dir: Path) -> None:
    from json_schema_for_humans.generate import generate_from_filename
    from json_schema_for_humans.generation_configuration import GenerationConfiguration

    schema_file = SCHEMA_DIR / f"fluid-schema-{version}.json"
    if not schema_file.is_file():
        sys.exit(f"generate-docs: no schema for version {version}: {schema_file}")
    out_dir.mkdir(parents=True, exist_ok=True)
    config = GenerationConfiguration(footer_show_time=False)
    generate_from_filename(str(schema_file), str(out_dir / "fluid-spec.html"), config=config)


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    which = ap.add_mutually_exclusive_group()
    which.add_argument("--all", action="store_true", help="every synced version (the default)")
    which.add_argument("--version", action="append", dest="versions", metavar="X.Y.Z")
    ap.add_argument(
        "--check",
        action="store_true",
        help="fail if specs/ differs from a fresh render, or schema/ or specs/ holds an unaccounted-for file",
    )
    ap.add_argument(
        "--check-files",
        action="store_true",
        help="only the offline half of --check (every file accounted for, lock matches pins); needs no renderer",
    )
    ap.add_argument("--print-latest-stable", action="store_true")
    args = ap.parse_args(argv)

    data = load_versions()
    if args.print_latest_stable:
        print(data["latestStable"])
        return 0

    versions = args.versions or data["synced"]

    if args.check or args.check_files:
        lock_problems = check_lock()
        if lock_problems:
            print("generate-docs: the lock does not match the pins:", file=sys.stderr)
            for problem in lock_problems:
                print(f"  {problem}", file=sys.stderr)
        inventory_problems = check_inventory(data)
        if inventory_problems:
            print("generate-docs: files under schema/ and specs/ that are not accounted for:", file=sys.stderr)
            for problem in inventory_problems:
                print(f"  {problem}", file=sys.stderr)
        file_problems = lock_problems + inventory_problems
        if args.check_files:
            if file_problems:
                return 1
            log("every file under schema/ and specs/ is generated or frozen, and the lock matches the pins")
            return 0
    else:
        file_problems = []

    check_renderer_pins()

    if not args.check:
        for v in versions:
            log(f"rendering {v} -> specs/{v}/fluid-spec.html")
            render(v, SPECS_DIR / v)
        log(f"latest stable: {data['latestStable']}; preview: {', '.join(data.get('preview', [])) or 'none'}")
        return 0

    stale = []
    with tempfile.TemporaryDirectory() as tmp:
        for v in versions:
            fresh = Path(tmp) / v
            render(v, fresh)
            for name in OUTPUT_FILES:
                committed = SPECS_DIR / v / name
                if not committed.is_file() or not filecmp.cmp(fresh / name, committed, shallow=False):
                    stale.append(f"specs/{v}/{name}")
    if stale:
        print("generate-docs: specs/ is out of date with schema/:", file=sys.stderr)
        for path in stale:
            print(f"  {path}", file=sys.stderr)
        print(
            "Run `python3 generate-docs.py` and commit the result.",
            file=sys.stderr,
        )
    if stale or file_problems:
        return 1
    log(f"specs/ is current for {', '.join(versions)}; every other file under schema/ and specs/ is frozen and unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
