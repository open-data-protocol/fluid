#!/usr/bin/env python3
"""Check that the vendored schemas equal the reference implementation's release.

    python3 scripts/check-schema-drift.py                  # the PINNED release
    python3 scripts/check-schema-drift.py --latest         # advisory: is there a newer one?
    python3 scripts/check-schema-drift.py --ref v0.18.1    # an arbitrary tag (re-vendoring)
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

WHICH release is recorded in scripts/schema-versions.json ("upstream.ref" and
"upstream.commit"), not looked up at run time. The default run is therefore
deterministic: it compares the working tree with that one commit and nothing
upstream can change the result. It fetches by the commit, which cannot move,
and only reports (as a warning) if the tag now points somewhere else. A new
forge-cli release does not turn a pull request red; moving to it is a change
to those two fields, in a pull request, where a reviewer sees which upstream
commit is being trusted. `--latest` is the separate, advisory question "has
forge-cli released since?"; it exits 1 when it has, and CI runs it as a
non-blocking job.

What the default run checks, against scripts/schema-versions.json:

  1. every version listed in "synced" is byte-identical to the release's copy;
  2. the release bundles no version, at or above the oldest synced one, that
     is missing from "synced" -- so a new schema cannot ship unpublished;
  3. the release's preview set (PREVIEW_VERSIONS in schema_manager.py) equals
     "preview", and "latestStable" is the release's highest non-preview
     version -- so a promotion to stable is not missed.

Exit 0 when everything matches; 1 on drift (with --latest: when a newer
release exists); 2 when the release cannot be read or the pin is malformed. The
output says how to re-vendor.

Set GITHUB_TOKEN to avoid the unauthenticated API rate limit; it is sent only
to api.github.com and is never forwarded across a redirect.
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
from typing import Dict, List, Optional, Set, Tuple

REPO = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO / "schema"
VERSIONS_FILE = REPO / "scripts" / "schema-versions.json"
SCHEMA_RE = re.compile(r"^fluid-schema-(\d+\.\d+\.\d+)\.json$")
PREVIEW_RE = re.compile(r"PREVIEW_VERSIONS\b[^=\n]*=\s*frozenset\(\s*\{([^}]*)\}\s*\)")

# A release tag, and nothing else. A ref is interpolated into URLs and into the
# re-vendor hint this script prints (which people paste into a shell), so a
# value read from the network or from a file is checked before it is used.
REF_RE = re.compile(r"v?\d+\.\d+\.\d+([.+-][0-9A-Za-z.]+)?")
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
REPOSITORY_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
REPO_PATH_RE = re.compile(r"[A-Za-z0-9_.][A-Za-z0-9_./-]*")


class SourceError(RuntimeError):
    pass


def vkey(v: str):
    return tuple(int(p) for p in v.split("."))


def validate_ref(ref: object, what: str) -> str:
    """Return `ref` if it is a release tag; otherwise fail closed."""
    if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
        raise SourceError(f"{what} is not a release tag (expected something like v1.2.3): {ref!r}")
    return ref


def validate_commit(commit: object, what: str) -> str:
    if not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit):
        raise SourceError(f"{what} is not a full 40-character lowercase commit SHA: {commit!r}")
    return commit


def validate_repo_fields(repository: object, schema_dir: object, preview_source: object) -> None:
    if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
        raise SourceError(f"upstream.repository is not an owner/name pair: {repository!r}")
    for name, value in (("upstream.schemaDir", schema_dir), ("upstream.previewSource", preview_source)):
        if not isinstance(value, str) or not REPO_PATH_RE.fullmatch(value) or ".." in value.split("/"):
            raise SourceError(f"{name} is not a plain repository path: {value!r}")


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------


def _get(url: str, accept: Optional[str] = None) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "fluid-schema-drift-check"})
    if accept:
        req.add_header("Accept", accept)
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        # Unredirected: urllib copies ordinary request headers onto a redirected
        # request, so a redirect away from api.github.com would carry the token
        # with it. Unredirected headers are sent to the original host only.
        req.add_unredirected_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise SourceError(f"could not fetch {url}: {exc}") from exc


def latest_release_tag(repository: str) -> str:
    data = json.loads(_get(f"https://api.github.com/repos/{repository}/releases/latest"))
    tag = data.get("tag_name")
    if not tag:
        raise SourceError(f"{repository} reports no latest release")
    return validate_ref(tag, f"{repository}'s latest release tag")


class GitHubRelease:
    """A forge-cli release, read from GitHub.

    With `commit`, every file is fetched by that commit rather than by the tag,
    so the content compared is immutable; `ref` is then only the human-readable
    name for it.
    """

    def __init__(
        self,
        repository: str,
        schema_dir: str,
        preview_source: str,
        ref: str,
        commit: Optional[str] = None,
    ):
        validate_repo_fields(repository, schema_dir, preview_source)
        self.repository = repository
        self.schema_dir = schema_dir
        self.preview_source = preview_source
        self.ref = validate_ref(ref, "the release ref")
        self.commit = validate_commit(commit, "the pinned commit") if commit else None
        self.fetch_ref = self.commit or self.ref
        self.label = f"{repository}@{self.ref}" + (f" (commit {self.commit[:12]})" if self.commit else "")

    def tag_warning(self) -> Optional[str]:
        """A warning when the tag no longer points at the pinned commit.

        Not a failure: the content compared is fetched by commit, so a moved
        tag changes nothing this script decides. It does mean the recorded tag
        name no longer describes the recorded commit, which a person should look at.
        """
        if not self.commit:
            return None
        try:
            now = _get(
                f"https://api.github.com/repos/{self.repository}/commits/{self.ref}",
                accept="application/vnd.github.sha",
            ).decode("ascii", "replace").strip()
        except SourceError as exc:
            return f"could not confirm that tag {self.ref} still points at {self.commit}: {exc}"
        if now != self.commit:
            return (
                f"tag {self.ref} now points at {now[:12]}, but {VERSIONS_FILE.name} pins {self.commit[:12]}; "
                "the comparison used the pinned commit, but the tag has been moved or the pin is wrong"
            )
        return None

    def _raw(self, path: str) -> bytes:
        return _get(f"https://raw.githubusercontent.com/{self.repository}/{self.fetch_ref}/{path}")

    def versions(self) -> List[str]:
        listing = json.loads(
            _get(f"https://api.github.com/repos/{self.repository}/contents/{self.schema_dir}?ref={self.fetch_ref}")
        )
        names = [entry["name"] for entry in listing if entry.get("type") == "file"]
        return sorted((m.group(1) for n in names if (m := SCHEMA_RE.match(n))), key=vkey)

    def schema(self, version: str) -> bytes:
        return self._raw(f"{self.schema_dir}/fluid-schema-{version}.json")

    def preview_text(self) -> Optional[str]:
        return self._raw(self.preview_source).decode("utf-8")

    def url(self, version: str) -> str:
        return f"https://raw.githubusercontent.com/{self.repository}/{self.fetch_ref}/{self.schema_dir}/fluid-schema-{version}.json"


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


# --------------------------------------------------------------------------
# modes
# --------------------------------------------------------------------------


def warn(message: str) -> None:
    """A warning on stderr, and an annotation on the run page under GitHub Actions."""
    print(f"check-schema-drift: warning: {message}", file=sys.stderr)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::warning title=forge-cli release::{message}")


def read_upstream(record: Dict) -> Tuple[str, str, str, str, str]:
    """The pinned upstream, validated. Anything missing or malformed fails closed."""
    up = record.get("upstream")
    if not isinstance(up, dict):
        raise SourceError(f"{VERSIONS_FILE.name} has no \"upstream\" object")
    for key in ("repository", "schemaDir", "previewSource", "ref", "commit"):
        if key not in up:
            raise SourceError(
                f"{VERSIONS_FILE.name}: upstream.{key} is missing. The drift check compares against a "
                "pinned release (upstream.ref and upstream.commit); it does not guess one."
            )
    validate_repo_fields(up["repository"], up["schemaDir"], up["previewSource"])
    validate_ref(up["ref"], "upstream.ref")
    validate_commit(up["commit"], "upstream.commit")
    return up["repository"], up["schemaDir"], up["previewSource"], up["ref"], up["commit"]


def newer_than(candidate: str, pinned: str) -> Optional[bool]:
    """True/False when both tags order numerically; None when they do not."""
    def numeric(tag: str):
        m = re.match(r"v?(\d+)\.(\d+)\.(\d+)", tag)
        return tuple(int(p) for p in m.groups()) if m else None

    a, b = numeric(candidate), numeric(pinned)
    return None if a is None or b is None else a > b


def run_latest(record: Dict) -> int:
    """Advisory: has forge-cli published a release after the pinned one?"""
    repository, schema_dir, preview_source, pinned_ref, _ = read_upstream(record)
    latest = latest_release_tag(repository)
    if latest == pinned_ref:
        print(f"check-schema-drift: {repository}'s latest release, {latest}, is the pinned one.")
        return 0

    ordering = newer_than(latest, pinned_ref)
    if ordering is False:
        print(
            f"check-schema-drift: {repository}'s latest release is {latest}, which is older than the "
            f"pinned {pinned_ref}. Nothing to do."
        )
        return 0

    print(f"check-schema-drift: a newer forge-cli release exists: {latest} (this repository vendors {pinned_ref}).")
    print("What moving to it would involve, from a byte comparison with its schemas:")
    problems = check(GitHubRelease(repository, schema_dir, preview_source, latest), record)
    if problems:
        for p in problems:
            print(f"  - {p}")
    else:
        print(f"  nothing: the vendored schemas already equal {latest}'s; only the pin in {VERSIONS_FILE.name} would move.")
    warn(
        f"forge-cli {latest} is released; this repository vendors {pinned_ref}. "
        f"To move: set upstream.ref and upstream.commit in scripts/{VERSIONS_FILE.name}, re-vendor, and "
        "regenerate (see CONTRIBUTING.md). This does not fail pull requests."
    )
    return 1


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    which = ap.add_mutually_exclusive_group()
    which.add_argument(
        "--latest",
        action="store_true",
        help="advisory: report whether forge-cli has released after the pinned release (exit 1 if so)",
    )
    which.add_argument("--ref", help="compare against this forge-cli tag instead of the pinned release")
    which.add_argument("--source-dir", type=Path, help="compare against this directory instead of GitHub")
    ap.add_argument(
        "--schema-manager",
        type=Path,
        help="with --source-dir: the schema_manager.py whose PREVIEW_VERSIONS to compare",
    )
    args = ap.parse_args(argv)
    if args.schema_manager and not args.source_dir:
        ap.error("--schema-manager is only meaningful with --source-dir")

    record = json.loads(VERSIONS_FILE.read_text())
    try:
        if args.latest:
            return run_latest(record)

        warnings: List[str] = []
        if args.source_dir:
            source = LocalDir(args.source_dir, args.schema_manager)
        elif args.ref:
            repository, schema_dir, preview_source, _, _ = read_upstream(record)
            source = GitHubRelease(repository, schema_dir, preview_source, validate_ref(args.ref, "--ref"))
        else:
            repository, schema_dir, preview_source, ref, commit = read_upstream(record)
            source = GitHubRelease(repository, schema_dir, preview_source, ref, commit)
            tag_note = source.tag_warning()
            if tag_note:
                warnings.append(tag_note)
        problems = check(source, record)
        for w in warnings:
            warn(w)
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
