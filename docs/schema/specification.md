# FLUID Specification

::: tip Versions
**Latest stable: 0.7.5. Preview: 0.7.6.** This page specifies the structure of a FLUID document as defined by the **0.7.5** JSON Schema. For every version's schema and generated field-by-field reference, see [**Versions**](/fluid/schema/versions); for what is new in the preview, see [0.7.6 (preview)](/fluid/releases/0.7.6).
:::

FLUID (Federated Layered Unified Interchange Definition) is an open, declarative specification for **data products**, written in YAML or JSON and kept in version control. It is not a platform or a single tool: it is a shared language that tools read to build, deploy, govern and serve a data product.

A FLUID document describes one data product: what it **consumes** (its inputs), what it **exposes** (its output ports, each with a contract and a binding to where the data lives), how it is **built**, and the policies around it — access, sovereignty, AI-agent use, retention. This page is for anyone implementing a FLUID-aware tool or checking that one conforms.

**What defines conformance.** The published JSON Schemas define which documents are valid FLUID documents, and the [conformance corpus](https://github.com/open-data-protocol/fluid/blob/main/tests/README.md) pins that behaviour case by case, so that "FLUID-conformant" can be checked without any particular implementation ([GOVERNANCE.md](https://github.com/open-data-protocol/fluid/blob/main/GOVERNANCE.md)). [`data-product-forge`](/fluid/concepts/forge-cli) is the reference implementation: implementation #1 under test, not the referee. Where this page and a schema disagree, the schema is authoritative and this page is wrong.

---

## Core principles

- **Data as a product** — data is a first-class asset with an owner, a versioned interface and a machine-readable contract.
- **Declarative, not imperative** — a document states the desired end state; FLUID-aware tools decide how to reach it.
- **Contracts as code** — schema, quality, build and policy live in version-controlled files, so they can be checked automatically.
- **Federated ownership** — data products are owned by the domain teams that know the data.

---

## Documents and files

A FLUID document is a single YAML or JSON object. **The file name is not normative.** Pages on this site name files `*.fluid.yml`; the reference implementation scaffolds and looks for `contract.fluid.yaml`. Either is fine.

## Validation semantics

A FLUID document is validated against the published JSON Schema whose version matches its `fluidVersion`. Every published schema declares `"$schema": "https://json-schema.org/draft/2020-12/schema"`, so JSON Schema Draft 2020-12 defines the meaning of every keyword except where this section says otherwise.

### `format` is an annotation, never an assertion

A validator **MUST NOT** reject a FLUID document solely because a string does not match the `format` named for it. A validator **MAY** surface the mismatch as a warning, and a governance or linting layer built on FLUID **MAY** treat it as an error of its own; neither affects whether the document is a valid FLUID document.

The consequence is worth stating plainly rather than leaving for a reader to discover: **a document that validates is not thereby guaranteed to carry a well-formed `metadata.owner.email`.** Three formats appear across the published schemas — `uri`, `date-time` and `email` — and all three are descriptive.

This is the Draft 2020-12 default, and FLUID keeps it for two reasons of its own.

The first is that conformance must not depend on which validator you run. `format` vocabularies are optional in Draft 2020-12 and implementations differ widely in which formats they recognise and what they pull in to check them. Were FLUID to make `format` assertive, the same document could be conformant in one language and non-conformant in another, which would defeat the purpose of publishing a conformance corpus at all.

The second is that the choice is not symmetric. Declaring `format` assertive would invalidate documents that are valid today — a narrowing, which [GOVERNANCE.md](https://github.com/open-data-protocol/fluid/blob/main/GOVERNANCE.md) forbids between versions and `scripts/check-compat.py` enforces on every pull request. Annotation-only is therefore the only reading available to a pre-1.0 specification that has already published many schema versions. A future version may add assertive checking behind a new, opt-in keyword; it may not retroactively sharpen this one.

Implementations that do want to assert formats are served by the conformance corpus rather than left to guess: the cases that depend on assertion live in [`tests/optional/`](https://github.com/open-data-protocol/fluid/tree/main/tests/optional), separated from the core tier for exactly this reason, and `conformance/run.py` runs them under a format-asserting validator.

### FLUID's own `format` field is unrelated

FLUID defines a **field** named `format` in several places — `exposes[].binding.format` (`bigquery_table`, `snowflake_table`, `gcs_file`, …) and the `format` keys in the acquisition blocks. These are ordinary FLUID fields constrained by `enum`, and `enum` **is** assertive: a `binding.format` outside the enumerated set makes the document invalid.

The collision of names is unfortunate and is called out here because it is easy to read "`format` is an annotation" as applying to them. It does not. The sentence above is about the JSON Schema *keyword*; this paragraph is about a FLUID *field* that happens to share its spelling.

### The declared `fluidVersion` selects the schema

Because the schema is chosen by the document's own `fluidVersion`, a later schema accepting an earlier `fluidVersion` value is not a verdict on documents that declare that earlier version. The 0.7.5 schema's `fluidVersion` enum lists `"0.7.3"`, `"0.7.4"` and `"0.7.5"`; a document declaring `"0.7.4"` is still validated against the 0.7.4 schema, so it cannot use a field that only 0.7.5 defines. See [Choosing `fluidVersion`](/fluid/schema/versions#choosing-fluidversion).

### Known interoperability issue: one `pattern` is not an ECMA-262 regular expression

Draft 2020-12 says a `pattern` SHOULD be a valid ECMA-262 regular expression. In the 0.7.2 to 0.7.6 schemas, the second alternative of the column `type` (`$defs/column/properties/type`) begins with the inline flag `(?i)`, which ECMA-262 does not have: JavaScript's `RegExp` rejects it as an invalid group. Python's `re`, which the conformance tooling in this repository uses, accepts it and matches case-insensitively. A validator that compiles patterns as ECMA-262 may therefore refuse that pattern, or the schema, where a Python-based validator does not. This is recorded here rather than resolved: changing the pattern would be a schema change, and schemas are changed upstream (see [CONTRIBUTING.md](https://github.com/open-data-protocol/fluid/blob/main/CONTRIBUTING.md)).

---


## Composing a document from several files

FLUID defines **one document**. The standard does not define how a document may be assembled from several files; any such mechanism is **implementation-defined**, and nothing in this section is normative.

What follows from the rest of this specification:

1. **A composed root is not a FLUID document.** The published schemas have no `$ref` property in a document, and the root object and most nested objects are closed (`additionalProperties: false`), so a file that stands in `{ $ref: ... }` for a block fails validation. Splitting a valid contract into fragments with the reference implementation's `fluid split` and validating the root file directly against the 0.7.5 schema gives errors such as `Additional properties are not allowed ('$ref' was unexpected)`.
2. **Validate the resolved document.** Conformance is a property of the single document a composition mechanism produces. Resolve first, then validate that result against the schema of its `fluidVersion`.

### How the reference implementation composes contracts (non-normative)

`data-product-forge` resolves `$ref` nodes before it validates, plans or applies a contract, so the rest of its pipeline sees one document. As of data-product-forge 0.18:

- A `$ref` node is an object whose only key is `$ref`; its value is a path to a YAML or JSON file, resolved relative to the file that contains it, optionally followed by `#` and an [RFC 6901](https://www.rfc-editor.org/rfc/rfc6901) JSON Pointer. A referenced YAML file must hold an object, not a list. Same-document refs (`#/...`) are left as written; cycles and nesting deeper than 20 levels are errors.
- **Refs are confined to the root contract's directory tree.** A ref that resolves outside it — through `..` or a symlink — is refused, as are absolute paths and URLs (`https://`, `file://`, `s3://`, …). Setting `FLUID_REF_ROOT` (or passing `ref_root=` to the loader) widens the root to a directory that contains the contract, for monorepos that share fragments; a `FLUID_REF_ROOT` that does not contain the contract is ignored with a `ref_root_env_ignored` warning.
- `fluid split` turns a single-file contract into a root plus a `fragments/` directory (`fragments/exposes/<exposeId>.yaml`, `fragments/builds/<id>.yaml`, `fragments/sovereignty.yaml`, `fragments/access-policy.yaml`); `fluid bundle` resolves a root back into one document.
- Its `.fluid/` directories hold the tool's own runtime state (receipts, run records, staging data), which its generated `.gitignore` partly excludes from version control. They are not a place for contract fragments.

Details: [Composing a contract from fragments](https://agenticstiger.github.io/forge_docs/concepts/contract-refs.html), [`fluid split`](https://agenticstiger.github.io/forge_docs/cli/split.html) and [`fluid bundle`](https://agenticstiger.github.io/forge_docs/cli/bundle.html) in the reference implementation's documentation.

---

## 1. Document structure (0.7.5)

The tables summarise the 0.7.5 schema. They name every top-level member and the main nested blocks; the [generated reference](/fluid/specs/0.7.5/fluid-spec.html) has every field. **Closed** means `additionalProperties: false`: a member the table does not list makes the document invalid.

### 1.1 Root

The root object is **closed**.

| Member | Type | Required | Meaning |
|---|---|:-:|---|
| `fluidVersion` | string, one of `"0.7.3"`, `"0.7.4"`, `"0.7.5"` | ✅ | The schema version the document declares. It selects the schema the document is validated against. |
| `kind` | `DataProduct` \| `MLPipeline` | ✅ | The kind of product. |
| `id` | identifier | ✅ | Globally unique product id, e.g. `finance.gold.customer_360`. |
| `name` | string | ✅ | Display name. |
| `metadata` | object (§1.2) | ✅ | Ownership and classification. |
| `exposes` | array of expose (§1.3) | ✅ | The product's output ports. |
| `description`, `domain` | string | | Business description and owning domain. |
| `tags` | array of unique tags | | Each tag lower-case: `^[a-z0-9][a-z0-9-]*[a-z0-9]$` or a single character. |
| `labels` | map of string → string | | Key/value labels. |
| `consumes` | array of consume (§1.4) | | Upstream data products this product reads. |
| `build` | build (§1.5) | | How the product is built. |
| `builds` | array of build (§1.5) | | Several builds for one product. |
| `orchestration` | object (§1.6) | | Scheduling and workflow-engine settings. |
| `accessPolicy` | object (§1.7) | | Access grants for the product. |
| `sovereignty` | object (§1.7) | | Jurisdiction and data-residency constraints. |
| `governance` | object (§1.7) | | Account-wide AWS Lake Formation settings. |
| `retention` | object | | ISO-8601 durations for operational records: `runState`, `runLogs`, `lineage`, `dlq`. |
| `lifecycle` | object | | `state` (`preview` \| `active` \| `deprecated` \| `retired`), `retention`, `deprecationPolicy`. |
| `lineage` | object | | `granularity` (`table_level` \| `field_level`), `upstream[]`, `downstream[]`. |
| `schemaEvolution` | object | | `strategy` (`semantic_versioning` \| `date_based` \| `sequential`), `compatibility` (`backward_compatible` \| `forward_compatible` \| `full_compatible` \| `breaking`), `changePolicy`. |
| `machineLearning` | object | | `enabled`, `framework`, `models[]`. |
| `environments` | map of name → environment | | Per-environment overrides of `metadata` and `exposes`. |
| `docs` | object | | `homepage`, `runbook`, `dictionary`, `changeLog`. |
| `extensions` | object (open) | | Vendor- or plugin-namespaced configuration. |

An **identifier** matches `^[A-Za-z0-9_][A-Za-z0-9_.-]*[A-Za-z0-9_]$` (or is a single letter, digit or underscore). A **duration** is an ISO-8601 duration such as `P30D` or `PT15M`.

### 1.2 `metadata`

**Closed.** `owner` is required; no member of `owner` is.

| Member | Type | Meaning |
|---|---|---|
| `owner` (required) | object, closed: `team`, `email`, `slack`, `oncall` | Who owns the product. `email` carries `format: email`, which is an annotation (see [Validation semantics](#validation-semantics)). |
| `layer` | string | Free-form layer label; `Bronze` / `Silver` / `Gold` is a convention, not an enum. |
| `productType` | `SDP` \| `ADP` \| `CDP` | Source-aligned, aggregated or consumption-aligned data product. |
| `classification` | `public` \| `internal` \| `confidential` \| `restricted` | Default classification. Optional. |
| `businessContext` | object: `domain`, `subdomain`, `businessCapability`, `valueStream` | Business context. |
| `experimental` | array of unique strings | Experimental features the document opts into. |
| `createdAt` | string, `format: date-time` | Creation time. |
| `provenance` | object | Generation envelope written by tooling (tool, version, command, time). |
| `tags` | array of tags | |

### 1.3 `exposes[]` — output ports

Each expose is **closed** and requires `exposeId`, `kind`, `contract` and `binding`.

| Member | Type | Meaning |
|---|---|---|
| `exposeId` (required) | identifier | Id of the port, unique within the product. |
| `kind` (required) | `table` \| `view` \| `api` \| `file` \| `stream` \| `topic` \| `feature_store` \| `model` \| `vector` \| `graph` \| `time_series` \| `other` | What the port is. |
| `contract` (required) | object, closed | The data's shape and promises. Must contain `schema` or `openapiRef` (or both). |
| `binding` (required) | object, closed | Where the data lives (§1.3.2). |
| `policy` | object, closed | `authn`, `authz` (`readers`, `writers`, `columnRestrictions`), `privacy` (`masking[]`, `rowLevelPolicy`), `classification`, `agentPolicy`. |
| `semantics` | object, closed | Business meaning: `entities`, `measures`, `dimensions`, `metrics`. |
| `qos` | object, closed | `availability`, `freshnessSLO`, `dataLossSLO`, `latencyP95`, `completenessTarget`, `errorBudget`. |
| `mcp` | object, closed | `sampling.maxRows`, `classification.dataClass` for serving the port to AI agents over MCP. |
| `lifecycle`, `observability`, `docs` | object | Per-port lifecycle, observability and documentation. |
| `title`, `description`, `version` | string (`version` is semver) | |
| `crawler`, `iceberg` | object | AWS Glue crawler and Iceberg table-maintenance settings. |
| `tags`, `labels` | | |

#### 1.3.1 `contract`

| Member | Type | Meaning |
|---|---|---|
| `schema` | array of column | The columns. |
| `openapiRef` | string | Reference to an OpenAPI document, for `kind: api`. |
| `dq` | object: `rules[]`, `monitoring` | Data-quality rules. Each rule is closed and requires `id`, `type` (`freshness` \| `completeness` \| `uniqueness` \| `valid_values` \| `accuracy` \| `schema` \| `anomaly_detection` \| `drift_detection`) and `severity` (`info` \| `warn` \| `error` \| `critical`). |
| `schemaPolicy` | `strict` \| `discover_and_freeze` \| `evolve_safe` \| `evolve_all` | How the output schema may change. |
| `schemaSignature` | `sha256:` + 64 hex | A digest of the schema. |
| `guarantees`, `quality` | object, array | Compatibility promises and additional quality checks. |

A **column** is closed and requires `name` and `type`. `type` is a type name such as `string`, `int64`, `numeric`, `timestamp` or `json` from a fixed list, matched case-insensitively and optionally with parameters (`VARCHAR(255)`, `DECIMAL(10,2)`). Other members: `required` (boolean), `description`, `sensitivity` (`none` \| `internal` \| `confidential` \| `restricted` \| `pii` \| `phi` \| `cleartext` \| `treated` \| `anonymized` \| `pseudonymized` \| `tokenized` \| `encrypted`), `semanticType`, `businessName`, `businessDefinition`, `validationRules`, `tags`, `labels`.

#### 1.3.2 `binding`

Closed; requires `platform`, `format` and `location`.

| Member | Type | Meaning |
|---|---|---|
| `platform` (required) | `gcp` \| `aws` \| `azure` \| `snowflake` \| `databricks` \| `kafka` \| `confluent` \| `local` \| `kubernetes` \| `postgres` \| `pgvector` \| `other` | The platform. |
| `format` (required) | `bigquery_table`, `snowflake_table`, `snowflake_view`, `gcs_file`, `s3_file`, `http_api`, `grpc_api`, `pubsub_topic`, `kafka_topic`, `delta_table`, `iceberg`, `parquet`, `csv`, `json`, `redshift_table`, `redshift_serverless`, `redshift_external_schema`, `postgres_table`, `athena_table`, `glue_table`, `pgvector_table`, `other` | The physical format. |
| `location` (required) | object, closed | Platform-specific address. Members: `account`, `project`, `dataset`, `database`, `schema`, `table`, `bucket`, `path`, `gateway`, `baseUrl`, `topic`, `subscription`, `region`, `zone`, `environment_id`, `kafka_cluster_id`, `confluent_role_arn`, `stream`, `namespace`, `workgroup`, `iam_role_arn`, `external_schema`, `glue_database`, `catalog`, `warehouse`, `uri`, `partitionBy`. None is required by the schema. |
| `icebergConfig` | object | Iceberg table settings (write version, file format, partition spec, sort order). |
| `vectorConfig` | object, closed; `dimensions` required | Vector / embeddings output-port settings. |
| `governance` | object: `lakeFormation` | Per-resource AWS Lake Formation settings: `registerLocation`, `grants[]`, `tags`, `rowFilter`. |
| `properties` | object (open) | Platform-specific extra properties. |
| `tags`, `labels` | | |

### 1.4 `consumes[]` — input ports

Each entry is **closed** and requires `productId` and `exposeId`: the upstream product and the port it reads. Optional: `versionConstraint` (a semver range such as `^2.0.0`), `qosExpectations` (`freshnessMax`, `maxStaleness`, `minCompleteness`), `requiredPolicies[]`, `purpose`, `tags`, `labels`.

### 1.5 `build` and `builds[]`

A build is **closed**; no member is required.

| Member | Type | Meaning |
|---|---|---|
| `id` | identifier | Build id (useful when there are several). |
| `pattern` | `hybrid-reference` \| `embedded-logic` \| `multi-stage` \| `acquisition` | Selects the shape of `properties`. |
| `engine` | `dbt`, `sql`, `python`, `spark`, `glue`, `custom`, `duckdb`, `airbyte`, `meltano`, `dlt`, `kafka-connect`, `debezium`, or `dbt-<adapter>` | The engine. |
| `properties` | object | The pattern's settings (below). |
| `execution` | object, closed | `trigger`, `runtime`, `retries`, `notifications[]`, `orchestration`. |
| `capabilities` | array | What the build asks of its runner, e.g. `incremental_dedup`, `cdc`, `streaming`, `exactly_once`. |
| `repository`, `description` | string | |
| `outputs` | array of identifier | The `exposeId`s the build produces. |
| `dependencies`, `transformations` | array | |

`properties` is validated according to `pattern`:

| `pattern` | `properties` shape | Required |
|---|---|---|
| `hybrid-reference` | `model`, `target`, `select`, `models`, `vars`, `materializations` — a reference to a model kept elsewhere, such as a dbt project | `model` |
| `embedded-logic` | `sql`, `language` (`sql` \| `flink_sql` \| `pyspark` \| `scala` \| `python` \| `r`), `parameters` | `sql` |
| `multi-stage` | `stages[]`, `orchestration` | — |
| `acquisition` | `source` (`kind`, `mode` required), `sink`, `delivery`, `schemaEvolution`, `preLand`, `quality`, `cost`, `catalog`, `concurrency`, `lineage`, and one settings key per engine: `duckdb`, `airbyte`, `meltano`, `dlt`, `kafka-connect`, `debezium` | `source` |

### 1.6 `orchestration`

Requires `engine` (`airflow` \| `dagster` \| `prefect` \| `kubeflow` \| `custom` \| `none`). Defined members: `mode` (`generated` \| `manual` \| `hybrid`), `generateOnChange`, and per-engine settings `airflow` (which requires `dagId`, and holds `tasks[]`), `dagster`, `prefect`.

The object is **open**: it does not set `additionalProperties`, so members it does not define — such as an `orchestration.tasks` list — are accepted **without being checked**. The only task shape the schema checks is `orchestration.airflow.tasks[]` (and the same under `build.execution.orchestration`). See the [Cheatsheet](/fluid/schema/cheatsheet#orchestration-fields).

### 1.7 Access and governance

| Block | Shape |
|---|---|
| `accessPolicy` | Closed; `grants[]`, each closed with `principal` (required), `permissions` (`read`, `select`, `query`, `write`, `insert`, `update`, `delete`, `create`, `admin`, `manage`), `resources` (array of strings, e.g. JSONPath selecting exposes) and `conditions` (open object). |
| `sovereignty` | Closed: `jurisdiction`, `allowedRegions`, `deniedRegions`, `dataResidency` (boolean), `crossBorderTransfer` (boolean), `transferMechanisms`, `regulatoryFramework`, `enforcementMode` (`strict` \| `advisory` \| `audit`), `validationRequired`. |
| `exposes[].policy.agentPolicy` | Closed: `allowedModels`, `deniedModels`, `maxTokensPerRequest`, `maxTokensPerDay`, `allowedUseCases` / `deniedUseCases` (from `inference`, `reasoning`, `analysis`, `summarization`, `classification`, `embedding`, `search`, `qa`, `code_generation`, `fine_tuning`, `training`, `rag`), `canReason`, `canStore`, `retentionPolicy`, `auditRequired`, `purposeLimitation`. It exists only per expose, not at the root. |
| `governance.lakeFormation` | Closed: `admins` (IAM ARNs) and `tagDefinitions` (tag key → allowed values). `admins` is **authoritative**: applying it replaces the account's Lake Formation admin list. The schema's description adds that applying it also clears the account's create-database and create-table default permissions, trusted resource owners and parameters, and that destroying the emitted `aws_lakeformation_data_lake_settings` resource empties the admin list and resets `CROSS_ACCOUNT_VERSION` to 1. |

---

## Further reading

- [Anatomy](/fluid/schema/anatomy) — a guided tour of the blocks, with examples.
- [Cheatsheet](/fluid/schema/cheatsheet) — one row per field.
- [Changelog](/fluid/schema/changelog) — what changed in each version.
- *FLUID Data Products* (book) is [available on Amazon](https://amzn.eu/d/ikMlWNV).
