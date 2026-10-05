# Contributing to FLUID

FLUID is an open specification, licensed under the [Apache License 2.0](https://github.com/open-data-protocol/fluid/blob/main/LICENSE) and held by **The FLUID Authors** — everyone whose work has been merged into the repository. This page summarises how to take part. The authoritative versions are [CONTRIBUTING.md](https://github.com/open-data-protocol/fluid/blob/main/CONTRIBUTING.md) and [GOVERNANCE.md](https://github.com/open-data-protocol/fluid/blob/main/GOVERNANCE.md) in the repository; where they and this page differ, they win.

---

## The schemas are not authored here

The JSON Schemas under `schema/` are **vendored**: they are authored in [forge-cli](https://github.com/Agenticstiger/forge-cli), the reference implementation, and this repository is their public distribution point. Nothing copies them here automatically: the `drift` job in `.github/workflows/conformance.yml` runs on every pull request and fails when a synced schema differs by even one byte from the copy in the forge-cli release **pinned** in [`scripts/schema-versions.json`](https://github.com/open-data-protocol/fluid/blob/main/scripts/schema-versions.json) (`upstream.ref`, and `upstream.commit`, which is what the check fetches), when that release bundles a schema version not published here, or when its preview versions or latest stable version differ from that file. A pull request that edits a file under `schema/` by hand fails the `drift` job — not because the change is wrong, but because the published schema must be the one the reference implementation ships. The job fails that pull request's checks; whether a failing check also blocks the merge is a branch-protection setting, not something this page promises. Propose schema changes upstream in forge-cli.

The comparison is with the pinned release, not with whatever forge-cli released last, so a new forge-cli release does not turn unrelated pull requests red; moving to one is a change to the pin, reviewed in a pull request. A separate, advisory `drift-latest` job warns when forge-cli has released after the pinned release, and cannot fail a run. The `generated` job also fails when a file under `schema/` or `specs/` is neither generated for a synced version nor listed, with its sha256, in the `frozen` map of `scripts/schema-versions.json`, or when a frozen file changes.

`scripts/schema-versions.json` is the record of which versions are synced, which is the latest **stable** version and which are **previews**; `python3 generate-docs.py --print-latest-stable` prints the stable one. To re-vendor after a drift failure or a new forge-cli release (`python3 scripts/check-schema-drift.py --latest` says whether there is one): choose a release tag (never `main`) and find its commit with `git ls-remote`, set `upstream.ref` and `upstream.commit` in `scripts/schema-versions.json` (and `synced`, `preview` and `latestStable` if a version was added or its status changed), copy each changed schema byte for byte from that commit, regenerate `specs/` and `schema-diffs/` with `generate-docs.py` and `generate-schema-diffs.py` (the renderer is installed with `pip install --require-hashes -r scripts/requirements-docs.lock`), run the gates — `python3 scripts/check-schema-drift.py` now compares with the commit you recorded — and name the release and commit in the pull request. The full steps are in [CONTRIBUTING.md](https://github.com/open-data-protocol/fluid/blob/main/CONTRIBUTING.md#re-vendoring-a-schema).

What you can change here:

| Area | What it is |
|---|---|
| `tests/**` | The **conformance corpus** — where "FLUID-conformant" is defined. See [tests/README.md](https://github.com/open-data-protocol/fluid/blob/main/tests/README.md). |
| `conformance/**` | The corpus runner, the reference-implementation check, and the mutation-coverage tool. |
| `scripts/check-compat.py`, `scripts/compat-waivers.txt` | The backward-compatibility gate and its decision record. |
| `docs/**` | This documentation site. |
| `examples/**` | Example contracts. |

---

## The most valuable contribution: conformance cases

The corpus is what makes conformance a fact rather than a claim, and it lets anyone check an implementation without access to the reference one. The rules, in short (full version in [tests/README.md](https://github.com/open-data-protocol/fluid/blob/main/tests/README.md)):

- Assert on **JSON Schema keyword + RFC 6901 pointer**, never on message text.
- An invalid case must declare **why** it is invalid.
- Keep cases **minimal**: an invalid document differs from a valid one in exactly the way under test.
- The bar is **falsifiability**: if deleting the constraint you meant to pin leaves the corpus green, the case is not doing its job (`python3 conformance/mutation_coverage.py --group <yours>`).

Run the gates locally before opening a pull request:

```bash
pip install "jsonschema[format]>=4.22"
python3 conformance/run.py          # the corpus must be green
python3 tests/meta_test.py          # the gates must be able to fail
python3 scripts/check-compat.py     # no release may break its promise
```

Optionally, check the corpus against the reference implementation:

```bash
pip install data-product-forge
python3 conformance/check_reference.py
```

---

## Changing what the schema means

Anything that changes which documents validate is **normative**. Open an issue before writing code, and expect to be asked for the corpus cases that pin the new behaviour. Editorial changes — typos, prose, descriptions that do not affect validation — can go straight to a pull request.

**Compatibility.** Every release promises that valid contracts keep validating, and `scripts/check-compat.py` checks it on every pull request. A deliberate narrowing goes in `scripts/compat-waivers.txt` *with the evidence that settled it*; the waiver file is a decision record, not a mute button.

---

## Pull requests

- One concern per pull request.
- Say what you verified and how — the command you ran and what it printed.
- New behaviour needs a case that would fail without it.
- Be honest about what you did not do.

**Licence and provenance.** Contributions are accepted under the repository's Apache License 2.0. By opening a pull request you certify that you wrote the contribution or otherwise have the right to submit it under that licence — the [Developer Certificate of Origin](https://developercertificate.org/). Sign your commits with `git commit -s` if you want that recorded explicitly. There is **no contributor licence agreement**.

---

## Governance in brief

- FLUID is pre-1.0 and is stewarded by its originating maintainers in the [open-data-protocol](https://github.com/open-data-protocol) organization; decisions are made in the open, in issues and pull requests.
- **Two homes:** the JSON Schemas are authored in forge-cli; the conformance corpus lives here, so that conformance can be checked by someone who has neither the engine nor an account with the maintainers. forge-cli is implementation #1 under test — never the referee.
- Anything the specification does not decide is written down as an open question rather than settled by implementation behaviour (see "Known ambiguities" in [tests/README.md](https://github.com/open-data-protocol/fluid/blob/main/tests/README.md)).

Read [GOVERNANCE.md](https://github.com/open-data-protocol/fluid/blob/main/GOVERNANCE.md) for the full model, including vendor neutrality and trademarks.

---

## Reporting problems

- **Bugs and spec questions** — open an [issue](https://github.com/open-data-protocol/fluid/issues).
- **Security vulnerabilities** — do not open an issue; see [SECURITY.md](https://github.com/open-data-protocol/fluid/blob/main/SECURITY.md).
- **Conduct** — see [CODE_OF_CONDUCT.md](https://github.com/open-data-protocol/fluid/blob/main/CODE_OF_CONDUCT.md).

## Where to go next

- **[Core Principles](/fluid/concepts/principles)** — the principles every contribution should align with.
- **[Schema Versions](/fluid/schema/versions)** — stable and preview versions, and what each status means.
- **[Vision](/fluid/vision/)** — where the standard is heading.
