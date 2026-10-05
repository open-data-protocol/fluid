# Schema Anatomy

A FLUID contract is one YAML file. This page walks **every top-level block** of the latest stable schema, **0.7.5**, in the order you'd typically author them, with a one-paragraph "what / when / why" for each and a link into the generated reference doc for the field-by-field details.

> 📋 If you just want a one-line-per-field table, see the [**Cheatsheet**](/fluid/schema/cheatsheet).
> 🟢 If you want a copy-pasteable minimal example, see the [**Minimal Valid Contract**](/fluid/schema/minimal-contract).
> 📚 Full field-by-field reference: [`specs/0.7.5/fluid-spec.html`](/fluid/specs/0.7.5/fluid-spec.html).
> 🧪 Blocks marked **0.7.6 preview** need `fluidVersion: "0.7.6"` and can still change — see [0.7.6 (preview)](/fluid/releases/0.7.6).

The YAML blocks on this page fit together: merged in order into the [minimal contract](/fluid/schema/minimal-contract), they form one contract that validates against the 0.7.5 schema.

---

## The mental model in one picture

```
┌────────────────────────── IDENTITY ──────────────────────────┐
│  fluidVersion  kind  id  name  description  domain           │
│  metadata { owner, layer, productType, businessContext }     │
│  tags  labels                                                │
└──────────────────────────────────────────────────────────────┘

┌────── INTERFACE (what you publish) ───────┐  ┌── INTAKE ────┐
│  exposes[]                                │  │  consumes[]  │
│    ├─ contract  (schema, dq, schemaPolicy)│  │              │
│    ├─ policy    (authz, privacy, agent…)  │  │              │
│    ├─ semantics (entities, measures, …)   │  │              │
│    ├─ mcp       (MCP gateway opt-in) ⭐0.7.4│ │              │
│    └─ binding   (platform, location, …)   │  │              │
└───────────────────────────────────────────┘  └──────────────┘

┌────── IMPLEMENTATION (how it's built) ───────────────────────┐
│  build { pattern, engine, properties, capabilities, … }      │
│    └─ acquisition (source-aligned ingestion)   ⭐ 0.7.3       │
│  orchestration { engine, airflow, … }  top-level ⭐ 0.7.2     │
└──────────────────────────────────────────────────────────────┘

┌────── GOVERNANCE (rules around the product) ─────────────────┐
│  sovereignty   (jurisdiction)            top-level   ⭐ 0.7.1 │
│  accessPolicy  (IAM grants)              top-level   ⭐ 0.7.1 │
│  retention     (data/log TTLs)           top-level   ⭐ 0.7.3 │
│  governance    (AWS Lake Formation)      top-level   ⭐ 0.7.3 │
│  exposes[].policy.agentPolicy (AI/LLM)   per-expose  ⭐ 0.7.1 │
│  lineage  schemaEvolution  observability                     │
└──────────────────────────────────────────────────────────────┘

┌────── LIFECYCLE & ENVIRONMENTS ──────────────────────────────┐
│  lifecycle { state }  environments { dev, staging, prod }    │
│  machineLearning { ... }   docs { ... }                      │
└──────────────────────────────────────────────────────────────┘

  0.7.6 preview adds: packaging, consumers[], consumes[].upstream*,
  binding.{encryption, principals, packaging}, lifecycle.expire
```

---

## 1. Identity: *who is this product?*

<!-- fluid-check: merge-into=minimal@0.7.5 -->
```yaml
fluidVersion: "0.7.5"           # required
kind: DataProduct               # required — DataProduct | MLPipeline
id:   finance.gold.customer_360 # required — globally unique, dot-separated
name: "Customer 360"            # required — display name
description: "Unified customer profiles across billing, support, and product."
domain: "Customer Experience"
tags:   [pii, gold-layer, customer-data]
labels: { team: customer-analytics, criticality: high, cost-center: engineering }
```

**What:** how the contract identifies itself in the data mesh.
**When:** always — `fluidVersion`, `kind`, `id`, `name` are required.
**Why:** the `id` is the join key for every catalog, lineage graph, and `consumes:` reference. Pick it carefully — it's the public address of this product forever.

---

## 2. `metadata`: *who owns it, where does it sit in the medallion?*

<!-- fluid-check: merge-into=prev -->
```yaml
metadata:                                            # required (only metadata.owner is required inside)
  owner:                                             # required — no member of owner is required by the schema
    team:  customer-analytics                        # name a team: tools route alerts and ownership by it
    email: customer-analytics@company.com
    slack: "#customer-analytics-eng"
  layer: Gold                                        # free-form string; convention: Bronze | Silver | Gold
  productType: CDP                                   # SDP | ADP | CDP (source-aligned, aggregated, consumption-aligned)
  businessContext:
    domain:    "Customer Experience"
    subdomain: "Customer Intelligence"
```

**What:** ownership and business context that doesn't fit in `id`.
**When:** always — `metadata` is required, and inside it only `owner` is. The schema requires no member of `owner`, so `owner: {}` validates; name at least a `team`.
**Why:** every alert, catalog page, and ownership audit traces back here. Without an `owner.email`, a broken product has no human to wake up.

> 💡 `metadata.layer` is a **free-form string** (not an enum). `Bronze`/`Silver`/`Gold` is the conventional medallion vocabulary, but the schema doesn't enforce it.

---

## 3. `consumes`: *what upstream products do I need?*

<!-- fluid-check: merge-into=prev -->
```yaml
consumes:
  - productId: finance.bronze.raw_payments
    exposeId: payment_events
  - productId: crm.silver.customer_master
    exposeId: customer_data
    versionConstraint: "^2.0.0"
```

**What:** explicit, version-constrained dependencies on other FLUID products.
**When:** any product that isn't strictly source-aligned (i.e. not `build.pattern: acquisition`).
**Why:** the orchestrator builds the DAG from `consumes`. No `consumes` → no automatic upstream waiting, no automatic lineage. Each entry can also state `qosExpectations` (`freshnessMax`, `maxStaleness`, `minCompleteness`) and `requiredPolicies`.

> 🧪 **0.7.6 preview:** `upstreamWorkspace` and `upstreamDigest` pin an upstream that lives in another mesh; setting the first requires the second. See [0.7.6](/fluid/releases/0.7.6#cross-mesh-pins-on-consumes).

---

## 4. `exposes`: *what does this product publish?*

This is the heart of the contract. A product can expose multiple ports (e.g. a Snowflake table **and** a Kafka stream **and** an API).

<!-- fluid-check: merge-into=prev -->
```yaml
exposes:
  - exposeId: customer_profiles                  # required
    kind: table                                  # required — table | view | api | file | stream | topic | feature_store | model | vector | graph | time_series | other
    description: "Unified customer profile records, refreshed nightly."
    version: "2.1.0"
    tags:   [pii, customer-facing]

    # ── 4a. CONTRACT ──────────────────────────────────────────
    contract:                                    # required on every expose; must define schema (or openapiRef)
      schema:
        - { name: customer_id, type: STRING,  required: true,  description: "Stable customer key", tags: [identifier, primary-key] }
        - { name: email,       type: STRING,  required: true,  sensitivity: tokenized }
        - { name: ltv,         type: NUMERIC, required: false, description: "Lifetime value in USD" }
      dq:
        rules:
          - id: ltv_non_negative
            type: valid_values                   # type ∈ freshness | completeness | uniqueness | valid_values | accuracy | schema | anomaly_detection | drift_detection
            selector: "ltv >= 0"
            severity: error                      # severity ∈ info | warn | error | critical
      schemaPolicy: evolve_safe                  # strict | discover_and_freeze | evolve_safe | evolve_all

    # ── POLICY — a sibling of contract, not inside it ─────────
    policy:
      authn:   iam
      authz:   { readers: [analytics-team, ml-agents] }
      privacy:
        masking:
          - { column: email, strategy: tokenize }

    # ── QoS ───────────────────────────────────────────────────
    qos:
      availability: "99.9%"                      # a percentage string
      freshnessSLO: PT1H                         # ISO-8601 durations
      latencyP95: PT2S

    # ── 4b. SEMANTICS (⭐ 0.7.2) ─────────────────────────────
    semantics:
      entities:
        - { name: customer, type: primary, expr: customer_id }
      measures:
        - { name: total_ltv, agg: sum, expr: ltv }
      dimensions:
        - { name: signup_month, type: time, expr: "DATE_TRUNC('month', created_at)" }
      metrics:
        - { name: avg_ltv_per_customer, type: ratio, numerator: total_ltv, denominator: customer_count }

    # ── 4c. MCP (⭐ 0.7.4) ─────────────────────────────────────
    mcp:                                         # presence opts this expose into the Fluid MCP gateway
      sampling: { maxRows: 100 }                 # hard cap for the `sample` tool (integer ≥1, default 100)
      classification: { dataClass: confidential }# public | internal | confidential | restricted

    # ── 4d. BINDING ───────────────────────────────────────────
    binding:
      platform: gcp                              # gcp | aws | azure | snowflake | databricks | kafka | confluent ⭐0.7.5 | local | kubernetes | postgres ⭐0.7.4 | pgvector ⭐0.7.5 | other
      format:   bigquery_table                   # bigquery_table | snowflake_table | iceberg | delta_table | parquet | http_api | kafka_topic | postgres_table ⭐0.7.4 | athena_table ⭐0.7.4 | glue_table ⭐0.7.4 | pgvector_table ⭐0.7.5 | …
      location: { project: company-data, dataset: gold_customer, table: profiles_v1, region: europe-west1 }
```

### `contract`: *the data shape and the rules around it*

- **`schema`**: columns, types, `required`, sensitivity (`cleartext` | `tokenized` | `pseudonymized` | `encrypted` | `pii` | …), tags.
- **`dq.rules`**: declarative data-quality assertions (`valid_values`, `freshness`, `completeness`, `uniqueness`, `accuracy`, `anomaly_detection`, `drift_detection`, `schema`).
- **`schemaPolicy`** (0.7.3+): how the output schema may change.

`contract` is closed: `policy` is **not** a member of it. Privacy treatments, readers/writers, column restrictions and the per-expose `agentPolicy` go in **`exposes[].policy`**, next to `contract` (see §7). `qos` states service levels for the port: `availability`, `freshnessSLO`, `dataLossSLO`, `latencyP95`, `completenessTarget`, `errorBudget`.

### `semantics` (0.7.2): *the business meaning layer*

`entities`, `measures`, `dimensions`, `metrics` — the same primitives as dbt MetricFlow and Snowflake Semantic Views. An LLM or BI tool reading this block can answer *"what is our MRR?"* without inventing SQL.

### `mcp` (0.7.4): *opt this expose into the MCP output-port gateway*

**What:** the `exposes[].mcp` block declares this expose as agent-consumable over MCP. Its two sub-blocks are `sampling.maxRows` (integer ≥1, default 100 — a hard cap on the `sample` tool so an over-curious agent can't pull petabyte-scale rows) and `classification.dataClass` (`public` | `internal` | `confidential` | `restricted` — an advisory hint surfaced on the `describe` tool so consumer agents can declare downstream handling).

**When:** any expose you want served through `fluid mcp output-port serve` and reachable by AI agents over MCP.

**Why:** the *presence* of a (non-empty) `mcp` block is what flips on runtime enforcement. Once present, the expose's `policy.agentPolicy` (`allowedModels` / `deniedModels`, `allowedUseCases` / `deniedUseCases`, token caps) is enforced **on every read** by an MCP gateway that implements 0.7.4 (the reference implementation's does) — where before those fields were declarative metadata only. The `agentPolicy` shape itself is unchanged from 0.7.3; 0.7.4 makes it a runtime gate.

> 🔗 See the [**MCP how-to**](/fluid/how-to/mcp) for an end-to-end walkthrough of serving an expose over MCP with governed agent access.

### `binding`: *where the data physically lives*

Platform + format + location. Plus `icebergConfig` (0.7.2+) when format is `iceberg` (write version, file format, `partitionSpec`, `sortOrder`), so the contract owns table-format details too. **0.7.4** adds the `postgres` platform and the `postgres_table` / `athena_table` / `glue_table` formats. **0.7.5** adds the `confluent` (Tableflow) and `pgvector` platforms, `pgvector_table`, `vectorConfig`, and location fields for Iceberg catalogs, Redshift Serverless and Kinesis — see [0.7.5](/fluid/releases/0.7.5). Optional `binding.governance` carries per-resource AWS Lake Formation settings.

> 🧪 **0.7.6 preview** adds `binding.encryption.kms`, `binding.principals` (logical principal → platform identity), `binding.packaging`, and Lake Formation `bucketPolicy`; a bucket policy it emits is **authoritative** and replaces every other statement on the bucket. See [0.7.6](/fluid/releases/0.7.6#binding-fields-encryption-principals-lake-formation-bucket-policy).

---

## 5. `build`: *how the product is produced*

Four patterns, validated conditionally:

| `pattern` | Use when |
|---|---|
| `hybrid-reference` | dbt-style: contract references a model in another repo. |
| `embedded-logic` | The SQL / Python / Spark code lives in the contract itself. |
| `multi-stage` | Multi-step pipeline (bronze → silver → gold) in one product. |
| `acquisition` ⭐ 0.7.3 | Source-aligned ingestion from external systems (Postgres, Salesforce, Kafka, files, …). |

<!-- fluid-check: merge-into=prev -->
```yaml
build:
  pattern: acquisition                         # ⭐ 0.7.3 — picks acquisitionPattern shape for build.properties below
  engine:  airbyte                             # dbt | dbt-<adapter> | sql | python | spark | glue | custom | duckdb | airbyte | meltano | dlt | kafka-connect | debezium
  capabilities: [incremental_dedup, schema_evolution, dlp_scan]
  properties:                                  # ← schema validates this as acquisitionPattern when pattern=acquisition
    source:
      kind: postgres
      mode: incremental_dedup                  # full_refresh | incremental_append | incremental_dedup | incremental_merge | cdc | streaming
      cursor_field: updated_at
      connection:
        secretRef: "vault://pg-prod-readonly"  # must be a URI (<scheme>://…), e.g. vault://, env://
      streams: [public.customers, public.orders]
    sink:
      format: bigquery_table                   # iceberg | delta | parquet | csv | json | snowflake_table | bigquery_table | redshift_table | duckdb_table
      partitionBy: ["day(ingested_at)"]        # array of strings (function-form) — not the object form of binding.icebergConfig.partitionSpec
    delivery:
      guarantee: at_least_once                 # at_most_once | at_least_once | exactly_once
      idempotencyKey: "${stream}|${batch_id}"
      dlq:
        enabled: true
        sink: { format: parquet, location: "s3://acme-dlq/customers/" }
        maxRecordsBeforeAbort: 10000
    schemaEvolution:
      policy: evolve_safe                      # strict | discover_and_freeze | evolve_safe | evolve_all
      onAddedColumn: include                   # include | warn | fail
      onRemovedColumn: warn                    # drop | warn | fail
      onTypeChange: fail                       # cast | warn | fail
    preLand: [dlp_scan, tokenize_pii, quality_gate, emit_lineage_input]
    airbyte:
      connector_image: airbyte/source-postgres
      image_signature:                         # ⭐ supply-chain trust
        verifier: cosign                       # cosign (only verifier today)
        publicKey: "k8s://acme/cosign-pub"
        slsaProvenance: required               # required | optional | disabled
      deployment: { mode: managed }            # embedded | bring-your-own | managed
```

> 🧭 **Where `acquisitionPattern` actually lives:** in the schema, `build.properties` is validated against a different shape depending on `build.pattern` (`hybrid-reference` → `hybridReferencePattern`, `embedded-logic` → `embeddedLogicPattern`, `multi-stage` → `multiStagePattern`, `acquisition` → `acquisitionPattern`). The pattern name is the discriminator; `properties` is always the payload key.

**When:** any product that is built rather than virtual. Use `build` for one build, or `builds[]` (each with an `id`) for several; both have the same shape.

---

## 6. `orchestration`: *who actually runs the build?*

<!-- fluid-check: merge-into=prev -->
```yaml
orchestration:
  engine: airflow                              # required — airflow | dagster | prefect | kubeflow | custom | none
  mode: generated                              # generated | manual | hybrid
  generateOnChange: true
  airflow:
    dagId: customer_360                        # required when airflow is present
    dagConfig: { schedule: "0 2 * * *", catchup: false }
    tasks:
      - taskId: ensure_warehouse
        type: provider_action                  # provider_action | fluid_validate | fluid_plan | fluid_apply | fluid_execute | fluid_verify | fluid_dq_check | bash | python | sensor | …
        operator: ProviderActionOperator
        provider: snowflake                    # aws | gcp | azure | snowflake | databricks | kafka | kubernetes | local | custom
        action: warehouse.ensure               # <service>.<action>
        params: { name: ANALYTICS_WH, size: medium }
      - taskId: load_customers
        type: provider_action
        operator: ProviderActionOperator
        provider: snowflake
        action: table.ensure
        params: { name: CUSTOMERS }
        buildStepRef: customers_ingest
        dependencies: [ensure_warehouse]
```

**What:** how the build is scheduled and run. The top-level `orchestration` key exists from 0.7.2; the same block can sit under `build.execution.orchestration` (from 0.7.1).
**Why:** the orchestrator config used to be the part most likely to drift from the contract. Embedding it keeps "what runs" and "what gets produced" in one file.

> ⚠️ **Only `orchestration.airflow.tasks[]` is checked.** `orchestration` is an open object, so a top-level `orchestration.tasks` list — which some FLUID tooling reads — is accepted with **no validation at all**: a typo in it is not reported. The key names in such a list are implementation-defined. In the reference implementation, the AWS and GCP code generators read `params` and `dependsOn` from `orchestration.tasks[]`, while its Snowflake Airflow generator reads `parameters`.
>
> Name each task's **`operator`**, as above. In the 0.7.1 to 0.7.6 schemas the conditional rules for `fluid_execute`, `bash` and `python` tasks also match a task that has no `operator`, so such a task must satisfy all three at once and is in practice rejected.

---

## 7. Governance: `sovereignty`, `accessPolicy`, `governance`, and `exposes[].policy.agentPolicy`

The agentic-era governance layer is mostly 0.7.1 (`sovereignty`, `accessPolicy`, `agentPolicy`), plus the top-level `governance` block (AWS Lake Formation, since 0.7.3; an unrelated `governance` block existed from 0.0.1 to 0.4.0 and was removed in 0.5.7). **Three blocks are top-level (`sovereignty`, `accessPolicy`, `governance`); `agentPolicy` is per-expose** — it lives inside `exposes[].policy.agentPolicy`, not at the root (earlier versions of the 0.7.1 release note showed it at the top level).

<!-- fluid-check: merge-into=prev -->
```yaml
sovereignty:                                   # ⭐ 0.7.1 — where data may live (top-level)
  jurisdiction: EU
  allowedRegions: [europe-west1, europe-west3]
  deniedRegions:  [us-central1]
  dataResidency:  true
  crossBorderTransfer: false
  regulatoryFramework: [GDPR, HIPAA]
  enforcementMode: strict                      # strict | advisory | audit
  validationRequired: true

accessPolicy:                                  # ⭐ 0.7.1 — IAM grants generated from this (top-level)
  grants:
    - principal: "group:data-analytics@company.com"
      permissions: [read, select, query]
      resources:   ["$.exposes[?(@.kind=='table')]"]   # JSONPath
    - principal: "serviceAccount:pipeline@project.iam.gserviceaccount.com"
      permissions: [write, insert, update]
      conditions:  { ipRanges: ["10.0.0.0/8"] }

governance:                                    # ⭐ 0.7.3 — account-wide AWS Lake Formation (top-level)
  lakeFormation:                               # admins + LF-tag definitions (per-resource grants live under binding.governance)
    admins:                                    # AUTHORITATIVE: replaces the account's admin list — see the warning below
      - "arn:aws:iam::123456789012:role/LakeAdmins"
      - "arn:aws:iam::123456789012:role/fluid-deployer"   # the role that runs the apply
    tagDefinitions:                            # tag key -> allowed values (emitted as aws_lakeformation_lf_tag)
      classification: [public, internal, confidential, restricted]

exposes:
  - exposeId: customer_profiles
    # ...
    policy:                                    # exposes[].policy is the expose-level governance block
      authn: iam                               # oidc | oauth2 | api_key | none | custom | iam | jwt
      authz: { readers: [analytics-team, ml-agents] }
      privacy:
        masking:                               # NOT `piiColumns` — the schema uses column+strategy rules
          - { column: email, strategy: tokenize }
          - { column: ssn,   strategy: hash }
      agentPolicy:                             # ⭐ 0.7.1 — who/what AI can read this expose
        allowedModels: [gpt-4, claude-3-opus]
        maxTokensPerRequest: 4096
        maxTokensPerDay: 100000
        # allowedUseCases / deniedUseCases use a CONTROLLED VOCABULARY — not free strings:
        # inference | reasoning | analysis | summarization | classification |
        # embedding | search | qa | code_generation | fine_tuning | training | rag
        allowedUseCases: [inference, qa, rag, summarization]
        deniedUseCases:  [training, fine_tuning]
        canReason:  false                      # allow chain-of-thought reasoning?
        canStore:   false                      # allow caching the data?
        retentionPolicy: { maxRetentionDays: 0, requireDeletion: true }
        auditRequired: true                    # log all AI consumption
        purposeLimitation: "Customer support chatbot only — not for marketing."
```

**Why:** the contract becomes the source of truth for compliance reviewers, and drift between "what the contract says" and "what IAM bindings exist" becomes checkable.

::: danger `governance.lakeFormation.admins` replaces the admin list
`admins` is **authoritative, not additive**. Applying it sets the account's Lake Formation admins to exactly this list, so any admin you do not list is **removed** — including the role or user that runs the apply, after which Lake Formation grants and registrations that need an admin can fail. List every principal that must stay an admin, the deploying identity included. (The 0.7.3–0.7.5 schemas were first published with a description saying the opposite; see the [Changelog](/fluid/schema/changelog#corrections-to-published-schemas).) In the reference implementation, applying this block also clears the account's other data-lake settings that it does not set: the create-database and create-table default permissions, trusted resource owners and parameters. Destroying the emitted `aws_lakeformation_data_lake_settings` resource empties the admin list and resets `CROSS_ACCOUNT_VERSION` to 1. See the field's description in the [schema](/fluid/specs/0.7.5/fluid-spec.html).
:::

> 🧪 **0.7.6 preview** adds `binding.principals`, which maps the logical principals named in `accessPolicy` and `columnRestrictions` to each platform's identities, writes down what `columnRestrictions` means (deny beats allow; a restriction never grants access), and adds typed masking `params`. See [0.7.6](/fluid/releases/0.7.6).

> ⭐ **0.7.4 — runtime enforcement.** When an expose also carries an [`mcp` block](#mcp-0-7-4-opt-this-expose-into-the-mcp-output-port-gateway), the `agentPolicy` above stops being passive metadata: an MCP gateway that implements 0.7.4, such as the reference implementation's, enforces `allowedModels` / `deniedModels` and `allowedUseCases` / `deniedUseCases` on every read. The `agentPolicy` shape is unchanged — 0.7.4 only changes *when* it bites.

---

## 8. `retention` (0.7.3): *TTLs for everything around the product*

<!-- fluid-check: merge-into=prev -->
```yaml
retention:                                     # ISO-8601 durations; defaults shown
  runState: P30D
  runLogs:  P90D
  lineage:  P365D
  dlq:      P180D
```

**What:** how long the platform retains operational records — run state, run logs, lineage events, dead-letter records. It does not govern the product's data; that is `lifecycle.retention`.
**Why:** before 0.7.3 these knobs were scattered across tools. One block in the contract states them once.

---

## 9. `lineage`, `schemaEvolution`, `observability`, `machineLearning`, `environments`, `lifecycle`, `docs`

These are the deeper-cut blocks — every one is opt-in:

- **`lineage`** — `granularity` (`table_level` | `field_level`), `upstream[]` (with optional `fieldMappings`) and `downstream[]`.
- **`schemaEvolution`** — `strategy` (`semantic_versioning` | `date_based` | `sequential`), `compatibility` (`backward_compatible` | `forward_compatible` | `full_compatible` | `breaking`) and `changePolicy`.
- **`observability`** (per expose) — `metrics`, `onBreach` actions, `defaultSLIs`, and (0.7.3+) `alert` channels.
- **`machineLearning`** — `enabled`, `framework` (`mlflow` | `kubeflow` | `sagemaker` | `vertex_ai` | `custom`), `models[]`.
- **`environments`** — per-environment overrides of `metadata` and `exposes`.
- **`lifecycle`** — `state: preview | active | deprecated | retired`, `retention` (an ISO-8601 duration) and `deprecationPolicy` (`noticePeriod`, `contact`, `replacement`). Note that `preview` here is a *product's* state; it has nothing to do with preview *schema versions*. 🧪 In the 0.7.6 preview, an expose's `lifecycle` also takes `expire: true`, which deletes data older than `retention`.
- **`docs`** — `homepage`, `runbook`, `dictionary`, `changeLog`.

For the field-by-field detail on each, see the generated reference: [`specs/0.7.5/fluid-spec.html`](/fluid/specs/0.7.5/fluid-spec.html).

---

## Reading order recommendation

If you've never written a FLUID contract:

1. Skim §1–§4 here (identity → metadata → consumes → exposes).
2. Copy the [Minimal Valid Contract](/fluid/schema/minimal-contract) and run it.
3. Walk through the [**Examples**](/fluid/examples/) — each example adds one block from this anatomy until you reach a production-grade source-aligned acquisition product.
4. Use the [**Cheatsheet**](/fluid/schema/cheatsheet) as a lookup table when you're authoring.
5. Drop into the generated [`fluid-spec.html`](/fluid/specs/0.7.5/fluid-spec.html) for exact types and enums.
