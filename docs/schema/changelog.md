# Changelog

Human-readable diffs between consecutive versions of the FLUID schema. Each entry links to the full auto-generated change list on GitHub. The latest version is **0.7.4**.

## 0.7.3 → 0.7.4 — Runtime agentPolicy Enforcement at the MCP Gateway

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.7.3-to-0.7.4.md)

This release makes an expose *agent-consumable over MCP* and turns `policy.agentPolicy` into a gate the Fluid MCP output-port gateway enforces on every read. The `policy.agentPolicy` **shape is unchanged** from 0.7.3 — the enforcement is behavioral, not a new field. **Fully backward-compatible: this release is purely additive, so every valid 0.7.3 contract validates as 0.7.4 unchanged.**

**Added**

- **`exposes[].mcp`** (new `exposeMcp` block) opts an expose into the MCP gateway. `mcp.sampling.maxRows` (integer ≥ 1, default 100) hard-caps the `sample` tool; `mcp.classification.dataClass` (`public` / `internal` / `confidential` / `restricted`) is an advisory hint surfaced on `describe`.
- **`binding.platform`** gains `postgres`.
- **`binding.format`** gains `postgres_table`, `athena_table`, `glue_table` (added alongside the existing formats, including `snowflake_view` and the `redshift_*` values).
- **`fluidVersion`** moves from `const: "0.7.3"` to `enum: ["0.7.3", "0.7.4"]`, so existing `0.7.3` values still validate.

**Unchanged & still valid.** Nothing was removed — the top-level `governance` block and `binding.governance` (AWS Lake Formation), the `snowflake_view` / `redshift_table` / `redshift_serverless` / `redshift_external_schema` formats, the `athena` / `glue` / `redshift` runtimes, `datamesh_manager` catalog registration, and the `opentofu` deployment target all remain valid in 0.7.4.

**Upgrading.** Set `fluidVersion: "0.7.4"` (or keep `"0.7.3"` — it still validates). There are no removed fields to migrate off.

## 0.7.2 → 0.7.3 — Source-Aligned Acquisition

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.7.2-to-0.7.3.md)

Adds the `acquisition` build pattern, six ingestion engines, `build.capabilities`, delivery guarantees + DLQ, source-side `schemaEvolution`, supply-chain image signatures, and the top-level `retention` block. Additive over 0.7.2.

## 0.7.1 → 0.7.2 — Semantic Truth Engine

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.7.1-to-0.7.2.md)

Adds the per-expose `semantics` block (entities, measures, dimensions, metrics) and `binding.icebergConfig`. Additive over 0.7.1.

## 0.5.7 → 0.7.1 — Agentic Governance & Provider-First Orchestration

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.5.7-to-0.7.1.md)

Adds `exposes[].policy.agentPolicy`, top-level `sovereignty`, top-level `accessPolicy`, and provider-first `orchestration` tasks.

## 0.4.0 → 0.5.7

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.4.0-to-0.5.7.md)

Adds `builds`, `machineLearning`, `environments`, `lifecycle`, `docs`, and `extensions`.

## 0.3.0 → 0.4.0

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.3.0-to-0.4.0.md)

Adds `lineage`, `governance`, and `schemaEvolution`.

## 0.2.0 → 0.3.0

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.2.0-to-0.3.0.md)

Adds the `build` block.

## 0.1.1 → 0.2.0

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.1.1-to-0.2.0.md)

Adds the `consumes` block.

## 0.1.0 → 0.1.1

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.1.0-to-0.1.1.md)

## 0.0.1 → 0.1.0

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.0.1-to-0.1.0.md)
