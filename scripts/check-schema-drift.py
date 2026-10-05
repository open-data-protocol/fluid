#!/usr/bin/env python3
"""Check that the vendored schemas equal the reference implementation's latest release.

    python3 scripts/check-schema-drift.py                  # latest forge-cli release
    python3 scripts/check-schema-drift.py --ref v0.18.1    # a named tag
    python3 scripts/check-schema-drift.py --source-dir DIR # offline: a directory
                                                           # holding fluid-schema-*.json
                                                           # (and, optionally,
                                                           # schema_manager.py)

The FLUID schemas are authored in forge-cli and vendored into schema/ byte for
byte. This script is the check that they still match; it lands nothing. It
compares against a RELEASE, not forge-cli's main branch: a release is what
`pip install data-product-forge` gives people, while main carries unreleased
schema edits that would turn this check red before anyone could validate a
contract against them.

What it checks, against scripts/schema-versions.json:

  1. every version listed in "synced" is byte-identical to the release's copy;
  2. the release bundles no version, at or above the oldest synced one, that
     is missing from "synced" -- so a new schema cannot ship unpublished;
  3. the release's preview set (PREVIEW_VERSIONS in schema_manager.py) equals
     "preview", and "latestStable" is the release's highest non-preview
     version -- so a promotion to stable is not missed.

Exit 0 when everything matches; 1 on drift; 2 when the release cannot be
read. The output says how to re-vendor.

The latest release is resolved at run time from the GitHub API; set
GITHUB_TOKEN to avoid the unauthenticated rate limit.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Set

REPO = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO / "schema"
VERSIONS_FILE = REPO / "scripts" / "schema-versions.json"
SCHEMA_RE = re.compile(r"^fluid-schema-(\d+\.\d+\.\d+)\.json$")
PREVIEW_RE = re.compile(r"PREVIEW_VERSIONS\b[^=\n]*=\s*frozenset\(\s*\{([^}]*)\}\s*\)")


class SourceError(RuntimeError):
    pass


def vkey(v: str):
    return tuple(int(p) for p in v.split("."))


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------


def _get(url: str) -> bytes:
    headers = {"User-Agent": "fluid-schema-drift-check"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
            return r.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise SourceError(f"could not fetch {url}: {exc}") from exc


class GitHubRelease:
    def __init__(self, repository: str, schema_dir: str, preview_source: str, ref: Optional[str]):
        self.repository = repository
        self.schema_dir = schema_dir
        self.preview_source = preview_source
        if ref is None:
            data = json.loads(_get(f"https://api.github.com/repos/{repository}/releases/latest"))
            ref = data.get("tag_name")
            if not ref:
                raise SourceError(f"{repository} reports no latest release")
        self.ref = ref
        self.label = f"{repository}@{ref}"

    def _raw(self, path: str) -> bytes:
        return _get(f"https://raw.githubusercontent.com/{self.repository}/{self.ref}/{path}")

    def versions(self) -> List[str]:
        listing = json.loads(
            _get(f"https://api.github.com/repos/{self.repository}/contents/{self.schema_dir}?ref={self.ref}")
        )
        names = [entry["name"] for entry in listing if entry.get("type") == "file"]
        return sorted((m.group(1) for n in names if (m := SCHEMA_RE.match(n))), key=vkey)

    def schema(self, version: str) -> bytes:
        return self._raw(f"{self.schema_dir}/fluid-schema-{version}.json")

    def preview_text(self) -> Optional[str]:
        return self._raw(self.preview_source).decode("utf-8")

    def url(self, version: str) -> str:
        return f"https://raw.githubusercontent.com/{self.repository}/{self.ref}/{self.schema_dir}/fluid-schema-{version}.json"


class LocalDir:
    def __init__(self, path: Path, preview_source: Optional[Path]):
        if not path.is_dir():
            raise SourceError(f"not a directory: {path}")
        self.path = path
        self.preview_path = preview_source
        self.label = str(path)

    def versions(self) -> List[str]:
        return sorted((m.group(1) for p in self.path.iterdir() if (m := SCHEMA_RE.match(p.name))), key=vkey)

    def schema(self, version: str) -> bytes:
        return (self.path / f"fluid-schema-{version}.json").read_bytes()

    def preview_text(self) -> Optional[str]:
        if self.preview_path and self.preview_path.is_file():
            return self.preview_path.read_text()
        return None

    def url(self, version: str) -> str:
        return str(self.path / f"fluid-schema-{version}.json")


def parse_preview(text: str) -> Set[str]:
    m = PREVIEW_RE.search(text)
    if not m:
        raise SourceError(
            "could not find `PREVIEW_VERSIONS = frozenset({...})` in the reference "
            "implementation's schema manager; update PREVIEW_RE in this script"
        )
    return set(re.findall(r"[\"'](\d+\.\d+\.\d+)[\"']", m.group(1)))


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------


def canonical(raw: bytes):
    return json.loads(raw)


def check(source, record: Dict) -> List[str]:
    problems: List[str] = []
    synced: List[str] = record["synced"]
    preview: Set[str] = set(record.get("preview", []))
    stable: str = record["latestStable"]
    floor = min(synced, key=vkey)

    upstream = source.versions()
    print(f"reference: {source.label}")
    print(f"  bundles: {', '.join(upstream) or '(none)'}")

    for version in synced:
        local = SCHEMA_DIR / f"fluid-schema-{version}.json"
        if version not in upstream:
            problems.append(f"{version}: listed as synced, but {source.label} does not bundle it")
            continue
        if not local.is_file():
            problems.append(f"{version}: listed as synced, but schema/{local.name} is missing")
            continue
        theirs = source.schema(version)
        ours = local.read_bytes()
        if ours == theirs:
            print(f"  ok   {version}  byte-identical")
            continue
        kind = "formatting only (same JSON, different bytes)" if canonical(ours) == canonical(theirs) else "content differs"
        problems.append(
            f"{version}: schema/{local.name} drifted from {source.label}: {kind}\n"
            f"        re-vendor: curl -fsSL {source.url(version)} -o schema/{local.name}"
        )

    for version in upstream:
        if vkey(version) >= vkey(floor) and version not in synced:
            problems.append(
                f"{version}: {source.label} bundles it, but it is not vendored here "
                f"(add it to schema/ and to \"synced\" in {VERSIONS_FILE.name})"
            )

    text = source.preview_text()
    if text is None:
        print("  preview set: not checked (no schema manager source given)")
    else:
        theirs = parse_preview(text)
        if theirs != preview:
            problems.append(
                f"preview versions: {source.label} has {sorted(theirs, key=vkey)}, "
                f"{VERSIONS_FILE.name} says {sorted(preview, key=vkey)}"
            )
        stable_upstream = [v for v in upstream if v not in theirs]
        if stable_upstream and stable_upstream[-1] != stable:
            problems.append(
                f"latest stable: {source.label}'s highest non-preview version is "
                f"{stable_upstream[-1]}, {VERSIONS_FILE.name} says {stable}"
            )
        if not problems:
            print(f"  ok   preview {sorted(theirs, key=vkey)}, latest stable {stable}")
    return problems


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ref", help="forge-cli tag to compare against (default: its latest release)")
    ap.add_argument("--source-dir", type=Path, help="compare against this directory instead of GitHub")
    ap.add_argument(
        "--schema-manager",
        type=Path,
        help="with --source-dir: the schema_manager.py whose PREVIEW_VERSIONS to compare",
    )
    args = ap.parse_args(argv)

    record = json.loads(VERSIONS_FILE.read_text())
    up = record["upstream"]
    try:
        if args.source_dir:
            source = LocalDir(args.source_dir, args.schema_manager)
        else:
            source = GitHubRelease(up["repository"], up["schemaDir"], up["previewSource"], args.ref)
        problems = check(source, record)
    except SourceError as exc:
        print(f"check-schema-drift: {exc}", file=sys.stderr)
        return 2

    if problems:
        print("\ncheck-schema-drift: the published schemas no longer match the reference release:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print(
            "\nRe-vendor byte for byte (never edit a schema here), update "
            f"scripts/{VERSIONS_FILE.name}, then run `python3 generate-schema-diffs.py` "
            "and `python3 generate-docs.py` and commit the results. CONTRIBUTING.md "
            "lists the steps.",
            file=sys.stderr,
        )
        return 1
    print("\ncheck-schema-drift: every synced schema matches the reference release.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
