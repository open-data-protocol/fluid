# What's New

Release notes for the FLUID specification, newest first. Each entry links to its full page and to the auto-generated schema diff.

**0.7.5 is the latest stable version. 0.7.6 is a preview**: a contract uses it only by declaring `fluidVersion: "0.7.6"`, and it can still change before it is promoted. See [Stable and preview versions](/fluid/schema/versions#stable-and-preview-versions).

| Version | Status | Codename | Compatibility | Summary |
|---|---|---|---|---|
| **[0.7.6](/fluid/releases/0.7.6)** | **Preview** | Declarative Packaging Modes | ✅ Additive over 0.7.5 | Adds top-level `packaging` and `consumers`, cross-mesh pins on `consumes[]` (`upstreamWorkspace` + `upstreamDigest`), `aggParams` on semantic measures, and on bindings `encryption.kms`, `principals` and Lake Formation `bucketPolicy`; an expose's `lifecycle` gains `expire`, and masking rules gain typed `params`. |
| **[0.7.5](/fluid/releases/0.7.5)** | **Stable (latest)** | Streaming Kafka → Iceberg Sink & Confluent Tableflow | ✅ Additive over 0.7.4 | Adds an opt-in Iceberg streaming sink on the `kafka-connect` acquisition engine, the `confluent` (Tableflow) and `pgvector` binding platforms, the `pgvector_table` format and `binding.vectorConfig`, and location fields for Tableflow, Iceberg catalogs, Redshift Serverless and Kinesis. |
| **[0.7.4](/fluid/releases/0.7.4)** | Stable | Runtime agentPolicy Enforcement at the MCP Gateway | ✅ Additive over 0.7.3 | Adds the optional `exposes[].mcp` block, the `postgres` binding platform, and the `postgres_table` / `athena_table` / `glue_table` formats. |
| **[0.7.3](/fluid/releases/0.7.3)** | Stable | Source-Aligned Acquisition | ✅ Additive over 0.7.2 | The `acquisition` build pattern and six ingestion engines, top-level `retention`, `governance` (AWS Lake Formation) and `extensions`, `binding.governance`, `metadata.productType`, and `exposes[].contract.schemaPolicy`. |
| **[0.7.2](/fluid/releases/0.7.2)** | Stable | Semantic Truth Engine | ⚠️ One narrowing: `notification` became a closed object | A per-expose `semantics` block, `binding.icebergConfig`, the top-level `orchestration` key, and adapter-qualified dbt engines (`build.engine: dbt-<adapter>`). |
| **[0.7.1](/fluid/releases/0.7.1)** | Stable | Agentic Governance + Provider-First Orchestration | ✅ Additive over 0.5.7 | `exposes[].policy.agentPolicy`, top-level `sovereignty` and `accessPolicy`, and provider-action tasks under `builds[].execution.orchestration`. |

---

## Reading the compatibility column

"Additive" means what [`scripts/check-compat.py`](https://github.com/open-data-protocol/fluid/blob/main/scripts/check-compat.py) checks on every pull request: no document that validates under one version stops validating under the next. Every transition in the table is additive except **0.7.1 → 0.7.2**, where `$defs/notification` gained `additionalProperties: false`. That break is recorded in [`scripts/compat-waivers.txt`](https://github.com/open-data-protocol/fluid/blob/main/scripts/compat-waivers.txt) and explained in the [0.7.2 note](/fluid/releases/0.7.2#backward-compatibility-with-0-7-1-one-narrowing-change).

Additive does **not** mean that an older `fluidVersion` may use newer fields. A document is validated against the schema of the version it declares, so to use a field you declare the version that added it. See [Choosing `fluidVersion`](/fluid/schema/versions#choosing-fluidversion).

For the field-by-field history, see the [**Schema Changelog**](/fluid/schema/changelog).
