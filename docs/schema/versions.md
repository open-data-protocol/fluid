# Schema Versions

Every published version of the FLUID JSON Schema. Point your validator at a version's JSON Schema; read its generated HTML reference for the field-by-field detail.

- **Latest stable: 0.7.5.** Use it for new contracts.
- **Preview: 0.7.6.** Published so that it can be read and validated against. It can still change before it is promoted. See [Stable and preview versions](#stable-and-preview-versions).

| Version | Status | JSON Schema | HTML Reference |
|---|---|---|---|
| **0.7.6** | **Preview** | [`fluid-schema-0.7.6.json`](/fluid/schema/fluid-schema-0.7.6.json) | [`0.7.6/fluid-spec.html`](/fluid/specs/0.7.6/fluid-spec.html) |
| **0.7.5** | **Stable (latest)** | [`fluid-schema-0.7.5.json`](/fluid/schema/fluid-schema-0.7.5.json) | [`0.7.5/fluid-spec.html`](/fluid/specs/0.7.5/fluid-spec.html) |
| 0.7.4 | Stable | [`fluid-schema-0.7.4.json`](/fluid/schema/fluid-schema-0.7.4.json) | [`0.7.4/fluid-spec.html`](/fluid/specs/0.7.4/fluid-spec.html) |
| 0.7.3 | Stable | [`fluid-schema-0.7.3.json`](/fluid/schema/fluid-schema-0.7.3.json) | [`0.7.3/fluid-spec.html`](/fluid/specs/0.7.3/fluid-spec.html) |
| 0.7.2 | Stable | [`fluid-schema-0.7.2.json`](/fluid/schema/fluid-schema-0.7.2.json) | [`0.7.2/fluid-spec.html`](/fluid/specs/0.7.2/fluid-spec.html) |
| 0.7.1 | Stable — [see note](#_0-7-1-two-documents-share-one-id) | [`fluid-schema-0.7.1.json`](/fluid/schema/fluid-schema-0.7.1.json) | [`0.7.1/fluid-spec.html`](/fluid/specs/0.7.1/fluid-spec.html) |
| 0.5.7 | Historical | [`fluid-schema-0.5.7.json`](/fluid/schema/fluid-schema-0.5.7.json) | [`0.5.7/fluid-spec.html`](/fluid/specs/0.5.7/fluid-spec.html) |
| 0.4.0 | Historical | [`fluid-schema-0.4.0.json`](/fluid/schema/fluid-schema-0.4.0.json) | [`0.4.0/fluid-spec.html`](/fluid/specs/0.4.0/fluid-spec.html) |
| 0.3.0 | Historical | [`fluid-schema-0.3.0.json`](/fluid/schema/fluid-schema-0.3.0.json) | [`0.3.0/fluid-spec.html`](/fluid/specs/0.3.0/fluid-spec.html) |
| 0.2.0 | Historical | [`fluid-schema-0.2.0.json`](/fluid/schema/fluid-schema-0.2.0.json) | [`0.2.0/fluid-spec.html`](/fluid/specs/0.2.0/fluid-spec.html) |
| 0.1.1 | Historical | [`fluid-schema-0.1.1.json`](/fluid/schema/fluid-schema-0.1.1.json) | — |
| 0.1.0 | Historical | [`fluid-schema-0.1.0.json`](/fluid/schema/fluid-schema-0.1.0.json) | — |
| 0.0.1 | Historical | [`fluid-schema-0.0.1.json`](/fluid/schema/fluid-schema-0.0.1.json) | — |

For what changed between any two versions, see the [**Changelog**](/fluid/schema/changelog). For the release notes, see [**What's New**](/fluid/releases/).

---

## Stable and preview versions

| Status | Meaning |
|---|---|
| **Stable** | Published and settled. Each stable version is checked on every pull request by [`scripts/check-compat.py`](https://github.com/open-data-protocol/fluid/blob/main/scripts/check-compat.py): a document valid under one version must stay valid under the next (see [GOVERNANCE.md](https://github.com/open-data-protocol/fluid/blob/main/GOVERNANCE.md#versioning-and-compatibility)). |
| **Preview** | Published so that its `$id` resolves and a document that declares it can be validated by any JSON Schema validator. It is **not settled**: until it is promoted to stable, its fields and their meaning can still change, and the file at its URL is replaced when they do. |
| **Historical** | 0.5.7 and earlier. These predate the compatibility promise, which the gate enforces from 0.7.1 on. Several of those transitions removed or narrowed fields; the [Changelog](/fluid/schema/changelog) marks which. |

### What "preview" means for you

- **A contract opts in explicitly**, by declaring `fluidVersion: "0.7.6"`. Nothing else selects a preview.
- **Expect to re-validate.** The compatibility gate compares two *versions*. It cannot compare one revision of the 0.7.6 file with an earlier revision of the same file, so a contract written against an earlier revision of 0.7.6 may need changes after a later one. The schemas are authored in the reference implementation, [forge-cli](https://github.com/Agenticstiger/forge-cli), where `fluid_build/schemas/fluid-schema-0.7.6.json` has changed several times since 0.7.6 opened; its history is the record of those changes.
- **Promotion** makes a preview the latest stable version and is announced in its release notes. 0.7.5 went through the same path: it was an opt-in preview in forge-cli from 0.9.0 and was promoted to stable in forge-cli 0.12.0, when 0.7.6 opened as the next preview.

### How the reference implementation treats a preview (non-normative)

[`data-product-forge`](/fluid/concepts/forge-cli) bundles 0.7.6 and validates a contract that declares it (`✅ Valid FLUID contract (schema v0.7.6)`), but never chooses it on its own: its newest *stable* bundled version is its default, and `fluid init --quickstart` writes `fluidVersion: 0.7.5`. This describes one implementation. The standard's rule is only the one in [Validation semantics](/fluid/schema/specification#validation-semantics): a document is validated against the schema of the version it declares.

---

## Choosing `fluidVersion`

A document is validated against the schema whose version matches its `fluidVersion` ([Validation semantics](/fluid/schema/specification#validation-semantics)). Three consequences are easy to miss:

1. **To use a field, declare the version that defines it.** The 0.7.5 schema's own `fluidVersion` enum also accepts `"0.7.3"` and `"0.7.4"`. That does not make a document declaring `"0.7.4"` valid when it uses a 0.7.5 field: its matching schema is 0.7.4, which rejects the field. For example, `binding.platform: confluent` (added in 0.7.5) in a contract declaring `"0.7.4"` is invalid, although the 0.7.5 schema alone would accept it. The reference implementation agrees: it reports `'confluent' is not one of [...]` against schema v0.7.4.
2. **Point your editor at the matching schema.** In a `# yaml-language-server: $schema=…` line, use the URL of the version the file declares. Pointing an older file at a newer schema hides exactly the mistake in (1).
3. **Upgrading is changing the number.** Every stable transition from 0.7.2 on keeps every valid document valid, so moving a valid contract to a later stable version is a one-line change. The one recorded exception is 0.7.1 → 0.7.2, where `notification` became a closed object (see the [0.7.2 release note](/fluid/releases/0.7.2#backward-compatibility-with-0-7-1-one-narrowing-change)).

---

## 0.7.1: two documents share one `$id`

The 0.7.1 file published here and the 0.7.1 file the reference implementation bundles carry the same `$id` (`…/schema/fluid-schema-0.7.1.json`) but are different documents, and they disagree in both directions:

- The reference implementation's copy accepts fields the published file rejects — for example top-level `orchestration`, `binding.icebergConfig` and `exposes[].contract.quality`.
- It also rejects documents the published file accepts — for example an extra member on a `notifications[]` entry, or a column `type` outside its list of type names.

This repository does not re-synchronise 0.7.1 (see [CONTRIBUTING.md](https://github.com/open-data-protocol/fluid/blob/main/CONTRIBUTING.md#the-schemas-are-not-authored-here)), so the file above is the 0.7.1 that this site documents. If a 0.7.1 result has to be reproducible across tools, validate against this file, or move the contract to 0.7.2 or later, where the published files and the reference implementation's copies agree on which documents are valid.

## 0.4.0 and earlier: `$id`s that do not resolve

The schemas from 0.0.1 to 0.4.0 declare `$id`s on `open-data-protocol.org`, a host that does not resolve, and their `$id`s do not follow the FLUID version (0.1.0 and 0.1.1 both declare `…/fluid.schema.v2.0.json`, 0.2.0 declares `…/fluid.schema.v2.3.json`). Two different documents sharing an `$id` cannot both be registered in a validator that keys schemas by `$id`. Load these files by their URL on this site instead. They are kept unchanged as history; from 0.5.7 on, every `$id` is the file's own URL here.
