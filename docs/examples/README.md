# FLUID by Example — Eleven Steps from "Hello World" to Production

> All examples target **`fluidVersion: "0.7.4"`** (the [latest schema](/fluid/schema/fluid-schema-0.7.4.json)).
> Each example **adds one block** to the previous one. Read in order to learn the schema by accretion.
> For the schema's mental model first, see [**Anatomy**](/fluid/schema/anatomy).
> For a one-row-per-field lookup, see [**Cheatsheet**](/fluid/schema/cheatsheet).

---

## Table of Contents

| # | Example | What it adds |
|---|---|---|
| 1 | [Minimal valid contract](#_1-minimal-valid-contract) | the six required fields, nothing else |
| 2 | [Add a schema](#_2-add-a-schema) | `exposes[].contract.schema` |
| 3 | [Add data quality](#_3-add-data-quality) | `exposes[].contract.dq.rules` |
| 4 | [Add a build](#_4-add-a-build-embedded-sql) | `build` — embedded SQL |
| 5 | [Consume another product](#_5-consume-another-product) | `consumes` + `build.pattern: hybrid-reference` (dbt) |
| 6 | [Restrict access](#_6-restrict-access-with-accesspolicy) | `accessPolicy` |
| 7 | [Govern AI consumers](#_7-govern-ai-consumers-with-agentpolicy) | `agentPolicy` |
| 8 | [Pin to a jurisdiction](#_8-pin-to-a-jurisdiction-with-sovereignty) | `sovereignty` |
| 9 | [Define business semantics](#_9-define-business-semantics) | `exposes[].semantics` |
| 10 | [Source-aligned acquisition](#_10-source-aligned-acquisition) | `build.pattern: acquisition` |
| 11 | [Agent-consumable output port (MCP)](#_11-agent-consumable-output-port-mcp) | `exposes[].mcp` (⭐ 0.7.4) |

---

## 1. Minimal valid contract

> **Goal:** get a `.fluid.yml` that validates against v0.7.4 with the fewest possible lines.
> **New in this step:** the six required top-level keys (`fluidVersion`, `kind`, `id`, `name`, `metadata`, `exposes`) and the four required fields inside each expose (`exposeId`, `kind`, `contract`, `binding`).

```yaml
# 01-minimal.fluid.yml
fluidVersion: "0.7.4"
kind: DataProduct
id:   demo.bronze.hello_world
name: "Hello World"
metadata:
  owner: { team: data-platform }
exposes:
  - exposeId: hello
    kind: table
    contract:
      schema:
        - { name: id, type: STRING, required: true }
    binding:
      platform: local
      format:   parquet
      location: { path: "./hello.parquet" }
```

That's it. Everything else in this guide is opt-in.

> 💡 `contract` must define at least one of `schema` or `openapiRef` — an empty `contract: {}` fails validation. We use a one-column `schema` here.

---

## 2. Add a schema

> **Goal:** describe the columns of the exposed table.
> **New in this step:** `exposes[].contract.schema[]`.

```yaml
# 02-with-schema.fluid.yml
fluidVersion: "0.7.4"
kind: DataProduct
id:   demo.bronze.payments
name: "Raw Payments"
metadata:
  owner: { team: data-platform, email: data-platform@company.com }
  layer: Bronze
exposes:
  - exposeId: payment_events
    kind: table
    contract:
      schema:
        - { name: payment_id, type: STRING,  required: true,  description: "Unique payment id" }
        - { name: amount,     type: NUMERIC, required: true,  description: "Payment amount" }
        - { name: currency,   type: STRING,  required: true,  description: "ISO 4217 currency code" }
        - { name: created_at, type: TIMESTAMP, required: true }
    binding:
      platform: gcp
      format:   bigquery_table
      location: { project: company-data, dataset: bronze_finance, table: payments }
```

Why bother: every consumer (humans, BI tools, AI agents) now has a machine-readable contract for the columns they'll see.

---

## 3. Add data quality

> **Goal:** assert that certain quality conditions must hold for the data to be considered valid.
> **New in this step:** `exposes[].contract.dq.rules[]`.

```yaml
# 03-with-dq.fluid.yml
# ... (everything from example 2, plus:)
exposes:
  - exposeId: payment_events
    kind: table
    contract:
      schema:
        - { name: payment_id, type: STRING,  required: true }
        - { name: amount,     type: NUMERIC, required: true }
        - { name: currency,   type: STRING,  required: true }
      dq:
        rules:
          - id: positive_amount
            type: valid_values                          # type ∈ freshness | completeness | uniqueness | valid_values | accuracy | schema | anomaly_detection | drift_detection
            selector: "amount > 0"
            severity: error                             # severity ∈ info | warn | error | critical
          - id: known_currency
            type: valid_values
            selector: "currency IN ('USD','EUR','GBP','JPY')"
            severity: warn
          - id: freshness_15m
            type: freshness
            selector: created_at
            window: PT15M                               # ISO-8601 duration window
            severity: error
    binding:
      platform: gcp
      format:   bigquery_table
      location: { project: company-data, dataset: bronze_finance, table: payments }
```

DQ rules run as part of every build. `severity: error` fails the pipeline; `warn` annotates the run.

---

## 4. Add a build (embedded SQL)

> **Goal:** describe how the data actually gets produced.
> **New in this step:** the `build` block with `pattern: embedded-logic`.

```yaml
# 04-with-build.fluid.yml
# ... (everything from example 3, plus:)
build:
  pattern: embedded-logic
  engine:  sql
  properties:
    sql: |
      SELECT
        payment_id,
        amount,
        currency,
        created_at
      FROM raw_source.payments
      WHERE amount > 0
  execution:
    trigger:
      type: schedule                                # schedule | event | manual | dependency | dataset | schedule_and_dataset | timetable
      schedule: "0 * * * *"                         # cron expression (or named preset)
    retries:
      maxAttempts: 3
      backoffStrategy: exponential                  # fixed | exponential | linear
      initialDelay: PT60S                           # ISO-8601 duration
```

`embedded-logic` keeps the transformation in-file. For dbt-style references, use `hybrid-reference` (next example).

---

## 5. Consume another product

> **Goal:** depend on another FLUID product upstream, and reference a dbt model for the build.
> **New in this step:** `consumes[]` + `build.pattern: hybrid-reference`.

```yaml
# 05-customer-ltv.fluid.yml
fluidVersion: "0.7.4"
kind: DataProduct
id:   analytics.silver.customer_ltv
name: "Customer Lifetime Value"
metadata:
  owner: { team: analytics, email: analytics@company.com }
  layer: Silver

consumes:
  - productId: demo.bronze.payments        # from example 4
    exposeId:  payment_events
  - productId: crm.bronze.raw_customers
    exposeId:  customer_data
    versionConstraint: "^2.0.0"

exposes:
  - exposeId: customer_ltv
    kind: table
    contract:
      schema:
        - { name: customer_id,     type: STRING,  required: true, tags: [identifier] }
        - { name: total_spent,     type: NUMERIC, required: true }
        - { name: order_count,     type: INTEGER, required: true }
        - { name: avg_order_value, type: NUMERIC, required: true }
    binding:
      platform: gcp
      format:   bigquery_table
      location: { project: company-data, dataset: silver_analytics, table: customer_ltv }

build:
  pattern: hybrid-reference
  engine:  dbt
  repository: "github.com/acme/analytics-dbt"
  properties:
    model: customer_ltv                    # path within the dbt repo
```

Now the orchestrator can auto-build the DAG: `demo.bronze.payments` → `analytics.silver.customer_ltv`.

---

## 6. Restrict access with `accessPolicy`

> **Goal:** declare exactly who can read this product. The platform generates cloud IAM bindings from this block.
> **New in this step:** root-level `accessPolicy`.

```yaml
# 06-with-access.fluid.yml
# ... (everything from example 5, plus:)
accessPolicy:
  grants:
    - principal: "group:analytics-team@company.com"
      permissions: [read, select, query]
      resources:   ["$.exposes[?(@.kind=='table')]"]
    - principal: "serviceAccount:airflow@acme-prod.iam.gserviceaccount.com"
      permissions: [read, select]
      conditions:
        ipRanges: ["10.0.0.0/8"]
    - principal: "user:alice@company.com"   # individual grant — labels go in commit msg / PR, not the contract
      permissions: [read, select, query]
```

The `resources` field uses JSONPath to target subsets of `exposes` — useful when some ports are public and others are restricted. The schema's `accessPolicy.grants[]` block accepts only `principal`, `permissions`, `resources`, and `conditions` — keep ticket/audit context in your commit message or PR, not the contract.

---

## 7. Govern AI consumers with `agentPolicy`

> **Goal:** decide *whether* AI agents may read this product, *which models*, and *for what purposes*.
> **New in this step:** `agentPolicy` under `exposes[].policy.agentPolicy`.
> ⚠️ **Important shape note:** `agentPolicy` is **per-expose**, not top-level — it lives inside `exposes[].policy.agentPolicy`. (Some prior release notes show it at the root; the schema has never accepted it there.)

```yaml
# 07-with-agent-policy.fluid.yml
# ... (everything from example 6, plus inside the relevant expose:)
exposes:
  - exposeId: customer_ltv
    kind: table
    # ...contract, binding as before...
    policy:                                       # ← expose-level policy block
      authn: iam                                  # oidc | oauth2 | api_key | none | custom | iam | jwt
      authz:
        readers: ["group:analytics-team@company.com"]
      privacy:
        masking:                                  # schema uses column+strategy, not a `piiColumns` shortcut
          - { column: email, strategy: tokenize }
      agentPolicy:
        allowedModels:   [gpt-4, gpt-4-turbo, claude-3-opus, claude-3-sonnet]
        deniedModels:    [gpt-3.5-turbo]          # legacy, not approved for PII
        maxTokensPerRequest: 8192
        maxTokensPerDay:     500000
        # allowedUseCases / deniedUseCases use a CONTROLLED VOCABULARY — not free strings.
        # Valid values: inference | reasoning | analysis | summarization | classification |
        #               embedding | search | qa | code_generation | fine_tuning | training | rag
        allowedUseCases: [inference, qa, rag, summarization, analysis]
        deniedUseCases:  [training, fine_tuning]
        canReason: true
        canStore:  false                          # ephemeral processing only
        retentionPolicy: { maxRetentionDays: 0, requireDeletion: true }
        auditRequired: true                       # log all AI consumption (required for SOC2)
        purposeLimitation: "Customer-LTV analytics and retention modeling only."
```

This block is enforced by FLUID-aware AI gateways. An LLM request that doesn't match `allowedModels` ∧ `allowedUseCases` ∧ token quotas is rejected before it ever sees the data.

> 💡 **Custom business use-case names don't validate.** The schema enforces a fixed twelve-value vocabulary. Use `purposeLimitation` (free text) when you need to express something more specific like "Customer support chatbot only."

---

## 8. Pin to a jurisdiction with `sovereignty`

> **Goal:** enforce data residency — apply-time blocks any `binding` that would land data outside the allowed region.
> **New in this step:** root-level `sovereignty`.

```yaml
# 08-with-sovereignty.fluid.yml
# ... (everything from example 7, plus:)
sovereignty:
  jurisdiction: EU
  allowedRegions: [europe-west1, europe-west3, europe-west4]
  deniedRegions:  [us-central1, us-east1, asia-southeast1]
  dataResidency:  true
  crossBorderTransfer: false
  regulatoryFramework: [GDPR]
  enforcementMode: strict                         # strict (block apply) | advisory (warn) | audit (log only)
  validationRequired: true                        # CI fails if binding location violates
```

With `enforcementMode: strict` and `validationRequired: true`, contract-apply diff-checks every `binding.location` against `allowedRegions` and refuses to deploy mismatches. No more "we accidentally provisioned a PII table in us-east1."

---

## 9. Define business semantics

> **Goal:** give an LLM or BI tool the *business* meaning of the columns — so "What's our MRR?" returns the *correct* SQL, not an invented one.
> **New in this step:** `exposes[].semantics`.

```yaml
# 09-with-semantics.fluid.yml
fluidVersion: "0.7.4"
kind: DataProduct
id:   analytics.gold.orders_revenue
name: "Orders Revenue Semantic Model"
metadata:
  owner: { team: finance-data, email: finance-data@company.com }
  layer: Gold

exposes:
  - exposeId: orders
    kind: table
    contract:
      schema:
        - { name: order_id,     type: STRING,    required: true }
        - { name: customer_id,  type: STRING,    required: true }
        - { name: amount,       type: NUMERIC,   required: true }
        - { name: status,       type: STRING,    required: true }
        - { name: discount,     type: NUMERIC }
        - { name: completed_at, type: TIMESTAMP, required: true }

    semantics:
      name: orders_revenue_model
      description: "Canonical semantic model for revenue analytics."
      defaultAggTimeDimension: order_date

      entities:
        - { name: order,    type: primary, expr: order_id }
        - { name: customer, type: foreign, expr: customer_id }

      measures:
        - { name: order_amount,  agg: sum,            expr: amount,   description: "Sum of order amounts" }
        - { name: order_count,   agg: count_distinct, expr: order_id, createMetric: true }
        - { name: total_discount, agg: sum,           expr: discount }

      dimensions:
        - { name: order_date, type: time,        expr: completed_at, typeParams: { timeGranularity: day } }
        - { name: region,     type: categorical }

      metrics:
        - name: gross_revenue
          description: "Total value of completed orders."
          type: simple
          measure: order_amount
          filter: "status = 'completed'"
        - name: net_revenue
          description: "GAAP-compliant net revenue — completed orders minus discounts."
          type: derived
          inputMetrics: [gross_revenue, total_discount]
          expr: "gross_revenue - total_discount"
          owner: "finance-data@company.com"

    binding:
      platform: snowflake
      format:   snowflake_table
      location: { database: ANALYTICS, schema: GOLD, table: ORDERS }
```

Now an agent asked *"what is net revenue last quarter?"* reads the `net_revenue` metric definition and produces the canonically-correct SQL instead of guessing.

The shape mirrors **dbt MetricFlow** and **Snowflake Semantic Views** — portable across engines.

---

## 10. Source-aligned acquisition

> **Goal:** ingest an external system (Postgres CDC → Iceberg) as a first-class FLUID product, with delivery guarantees, schema-evolution semantics, DLP, and signed connector images.
> **New in this step:** `build.pattern: acquisition`.

```yaml
# 10-acquisition.fluid.yml
fluidVersion: "0.7.4"
kind: DataProduct
id:   crm.bronze.customers_cdc
name: "Customers CDC from Production Postgres"
description: "Source-aligned ingestion of the customers table from prod Postgres into the bronze Iceberg lake."
metadata:
  owner: { team: data-platform, email: data-platform@company.com }
  layer: Bronze

exposes:
  - exposeId: customers
    kind: table
    contract:
      schema:
        - { name: customer_id,  type: STRING,    required: true,  tags: [primary-key] }
        - { name: email,        type: STRING,    required: true,  sensitivity: tokenized }
        - { name: country,      type: STRING,    required: true }
        - { name: created_at,   type: TIMESTAMP, required: true }
        - { name: updated_at,   type: TIMESTAMP, required: true }
        - { name: _ingested_at, type: TIMESTAMP, required: true, description: "FLUID-emitted ingestion timestamp" }
      dq:
        rules:
          - { id: not_null_pk,  type: completeness, selector: "customer_id IS NOT NULL",         severity: error }
          - { id: valid_email,  type: valid_values, selector: "email RLIKE '^[^@]+@[^@]+\\.[^@]+$'", severity: warn }
          - { id: unique_pk,    type: uniqueness,   selector: customer_id,                       severity: error }
    policy:                                          # expose-level (sibling of contract), not inside contract
      authn: iam
      authz:
        readers: ["group:customer-success@company.com"]
      privacy:
        masking:
          - { column: email, strategy: tokenize }
      agentPolicy:                                   # per-expose location for AI/LLM governance
        allowedModels: [claude-3-opus, gpt-4-turbo]
        allowedUseCases: [inference, qa, rag, summarization]   # controlled vocab (not free strings)
        deniedUseCases:  [training, fine_tuning]
        canStore: false
        auditRequired: true
        purposeLimitation: "Customer-support context and analytics only — never for marketing targeting or credit decisions."
    binding:
      platform: aws
      format:   iceberg
      location: { bucket: acme-bronze, path: "crm/customers/" }
      icebergConfig:                                 # NB: icebergConfig.partitionSpec uses OBJECT form;
        writeVersion: 2                              #     acquisitionSink.partitionBy below uses STRING form
        fileFormat:   parquet
        partitionSpec: [ { sourceColumn: _ingested_at, transform: day } ]

build:
  pattern: acquisition                             # schema validates build.properties below as acquisitionPattern
  engine:  debezium                                # CDC engine
  capabilities: [cdc, schema_evolution, dlp_scan, at_least_once]

  properties:                                      # ← acquisitionPattern lives here
    source:
      kind: postgres
      mode: cdc
      cursor_field: updated_at
      connection:
        secretRef: "vault://pg-prod-readonly"      # URI form required (vault:// aws:// gcp:// azure:// env://)
      streams: [public.customers]
      watermark: { strategy: lsn }                 # Postgres LSN-based

    sink:
      format: iceberg
      catalog: glue
      partitionBy: ["day(_ingested_at)"]           # acquisitionSink uses STRING array (function-form)

    delivery:
      guarantee: at_least_once
      idempotencyKey: "${stream}|${lsn}"
      dlq:
        enabled: true
        sink: { format: parquet, location: "s3://acme-dlq/customers/" }
        maxRecordsBeforeAbort: 10000
        alertOn: [pii_classification_failed, schema_violation, quality_gate_failed]

    schemaEvolution:
      policy: evolve_safe                          # additive allowed, removals warn, type changes fail
      onAddedColumn:   include                     # include | warn | fail
      onRemovedColumn: warn                        # drop    | warn | fail
      onTypeChange:    fail                        # cast    | warn | fail

    preLand: [dlp_scan, tokenize_pii, quality_gate, emit_lineage_input]

    cost:
      budget:
        monthly: { rows: 50000000, bytes: "200GB", computeMinutes: 600 }
        onExceed: warn                             # warn | abort
      chargeback: { team: data-platform, costCenter: ENG-1407 }

    catalog:
      register: [datahub]
      documentation: auto

    concurrency:
      lock: { scope: product }                     # single in-flight run per product

    debezium:
      connector_class: io.debezium.connector.postgresql.PostgresConnector
      deployment: { mode: managed }                # Forge provisions via Helm
      image_signature:
        verifier: cosign                           # cosign is the only verifier today
        publicKey: "k8s://acme/cosign-pub"
        slsaProvenance: required                   # required | optional | disabled

orchestration:
  engine: airflow
  generateOnChange: true

# (agentPolicy is on the expose above, under exposes[].policy.agentPolicy)

sovereignty:
  jurisdiction: EU
  allowedRegions: [eu-west-1, eu-central-1]
  deniedRegions:  [us-east-1, us-west-2]
  regulatoryFramework: [GDPR]
  enforcementMode: strict                          # strict | advisory | audit
  validationRequired: true

accessPolicy:
  grants:
    - principal: "group:customer-success@company.com"
      permissions: [read, select]
    - principal: "serviceAccount:ml-platform@acme-prod.iam.gserviceaccount.com"
      permissions: [read, select]

retention:
  runState: P30D
  runLogs:  P90D
  lineage:  P365D
  dlq:      P180D

lifecycle:
  state: active
```

This single file expresses, end-to-end:

- **What** is published (Iceberg table, schema, DQ rules, PII treatment)
- **How** it's produced (Debezium CDC from prod Postgres, exactly-once intent, schema-evolution policy, DLP pre-land hooks, signed connector image)
- **Who** may read it (group + service-account grants, agent policy for AI)
- **Where** it may live (EU only, GDPR)
- **How long** operational artifacts stick around

A FLUID-aware platform takes this file, provisions the connector, registers it in DataHub, wires the orchestrator, applies the IAM bindings, and starts emitting OpenLineage events — all from this one contract.

---

## 11. Agent-consumable output port (MCP)

> **Goal:** publish an output port that an AI agent can describe, sample, and query directly — with governance enforced from the contract, not bolted on at the gateway.
> **New in this step:** `exposes[].mcp` (⭐ 0.7.4).

Adding an `mcp` block to an expose opts that output port into the **Fluid MCP gateway**. A tool such as `fluid mcp output-port serve` then surfaces the port to Claude Code, Cursor, or any MCP client, exposing `describe` / `sample` / `query` operations against the contract.

The contract below is `0.7.4`-valid and runs without cloud credentials (DuckDB over a local CSV):

```yaml
fluidVersion: "0.7.4"
kind: DataProduct
id: silver.demo.customer_segments_v1
name: Customer Segments (MCP demo)
description: |
  Reference contract for `fluid mcp output-port serve`. Backed by a
  small DuckDB-loaded CSV so the demo runs without cloud credentials.
  Drop into Claude Code / Cursor as an MCP server to see describe /
  sample / query in action.
domain: demo
metadata:
  layer: Silver
  owner:
    team: data-platform
    email: platform@example.com
  businessContext:
    domain: Customer
exposes:
  - exposeId: customer_segments
    title: Customer Segments
    kind: table
    version: "1.0.0"
    contract:
      schema:
        - name: customer_id
          type: STRING
          required: true
          sensitivity: cleartext
        - name: email
          type: STRING
          businessName: Email Address
          # `sensitivity: pii` makes the gateway redact this column's
          # VALUES (→ "[REDACTED-PII]") on every sample / query result
          # while keeping the column visible. The agent learns the field
          # exists but never sees a real address. No flag, no proxy —
          # governance is enforced from the contract.
          sensitivity: pii
        - name: segment
          type: STRING
          required: true
          businessName: Customer Segment
          businessDefinition: enterprise / smb / consumer
        - name: signup_date
          type: DATE
        - name: lifetime_value_usd
          type: FLOAT64
          businessName: Lifetime Value (USD)
    binding:
      platform: local
      format: csv
      location:
        # Relative to the directory that contains this contract.
        # `fluid mcp output-port serve` resolves the path against
        # the contract's parent directory by default.
        path: ./customers.csv
        table: customer_segments
    semantics:
      name: customer_segments
      measures:
        - name: customer_count
          agg: count_distinct
          expr: customer_id
        - name: total_ltv_usd
          agg: sum
          expr: lifetime_value_usd
      dimensions:
        - name: segment
          type: categorical
        - name: signup_date
          type: time
      metrics:
        - name: active_customers
          type: simple
          measure: customer_count
        - name: ltv_total
          type: simple
          measure: total_ltv_usd
    mcp:
      sampling:
        maxRows: 50
      classification:
        dataClass: internal
```

### What the `mcp` block does

- **`mcp.sampling.maxRows`** (integer ≥ 1, default `100`) — caps the number of rows any single `sample` / `query` response may return. Here it's lowered to `50`, so an agent calling `sample` never pulls back more than 50 rows regardless of what it asks for.
- **`mcp.classification.dataClass`** (`public` | `internal` | `confidential` | `restricted`) — declares the sensitivity tier of the port. The gateway uses it to decide which agents and use cases are allowed near the data and how responses are logged. `internal` means employees/approved agents, not the public.

### How governance is enforced at the gateway

The `mcp` block opts the port in; the actual *who/what/how* rules come from the same blocks you've already seen:

- **`policy.agentPolicy`** (Example 7) is enforced **at the gateway on every read**. `allowedModels` / `deniedModels` gate which LLM may call the port, and `allowedUseCases` / `deniedUseCases` gate why. A request that doesn't satisfy `allowedModels` ∧ `allowedUseCases` is rejected before any data is read.
- **Column-level `sensitivity`** drives **value redaction**. A column marked `sensitivity: pii` (like `email` above) has its *values* replaced with a redaction marker (e.g. `[REDACTED-PII]`) in every `sample` / `query` result, while the column itself stays visible — the agent learns the field exists but never sees a real address. `sensitivity: phi` is treated the same way for protected health information.

The result: an agent connected through the Fluid MCP gateway can explore the port's shape and semantics, run governed queries, and stay inside the contract's model/use-case/redaction guardrails — without a single flag or proxy outside the contract.

> See the [MCP how-to](/fluid/how-to/mcp) for the end-to-end agentic-access story, and the [0.7.4 release notes](/fluid/releases/0.7.4) for the full `exposes[].mcp` reference.

---

## Where to go from here

- [**Anatomy**](/fluid/schema/anatomy) — guided tour of every top-level block.
- [**Cheatsheet**](/fluid/schema/cheatsheet) — one-row-per-field lookup table.
- [**What's New**](/fluid/releases/) — auto-generated diffs between each version.
- [**Full Specification**](/fluid/schema/specification) — exhaustive field-by-field reference.
