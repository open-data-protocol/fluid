# Contributing to FLUID

Thanks for helping build FLUID. Read the first section before opening a pull
request — it is the rule that most often surprises people.

## The schemas are not authored here

`schema/fluid-schema-*.json` is **vendored**. The FLUID JSON Schemas are
authored in [`forge-cli`](https://github.com/Agenticstiger/forge-cli), the
reference implementation, and land here through
[`.github/workflows/schema-sync.yml`](.github/workflows/schema-sync.yml), which
fails the build if the two ever drift. This repository is the public
distribution point.

**So a pull request that edits a file under `schema/` will be rejected**, not
because the change is wrong but because it will be silently reverted by the next
sync. Propose schema changes upstream in forge-cli. The sync currently covers
0.7.2 and later; earlier versions diverge historically and are excluded on
purpose.

What you *can* change here:

| Area | Notes |
|---|---|
| `tests/**` | The conformance corpus. This is where "FLUID-conformant" is defined — see [tests/README.md](tests/README.md). |
| `conformance/**` | The runner, the reference check, the coverage tool. |
| `scripts/check-compat.py`, `scripts/compat-waivers.txt` | The backward-compatibility gate. |
| `docs/**` | The documentation site. |
| `examples/**` | Example contracts. |

## Setup

```bash
pip install "jsonschema[format]>=4.22"

python3 conformance/run.py          # the corpus must be green
python3 tests/meta_test.py          # the gates must be able to fail
python3 scripts/check-compat.py     # no release may break its promise
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

Contributions are accepted under this repository's [MIT licence](LICENSE). By
opening a pull request you certify that you wrote the contribution or otherwise
have the right to submit it under that licence — the
[Developer Certificate of Origin](https://developercertificate.org/). Sign your
commits with `git commit -s` if you would like that certification recorded
explicitly.

There is no contributor licence agreement. A CLA on a specification would signal
reserved relicensing rights, which is not the intent — see
[GOVERNANCE.md](GOVERNANCE.md).
