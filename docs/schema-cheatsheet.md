# 📋 FLUID Schema Cheatsheet (v0.7.3)

One row per top-level field. Use this as a lookup table when you're reading or writing a `.fluid.yml` — find the field on the left, get a one-line meaning, find out if it's required, and jump to the deep-dive.

> 🧭 For a guided tour with context per block, read the [**Schema Anatomy**](anatomy.md).
> 📚 For the exhaustive field-by-field reference, see [`specs/0.7.3/fluid-spec.html`](../specs/0.7.3/fluid-spec.html).

---

## Top-level fields

| Field | Purpose | Required | Added in | Type |
|---|---|:-:|:-:|---|
| `fluidVersion` | Which contract version this file targets. Must equal `"0.7.3"`. | ✅ | 0.1.0 | `string` |
| `kind` | Product kind: `DataProduct` \| `MLPipeline`. | ✅ | 0.1.0 | `enum` |
| `id` | Globally unique, dot-separated product id. The public address of this product. | ✅ | 0.1.0 | `string` |
| `name` | Human-readable display name. | ✅ | 0.1.0 | `string` |
| `description` | Business-facing summary. | | 0.1.0 | `string` |
| `domain` | Owning business domain (e.g. `Finance`, `Customer Experience`). | | 0.1.0 | `string` |
| `tags` | Free-text categorization labels. | | 0.1.0 | `string[]` |
| `labels` | Key/value categorization for catalog and IAM. | | 0.1.0 | `map<string,string>` |
| `metadata` | Owner, layer, business context. | ✅ | 0.1.0 | `object` |
| `consumes` | Upstream FLUID products this product depends on (with version constraints). | | 0.2.0 | `object[]` |
| `exposes` | Ports this product publishes (table / api / stream / feature_store / …). | ✅ | 0.1.0 | `object[]` |
| `build` | How the product is produced (pattern + engine + properties). | | 0.3.0 | `object` |
| `builds` | Multi-build orchestration (when one product has several builds). | | 0.5.7 | `object[]` |
| `orchestration` | Schedule + tasks for the build. Provider-first since 0.7.0. | | 0.7.0 | `object` |
| `sovereignty` ⭐ | Data residency & jurisdictional compliance. | | **0.7.1** | `object` |
| `accessPolicy` ⭐ | Root-level IAM grants — generates cloud IAM bindings. | | **0.7.1** | `object` |
| `retention` ⭐ | TTLs for runState / runLogs / lineage / dlq (ISO-8601). | | **0.7.3** | `object` |
| `lineage` | Upstream/downstream graph + optional field-level mappings. | | 0.4.0 | `object` |
| `governance` | Broader policy assertions (retention class, classification). | | 0.4.0 | `object` |
| `schemaEvolution` | Compatibility strategy (`backward` / `forward` / `full`). | | 0.4.0 | `object` |
| `machineLearning` | Model spec for ML-product kinds (features, training, inference). | | 0.5.7 | `object` |
| `environments` | Per-environment overrides (`dev` / `staging` / `prod`). | | 0.5.7 | `object` |
| `lifecycle` | `state: preview \| active \| deprecated \| retired` + deprecation date. | | 0.5.7 | `object` |
| `docs` | External documentation URLs (runbook, design doc, dashboard). | | 0.5.7 | `object` |
| `extensions` | Escape hatch for vendor-specific additions. | | 0.5.7 | `object` |

---

## `metadata` (required) — fields

`metadata` itself is required at the top level, but only `metadata.owner` is required inside it.

| Field | Purpose | Required |
|---|---|:-:|
| `metadata.owner` | Owning team object. | ✅ |
| `metadata.owner.team` | Owning team handle. | ✅ |
| `metadata.owner.email` | Owner email for alerts and audit. | |
| `metadata.owner.slack` | Owner Slack channel. | |
| `metadata.layer` | Medallion layer label. **Free-form string** — `Bronze`/`Silver`/`Gold` is convention, not enum. | |
| `metadata.businessContext.domain` | Business domain. | |
| `metadata.businessContext.subdomain` | Business subdomain. | |
| `metadata.provenance` | Auto-injected generation envelope (tool + version + timestamp). Machine-written. | |

---

## `exposes[]` — fields

Each entry in `exposes[]` requires `exposeId`, `kind`, `contract`, and `binding`.

| Field | Purpose | Required |
|---|---|:-:|
| `exposes[].exposeId` | Stable id of this port within the product. | ✅ |
| `exposes[].kind` | `table` \| `view` \| `api` \| `file` \| `stream` \| `topic` \| `feature_store` \| `model` \| `vector` \| `graph` \| `time_series` \| `other`. | ✅ |
| `exposes[].contract` | Schema + dq + policy. Must define at least `schema` or `openapiRef`. | ✅ |
| `exposes[].binding` | Where it lives — `platform`, `format`, `location`. | ✅ |
| `exposes[].description` | What this port is. *(NEW in 0.7.2)* | |
| `exposes[].version` | Semver of this port. | |
| `exposes[].contract.schema[]` | Column list with type, required, sensitivity, tags. | (one of) |
| `exposes[].contract.openapiRef` | Reference to an external OpenAPI spec (for `kind: api`). | (one of) |
| `exposes[].contract.dq.rules[]` | Declarative quality assertions. | |
| `exposes[].contract.policy` | Privacy + RBAC + column-level access. | |
| `exposes[].semantics` ⭐ 0.7.2 | Entities, measures, dimensions, metrics. | |
| `exposes[].binding.platform` | `gcp` \| `aws` \| `azure` \| `snowflake` \| `databricks` \| `kafka` \| `local` \| `kubernetes` \| `other`. | |
| `exposes[].binding.format` | `bigquery_table` \| `snowflake_table` \| `snowflake_view` \| `iceberg` \| `delta_table` \| `parquet` \| `csv` \| `json` \| `http_api` \| `grpc_api` \| `kafka_topic` \| `pubsub_topic` \| `gcs_file` \| `s3_file` \| `redshift_table` \| `redshift_serverless` \| `redshift_external_schema` \| `other`. | |
| `exposes[].binding.icebergConfig` ⭐ 0.7.2 | Iceberg specifics when `format: iceberg`. | |
| `exposes[].qos` | Availability, freshness, latency targets. | |
| `exposes[].tags`, `exposes[].labels` | Port-level categorization. | |

### `contract.dq.rules[]` — fields

| Field | Purpose | Required |
|---|---|:-:|
| `dq.rules[].id` | Rule id (unique within the contract). | ✅ |
| `dq.rules[].type` | `freshness` \| `completeness` \| `uniqueness` \| `valid_values` \| `accuracy` \| `schema` \| `anomaly_detection` \| `drift_detection`. | ✅ |
| `dq.rules[].severity` | `info` \| `warn` \| `error` \| `critical`. | ✅ |
| `dq.rules[].selector` | SQL-like predicate (e.g. `"amount > 0"`). | |
| `dq.rules[].threshold` | Numeric threshold for the operator. | |
| `dq.rules[].operator` | `>=` \| `>` \| `<=` \| `<` \| `==` \| `!=`. | |
| `dq.rules[].window` | ISO-8601 duration window (e.g. `PT15M`). | |
| `dq.rules[].description` | Human-readable purpose. | |

---

## `build` — fields

| Field | Purpose | Required |
|---|---|:-:|
| `build.pattern` | `hybrid-reference` \| `embedded-logic` \| `multi-stage` \| `acquisition` ⭐ 0.7.3. | |
| `build.engine` | `dbt` \| `sql` \| `python` \| `spark` \| `glue` \| `custom` \| `duckdb` ⭐ \| `airbyte` ⭐ \| `meltano` ⭐ \| `dlt` ⭐ \| `kafka-connect` ⭐ \| `debezium` ⭐ (⭐ added 0.7.3). | |
| `build.capabilities` ⭐ 0.7.3 | What the build asks for: `full_refresh`, `incremental_dedup`, `cdc`, `schema_discovery`, `dlp_scan`, `exactly_once`, … | |
| `build.properties` | Pattern-specific properties (validated conditionally). | |
| `build.execution.trigger` | `schedule` / `event` / `manual`. | |
| `build.execution.runtime` | Where it runs (platform + resources). | |
| `build.execution.retries` | Retry policy. | |
| `build.outputs` | List of `exposeId`s this build produces. | |
| `build.dependencies` | Other builds this one waits on. | |
| `build.properties` | Pattern-specific payload — schema validates this against `acquisitionPattern` when `pattern: acquisition` (see below). | (when `pattern: acquisition`) |

---

## `build.properties` when `pattern: acquisition` ⭐ 0.7.3 — fields

When `build.pattern: acquisition`, the schema validates `build.properties` against the `acquisitionPattern` shape below. (For other patterns, `properties` conforms to `hybridReferencePattern` / `embeddedLogicPattern` / `multiStagePattern` respectively.)

| Field (under `build.properties`) | Purpose | Required |
|---|---|:-:|
| `source.kind` | `filesystem` \| `postgres` \| `mysql` \| `sqlite` \| `http` \| `salesforce` \| `stripe` \| … (free string with example values, no enum). | ✅ |
| `source.mode` | `full_refresh` \| `incremental_append` \| `incremental_dedup` \| `incremental_merge` \| `cdc` \| `streaming`. | ✅ |
| `source.cursor_field` | Column used as incremental cursor. | |
| `source.connection` | Connection details. `secretRef` must be a URI: `vault://...`, `aws://...`, `gcp://...`, `azure://...`, or `env://...`. Inline secrets are rejected by the validator. | |
| `source.streams` | List of streams/tables/objects to ingest. | |
| `sink.format` | `iceberg` \| `delta` \| `parquet` \| `csv` \| `json` \| `snowflake_table` \| `bigquery_table` \| `redshift_table` \| `duckdb_table`. | |
| `sink.partitionBy` | Array of **strings** (function-form, e.g. `["day(ingested_at)"]`). Note: `binding.icebergConfig.partitionSpec` uses an object form — different shape. | |
| `sink.catalog` | Catalog identifier (e.g. `glue`, `snowflake_horizon`). | |
| `delivery.guarantee` | `at_most_once` \| `at_least_once` \| `exactly_once`. | |
| `delivery.idempotencyKey` | Template, e.g. `"${stream}\|${batch_id}"`. | |
| `delivery.dlq.enabled` | Boolean — DLQ on/off (default `true`). | |
| `delivery.dlq.sink.format` | `parquet` \| `json` \| `ndjson`. | |
| `delivery.dlq.sink.location` | DLQ destination URI. | |
| `delivery.dlq.maxRecordsBeforeAbort` | Integer (default 10000). | |
| `delivery.dlq.alertOn` | List: `pii_classification_failed` \| `schema_violation` \| `destination_write_failed` \| `quality_gate_failed`. | |
| `schemaEvolution.policy` | `strict` \| `discover_and_freeze` \| `evolve_safe` \| `evolve_all`. | |
| `schemaEvolution.onAddedColumn` | `include` \| `warn` \| `fail`. | |
| `schemaEvolution.onRemovedColumn` | `drop` \| `warn` \| `fail`. | |
| `schemaEvolution.onTypeChange` | `cast` \| `warn` \| `fail`. | |
| `schemaEvolution.sourceFingerprint` | `required` \| `optional` \| `disabled` (default: `required`). | |
| `preLand` | Hook chain: `dlp_scan`, `tokenize_pii`, `quality_gate`, `emit_lineage_input`. | |
| `quality` | Pre-land quality gates (gate-or-quarantine semantics). | |
| `cost.budget.monthly` | `{ rows, bytes (e.g. "50GB"), computeMinutes }`. | |
| `cost.budget.onExceed` | `warn` (default) \| `abort`. | |
| `cost.chargeback` | `{ team, project, costCenter }`. | |
| `catalog.register` | Catalog auto-registration targets: `datahub`, `openmetadata`, `datamesh_manager`. | |
| `concurrency.lock` | Single-flight lock scope (`product` or `build`). | |
| `lineage.emit` | Whether to emit OpenLineage events (default: `true`). | |
| `<engine>` (`airbyte` \| `meltano` \| `dlt` \| `duckdb` \| `kafka-connect` \| `debezium`) | Engine-specific config block. | |
| `<engine>.deployment.mode` | `embedded` \| `bring-your-own` \| `managed`. | |
| `<engine>.image_signature.verifier` | `cosign` (only value today, default `cosign`). | (prod) |
| `<engine>.image_signature.publicKey` | Public key reference for signature verification. | (prod) |
| `<engine>.image_signature.slsaProvenance` | `required` \| `optional` (default) \| `disabled`. | (prod) |

---

## `exposes[].policy.agentPolicy` ⭐ 0.7.1 — fields

> ⚠️ **Location.** `agentPolicy` is **per-expose**, nested under `exposes[].policy.agentPolicy`. It is not a top-level property in the schema (despite the 0.7.1 release notes showing it that way).

| Field | Purpose | Required |
|---|---|:-:|
| `…policy.agentPolicy.allowedModels` | Whitelist of AI model ids (e.g. `gpt-4`, `claude-3-opus`). Empty array = no AI access. | |
| `…policy.agentPolicy.deniedModels` | Blacklist (takes precedence over `allowedModels`). | |
| `…policy.agentPolicy.maxTokensPerRequest` | Per-request token cap (positive integer). | |
| `…policy.agentPolicy.maxTokensPerDay` | Per-day token cap. | |
| `…policy.agentPolicy.allowedUseCases` | Permitted use cases from the schema's controlled vocabulary: `inference` \| `reasoning` \| `analysis` \| `summarization` \| `classification` \| `embedding` \| `search` \| `qa` \| `code_generation` \| `fine_tuning` \| `training` \| `rag`. **Custom strings are rejected.** | |
| `…policy.agentPolicy.deniedUseCases` | Same controlled vocabulary as `allowedUseCases`. Useful pattern: allow `inference, qa, rag`; deny `training, fine_tuning`. | |
| `…policy.agentPolicy.canReason` | Boolean — allow chain-of-thought / multi-step reasoning? (default `false`) | |
| `…policy.agentPolicy.canStore` | Boolean — allow caching / persistence? (default `false`) | |
| `…policy.agentPolicy.retentionPolicy.maxRetentionDays` | Max days AI may retain data (`0` = no retention). | |
| `…policy.agentPolicy.retentionPolicy.requireDeletion` | Boolean — must AI delete after use? (default `true`) | |
| `…policy.agentPolicy.auditRequired` | Boolean — log all AI consumption? (default `true`) | |
| `…policy.agentPolicy.purposeLimitation` | Free-text purpose statement, e.g. `"Customer support chatbot only"`. | |

## `exposes[].policy` — sibling fields

| Field | Purpose | Required |
|---|---|:-:|
| `exposes[].policy.authn` | `oidc` \| `oauth2` \| `api_key` \| `none` \| `custom` \| `iam` \| `jwt`. | |
| `exposes[].policy.authz.readers` | List of principals with read access. | |
| `exposes[].policy.authz.writers` | List of principals with write access. | |
| `exposes[].policy.authz.columnRestrictions[]` | Per-principal column allow/deny rules. | |
| `exposes[].policy.privacy.masking[]` | Column-level masking rules: `{column, strategy: mask\|hash\|tokenize\|encrypt\|k_anonymity}`. | |
| `exposes[].policy.privacy.rowLevelPolicy.expression` | Provider-specific row-level filter predicate. | |
| `exposes[].policy.classification` | Data classification label. | |

---

## `sovereignty` ⭐ 0.7.1 — fields

| Field | Purpose | Required |
|---|---|:-:|
| `sovereignty.jurisdiction` | Required legal jurisdiction (e.g. `EU`, `US`, `APAC`). | |
| `sovereignty.allowedRegions` | Explicit allowed cloud regions. | |
| `sovereignty.deniedRegions` | Explicit denied cloud regions. | |
| `sovereignty.dataResidency` | Boolean — must data stay within jurisdiction? | |
| `sovereignty.crossBorderTransfer` | Boolean — is cross-border transfer permitted? | |
| `sovereignty.transferMechanisms` | If permitted, legal mechanisms (`SCC`, `BCR`, …). | |
| `sovereignty.regulatoryFramework` | Frameworks: `GDPR`, `HIPAA`, `SOC2`, `PCI-DSS`. | |
| `sovereignty.enforcementMode` | `strict` (block apply) \| `advisory` (warn only) \| `audit`. | |
| `sovereignty.validationRequired` | Whether `binding` regions are validated against this block at apply-time. | |

---

## `accessPolicy` ⭐ 0.7.1 — fields

Each grant requires only `principal`; everything else is opt-in.

| Field | Purpose | Required |
|---|---|:-:|
| `accessPolicy.grants[].principal` | `user:`, `group:`, `serviceAccount:` identifier. | ✅ |
| `accessPolicy.grants[].permissions` | List of permissions: `read` \| `select` \| `query` \| `write` \| `insert` \| `update` \| `delete` \| `create` \| `admin` \| `manage`. | |
| `accessPolicy.grants[].resources` | JSONPath expressions selecting which exposes are in scope. | |
| `accessPolicy.grants[].conditions` | Conditional access (IP ranges, time windows). | |

---

## `retention` ⭐ 0.7.3 — fields

| Field | Purpose | Default |
|---|---|:-:|
| `retention.runState` | How long the orchestrator keeps run state. | `P30D` |
| `retention.runLogs` | How long run logs are kept. | `P90D` |
| `retention.lineage` | How long emitted lineage events are kept. | `P365D` |
| `retention.dlq` | How long DLQ records are kept before purge. | `P180D` |

All values are [ISO-8601 durations](https://en.wikipedia.org/wiki/ISO_8601#Durations).

---

## `orchestration` — fields

| Field | Purpose | Required |
|---|---|:-:|
| `orchestration.engine` | `airflow` \| `dagster` \| `prefect` \| `kubeflow` \| `custom` \| `none`. | ✅ |
| `orchestration.mode` | Pull or push generation. | |
| `orchestration.generateOnChange` | Auto-regenerate DAGs when contract changes. | |
| `orchestration.tasks[].taskId` | Task id within the DAG. | |
| `orchestration.tasks[].type` | `provider_action` \| `fluid_validate` \| `fluid_plan` \| `fluid_apply` \| `fluid_execute` \| `fluid_verify` \| `fluid_dq_check` \| `bash` \| `python` \| `branch_python` \| `sensor` \| `email` \| `http` \| `snowflake_query` \| `bigquery_query` \| `bigquery_job` \| `glue_job` \| `databricks_job` \| `custom`. | |
| `orchestration.tasks[].provider` | For `provider_action`: e.g. `aws.s3`, `snowflake.table`. | |
| `orchestration.tasks[].action` | For `provider_action`: e.g. `ensure_bucket`, `ensure`. | |
| `orchestration.tasks[].parameters` | Action parameters. | |
| `orchestration.tasks[].dependsOn` | Upstream task ids. | |
| `orchestration.tasks[].buildStepRef` | Reference into `build` step. | |

---

## `lifecycle` — values

`lifecycle.state` ∈ `preview` \| `active` \| `deprecated` \| `retired`.

A `deprecated` product still serves reads but new `consumes:` references should fail validation in CI.

---

## Where each field is exhaustively documented

The auto-generated reference at [`specs/0.7.3/fluid-spec.html`](../specs/0.7.3/fluid-spec.html) is the authoritative source for every field's exact type, enum values, validation rules, and examples.
