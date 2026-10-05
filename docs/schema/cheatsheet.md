# Schema Cheatsheet

One row per field of the latest stable schema, **0.7.5**: a one-line meaning, whether it is required, and the version it first appeared in. Rows marked 🧪 are in the **0.7.6 preview** only; a contract needs `fluidVersion: "0.7.6"` to use them, and they can still change.

> 🧭 For a guided tour with context per block, read the [**Schema Anatomy**](/fluid/schema/anatomy).
> 📚 For the exhaustive field-by-field reference, see [`specs/0.7.5/fluid-spec.html`](/fluid/specs/0.7.5/fluid-spec.html) (stable) or [`specs/0.7.6/fluid-spec.html`](/fluid/specs/0.7.6/fluid-spec.html) (preview).

"Since" is the version from which the field has been in the schema without interruption; where a member of the same name existed earlier and was removed, the row says so. Contracts before 0.5.7 had a different overall shape (see the [Changelog](/fluid/schema/changelog#before-0-7-1-history-before-the-compatibility-promise)), so for those blocks the current *shape* is newer than the name.

---

## Top-level fields

The root object is closed: a top-level key not listed here makes the document invalid.

| Field | Purpose | Required | Since | Type |
|---|---|:-:|:-:|---|
| `fluidVersion` | The schema version this document declares; it selects the schema the document is validated against. 0.7.5 accepts `"0.7.3"`, `"0.7.4"`, `"0.7.5"` — but see [Choosing `fluidVersion`](/fluid/schema/versions#choosing-fluidversion). | ✅ | 0.0.1 | `enum` |
| `kind` | `DataProduct` \| `MLPipeline`. | ✅ | 0.0.1 | `enum` |
| `id` | Globally unique product id — the product's public address. | ✅ | 0.0.1 | identifier |
| `name` | Human-readable display name. | ✅ | 0.0.1 | `string` |
| `metadata` | Owner, layer, product type, business context. | ✅ | 0.0.1 | `object` |
| `exposes` | Ports this product publishes. | ✅ | 0.0.1 | `object[]` |
| `description` | Business-facing summary. | | 0.0.1 | `string` |
| `domain` | Owning business domain. | | 0.0.1 | `string` |
| `consumes` | Upstream FLUID products this product reads. | | 0.0.1 | `object[]` |
| `build` | How the product is produced (pattern + engine + properties). | | 0.0.1 | `object` |
| `builds` | Several builds for one product, same shape as `build`. | | 0.5.7 | `object[]` |
| `tags` | Lower-case categorization tags (`^[a-z0-9][a-z0-9-]*[a-z0-9]$`). | | 0.5.7 | `string[]` |
| `labels` | Key/value labels. | | 0.5.7 | `map<string,string>` |
| `lineage` | `granularity`, `upstream[]` (with `fieldMappings`), `downstream[]`. | | 0.5.7 | `object` |
| `schemaEvolution` | `strategy` and `compatibility` of the product's schema changes. | | 0.5.7 | `object` |
| `machineLearning` | `enabled`, `framework`, `models[]`. | | 0.5.7 | `object` |
| `environments` | Per-environment overrides of `metadata` and `exposes`. | | 0.5.7 | `map<string,object>` |
| `lifecycle` | `state`, `retention`, `deprecationPolicy`. | | 0.5.7 | `object` |
| `docs` | `homepage`, `runbook`, `dictionary`, `changeLog`. | | 0.5.7 | `object` |
| `sovereignty` | Jurisdiction and data residency. | | **0.7.1** | `object` |
| `accessPolicy` | Access grants for the product. (A different `accessPolicy` existed from 0.0.1 to 0.4.0.) | | **0.7.1** | `object` |
| `orchestration` | Scheduling and workflow-engine settings. Open object — see [below](#orchestration-fields). | | **0.7.2** | `object` |
| `retention` | ISO-8601 TTLs for run state, run logs, lineage events and DLQ records. | | **0.7.3** | `object` |
| `governance` | Account-wide AWS Lake Formation settings: `admins`, `tagDefinitions`. (A different `governance` existed from 0.0.1 to 0.4.0.) | | **0.7.3** | `object` |
| `extensions` | Vendor- or plugin-namespaced configuration. Open object. (Also in 0.0.1; absent from 0.1.0 to 0.7.2.) | | **0.7.3** | `object` |
| 🧪 `packaging` | Container ownership: `mode` (`isolated` \| `shared`), `pool`, `poolManifest`, `containers`. | | 0.7.6 | `object` |
| 🧪 `consumers` | Declared downstream artifacts: `name` and `type` required; `label`, `owner`, `url`, `maturity`, `exposeIds`. | | 0.7.6 | `object[]` |

---

## `metadata` (required) fields

`metadata` is required, and inside it only `owner` is. The schema requires **no** member of `owner`, so `owner: {}` validates; name at least a `team`.

| Field | Purpose | Required | Since |
|---|---|:-:|:-:|
| `metadata.owner` | Owner object: `team`, `email`, `slack`, `oncall`. | ✅ | 0.0.1 |
| `metadata.layer` | Layer label. **Free-form string** — `Bronze`/`Silver`/`Gold` is convention, not enum. | | 0.0.1 |
| `metadata.productType` | `SDP` (source-aligned) \| `ADP` (aggregated) \| `CDP` (consumption-aligned). | | 0.7.3 |
| `metadata.classification` | `public` \| `internal` \| `confidential` \| `restricted`. (A `classification` also existed in 0.0.1.) | | 0.7.3 |
| `metadata.experimental` | Experimental features the contract opts into. | | 0.7.3 |
| `metadata.businessContext` | `domain`, `subdomain`, `businessCapability`, `valueStream`. | | 0.5.7 |
| `metadata.tags` | Tags on the metadata. (Also existed from 0.0.1 to 0.4.0.) | | 0.7.2 |
| `metadata.createdAt` | Creation time (`format: date-time`, an annotation). | | 0.5.7 |
| `metadata.provenance` | Generation envelope written by tooling. | | 0.7.2 |

---

## `exposes[]` fields

Each entry requires `exposeId`, `kind`, `contract` and `binding`, and is closed.

| Field | Purpose | Required |
|---|---|:-:|
| `exposes[].exposeId` | Stable id of this port within the product. | ✅ |
| `exposes[].kind` | `table` \| `view` \| `api` \| `file` \| `stream` \| `topic` \| `feature_store` \| `model` \| `vector` \| `graph` \| `time_series` \| `other`. | ✅ |
| `exposes[].contract` | The data's shape and promises. Must contain `schema` or `openapiRef`. | ✅ |
| `exposes[].binding` | Where it lives — `platform`, `format`, `location` (all three required). | ✅ |
| `exposes[].policy` | **Sibling of `contract`**, not inside it: `authn`, `authz`, `privacy`, `classification`, `agentPolicy`. | |
| `exposes[].title`, `exposes[].description` | Display name and description of the port (`description` since 0.7.2; it also existed from 0.1.0 to 0.4.0). | |
| `exposes[].version` | Semver of this port. | |
| `exposes[].contract.schema[]` | Columns: `name` and `type` required; `required`, `description`, `sensitivity`, `semanticType`, `businessName`, `businessDefinition`, `validationRules`, `tags`, `labels`. | (one of) |
| `exposes[].contract.openapiRef` | Reference to an OpenAPI document (for `kind: api`). | (one of) |
| `exposes[].contract.dq.rules[]` | Declarative quality assertions (below). | |
| `exposes[].contract.schemaPolicy` | `strict` \| `discover_and_freeze` \| `evolve_safe` \| `evolve_all` (since 0.7.3). | |
| `exposes[].contract.schemaSignature` | `sha256:` + 64 hex — a digest of the schema. | |
| `exposes[].qos` | `availability` (a percentage string such as `"99.9%"`), `freshnessSLO`, `latencyP95` (ISO-8601 durations), `dataLossSLO`, `completenessTarget`, `errorBudget`. | |
| `exposes[].semantics` | Entities, measures, dimensions, metrics (since 0.7.2; a `semantics` member with a different shape existed from 0.1.0 to 0.4.0). | |
| `exposes[].mcp` | Serve the port to AI agents over MCP (since 0.7.4): `sampling.maxRows` (integer ≥ 1), `classification.dataClass` (`public` \| `internal` \| `confidential` \| `restricted`). | |
| `exposes[].lifecycle`, `exposes[].observability`, `exposes[].docs` | Per-port lifecycle, observability (`metrics`, `onBreach`, `defaultSLIs`, `alert`) and docs. | |
| `exposes[].binding.platform` | `gcp` \| `aws` \| `azure` \| `snowflake` \| `databricks` \| `kafka` \| `confluent` (0.7.5) \| `local` \| `kubernetes` \| `postgres` (0.7.4) \| `pgvector` (0.7.5) \| `other`. | ✅ |
| `exposes[].binding.format` | `bigquery_table` \| `snowflake_table` \| `snowflake_view` \| `iceberg` \| `delta_table` \| `parquet` \| `csv` \| `json` \| `http_api` \| `grpc_api` \| `kafka_topic` \| `pubsub_topic` \| `gcs_file` \| `s3_file` \| `redshift_table` \| `redshift_serverless` \| `redshift_external_schema` \| `postgres_table` (0.7.4) \| `athena_table` (0.7.4) \| `glue_table` (0.7.4) \| `pgvector_table` (0.7.5) \| `other`. | ✅ |
| `exposes[].binding.location` | Platform address; no member is required by the schema. 0.7.5 adds `environment_id`, `kafka_cluster_id`, `confluent_role_arn` (Tableflow), `catalog`, `warehouse`, `uri`, `partitionBy` (Iceberg catalogs), `namespace`, `workgroup`, `iam_role_arn`, `external_schema`, `glue_database` (Redshift Serverless), `stream` (Kinesis). | ✅ |
| `exposes[].binding.icebergConfig` | Iceberg table settings when `format: iceberg` (since 0.7.2). | |
| `exposes[].binding.vectorConfig` | Vector output port for `pgvector` (since 0.7.5): `dimensions` (required, 1–16000), `embeddingModel`, `vectorType`, `indexType`, `distanceMetric`, `hnsw`, `ivfflat`, `table`, `sourceKeyColumn`. | |
| `exposes[].binding.governance` | Per-resource AWS Lake Formation settings: `registerLocation`, `grants[]`, `tags`, `rowFilter` (since 0.7.3). Account-wide settings live in the top-level `governance` block. | |
| 🧪 `exposes[].binding.encryption.kms` | `product` \| `none` \| an AWS KMS alias or ARN \| a Cloud KMS key name. | |
| 🧪 `exposes[].binding.principals` | Logical principal → identity (or list) on this platform. | |
| 🧪 `exposes[].binding.packaging` | Per-binding override of `packaging`. | |
| 🧪 `exposes[].binding.governance.lakeFormation.bucketPolicy` | `cross-account` (default) \| `none` \| `all-grantees`. **Authoritative** — an emitted bucket policy replaces every other statement on the bucket; see the [0.7.6 notes](/fluid/releases/0.7.6#binding-fields-encryption-principals-lake-formation-bucket-policy). | |
| 🧪 `exposes[].lifecycle.expire` | `true` deletes data older than `retention` (default `false`). | |
| `exposes[].tags`, `exposes[].labels` | Port-level categorization. | |

### `contract.dq.rules[]` fields

| Field | Purpose | Required |
|---|---|:-:|
| `dq.rules[].id` | Rule id. | ✅ |
| `dq.rules[].type` | `freshness` \| `completeness` \| `uniqueness` \| `valid_values` \| `accuracy` \| `schema` \| `anomaly_detection` \| `drift_detection`. | ✅ |
| `dq.rules[].severity` | `info` \| `warn` \| `error` \| `critical`. | ✅ |
| `dq.rules[].selector` | Predicate or column the rule applies to (e.g. `"amount > 0"`). | |
| `dq.rules[].threshold` | Numeric threshold for the operator. | |
| `dq.rules[].operator` | `>=` \| `>` \| `<=` \| `<` \| `==` \| `!=`. | |
| `dq.rules[].window` | ISO-8601 duration window (e.g. `PT15M`). | |

---

## `build` / `builds[]` fields

A build is closed and has no required member.

| Field | Purpose | Required |
|---|---|:-:|
| `build.id` | Build id; give one to each entry of `builds[]`. | |
| `build.pattern` | `hybrid-reference` \| `embedded-logic` \| `multi-stage` \| `acquisition` (0.7.3). Selects the shape of `properties`. | |
| `build.engine` | `dbt` \| `sql` \| `python` \| `spark` \| `glue` \| `custom` \| `duckdb` \| `airbyte` \| `meltano` \| `dlt` \| `kafka-connect` \| `debezium` (the last six since 0.7.3), or `dbt-<adapter>` such as `dbt-databricks` (since 0.7.2). | |
| `build.capabilities` | What the build asks of its runner: `full_refresh`, `incremental_append`, `incremental_dedup`, `incremental_merge`, `cdc`, `streaming`, `schema_discovery`, `schema_evolution`, `dlp_scan`, `at_most_once`, `at_least_once`, `exactly_once` (since 0.7.3). | |
| `build.properties` | Pattern-specific settings. `hybrid-reference` requires `model`; `embedded-logic` requires `sql`; `acquisition` requires `source` (below). | |
| `build.execution.trigger` | `type`: `schedule` \| `event` \| `manual` \| `dependency` \| `dataset` \| `schedule_and_dataset` \| `timetable`, plus `schedule`, `cron`, `timezone`, … | |
| `build.execution.runtime` | Where it runs: `platform`, `resources`, `image`, `executor`, `serviceAccount`, `timeout`. | |
| `build.execution.retries` | `maxAttempts`, `backoffStrategy` (`fixed` \| `exponential` \| `linear`), `initialDelay`, `maxDelay`. | |
| `build.execution.notifications[]` | `type` (`email` \| `slack` \| `webhook` \| `pagerduty`), `target`, `condition` (`success` \| `failure` \| `always`). Closed since 0.7.2. | |
| `build.execution.orchestration` | The same shape as top-level `orchestration`. | |
| `build.outputs` | The `exposeId`s this build produces. | |
| `build.repository` | Where referenced code lives. | |

---

## `build.properties` when `pattern: acquisition` fields

When `pattern: acquisition` (0.7.3+), the schema validates `properties` against the acquisition shape below. (For the other patterns it uses the hybrid-reference, embedded-logic and multi-stage shapes.)

| Field (under `build.properties`) | Purpose | Required |
|---|---|:-:|
| `source.kind` | Source system — a free string, e.g. `postgres`, `kafka`, `salesforce`. | ✅ |
| `source.mode` | `full_refresh` \| `incremental_append` \| `incremental_dedup` \| `incremental_merge` \| `cdc` \| `streaming`. | ✅ |
| `source.cursor_field` | Column used as the incremental cursor. | |
| `source.connection` | Connection details (open object). `secretRef` must be a URI matching `<scheme>://…`; the schema's description names `vault://`, `aws://`, `gcp://`, `azure://` and `env://`. | |
| `source.streams` | Streams / tables / objects to ingest. | |
| `sink.format` | `iceberg` \| `delta` \| `parquet` \| `csv` \| `json` \| `snowflake_table` \| `bigquery_table` \| `redshift_table` \| `duckdb_table`. | |
| `sink.catalog` | `rest` \| `glue` \| `nessie` \| `unity` \| `snowflake-managed` \| `hive`. | |
| `sink.partitionBy` | Array of **strings** (function form, e.g. `["day(ingested_at)"]`) — not the object form of `binding.icebergConfig.partitionSpec`. | |
| `delivery.guarantee` | `at_most_once` \| `at_least_once` (default) \| `exactly_once`. | |
| `delivery.idempotencyKey` | Key template (default `{run_id}:{stream}:{record_pk}`). | |
| `delivery.dlq` | `enabled` (default `true`), `sink.format` (`parquet` \| `json` \| `ndjson`), `sink.location`, `maxRecordsBeforeAbort` (default 10000), `alertOn` (`pii_classification_failed` \| `schema_violation` \| `destination_write_failed` \| `quality_gate_failed`). | |
| `schemaEvolution.policy` | `strict` (default) \| `discover_and_freeze` \| `evolve_safe` \| `evolve_all`. | |
| `schemaEvolution.onAddedColumn` / `onRemovedColumn` / `onTypeChange` | `include` \| `warn` \| `fail` / `drop` \| `warn` \| `fail` / `cast` \| `warn` \| `fail`. | |
| `schemaEvolution.sourceFingerprint` | `required` (default) \| `optional` \| `disabled`. | |
| `preLand` | Hook chain: `dlp_scan`, `tokenize_pii`, `quality_gate`, `emit_lineage_input`. | |
| `quality` | Pre-land quality `gates[]` (`rule`, `severity` required), `onError`, `anomalies[]`. | |
| `cost.budget` | `monthly` (`rows`, `bytes`, `computeMinutes`) and `onExceed` (`warn` (default) \| `abort`). | |
| `cost.chargeback` | `team`, `project`, `costCenter`. | |
| `catalog.register` | `datahub`, `openmetadata`, `datamesh_manager`, `unity`, `glue`, `snowflake_horizon` (the last three since 0.7.4). | |
| `concurrency.lock` | `scope` (`product` (default) \| `build`), `timeout`, `onContended` (`abort` \| `queue` \| `replace`). | |
| `lineage.emit` | Emit lineage events (default `true`). | |
| `<engine>` (`duckdb` \| `airbyte` \| `meltano` \| `dlt` \| `kafka-connect` \| `debezium`) | Engine-specific settings. | |
| `<engine>.deployment.mode` | `embedded` (default) \| `bring-your-own` \| `managed`; with `managed`, `managed.target` is `docker` \| `kubernetes` \| `terraform` \| `opentofu`. | |
| `<engine>.image_signature` | `verifier` (`cosign`), `publicKey`, `slsaProvenance` (`required` \| `optional` (default) \| `disabled`). | |
| `kafka-connect.iceberg_sink_enabled`, `sink_topics`, `streamingSink`, `iceberg_catalog_overrides` | Opt-in Iceberg streaming sink (since 0.7.5). | |

---

## `exposes[].policy` fields

| Field | Purpose | Required |
|---|---|:-:|
| `exposes[].policy.authn` | `oidc` \| `oauth2` \| `api_key` \| `none` \| `custom` \| `iam` \| `jwt`. | |
| `exposes[].policy.authz.readers` / `writers` | Principals with read / write access. | |
| `exposes[].policy.authz.columnRestrictions[]` | `principal`, `columns`, `access` (`allow` \| `deny`). 🧪 The 0.7.6 schema defines its meaning: a column named in any restriction is restricted; `deny` removes access; `allow` limits the columns to the principals an `allow` names; deny beats allow; a restriction never grants access. | |
| `exposes[].policy.privacy.masking[]` | `{column, strategy}` required; `strategy` is `mask` \| `hash` \| `tokenize` \| `encrypt` \| `k_anonymity`; `params` is open. 🧪 0.7.6 types `params`: `keepFirst`, `keepLast` (mask), `saltEnv` (hash), `keyEnv` (tokenize, encrypt). | |
| `exposes[].policy.privacy.rowLevelPolicy.expression` | Provider-specific row filter predicate (required inside `rowLevelPolicy`). | |
| `exposes[].policy.classification` | `Public` \| `Internal` \| `Confidential` \| `Restricted`. | |
| `exposes[].policy.agentPolicy` | AI-consumer policy (below). | |

### `exposes[].policy.agentPolicy` (0.7.1) fields

> ⚠️ **Location.** `agentPolicy` is **per-expose**, under `exposes[].policy.agentPolicy`. It is not a top-level property.
>
> **0.7.4 — runtime enforcement.** When the same expose carries an `mcp` block, an MCP gateway that implements 0.7.4 enforces the model and use-case lists on every read; the reference implementation's gateway does. The shape is unchanged.

| Field | Purpose | Default |
|---|---|:-:|
| `…agentPolicy.allowedModels` | Model ids allowed to read the expose (lower-case ids such as `gpt-4`, `claude-3-opus`). | |
| `…agentPolicy.deniedModels` | Model ids denied. | |
| `…agentPolicy.maxTokensPerRequest` / `maxTokensPerDay` | Token caps (integers ≥ 1). | |
| `…agentPolicy.allowedUseCases` / `deniedUseCases` | From a fixed vocabulary: `inference` \| `reasoning` \| `analysis` \| `summarization` \| `classification` \| `embedding` \| `search` \| `qa` \| `code_generation` \| `fine_tuning` \| `training` \| `rag`. **Other strings are invalid.** | |
| `…agentPolicy.canReason` | Allow multi-step reasoning over the data. | `false` |
| `…agentPolicy.canStore` | Allow caching or persisting the data. | `false` |
| `…agentPolicy.retentionPolicy` | `maxRetentionDays` (≥ 0), `requireDeletion`. | `requireDeletion: true` |
| `…agentPolicy.auditRequired` | Log AI consumption. | `true` |
| `…agentPolicy.purposeLimitation` | Free-text purpose statement. | |

---

## `consumes[]` fields

| Field | Purpose | Required |
|---|---|:-:|
| `consumes[].productId` | Upstream product id. | ✅ |
| `consumes[].exposeId` | Upstream port. | ✅ |
| `consumes[].versionConstraint` | Semver range, e.g. `^2.0.0`. | |
| `consumes[].qosExpectations` | `freshnessMax`, `maxStaleness` (durations), `minCompleteness` (0–1). | |
| `consumes[].requiredPolicies` | Policies the upstream must carry. | |
| `consumes[].purpose` | Why this product reads the upstream. | |
| 🧪 `consumes[].upstreamWorkspace` | The other mesh that owns the upstream. Requires `upstreamDigest`. | |
| 🧪 `consumes[].upstreamDigest` | `sha256:` + 64 lowercase hex — the upstream contract this product was composed against. | |

---

## `sovereignty` (0.7.1) fields

| Field | Purpose |
|---|---|
| `sovereignty.jurisdiction` | `EU` \| `US` \| `UK` \| `CA` \| `AU` \| `JP` \| `CN` \| `IN` \| `BR` \| `Global` \| `Multi-Region`. |
| `sovereignty.allowedRegions` / `deniedRegions` | Cloud regions allowed / denied. |
| `sovereignty.dataResidency` | Boolean — must data stay within the jurisdiction? |
| `sovereignty.crossBorderTransfer` | Boolean — is cross-border transfer permitted? |
| `sovereignty.transferMechanisms` | `SCCs` \| `BCRs` \| `Adequacy` \| `DPF` \| `Consent` \| `Derogation`. |
| `sovereignty.regulatoryFramework` | `GDPR` \| `CCPA` \| `CPRA` \| `HIPAA` \| `PIPEDA` \| `LGPD` \| `PDPA` \| `POPIA` \| `DPA` \| `APPI`. |
| `sovereignty.enforcementMode` | `strict` \| `advisory` \| `audit`. |
| `sovereignty.validationRequired` | Whether bindings are checked against this block. |

---

## `accessPolicy` (0.7.1) fields

Each grant requires only `principal`, and is closed.

| Field | Purpose | Required |
|---|---|:-:|
| `accessPolicy.grants[].principal` | The principal, e.g. `group:analysts@example.com`. | ✅ |
| `accessPolicy.grants[].permissions` | `read` \| `select` \| `query` \| `write` \| `insert` \| `update` \| `delete` \| `create` (0.7.2) \| `admin` \| `manage`. | |
| `accessPolicy.grants[].resources` | Strings selecting the exposes in scope, e.g. JSONPath. | |
| `accessPolicy.grants[].conditions` | Open object for conditional access (IP ranges, time windows). | |

---

## `governance` (0.7.3) fields

| Field | Purpose |
|---|---|
| `governance.lakeFormation.admins` | IAM ARNs. **Authoritative:** applying it replaces the account's Lake Formation admin list, so list every admin, including the identity that applies it. The schema's description adds that applying it also clears the account's create-database and create-table default permissions, trusted resource owners and parameters, and that destroying the emitted `aws_lakeformation_data_lake_settings` resource empties the admin list and resets `CROSS_ACCOUNT_VERSION` to 1. |
| `governance.lakeFormation.tagDefinitions` | LF-tag key → allowed values. |

---

## `retention` (0.7.3) fields

| Field | Purpose | Default (schema description) |
|---|---|:-:|
| `retention.runState` | How long run state is kept. | `P30D` |
| `retention.runLogs` | How long run logs are kept. | `P90D` |
| `retention.lineage` | How long emitted lineage events are kept. | `P365D` |
| `retention.dlq` | How long DLQ records are kept. | `P180D` |

All values are [ISO-8601 durations](https://en.wikipedia.org/wiki/ISO_8601#Durations). `retention` covers operational records, not the product's data; for data, see `lifecycle.retention` (and, 🧪 in 0.7.6, `exposes[].lifecycle.expire`).

---

## `orchestration` fields

| Field | Purpose | Required |
|---|---|:-:|
| `orchestration.engine` | `airflow` \| `dagster` \| `prefect` \| `kubeflow` \| `custom` \| `none`. | ✅ |
| `orchestration.mode` | `generated` \| `manual` \| `hybrid`. | |
| `orchestration.generateOnChange` | Regenerate the workflow when the contract changes. | |
| `orchestration.airflow.dagId` | DAG id; required when `airflow` is present. | |
| `orchestration.airflow.dagConfig` | `schedule`, `startDate`, `catchup`, `maxActiveRuns`, … | |
| `orchestration.airflow.tasks[].taskId` | Task id (lower-case). | ✅ |
| `orchestration.airflow.tasks[].type` | `provider_action` \| `fluid_validate` \| `fluid_plan` \| `fluid_apply` \| `fluid_execute` \| `fluid_verify` \| `fluid_dq_check` \| `bash` \| `python` \| `branch_python` \| `sensor` \| `email` \| `http` \| `snowflake_query` \| `bigquery_query` \| `bigquery_job` \| `glue_job` \| `databricks_job` \| `custom`. | |
| `orchestration.airflow.tasks[].operator` | Operator name. **Set it** — see the note below. | |
| `orchestration.airflow.tasks[].provider` | For `provider_action`: `aws` \| `gcp` \| `azure` \| `snowflake` \| `databricks` \| `kafka` \| `kubernetes` \| `local` \| `custom`. | (provider_action) |
| `orchestration.airflow.tasks[].action` | For `provider_action`: `<service>.<action>`, e.g. `s3.ensure_bucket`. | (provider_action) |
| `orchestration.airflow.tasks[].params` | Action parameters (open object). | (provider_action) |
| `orchestration.airflow.tasks[].dependencies` | Upstream task ids. | |
| `orchestration.airflow.tasks[].buildStepRef` | Reference into a build step. | |

> ⚠️ **`orchestration.tasks` is not validated.** `orchestration` is an open object up to 0.7.6, so a top-level `orchestration.tasks` list is accepted without any check. Its keys are implementation-defined: the reference implementation's AWS and GCP code generators read `params` and `dependsOn` there, and its Snowflake Airflow generator reads `parameters`.
>
> **Name each Airflow task's `operator`.** In the 0.7.1 to 0.7.6 schemas the conditional rules for `fluid_execute`, `bash` and `python` tasks also match a task with no `operator`, so a task that has no `operator` and carries `params` must satisfy all three at once and is in practice rejected. A `provider_action` task always carries `params`, so it is always affected. A task with neither `operator` nor `params` validates.

---

## `lifecycle` values

`lifecycle.state` ∈ `preview` \| `active` \| `deprecated` \| `retired` — the state of the *product*, unrelated to preview *schema versions*. Other members: `retention` (ISO-8601 duration) and `deprecationPolicy` (`noticePeriod`, `contact`, `replacement`).

---

## Where each field is exhaustively documented

The auto-generated reference at [`specs/0.7.5/fluid-spec.html`](/fluid/specs/0.7.5/fluid-spec.html) renders every field's exact type, enum values and validation rules from the schema.
