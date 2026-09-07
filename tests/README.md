# The FLUID conformance corpus

This directory is the operative definition of "FLUID-conformant".

A schema tells you what shape a document has. It does not tell you whether two
implementations agree about it. FLUID already has more than one first-party
reader of the same contract — `FluidSchemaManager` in forge-cli, the FLUX
engine's `seam/`, and the Command Center — and until this corpus existed,
nothing proved they agreed. The corpus is how they are held to one answer, and
how a third party can demonstrate conformance without asking our permission.

**The corpus is data.** Reading it requires only a JSON parser. The runner in
`../conformance/` is a convenience for Python; it is not the definition, and an
implementation in any language is conformant if it reproduces these verdicts.

## Layout

```
tests/
  <version>/            # core tier: every conformant validator must agree
    envelope.json
    expose.json
    ...
  optional/<version>/   # behaviour an implementation may legitimately not have
    metadata.json
  meta_test.py          # proves the gates can fail
```

The core/optional split follows
[JSON-Schema-Test-Suite](https://github.com/json-schema-org/JSON-Schema-Test-Suite).
The core tier asserts only what every conformant JSON Schema 2020-12 validator
must do. The optional tier asserts behaviour the specification permits but does
not require — today, `format` assertion (see "Known ambiguities" below).

## File format

```json
{
  "corpusVersion": "0.7.5",
  "schema": "https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.5.json",
  "group": "envelope",
  "description": "What this group pins down.",
  "cases": [
    {
      "description": "minimal document carrying exactly the required members",
      "contract": { "fluidVersion": "0.7.5", "...": "..." },
      "valid": true
    },
    {
      "description": "metadata present but owner absent",
      "contract": { "...": "..." },
      "valid": false,
      "errors": [{ "pointer": "/metadata", "keyword": "required", "detail": "owner" }]
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `contract` | A complete FLUID document. Not a fragment. |
| `valid` | Whether a conformant implementation accepts it. |
| `errors` | Required when `valid` is false. Why it must be rejected. |
| `pointer` | RFC 6901 pointer to the failing instance location. `""` is the root. |
| `keyword` | The JSON Schema keyword that must fail: `required`, `enum`, `pattern`, `type`, `additionalProperties`, `minItems`, … |
| `detail` | For `required`, the missing property. For `additionalProperties`, the offending one. |

Three rules make the assertions portable and durable:

1. **Never assert on message text.** Wording is a rendering choice and every
   validator words it differently. Keyword and pointer are interoperable facts.
2. **Expectations are partial.** A case names only the fields it means to pin,
   so a case does not break when an unrelated part of the schema moves.
3. **An invalid case must say why.** A case that only asserts "rejected" passes
   for any reason at all, including reasons its author never intended. The
   runner refuses to load one.

Two further rules make cases meaningful rather than merely present:

4. **Minimality.** An invalid case differs from a valid document in exactly the
   one way under test. Two defects in one document prove neither.
5. **Falsifiability.** For every constraint the schema expresses, some case must
   go red if that constraint were deleted. That is the coverage bar — not
   "there are tests" but "weakening this definition is caught".

## Running it

```bash
# the [format] extra matters: without it jsonschema registers no
# date-time checker, and the optional tier passes vacuously
pip install "jsonschema[format]>=4.22"

python3 conformance/run.py                     # every published version
python3 conformance/run.py --version 0.7.5     # one version
python3 conformance/run.py --group agentpolicy # one group
python3 conformance/run.py --junit report.xml  # for CI
python3 conformance/run.py --list              # print test ids
```

Against the reference implementation, which is implementation #1 under test and
never the referee:

```bash
pip install data-product-forge
python3 conformance/check_reference.py
```

And to prove the gates can actually fail:

```bash
python3 tests/meta_test.py
```

## Known failures

`../conformance/known-failures.txt` lists test ids that are expected to fail:
one per line, `#` comments, kept sorted. Known-failing cases are still
**executed**, so a fix flips them green loudly rather than silently — the
[connectrpc/conformance](https://github.com/connectrpc/conformance) refinement
of protobuf's `failure_list`. A listed test that starts passing is an error,
and so is an entry naming a test that no longer exists.

The file is how a strict gate stays adoptable on the day it lands: a real
shortcoming is recorded in the repository instead of being hidden by weakening
the corpus.

## Known ambiguities the corpus has surfaced

Recorded here because a conformance suite's job is to turn disagreements into
written questions rather than silent divergence.

**Is `format` assertive in FLUID?** The specification does not say. In JSON
Schema 2020-12, `format` is an annotation by default — a conformant validator
may accept `"not-an-email"` for `{"format": "email"}`. The reference
implementation does not assert formats. Until FLUID states a position, the core
tier does not assert them either, and the cases that depend on assertion live
in `optional/`. A FLUID document is therefore **not** guaranteed to have a
well-formed `metadata.owner.email` merely because it validates.

**The reference implementation validates a 2020-12 schema with a Draft 7
validator.** `fluid_build/schema_manager.py` constructs a
`jsonschema.Draft7Validator` while every published schema declares
`"$schema": "https://json-schema.org/draft/2020-12/schema"`. Today this is
latent rather than active: the schemas use only `$defs` from the 2020-12-only
keyword set, and `#/$defs/...` references resolve under Draft 7 as ordinary
JSON pointers. It becomes a silent-acceptance bug the moment a schema uses
`prefixItems`, `unevaluatedProperties`, `dependentRequired`, `minContains` or
`maxContains` — Draft 7 ignores unknown keywords, so the implementation would
accept documents the published standard rejects, with no error anywhere.

## Measuring what the corpus is worth

Counting cases measures effort. `conformance/mutation_coverage.py` measures
coverage: it deletes one schema constraint at a time and re-runs the corpus.

```bash
python3 conformance/mutation_coverage.py                      # whole corpus
python3 conformance/mutation_coverage.py --group agentpolicy  # one group
python3 conformance/mutation_coverage.py --min-coverage 40    # gate mode
```

A constraint is **covered** when deleting it turns some case red, **uncovered**
when the corpus does not notice, and **redundant** when no case could ever
notice — because a sibling `enum` already restricts the instance to a set that
satisfies the constraint anyway. `fluidVersion` is the clearest example: it
carries `pattern`, `type: string` and an `enum` of three version strings, so
the pattern and the type are dead weight. Redundant constraints are excluded
from the denominator; counting them would blame the corpus for a gap it cannot
close, and they are findings about the *schema* instead.

Today: **40.7%** (415 of 1020 falsifiable constraints), with 120 redundant.
Most of what remains is `type` constraints, which need a wrong-typed value for
every property in the schema. Of the constraints that carry real meaning —
enums, required members, closed objects, bounds — 38 remain unpinned.

## Adding a version

1. Publish `schema/fluid-schema-<version>.json` (authored in forge-cli, synced
   here by `.github/workflows/schema-sync.yml`).
2. Create `tests/<version>/` and port the previous version's groups.
3. Run `scripts/check-compat.py --from <previous> --to <version>`. If it
   reports a narrowing, either the change is a mistake or it is deliberate and
   belongs in `scripts/compat-waivers.txt` **with the evidence that settled
   it** — the waiver file is a decision record, not a mute button.
