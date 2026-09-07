# Governance

## Current model: steward-maintainer

FLUID is pre-1.0. The specification is stewarded by its originating maintainers
in the [open-data-protocol](https://github.com/open-data-protocol) organization.
Decisions on spec changes are made by the maintainers, in the open, through
issues and pull requests on this repository.

This is an honest description of a small project, not a claim of formal
multi-vendor governance. There is no steering committee and no vote, because
there is not yet a constituency to hold one.

## Where things are decided

FLUID has two homes, on purpose, and the split matters for anyone proposing a
change:

| Artefact | Authored in | Why |
|---|---|---|
| The JSON Schemas | [`forge-cli`](https://github.com/Agenticstiger/forge-cli) | It is the only place with an exercised test suite over them, and it is the engine that enforces them. |
| The conformance corpus | **here** | Conformance must be checkable by someone who has neither the engine nor an account with us. |

That second row is the load-bearing one. A standard whose only definition is
"whatever the reference implementation accepts" is a vendor format with a
specification-shaped document attached. The corpus in [`tests/`](tests/) is what
makes "FLUID-conformant" mean something independent, and forge-cli is
implementation #1 under test — never the referee.

## Vendor neutrality

FLUID already lives in a vendor-neutral organization. The maintainers are
employed by a company that also ships a commercial control plane built on FLUID,
and that is a real conflict of interest, so the mitigations are structural
rather than promissory:

- The schemas are **MIT** and the corpus is data. Anyone can implement FLUID and
  demonstrate conformance without permission, tooling, or a relationship with us.
- **No CLA.** Contributions are accepted under the repository licence via the
  [DCO](https://developercertificate.org/). There is no mechanism by which
  contributed work could be relicensed out from under contributors.
- Compatibility is **enforced by CI**, not asserted in prose, so a change that
  would strand existing contracts is visible to everyone at review time rather
  than discovered later by users.
- Anything the specification does not decide is written down as an open question
  rather than settled silently by implementation behaviour. See "Known
  ambiguities" in [tests/README.md](tests/README.md).

As FLUID gains external implementers, the intent is to move toward a formal
governance model with representation from parties who do not share an employer.
Concrete triggers: a second independent implementation demonstrating
conformance, or sustained contribution from outside the current maintainers.

## Versioning and compatibility

Pre-1.0, minor versions may add. They may not narrow: a contract valid under one
version must stay valid under its successor. `scripts/check-compat.py` enforces
this on every pull request, and deliberate exceptions are recorded in
[`scripts/compat-waivers.txt`](scripts/compat-waivers.txt) with the evidence that
justified them.

One historical break is on record (0.7.1 → 0.7.2, `notification` became a closed
object). It was found by the gate after the fact, and the release note that
claimed otherwise has been corrected rather than quietly left standing.

## Trademarks

"FLUID" as a name for this specification is reserved by the maintainers. The
format is free to implement, describe, and build products on; the mark exists so
that "FLUID-conformant" keeps meaning what the corpus says it means. If you ship
an implementation, say so plainly — you do not need permission to state that
your tool implements FLUID.

## Contact

Open an issue for anything about the specification. See
[SECURITY.md](SECURITY.md) for vulnerabilities and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for conduct concerns.
