# Changelog

Human-readable summaries of what changed between consecutive versions of the FLUID schema. Each entry links to the full auto-generated change list on GitHub. **0.7.5 is the latest stable version; 0.7.6 is a preview** (see [Versions](/fluid/schema/versions#stable-and-preview-versions)).

"No narrowing change" below means that `python3 scripts/check-compat.py --from <a> --to <b>` reports none: every document valid under the earlier version stays valid under the later one (once it declares the later `fluidVersion`). Each summary lists the property paths present in the later schema and absent in the earlier one, plus new enum values.

## 0.7.5 to 0.7.6 (preview): Declarative Packaging Modes

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.7.5-to-0.7.6.md) · [Release note →](/fluid/releases/0.7.6)

No narrowing change. **Preview:** the 0.7.6 schema can still change before it is promoted.

**Added**

- Top-level `packaging` (`mode`, `pool`, `poolManifest`, `containers`) and its per-binding override `exposes[].binding.packaging`.
- Top-level `consumers[]` (`name` and `type` required; `label`, `owner`, `url`, `maturity`, `description`, `exposeIds`).
- `consumes[].upstreamWorkspace` and `consumes[].upstreamDigest` (`sha256:` + 64 lowercase hex), with `dependentRequired: {upstreamWorkspace: [upstreamDigest]}` — the first JSON Schema keyword in a FLUID schema that Draft 7 does not have.
- `exposes[].semantics.measures[].aggParams` (`percentile`, `useDiscretePercentile`).
- `exposes[].binding.encryption.kms`, with platform rules: no AWS key reference on a `gcp` binding, no Cloud KMS name on an `aws` binding.
- `exposes[].binding.principals`, with identity patterns for `gcp` (IAM members) and `aws` (IAM ARNs).
- `exposes[].binding.governance.lakeFormation.bucketPolicy` (`cross-account` | `none` | `all-grantees`; `cross-account` is the default). Its description says that an emitted `aws_s3_bucket_policy` is authoritative and replaces every other statement on the bucket; see the [0.7.6 notes](/fluid/releases/0.7.6#binding-fields-encryption-principals-lake-formation-bucket-policy).
- `exposes[].lifecycle` now refers to a new `exposeLifecycle` definition: the root `lifecycle` fields plus `expire` (default `false`).
- Typed `exposes[].policy.privacy.masking[].params`: `keepFirst`, `keepLast`, `saltEnv`, `keyEnv`.
- `fluidVersion` accepts `"0.7.6"`.

**Described:** `exposes[].policy.authz.columnRestrictions` gains a description of its semantics (deny beats allow; a restriction never grants access; principals are logical).

## 0.7.4 to 0.7.5: Streaming Kafka to Iceberg Sink & Confluent Tableflow

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.7.4-to-0.7.5.md) · [Release note →](/fluid/releases/0.7.5)

No narrowing change.

**Added**

- On the `kafka-connect` acquisition engine (`build(s).properties.kafka-connect`): `iceberg_sink_enabled`, `sink_topics`, `streamingSink`, `iceberg_catalog_overrides`.
- `binding.platform` values `confluent` and `pgvector`; `binding.format` value `pgvector_table`; `binding.vectorConfig`.
- `binding.location` fields: `environment_id`, `kafka_cluster_id`, `confluent_role_arn` (Confluent Tableflow); `catalog`, `warehouse`, `uri`, `partitionBy` (Iceberg catalogs); `namespace`, `workgroup`, `iam_role_arn`, `external_schema`, `glue_database` (Redshift Serverless and external schemas); `stream` (Kinesis).
- `fluidVersion` accepts `"0.7.5"`.

**Re-published.** The 0.7.5 schema first published here was a snapshot taken while 0.7.5 was still a preview in the reference implementation. It lacked `pgvector`, `pgvector_table`, `vectorConfig` and the Iceberg-catalog, Redshift Serverless and Kinesis location fields, which the stable 0.7.5 has. The published file has been re-vendored from forge-cli v0.18.1, which carries the stable 0.7.5; every document the snapshot accepted is still accepted.

## 0.7.3 to 0.7.4: Runtime agentPolicy Enforcement at the MCP Gateway

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.7.3-to-0.7.4.md) · [Release note →](/fluid/releases/0.7.4)

No narrowing change. The gate flags `fluidVersion`, which became an enum; the waiver in `scripts/compat-waivers.txt` records why that is intended.

**Added**

- `exposes[].mcp` (`sampling.maxRows`, `classification.dataClass`).
- `binding.platform` value `postgres`; `binding.format` values `postgres_table`, `athena_table`, `glue_table`.
- Acquisition `catalog.register` values `glue`, `snowflake_horizon`, `unity`.
- `fluidVersion` becomes `enum: ["0.7.3", "0.7.4"]`.

`policy.agentPolicy` is unchanged in shape; 0.7.4's headline change is how the reference implementation's MCP gateway enforces it.

## 0.7.2 to 0.7.3: Source-Aligned Acquisition

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.7.2-to-0.7.3.md) · [Release note →](/fluid/releases/0.7.3)

No narrowing change. The gate flags the identifier pattern (upper-case letters became allowed); the waiver records the exhaustive check that shows the new pattern only widens.

**Added**

- `build.pattern` value `acquisition`, the acquisition properties (`source`, `sink`, `delivery`, `schemaEvolution`, `preLand`, `quality`, `cost`, `catalog`, `concurrency`, `lineage`, and one key per engine: `duckdb`, `airbyte`, `meltano`, `dlt`, `kafka-connect`, `debezium`), the matching `build.engine` values, and `build.capabilities`.
- Top-level `retention`, `governance` (AWS Lake Formation `admins` and `tagDefinitions`) and `extensions`.
- `exposes[].binding.governance` (per-resource Lake Formation settings).
- `metadata.productType`, `metadata.classification`, `metadata.experimental`.
- `exposes[].contract.schemaPolicy`, `exposes[].observability.alert`.
- `binding.format` values `snowflake_view`, `redshift_table`, `redshift_serverless`, `redshift_external_schema`; `runtime.platform` values `athena`, `glue`, `redshift`.

## 0.7.1 to 0.7.2: Semantic Truth Engine

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.7.1-to-0.7.2.md) · [Release note →](/fluid/releases/0.7.2)

**One narrowing change:** `$defs/notification` gained `additionalProperties: false`, so an extra member on a `notifications[]` entry that 0.7.1 accepted is rejected by 0.7.2. It shipped before the gate existed and is recorded in `scripts/compat-waivers.txt`.

**Added**

- `exposes[].semantics` (entities, measures, dimensions, metrics).
- `exposes[].binding.icebergConfig`, `exposes[].binding.properties`, and `binding.format` value `iceberg`.
- Top-level `orchestration` (an open object; see the note under [Cheatsheet → orchestration](/fluid/schema/cheatsheet#orchestration-fields)).
- `exposes[].description`, `exposes[].crawler`, `exposes[].iceberg`, `exposes[].contract.quality`.
- `metadata.provenance`, `metadata.tags`.
- `hybrid-reference` build properties `models`, `select`, `target`.
- `build.engine` accepts adapter-qualified dbt engines matching `^dbt-[a-z0-9]+([_-][a-z0-9]+)*$` (for example `dbt-databricks`).
- `accessPolicy.grants[].permissions` value `create`.

## 0.5.7 to 0.7.1: Agentic Governance & Provider-First Orchestration

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.5.7-to-0.7.1.md) · [Release note →](/fluid/releases/0.7.1)

No narrowing change. 0.7.1 is the first version the compatibility promise covers; the gate runs from here on.

**Added**

- `exposes[].policy.agentPolicy`, top-level `sovereignty`, top-level `accessPolicy`.
- `build(s).execution.orchestration`, including Airflow DAG settings and `provider_action` tasks under `airflow.tasks[]`.
- Runtime fields (`platform`, `image`, `executor`, `serviceAccount`) and trigger fields (`cron`, `timezone`, `datasets`, `datasetsOperator`, `timetable`); trigger types `dataset`, `schedule_and_dataset`, `timetable`.

---

## Before 0.7.1: history before the compatibility promise

These versions predate the promise, and several transitions removed or narrowed fields. The gate is not run over them in CI; the result of running it by hand is given for each.

### 0.4.0 to 0.5.7 (breaking)

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.4.0-to-0.5.7.md)

`check-compat` reports breaking changes. The contract was restructured around today's shape: `exposes[]` gains `exposeId`, `kind`, `contract` and `binding`; `consumes[]` gains `productId`, `exposeId` and `versionConstraint`; `build` gains `id`, `pattern`, `engine` and `properties`. Added at the top level: `builds`, `tags`, `labels`, `lineage`, `schemaEvolution`, `machineLearning`, `environments`, `lifecycle`, `docs`. **Removed** at the top level: `accessPolicy`, `governance`, `operations`, `security`, `slo` (`accessPolicy` returns in 0.7.1 and a different `governance` in 0.7.3).

### 0.3.0 to 0.4.0

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.3.0-to-0.4.0.md)

Apart from the `$id`, the only change is in `build.transformation`: its `properties` are now chosen by `pattern` through `if`/`then` rules instead of a `oneOf`. `check-compat` reports no narrowing change.

### 0.2.0 to 0.3.0 (breaking)

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.2.0-to-0.3.0.md)

`check-compat` reports breaking changes. `build` is restructured into `build.transformation` (with build patterns) and `build.execution`, replacing `build.engine`, `runtime`, `trigger`, `retries` and `notifications` at the `build` level. `governance` gains `lineage`, `regulatory` and `stewardship` in place of `rules`.

### 0.1.1 to 0.2.0 (breaking)

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.1.1-to-0.2.0.md)

`check-compat` reports breaking changes: patterns are added to ids, `domain`, column names and access principals, bounds to SLA and lifecycle numbers, and a pattern to cron triggers. `exposes[].mappings` is added.

### 0.1.0 to 0.1.1

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.1.0-to-0.1.1.md)

No narrowing change. Note that 0.1.0 and 0.1.1 declare the same `$id` (see [Versions](/fluid/schema/versions#_0-4-0-and-earlier-ids-that-do-not-resolve)).

### 0.0.1 to 0.1.0 (breaking)

[Full diff →](https://github.com/open-data-protocol/fluid/blob/main/schema-diffs/diff-0.0.1-to-0.1.0.md)

`check-compat` reports breaking changes. Top-level `conformance`, `dynamicPolicies` and `extensions` are removed (`extensions` returns in 0.7.3), and `slo` is added. `consumes` and `build` exist from 0.0.1 on.

---

## Corrections to published schemas

- **Lake Formation `admins` (0.7.3, 0.7.4, 0.7.5).** These schemas were first published with a description of `governance.lakeFormation.admins` saying that principals not listed are not removed. That is the opposite of what applying it does: the list is **authoritative**, and an admin not listed — including the identity running the apply — loses Lake Formation admin. The description was corrected in the reference implementation and the published files carry the corrected text. Only the description changed; the same documents validate.
- **0.7.5** was re-published with the stable content (above).
