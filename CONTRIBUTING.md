# Contributing to FLUID

Thanks for helping build FLUID. Read the first section before opening a pull
request — it is the rule that most often surprises people.

## The schemas are not authored here

`schema/fluid-schema-*.json` is **vendored**. The FLUID JSON Schemas are
authored in [`forge-cli`](https://github.com/Agenticstiger/forge-cli), the
reference implementation, and copied here byte for byte. This repository is
the public distribution point: the schemas from 0.5.7 on declare an `$id`
under this site, and the site serves the copy in `schema/`.

Nothing copies them here automatically. They are **checked by** the `drift`
job in [`.github/workflows/conformance.yml`](.github/workflows/conformance.yml),
which runs on every pull request and fails when:

- a synced schema differs, by even one byte, from the copy in forge-cli's
  latest release;
- that release bundles a schema version that is not published here;
- that release's preview versions, or its latest stable version, differ from
  [`scripts/schema-versions.json`](scripts/schema-versions.json).

**So a pull request that edits a file under `schema/` by hand will be
rejected**, not because the change is wrong but because the published schema
must be the one the reference implementation ships. Propose schema changes
upstream in forge-cli.

[`scripts/schema-versions.json`](scripts/schema-versions.json) is the record of
which versions are synced, which one is the latest **stable** version, and
which are **previews**: a contract uses a preview only by naming it in
`fluidVersion`, and a preview can still change before it becomes stable.
`python3 generate-docs.py --print-latest-stable` prints the stable version.
Versions before 0.7.2 are not synced. The 0.7.1 published here differs from
the document forge-cli bundles under the same `$id`, and re-vendoring it would
change which documents it accepts — a decision for the maintainers, not a
sync.

### Re-vendoring a schema

When the drift check fails, or forge-cli releases a new schema version:

1. Copy each changed schema from the release, byte for byte. Use a release
   tag, never `main`:

   ```bash
   TAG=v0.18.1   # the forge-cli release you are vendoring from
   for v in 0.7.5 0.7.6; do
     curl -fsSL "https://raw.githubusercontent.com/Agenticstiger/forge-cli/$TAG/fluid_build/schemas/fluid-schema-$v.json" \
       -o "schema/fluid-schema-$v.json"
   done
   ```

2. For a new version, or a version whose status changed (a preview promoted
   to stable), update `scripts/schema-versions.json`, and for a new version
   follow "Adding a version" in [tests/README.md](tests/README.md).
3. Regenerate what is derived from the schemas, with the pinned renderer:

   ```bash
   pip install -r scripts/requirements-docs.txt
   python3 generate-docs.py            # specs/<version>/ for every synced version
   python3 generate-schema-diffs.py    # schema-diffs/
   ```

4. Run the gates below, plus `python3 scripts/check-schema-drift.py --ref $TAG`.
   A re-vendored schema can add constraints the corpus does not pin yet, which
   lowers mutation coverage; add the cases in the same pull request.
5. Name the release you vendored from in the pull request.

## Setup

```bash
pip install "jsonschema[format]>=4.22"

python3 conformance/run.py                          # the corpus must be green
python3 conformance/mutation_coverage.py --min-coverage 40   # and still worth something
python3 tests/meta_test.py                          # the gates must be able to fail
python3 scripts/check-compat.py                     # no release may break its promise
python3 scripts/check-schema-drift.py               # schema/ equals the latest forge-cli release
```

The `[format]` extra is not optional. Without it `jsonschema` registers no
`date-time` checker, and the `tests/optional/` cases pass vacuously in one
environment and fail in another.

Optionally, to check the corpus against the reference implementation:

```bash
pip install data-product-forge
python3 conformance/check_reference.py
```

## Adding conformance cases

The corpus is the most valuable thing you can contribute, because it is what
makes conformance a fact rather than a claim. [tests/README.md](tests/README.md)
has the file format and the rules in full; the short version:

- Assert on **JSON Schema keyword + RFC 6901 pointer**, never message text.
  Wording is a rendering choice; keywords and pointers are interoperable facts.
- An invalid case must declare **why** it is invalid. The loader refuses one
  that does not — a case asserting only "rejected" passes for any reason at all.
- Keep cases **minimal**: an invalid document differs from a valid one in
  exactly the one way under test.
- The bar is **falsifiability**, not case count. Run
  `python3 conformance/mutation_coverage.py --group <yours>`; if deleting the
  constraint you meant to pin leaves the corpus green, your case is not doing
  the work you think it is.

## Changing the schema's meaning

Anything that changes which documents validate is normative. Open an issue
before writing code, and expect to be asked for the corpus cases that pin the
new behaviour. Editorial changes — typos, prose, descriptions that do not affect
validation — can go straight to a pull request.

## The compatibility promise

Every FLUID release has claimed that valid contracts keep validating. That
promise is now enforced by `scripts/check-compat.py` on every pull request.

If it reports a narrowing change, one of two things is true: the change is a
mistake, or it is deliberate. A deliberate one goes in
[`scripts/compat-waivers.txt`](scripts/compat-waivers.txt) **with the evidence
that settled it**. The waiver file is a decision record, not a mute button —
read the existing entries for the standard being applied.

## Pull requests

- One concern per pull request.
- Say what you verified and how. "Tests pass" is less useful than the command
  you ran and what it printed.
- New behaviour needs a case that would fail without it.
- Be honest about what you did not do. A known gap that is written down is worth
  more than a claim nobody checked.

## Reporting problems

- **Bugs and spec questions** — open an issue.
- **Security vulnerabilities** — do not open an issue. See
  [SECURITY.md](SECURITY.md).
- **Conduct** — see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Licence and provenance

Contributions are accepted under this repository's
[Apache License 2.0](LICENSE), as its section 5 provides. By opening a pull
request you certify that you wrote the contribution or otherwise have the right
to submit it under that licence — the
[Developer Certificate of Origin](https://developercertificate.org/). Sign your
commits with `git commit -s` if you would like that certification recorded
explicitly.

There is no contributor licence agreement. A CLA on a specification would signal
reserved relicensing rights, which is not the intent — see
[GOVERNANCE.md](GOVERNANCE.md).

### Who "The FLUID Authors" are

The [LICENSE](LICENSE) is held by **The FLUID Authors** — everyone whose work
has been merged into this repository, as recorded in its commit history. There
is no list to be added to and no paperwork to file: contribute, and you are one
of them.

This is the ordinary form for a specification with no CLA (compare "The Go
Authors", "The Kubernetes Authors"), and it is the only form consistent with
what [GOVERNANCE.md](GOVERNANCE.md) already promises. Naming a single company
there would assert ownership over work contributed by people who never signed
anything away, and the no-CLA position exists precisely so that cannot happen.

The line previously read `fluid-steward`, the maintainers' shared account. That
was accurate about who pushed the first commit and increasingly inaccurate about
who owns the result.
