#!/usr/bin/env python3
"""Render the HTML schema reference: specs/<version>/fluid-spec.html.

    python3 generate-docs.py                      # every synced version
    python3 generate-docs.py --all                # the same, spelled out
    python3 generate-docs.py --version 0.7.6      # one version (repeatable)
    python3 generate-docs.py --check              # render to a temp dir and
                                                  # fail if specs/ is stale
    python3 generate-docs.py --print-latest-stable

Which versions are "synced", and which one is the latest STABLE version, is
recorded once, in scripts/schema-versions.json. The latest stable version is
not the highest version number: a preview has the higher number and is never
"latest". This script used to render only the highest-numbered schema, so a
re-vendored older version kept its stale HTML, and vendoring a preview would
have made the preview the only page CI and the docs deploy ever refreshed.

The renderer is json-schema-for-humans, run in-process, with the exact
versions pinned in scripts/requirements-docs.txt. The output is committed and
--check compares it byte for byte, so the renderer version is part of the
input; the script refuses to run with any other installed version. The footer
timestamp is switched off so that the same schema and the same renderer give
the same bytes.
"""

from __future__ import annotations

import argparse
import filecmp
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
            + f"\nInstall them with:  pip install -r {REQUIREMENTS.relative_to(REPO)}"
        )


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
    ap.add_argument("--check", action="store_true", help="fail if specs/ differs from a fresh render")
    ap.add_argument("--print-latest-stable", action="store_true")
    args = ap.parse_args(argv)

    data = load_versions()
    if args.print_latest_stable:
        print(data["latestStable"])
        return 0

    versions = args.versions or data["synced"]
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
        return 1
    log(f"specs/ is current for {', '.join(versions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
