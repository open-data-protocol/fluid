
<p align="center">
  <img src="./logo.png" width="400" alt="FLUID Logo"/>
</p>

# Federated Layered Unified Interchange Definition (FLUID)

> **The open, declarative standard for Data Products.**  
> FLUID provides the foundational protocol for building trustworthy, governable, and scalable data ecosystems—ready for the agentic era.

**Quick Start:**
- 🧭 [**FLUID at a Glance**](#-fluid-at-a-glance) — one screen, every top-level block, version-stamped
- 🟢 [**Minimal Valid Contract**](#-minimal-valid-contract) — smallest file that validates
- 📖 [FLUID Specification](https://github.com/open-data-protocol/fluid/blob/main/specification.md)
- 🔗 [JSON Schema v0.7.3 (latest)](https://github.com/open-data-protocol/fluid/blob/main/schema/fluid-schema-0.7.3.json) · [v0.7.2](https://github.com/open-data-protocol/fluid/blob/main/schema/fluid-schema-0.7.2.json) · [v0.7.1](https://github.com/open-data-protocol/fluid/blob/main/schema/fluid-schema-0.7.1.json)
- 📚 [Schema Anatomy](docs/anatomy.md) · [Schema Cheatsheet](docs/schema-cheatsheet.md)
- 🚀 [Examples in Action](https://github.com/open-data-protocol/fluid/blob/main/examples.md)
- 🤝 [Contributing Guide](https://github.com/open-data-protocol/fluid/blob/main/contribute.md)
- 🆕 [What's New in v0.7.3](#-whats-new-in-fluid-073) · [v0.7.2](#-whats-new-in-fluid-072) · [v0.7.1](#-whats-new-in-fluid-071)

---

## 🧭 FLUID at a Glance

A FLUID contract is one YAML file. The shape below shows **every top-level block** in v0.7.3, with one-line meaning and the version each was introduced. Required blocks are marked `[req]`; everything else is opt-in.

```yaml
fluidVersion: "0.7.3"            # [req] which contract version this file targets
kind: DataProduct                # [req] DataProduct | MLPipeline
id:   domain.layer.name          # [req] globally unique product id
name: "Human-readable name"      # [req] display name
description: "..."               #       business-facing summary
domain: "Finance"                #       owning business domain
tags:   [pii, gold-layer]        #       free-text categorization
labels: { team: analytics }      #       key/value categorization

metadata:                        # [req] only metadata.owner is required
  owner: { team, email }         # [req] team is the one truly required field
  layer: Gold                    #       free-form; convention: Bronze | Silver | Gold

consumes: [ ... ]                #       upstream FLUID products you depend on
exposes:  [ ... ]                # [req] ports you publish (each requires exposeId+kind+contract+binding)
  └── contract                   # [req] schema columns (or openapiRef), dq rules
  └── semantics                  #         ⭐ 0.7.2 — entities, measures, dimensions, metrics
  └── policy                     #         authn, authz, privacy, classification, agentPolicy (⭐ 0.7.1)
  └── binding                    # [req] where it lives (platform + format + location, + icebergConfig*)

build:                           #       how the product is produced
  pattern: hybrid-reference      #       | embedded-logic | multi-stage | acquisition (⭐ 0.7.3)
  engine:  dbt | sql | python | spark | glue | custom | duckdb | airbyte | meltano | dlt | kafka-connect | debezium
  properties: { ... }            #       pattern-specific block — acquisitionPattern when pattern=acquisition (⭐ 0.7.3)

orchestration: { engine: airflow | dagster | prefect | kubeflow | custom | none, tasks: [...] }   # ⭐ 0.7.0+
sovereignty:   { jurisdiction, allowedRegions, deniedRegions, enforcementMode, … }   # ⭐ 0.7.1
accessPolicy:  { grants: [{ principal, permissions, resources, conditions }] }       # ⭐ 0.7.1
retention:     { runState, runLogs, lineage, dlq }                                   # ⭐ 0.7.3
lineage:       { upstream, downstream, fieldLevel }
governance:    { ... }
schemaEvolution: { strategy, compatibility }
machineLearning: { ... }
environments:  { dev: {...}, staging: {...}, prod: {...} }
lifecycle:     { state: preview | active | deprecated | retired }
docs:          { ... }
```

> 💡 **`agentPolicy` location.** AI/LLM consumption policy lives **per-expose** under `exposes[].policy.agentPolicy` — not at the root. (Earlier release notes show it at the top level; the schema has never accepted it there.) See [docs/anatomy.md §7](docs/anatomy.md) for the correct shape.

> 📚 For a one-line-per-field reference with required/optional flags, see the [**Schema Cheatsheet**](docs/schema-cheatsheet.md).
> For a tour of each block with deep-dive links, see the [**Schema Anatomy**](docs/anatomy.md).

---

## 🟢 Minimal Valid Contract

The smallest file that passes JSON Schema validation against v0.7.3 — every other top-level block is opt-in:

```yaml
fluidVersion: "0.7.3"
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

> **What you can drop:** `description`, `domain`, `tags`, `labels`, `consumes`, `build`, `orchestration`, all governance blocks (`agentPolicy`, `sovereignty`, `accessPolicy`, `retention`), `lineage`, `lifecycle`, `environments`, `docs`. Everything else is layered on as you need it.

See [**examples.md**](examples.md) for the ten-step progression from this minimal file to a production source-aligned acquisition product.

---

## Comparison with Open Data Product Specification (ODPS) v4.0

While both FLUID and ODPS aim to standardize data product specifications, they represent fundamentally different paradigms for data management:

### Philosophy & Approach
- **FLUID**: **DataOps-native** approach emphasizing compliance-as-code, automated governance, and infrastructure-first data engineering
- **ODPS**: Business-first approach emphasizing data marketplace operations and commercial exchange

### Core Purpose
- **FLUID**: Enable **end-to-end data product lifecycle automation** with embedded compliance, quality, and governance from inception
- **ODPS**: Facilitate data product discovery, pricing, and commercial exchange between organizations

### Architecture Philosophy

#### FLUID: Compliance-as-Code + DataOps Excellence
- **Single Source of Truth**: All governance, quality, lineage, and access policies embedded in version-controlled `.fluid.yml`
- **Proactive Compliance**: Governance enforced at build-time, not bolt-on post-deployment
- **Infrastructure Automation**: Native CI/CD integration with GitOps workflows
- **Developer-Centric**: Engineers define compliance rules alongside code, ensuring alignment

#### ODPS: Business Operations + Marketplace Focus
- **Separation of Concerns**: Business metadata separate from technical implementation
- **Reactive Governance**: Quality and SLA monitoring applied after deployment
- **Commercial Operations**: Built for data monetization and external sales
- **Business-Centric**: Product managers define commercial terms separately from technical teams

### DataOps & Compliance Advantages: FLUID vs ODPS

| **DataOps Capability** | **FLUID v0.5.7** | **ODPS v4.0** | **FLUID Advantage** |
|------------------------|-------------------|----------------|---------------------|
| **Compliance-as-Code** | ✅ **Native**: Quality rules, policies, lineage embedded in specification | ⚠️ **External**: Requires separate DQ tools and monitoring systems | **Unified compliance** reduces tool sprawl and config drift |
| **GitOps Integration** | ✅ **Native**: Version-controlled `.fluid.yml` drives entire lifecycle | ⚠️ **Manual**: Business metadata managed separately from code | **Automated deployments** with compliance validation |
| **Developer Experience** | ✅ **Streamlined**: Single file defines data product + governance | ⚠️ **Complex**: Multiple systems for business vs technical concerns | **Faster development** with embedded governance |
| **Environment Promotion** | ✅ **Automated**: Same `.fluid.yml` works across dev/staging/prod | ⚠️ **Manual**: Business configs need separate environment management | **Consistent governance** across environments |
| **Change Management** | ✅ **Integrated**: Schema evolution + quality rules versioned together | ⚠️ **Fragmented**: Technical and business changes managed separately | **Atomic updates** prevent configuration skew |
| **Audit Trail** | ✅ **Complete**: Full lineage from source to governance in git history | ⚠️ **Partial**: Technical changes tracked separately from business rules | **Comprehensive audit** for compliance teams |
| **Testing Strategy** | ✅ **Holistic**: Data quality + business logic tested together | ⚠️ **Split**: Technical tests separate from business validation | **Higher confidence** in production deployments |
| **Rollback Capability** | ✅ **Atomic**: Entire data product + governance rolled back as unit | ⚠️ **Complex**: Technical and business rollbacks require coordination | **Safer operations** with unified rollback |

### Key Differentiators Favoring FLUID

| Feature | FLUID v0.5.7 | ODPS v4.0 | **Why FLUID Wins** |
|---------|--------------|-----------|---------------------|
| **Build Automation** | ✅ **Comprehensive**: dbt, Airflow, Python, multi-stage orchestration | ❌ **None**: No pipeline automation capabilities | **End-to-end automation** reduces operational overhead |
| **Compliance-as-Code** | ✅ **Native**: Quality, lineage, policies embedded in spec | ⚠️ **External**: Requires integration with separate DQ tools | **Unified governance** prevents compliance drift |
| **DataOps Workflows** | ✅ **Native**: GitOps, CI/CD, environment promotion built-in | ❌ **Manual**: No workflow automation | **Faster, safer deployments** with automated validation |
| **Schema Evolution** | ✅ **Managed**: Built-in schema versioning and compatibility rules | ⚠️ **Manual**: No automated schema management | **Reduced breaking changes** with automated compatibility checks |
| **Dependency Management** | ✅ **Explicit**: Formal `consumes` relationships with version constraints | ⚠️ **Informal**: Only recommendation links between products | **Reliable data lineage** prevents upstream breakage |
| **AI/ML Integration** | ✅ **Native**: ML pipelines, feature stores, model deployment patterns | ⚠️ **Limited**: Basic AI agent access via MCP | **Complete ML lifecycle** support for modern data teams |
| **Developer Velocity** | ✅ **High**: Single file defines entire data product lifecycle | ⚠️ **Fragmented**: Multiple systems and specifications to manage | **Faster iteration** with unified development experience |
| **Operational Excellence** | ✅ **Proactive**: Issues prevented through design-time validation | ⚠️ **Reactive**: Problems discovered after deployment | **Higher reliability** with shift-left quality approach |

### Enterprise Benefits: Why DataOps Teams Choose FLUID

#### 🚀 **Accelerated Development Velocity**
- **Single specification** eliminates context switching between business and technical tools
- **Embedded governance** removes compliance bottlenecks from development cycle
- **Automated deployments** with built-in quality gates reduce manual toil

#### 🛡️ **Enhanced Compliance & Governance**
- **Compliance-as-code** makes governance requirements explicit and testable
- **Version-controlled policies** provide complete audit trails for regulatory requirements
- **Proactive validation** prevents non-compliant data products from reaching production

#### 📈 **Operational Excellence**
- **Unified monitoring** of technical and business metrics from single specification
- **Atomic updates** eliminate configuration drift between environments
- **Comprehensive lineage** enables rapid impact analysis for changes

#### 🤖 **AI-Ready Architecture**
- **Native ML support** for modern data teams building intelligent products
- **Contract-driven development** enables reliable AI agent integration
- **Feature store patterns** built into the specification

### When to Choose Each Approach

#### **Choose FLUID v0.5.7 for:**
- ✅ **DataOps transformation** initiatives
- ✅ **Compliance-heavy industries** (finance, healthcare, government)
- ✅ **Engineering-led data teams** prioritizing automation
- ✅ **AI/ML-centric** organizations building intelligent products
- ✅ **Internal data products** requiring tight governance

#### **Choose ODPS v4.0 for:**
- ✅ **Data marketplace** operations
- ✅ **Commercial data sales** with complex pricing models
- ✅ **Business-led** data product organizations
- ✅ **External data distribution** requiring legal frameworks
- ✅ **Multi-vendor ecosystems** needing business standardization

### Where ODPS Excels: Intentional Design Boundaries

FLUID's focused scope is a **deliberate design decision**. Rather than trying to be everything to everyone, FLUID concentrates on what it does best—DataOps and technical governance—while acknowledging where ODPS provides superior capabilities:

#### 🎯 **ODPS's Domain of Excellence**

**Commercial Data Operations:**
- **Sophisticated pricing models**: 12 standardized pricing patterns with payment gateway integration
- **Legal framework management**: Comprehensive licensing, IPR, and contract governance
- **Multi-stakeholder governance**: Business process workflows with detailed lifecycle states
- **Marketplace operations**: Product catalogs, payment processing, and customer relationship management

**Business-Oriented Data Products:**
- **Rich business metadata**: Value propositions, use cases, brand management, and marketing content
- **Multi-language support**: ISO 639-1 compliant internationalization for global data products
- **Access diversity**: Multiple consumption patterns (API, file, SQL, AI agents) per single product
- **SLA sophistication**: 11 monitoring dimensions with enterprise tool integrations (SodaCL, Montecarlo, DQOps)

#### 🎯 **FLUID's Intentional Boundaries**

**What FLUID Deliberately Doesn't Do:**
- ❌ **Commercial operations**: No pricing, billing, or payment processing
- ❌ **Legal frameworks**: No licensing or IPR management
- ❌ **Marketing metadata**: No brand slogans, value propositions, or sales content
- ❌ **Multi-language UIs**: English-first specification for technical teams

**Why These Are Design Choices, Not Limitations:**

1. **Focus Drives Excellence**: By concentrating on DataOps and technical governance, FLUID delivers deeper automation and better developer experience in its domain

2. **Tool Ecosystem Integration**: FLUID is designed to work *with* existing business systems, not replace them. Your data products can use FLUID for technical implementation while leveraging other tools for commercial operations

3. **Separation of Concerns**: Technical teams need different abstractions than business teams. FLUID optimizes for engineering workflows while remaining compatible with business-oriented specifications

4. **Evolutionary Architecture**: Organizations can start with FLUID for technical governance and later add ODPS for commercial operations as they mature their data product strategy

#### 🤝 **Intentional Compatibility: The Hybrid Approach**

FLUID's design explicitly enables **complementary coexistence** with business-focused specifications:

```yaml
# FLUID: Technical implementation and governance
fluidVersion: "0.7.1"
kind: "DataProduct"
id: "analytics.gold.customer_segments"

# NEW in v0.7.1: AI model governance
agentPolicy:
  allowedModels: ["gpt-4", "claude-3-opus"]
  maxTokensPerRequest: 4096

# Technical contract and automation
exposes:
  - exposeId: "segments_api"
    kind: "api"
    contract:
      # Reference to ODPS business specification
      businessMetadata: "./customer-segments-odps.yaml"
      # FLUID handles technical contract
      schema: [...]
      dq: [...]
    binding:
      platform: "kubernetes"
      format: "http_api"

# FLUID handles build automation
build:
  engine: "python"
  pattern: "embedded-logic"
  # ... technical implementation details
```

```yaml
# ODPS: Business packaging and commercialization  
# File: customer-segments-odps.yaml
schema: https://opendataproducts.org/v4.0/schema/odps.yaml
version: 4.0
product:
  details:
    en:
      name: "Customer Segmentation Analytics"
      valueProposition: "AI-powered customer segments for personalized marketing"
      # ... business metadata
  
  pricingPlans:
    declarative:
      en:
        - name: "Professional API Access"
          price: 299
          # ... commercial details
          
  # Reference back to FLUID technical implementation
  dataAccess:
    api:
      accessURL: "https://api.company.com/segments"  # ← Deployed by FLUID
      specsURL: "./fluid-generated-openapi.yaml"     # ← Generated by FLUID
```

#### 🏗️ **Strategic Design Philosophy**

**FLUID's "Do One Thing Well" Approach:**
- **Technical Excellence**: Deep automation capabilities for data engineering teams
- **Ecosystem Friendly**: Designed to integrate with, not replace, existing business tools
- **Evolutionary Path**: Start with FLUID for technical governance, add business layers as needed

**The Result: Best of Both Worlds**
- Use **FLUID** for rapid development, automated compliance, and technical governance
- Use **ODPS** for commercial operations, legal frameworks, and business metadata
- **Combine them** for enterprises needing both technical excellence and business operations

This architectural approach allows organizations to:
✅ **Start fast** with FLUID's engineering-focused approach  
✅ **Scale commercially** by adding ODPS business layers  
✅ **Avoid vendor lock-in** through specification compatibility  
✅ **Optimize teams** by matching tools to team responsibilities  

### The FLUID Advantage: DataOps Excellence

FLUID represents the **evolution of data engineering** from reactive, tool-specific configurations to **proactive, unified specifications**. By embedding compliance, quality, and governance directly into the data product definition, FLUID enables organizations to achieve:

- **Higher velocity** through automated compliance validation
- **Better reliability** through design-time quality enforcement
- **Reduced complexity** through unified specifications
- **Enhanced auditability** through version-controlled governance

In an era where **data governance is becoming a competitive advantage**, FLUID provides the foundation for building trustworthy, scalable, and compliant data ecosystems ready for both human and AI consumption.

---

## 🚀 What's New in FLUID 0.7.3

**FLUID 0.7.3** is the **Source-Aligned Acquisition** release. It is **additive** over v0.7.2 — every existing contract remains valid — and finally makes *ingestion from external systems* a first-class FLUID concept rather than something you bolt on with Airbyte/Meltano configs outside the contract.

### 🛬 `acquisition` build pattern (NEW)

The `build` block gains a fourth pattern, `acquisition`, designed for source-aligned data products: contracts that *ingest* an external system (Salesforce, Postgres, Kafka, files, …) into your mesh, with no transformation logic.

```yaml
build:
  pattern: acquisition            # tells the schema that build.properties below is an acquisitionPattern
  engine: airbyte                 # see "Six engines" below
  capabilities: [incremental_dedup, schema_evolution, dlp_scan]
  properties:                     # ← pattern-specific block; acquisitionPattern shape
    source:
      kind: postgres              # filesystem | postgres | mysql | http | salesforce | stripe | …
      mode: incremental_dedup     # full_refresh | incremental_append | incremental_dedup | incremental_merge | cdc | streaming
      cursor_field: updated_at
      connection:
        secretRef: "vault://pg-prod-readonly"   # must be a URI: vault:// aws:// gcp:// azure:// env://
      streams: [public.customers, public.orders]
    sink:
      format: iceberg             # iceberg | delta | parquet | snowflake_table | bigquery_table | …
      partitionBy: ["day(ingested_at)"]    # function-form strings (acquisitionSink uses strings; binding.icebergConfig uses objects)
    delivery:
      guarantee: at_least_once    # at_most_once | at_least_once | exactly_once
      idempotencyKey: "${stream}|${batch_id}"
      dlq:
        enabled: true
        sink: { format: parquet, location: "s3://acme-dlq/customers/" }
        maxRecordsBeforeAbort: 10000
        alertOn: [pii_classification_failed, schema_violation, quality_gate_failed]
    schemaEvolution:
      policy: evolve_safe         # strict | discover_and_freeze | evolve_safe | evolve_all
      onAddedColumn: include      # include | warn | fail
      onRemovedColumn: warn       # drop | warn | fail
      onTypeChange: fail          # cast | warn | fail
    preLand: [dlp_scan, tokenize_pii, quality_gate, emit_lineage_input]
    airbyte:
      connector_image: airbyte/source-postgres
      version: "3.4.10"
      image_signature:            # ⭐ supply-chain security
        verifier: cosign          # cosign is the only verifier today
        publicKey: "k8s://acme/cosign-pub"
        slsaProvenance: required  # required | optional | disabled
      deployment: { mode: managed }    # embedded | bring-your-own | managed
```

**Why this matters:** ingestion is where most data-quality, compliance, and lineage debt is born. Previously a `.fluid.yml` could describe how data was *transformed* but stayed silent on how it *arrived*. v0.7.3 closes that gap with the same contract-as-code discipline applied to the source boundary.

### 🔌 Six ingestion engines

| Engine | Best for | Footprint |
|---|---|---|
| **duckdb** | files (Parquet/CSV/JSON), JDBC, zero infra | in-process |
| **airbyte** | 350+ SaaS connectors | container |
| **meltano** | 600+ Singer taps, Python ecosystem | container |
| **dlt** | Python-native, code-defined pipelines | library |
| **kafka-connect** | streaming, Confluent ecosystem | cluster |
| **debezium** | change data capture (CDC) | cluster |

### 🏗️ Three deployment modes

- **`embedded`** — runs in-process with the FLUID runner (no extra infra)
- **`bring-your-own`** — points at an existing Airbyte/Meltano/Kafka server you already operate
- **`managed`** — Forge provisions runtime via Helm / Docker Compose / OpenTofu

### 🤝 Capability-based negotiation

Runners publish what they can do (`full_refresh`, `incremental_dedup`, `cdc`, `schema_discovery`, `dlp_scan`, `exactly_once`, …). The contract publishes what it *asks* for via `build.capabilities`. The orchestrator validates ask ⊆ declarations before scheduling — incompatible source/runner pairs fail fast at contract apply, not at 3 AM in production.

### 📐 Schema evolution as a first-class policy

`schemaEvolution.policy` has four well-defined values:

| Policy | Behavior |
|---|---|
| `strict` | any schema change at source aborts the run |
| `discover_and_freeze` | discover schema on first run, lock it thereafter |
| `evolve_safe` | additive changes propagate; type changes / removals require approval |
| `evolve_all` | propagate everything (with full lineage) |

### 🚚 Delivery guarantees + DLQ

`delivery.guarantee` makes the contract honest about what the runner can promise: `at_most_once`, `at_least_once`, or `exactly_once`. Pair it with `idempotencyKey` (a template like `"${stream}|${batch_id}"`) and a `dlq` destination, and re-runs become safe by construction.

### 🔐 Source supply-chain security

For production-grade ingestion, the connector image you run is part of the data supply chain:

```yaml
airbyte:
  image_signature:
    verifier: cosign                              # signature verifier (cosign only today)
    publicKey: "k8s://acme/cosign-pub"            # public-key reference
    slsaProvenance: required                      # required | optional | disabled
```

### 🧹 Top-level `retention` block

```yaml
retention:
  runState: P30D     # ISO-8601 durations
  runLogs:  P90D
  lineage:  P365D
  dlq:      P180D
```

A single sweeper job honors these — no more per-tool TTL knobs scattered across the stack.

### 🔄 100% Backward Compatible with v0.7.2

- ✅ No breaking changes
- ✅ `acquisition`, `retention`, `build.capabilities`, and the six new engines are all opt-in
- ✅ All v0.7.2 semantics + v0.7.1 agentPolicy/sovereignty/accessPolicy fully preserved

**Migration:**
```yaml
fluidVersion: "0.7.3"  # was "0.7.2" — that's it
```

See [schema-diffs/diff-0.7.2-to-0.7.3.md](schema-diffs/diff-0.7.2-to-0.7.3.md) for the full auto-generated change list.

---

## 🚀 What's New in FLUID 0.7.2

**FLUID 0.7.2** is the **Semantic Truth Engine** release. It is **additive** over v0.7.1 — every v0.7.1 contract remains valid unchanged — and completes the agentic contract: *agentPolicy* decides **whether** an AI agent may act on a data product, and *semantics* tells it **how to act correctly**.

### 🧠 Semantic Model (NEW)

Each `exposes[]` entry now accepts an optional `semantics` block that maps physical columns to business concepts — entities, measures, dimensions, and metrics — in a form agents and BI tools can reason about without re-deriving KPIs.

```yaml
# NEW in v0.7.2: machine-readable business logic on an exposed table
exposes:
  - exposeId: customer_profiles
    kind: table
    # ...binding, contract, etc...
    semantics:
      entities:
        - name: customer
          primaryKey: customer_id
      measures:
        - name: revenue
          expr: "SUM(order_total)"
          agg: sum
      dimensions:
        - name: signup_month
          expr: "DATE_TRUNC('month', created_at)"
      metrics:
        - name: monthly_active_customers
          type: simple
          measure: customer_id
          filters: ["last_active_at >= CURRENT_DATE - INTERVAL 30 DAY"]
```

**Why this matters:** eliminates the *semantic hallucination* failure mode where an LLM asked "what's our MRR?" invents an SQL expression because the contract never told it how MRR is defined. The shape is aligned with dbt MetricFlow, Snowflake Semantic Views, and OSI-format metric definitions — portable across engines.

### 🧊 Apache Iceberg Binding Config (NEW)

`binding.icebergConfig` lets contracts declare Iceberg table format specifics — write version, file format, partition spec, sort order — directly in the FLUID contract, so provisioners don't need an out-of-band config file.

```yaml
binding:
  platform: aws
  format: iceberg
  location: { bucket: warehouse, path: "gold/customer_profiles" }
  icebergConfig:
    writeVersion: 2
    fileFormat: parquet
    partitionSpec:
      - { sourceColumn: created_at, transform: month }
```

### 🔄 100% Backward Compatible with v0.7.1

- ✅ No breaking changes
- ✅ `semantics` and `icebergConfig` are both opt-in
- ✅ All v0.7.1 features (agentPolicy, sovereignty, provider-first orchestration, root accessPolicy) fully preserved

**Migration:**
```yaml
# Change version number — that's it.
fluidVersion: "0.7.2"  # was "0.7.1"
# Optionally add a semantics block on any expose.
```

See [schema-diffs/diff-0.7.1-to-0.7.2.md](schema-diffs/diff-0.7.1-to-0.7.2.md) for the full auto-generated change list.

---

## 🚀 What's New in FLUID 0.7.1

**FLUID 0.7.1** represents a significant evolution focused on **Agentic Governance** and **Provider-First Orchestration**. Built with **100% backward compatibility** with v0.5.7, it adds powerful new capabilities for the AI-driven enterprise:

### 🤖 Agentic Governance (NEW)

Control **which AI models** can access your data and **how they can use it**:

```yaml
# NEW in v0.7.1: AI/LLM usage policies
agentPolicy:
  allowedModels:
    - "gpt-4"
    - "claude-3-opus"
    - "gemini-1.5-pro"
  maxTokensPerRequest: 8192
  maxTokensPerDay: 100000
  allowedUseCases:
    - "customer-insights"
    - "market-analysis"
  deniedUseCases:
    - "political-profiling"
    - "credit-scoring"
  requiresHumanReview: true
  auditLog:
    enabled: true
    includePrompts: true
```

**Why this matters:** As AI agents become primary data consumers, organizations need granular control over:
- ✅ **Model-specific access** - Whitelist/blacklist AI models
- ✅ **Usage boundaries** - Define permitted and prohibited use cases
- ✅ **Rate limiting** - Token quotas per request and per day
- ✅ **Audit compliance** - Full logging of AI interactions with data
- ✅ **Human oversight** - Require review for sensitive operations

### 🌍 Sovereignty Constraints (NEW)

Enforce **data residency** and **jurisdictional compliance** at the contract level:

```yaml
# NEW in v0.7.1: Top-level sovereignty requirements
sovereignty:
  jurisdiction: "EU"
  dataResidency:
    allowedRegions:
      - "europe-west1"
      - "europe-west3"
    deniedRegions:
      - "us-central1"
  complianceFrameworks:
    - "GDPR"
    - "HIPAA"
  crossBorderTransfer:
    allowed: false
```

**Why this matters:** Global compliance requires infrastructure-level enforcement:
- ✅ **Jurisdictional boundaries** - Enforce EU, US, APAC data laws
- ✅ **Regional constraints** - Specify allowed/denied cloud regions
- ✅ **Compliance frameworks** - Declare GDPR, HIPAA, SOC2 requirements
- ✅ **Transfer controls** - Block cross-border data movement

### ⚙️ Provider-First Orchestration (NEW)

Direct invocation of **provider actions** as first-class orchestration tasks:

```yaml
# NEW in v0.7.1: Provider actions without wrapper operators
orchestration:
  engine: "airflow"
  tasks:
    - taskId: "ensure_s3_bucket"
      type: "provider_action"
      provider: "aws.s3"
      action: "ensure_bucket"
      parameters:
        bucket_name: "customer-data-lake"
        region: "us-west-2"
      
    - taskId: "load_to_snowflake"
      type: "provider_action" 
      provider: "snowflake.table"
      action: "ensure"
      parameters:
        database: "ANALYTICS"
        schema: "GOLD"
        table: "CUSTOMER_360"
      dependsOn: ["ensure_s3_bucket"]
```

**Why this matters:** Simplifies multi-cloud orchestration:
- ✅ **Native provider actions** - AWS, GCP, Azure, Snowflake primitives
- ✅ **No wrapper complexity** - Direct action invocation
- ✅ **Cross-provider workflows** - Multi-cloud pipelines without vendor lock-in
- ✅ **Strong typing** - Provider-specific validation

### 📊 Enhanced Access Control (NEW)

Root-level **accessPolicy** for automated IAM binding generation:

```yaml
# NEW in v0.7.1: Declarative access grants
accessPolicy:
  grants:
    - principal: "group:data-analytics@company.com"
      permissions: ["read", "select", "query"]
      resources:
        - "$.exposes[?(@.kind=='table')]"
    
    - principal: "serviceAccount:pipeline@project.iam.gserviceaccount.com"
      permissions: ["write", "insert", "update"]
      conditions:
        ipRanges: ["10.0.0.0/8"]
```

**Why this matters:** Infrastructure-as-code for data access:
- ✅ **Automated IAM** - Generate cloud IAM bindings from FLUID spec
- ✅ **Resource targeting** - JSONPath expressions for fine-grained access
- ✅ **Conditional access** - IP restrictions, time windows
- ✅ **Audit-ready** - Version-controlled access policies

### 📈 Key Improvements Over v0.5.7

| Feature | v0.5.7 | v0.7.1 | Impact |
|---------|--------|--------|--------|
| **AI Model Control** | ❌ None | ✅ agentPolicy | Govern AI/LLM data access |
| **Data Sovereignty** | ❌ Manual | ✅ sovereignty | Automated compliance enforcement |
| **Orchestration** | ⚠️ Abstract | ✅ Provider-first | Direct cloud provider actions |
| **Access Control** | ⚠️ Expose-level | ✅ Root-level accessPolicy | Centralized IAM automation |
| **Cross-Provider** | ⚠️ Complex | ✅ Native | Simplified multi-cloud workflows |
| **Task Dependencies** | ⚠️ Build-only | ✅ Data product deps | Richer dependency graphs |
| **Error Handling** | ⚠️ Basic | ✅ Categorized | Intelligent retry strategies |
| **Cost Tracking** | ⚠️ Estimated | ✅ Actual vs estimated | Budget enforcement |

### 🔄 100% Backward Compatible

**All v0.5.7 contracts work unchanged in v0.7.1:**
- ✅ No breaking changes
- ✅ New features are opt-in
- ✅ Existing patterns fully preserved
- ✅ Gradual adoption path

**Migration is simple:**
```yaml
# Change version number - that's it!
fluidVersion: "0.7.1"  # was "0.5.7"

# Optionally add new features
agentPolicy: { ... }
sovereignty: { ... }
accessPolicy: { ... }
```

---
## The Looming Crisis of Context

The "modern data stack"—a disaggregated ecosystem of best-in-class tools—has enabled rapid progress, but is held together by fragile scripts, proprietary configs, and tribal knowledge. This complexity, manageable by humans, becomes a liability in the Agentic Revolution.

**Agentic AI**—capable of complex reasoning and autonomous tool use—will soon be the primary consumer of enterprise data. Their potential, however, is capped by the quality and reliability of accessible data.

**Key Questions:**
- How can an agent trust the data it consumes?
- How does an agent discover the correct data product?
- How can we govern and audit thousands of autonomous agents accessing sensitive data?

The current landscape, built on disconnected pipelines, offers no scalable answers. Deploying agents atop this foundation is like building a skyscraper on sand. What’s needed is a paradigm shift: from data as pipeline output to data as a product with a contract.

**FLUID** is that foundational, declarative protocol.

---

## What FLUID Is (and Is Not)

### What FLUID 0.7.1 Is: A Declarative Protocol for Data Products

FLUID is a **declarative specification** (YAML/JSON, version-controlled) that defines a data product's complete lifecycle. It's not an execution engine, but a universal contract language for the data ecosystem.

**Core Philosophy (F.L.U.I.D):**
- **Federated:** Distributed ownership and governance, enabling domain teams to own their data products while participating in a unified ecosystem. No central bottlenecks—each team controls their data destiny.
- **Labeled:** Rich metadata and semantic tagging throughout the specification, making data products discoverable, categorizable, and governable at scale. Every asset carries its context.
- **Unifying:** Single declarative contract that consolidates interface definitions, dependencies, build logic, quality rules, and access policies. One source of truth eliminates scattered configurations.
- **Instructional:** Clear, executable specifications that tell tools exactly how to build, deploy, and manage data products. The contract becomes the implementation blueprint.
- **Declaration:** Declarative-first approach where you specify *what* you want, not *how* to achieve it. Tools interpret the specification to determine optimal execution strategies.

**Key Components in v0.7.1:**
- **`exposes`**: What data this product provides (schema, location, quality guarantees)
- **`consumes`**: What data this product depends on (other FLUID products or external sources)  
- **`build`**: How the data gets created (dbt, SQL, Python, multi-stage pipelines)
- **`metadata`**: Ownership, business context, and governance information
- **`agentPolicy`** ⭐NEW: AI/LLM usage governance and control
- **`sovereignty`** ⭐NEW: Data residency and jurisdictional compliance
- **`accessPolicy`** ⭐NEW: Root-level access control with automated IAM
- **`orchestration`** ⭐NEW: Provider-first task orchestration
- **Enhanced Features**: Multi-modal builds, improved lineage, ML pipeline support, agentic governance

This structure separates **interface** (what you get) from **implementation** (how it's built), enabling reliable data ecosystems ready for both humans and AI agents.

### What It Is Not: A Monolithic Executor

FLUID is **not** a new central tool or platform. It does not replace Airflow, dbt, or Snowflake. It does **not** require a monolithic "Agentic Executor."

Instead, FLUID fosters a **decentralized, compliant ecosystem**. Tools become "FLUID-aware"—for example, Airflow dynamically generates DAGs from FLUID files, and data catalogs ingest lineage from FLUID repositories. FLUID is the shared language, not the central brain.

---

## 🔄 FLUID 0.7.1 vs. OpenAPI Data Specification (OPDS) v4

Understanding when to use FLUID versus OPDS v4 is crucial for making the right architectural decisions for your data ecosystem.

### **Quick Decision Matrix:**

| **Use FLUID When** | **Use OPDS v4 When** |
|---------------------|----------------------|
| Building **data products** with complex transformations | Exposing **data APIs** with simple CRUD operations |
| Need **end-to-end governance** (build → deploy → consume) | Need **API contract** definition and documentation |
| **Multi-modal pipelines** (batch, streaming, ML) | **Request/response** data access patterns |
| **Domain-driven data mesh** architecture | **Service-oriented** or microservices architecture |
| **Declarative infrastructure** as code | **Imperative API** development workflows |

### **Detailed Comparison:**

| **Aspect** | **FLUID 0.7.1** | **OPDS v4** |
|------------|------------------|--------------|
| **Primary Purpose** | End-to-end data product lifecycle management | API specification and documentation |
| **Scope** | Data ingestion → transformation → consumption | HTTP API endpoints and schemas |
| **Governance Model** | Built-in data quality, lineage, and access policies | API versioning and compatibility |
| **Build Patterns** | `hybrid-reference`, `embedded-logic`, `multi-stage` | Code generation from OpenAPI specs |
| **Data Paradigms** | Batch, streaming, ML pipelines, feature stores | Request/response, real-time queries |
| **Metadata Richness** | Business context, ownership, SLAs, observability | API documentation, examples, parameters |
| **Execution Model** | Tool-agnostic specification (dbt, Airflow, etc.) | HTTP server implementations |
| **Consumer Experience** | Data contracts with quality guarantees | API contracts with response schemas |
| **Versioning** | Semantic versioning with schema evolution | API version paths and deprecation |
| **Discovery** | Federated catalogs, lineage graphs | API registries, service mesh |

### **Architecture Patterns:**

#### **🏗️ When FLUID Excels:**

**Data Mesh / Domain-Driven Architecture:**
```yaml
# FLUID: Complete data product specification
fluidVersion: "0.7.1"
kind: "DataProduct"
id: "finance.gold.risk_metrics"

# NEW in v0.7.1: Agentic governance
agentPolicy:
  allowedModels: ["gpt-4", "claude-3"]
  maxTokensPerDay: 50000

# Includes: sources, transformations, quality, access, observability
consumes: [...]
exposes: [...]  
build: [...]
metadata: [...]
```

**Multi-Stage Data Pipelines:**
- Bronze → Silver → Gold transformations
- ML training → inference → monitoring
- Streaming + batch processing hybrid

**Enterprise Governance:**
- Data quality as code
- Automated lineage tracking  
- Policy-driven access control
- SLA monitoring and alerting

#### **🌐 When OPDS v4 Excels:**

**API-First Data Access:**
```yaml
# OPDS: API specification focus
openapi: 3.1.0
info:
  title: Customer Data API
  version: 4.0.0
paths:
  /customers/{id}:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Customer'
```

**Microservices Data Layer:**
- Service-to-service data exchange
- Real-time query interfaces
- API gateway integration
- Developer portal documentation

**Request/Response Patterns:**
- Interactive dashboards
- Mobile applications
- Third-party integrations
- Real-time analytics APIs

### **Hybrid Approach: Best of Both Worlds**

Many organizations benefit from using **both** specifications together:

```yaml
# FLUID: Data product that exposes an API
fluidVersion: "0.7.1"
kind: "DataProduct"
id: "customer.api.profiles_v1"

# NEW: AI model restrictions
agentPolicy:
  allowedModels: ["gpt-4-turbo"]
  maxTokensPerRequest: 4096

exposes:
  - exposeId: "customer_api"
    kind: "api"
    contract:
      openapiRef: "./customer-profiles-api-v4.yaml"  # ← OPDS v4 spec
    binding:
      platform: "kubernetes"
      format: "http_api"
      location:
        baseUrl: "https://api.company.com/customers"

build:
  engine: "python"
  pattern: "embedded-logic"
  # API server implementation details
```

### **Migration Strategy:**

#### **From OPDS v4 → FLUID:**
1. **Wrap existing APIs** in FLUID specifications
2. **Add governance layers** (quality, lineage, policies)  
3. **Extend to full pipelines** beyond just API endpoints
4. **Implement data mesh** patterns gradually

#### **From FLUID → OPDS v4:**
1. **Extract API specifications** from FLUID `exposes.contract.openapiRef`
2. **Focus on service boundaries** rather than data pipelines
3. **Simplify to request/response** patterns
4. **Optimize for developer experience**

### **Revised Concept Mapping: FLUID 0.7.1 ↔ OPDS v4.0**

Let me provide a more accurate comparison based on careful analysis of both specifications:

| **Concept Domain** | **FLUID 0.7.1** | **OPDS v4.0** | **Analysis** |
|-------------------|------------------|----------------|---------------|
| **Product Definition** | `id`, `name`, `description`, `domain` | `productID`, `name`, `description`, `valueProposition`, `productSeries` | **OPDS stronger**: Richer business context with value propositions and product series grouping |
| **Lifecycle Management** | `lifecycle.state` (4 states: preview→active→deprecated→retired) | `status` (8 states: announcement→draft→development→testing→acceptance→production→sunset→retired) | **OPDS stronger**: More granular lifecycle tracking for business processes |
| **Data Contracts** | Embedded `contract.schema[]` with inline field definitions | External `contract` with `contractURL` or inline `spec`, supports ODCS/DCS standards | **Different approaches**: FLUID=embedded simplicity, OPDS=external contract management standards |
| **Quality Management** | Built-in `dq.rules[]` with anomaly detection | Comprehensive `dataQuality` with both declarative targets AND executable monitoring (SodaCL, Montecarlo, DQOps, Custom) | **OPDS stronger**: Industry-standard DQ tool integration + declarative/executable pattern |
| **SLA Framework** | Basic `qos` (availability, freshness, latency) | Comprehensive `SLA` with declarative objectives AND executable monitoring, support contacts, detailed dimensions | **OPDS significantly stronger**: Production-grade SLA management |
| **Access Methods** | Single `binding` per expose | Multiple `dataAccess[]` items with different `outputPortType` (file, API, SQL, AI, gRPC, sFTP) and formats | **OPDS stronger**: Multiple access patterns per product |
| **Business Operations** | No commercial support | Complete `pricingPlans[]`, `paymentGateways[]`, `license` with legal frameworks | **OPDS exclusive**: Full commercial data product support |
| **Data Governance** | Technical governance via `policy`, `observability` | Business governance via `license.governance`, `dataHolder` legal entities | **Different focus**: FLUID=technical, OPDS=business/legal |
| **Pipeline Orchestration** | Complete `build` patterns (hybrid-reference, embedded-logic, multi-stage) | No transformation/pipeline logic | **FLUID exclusive**: Data engineering and pipeline management |
| **Dependency Management** | Formal `consumes[]` with version constraints | Informal `recommendedDataProducts[]` | **FLUID stronger**: Explicit dependency management |
| **Metadata Richness** | Technical metadata (`tags`, `labels`, `businessContext`) | Business metadata (`categories`, `standards`, `useCases[]`, `brandSlogan`) | **Different purposes**: FLUID=technical discovery, OPDS=business discovery |
| **Versioning Strategy** | Semantic versioning with `schemaEvolution` | Product versioning with `versionNotes` and `issues` tracking | **FLUID stronger**: Technical schema evolution, OPDS stronger for business version communication |
| **AI/LLM Governance** | ✅ NEW: `agentPolicy` with model whitelisting, usage quotas, audit logging | ❌ No AI-specific governance | **FLUID exclusive**: Granular control over AI model access and usage boundaries |
| **Data Sovereignty** | ✅ NEW: `sovereignty` with jurisdiction, residency, cross-border controls | ⚠️ Basic geographic metadata | **FLUID stronger**: Automated compliance enforcement at infrastructure level |
| **Orchestration** | ✅ NEW: Provider-first tasks with direct cloud action invocation | ❌ No orchestration capabilities | **FLUID exclusive**: Native multi-cloud workflow management |

### **Corrected Strength Analysis:**

#### **🎯 OPDS v4.0 Actually Excels At:**
- **Production SLA Management**: Comprehensive monitoring-as-code with industry tools
- **Business Product Management**: Value propositions, use cases, product series
- **Commercial Operations**: Complete pricing, billing, legal, and payment frameworks  
- **Multi-Access Patterns**: Supporting diverse consumption methods per product
- **Quality Tooling**: Integration with enterprise DQ tools (SodaCL, Montecarlo, DQOps)
- **Lifecycle Granularity**: Detailed business process states

#### **🎯 FLUID 0.7.1 Actually Excels At:**
- **Data Engineering**: Complete pipeline orchestration and transformation logic
- **Technical Governance**: Embedded contracts, lineage tracking, schema evolution
- **AI/ML Workflows**: Native support for ML pipelines and agentic consumption
- **Agentic Governance** ⭐NEW: AI model whitelisting, usage quotas, audit logging
- **Data Sovereignty** ⭐NEW: Jurisdiction enforcement, regional constraints, cross-border controls
- **Provider-First Orchestration** ⭐NEW: Direct cloud provider action invocation
- **Access Automation** ⭐NEW: Root-level IAM policy generation
- **Dependency Management**: Formal inter-product relationships with version constraints
- **Multi-Environment**: Environment-specific configurations (dev/staging/prod)
- **Developer Experience**: Unified specification for technical teams

#### **🤔 Where I Was Wrong Initially:**
1. **Underestimated OPDS quality management** - It's actually more comprehensive with tool integrations
2. **Missed OPDS SLA sophistication** - It's production-grade with monitoring-as-code
3. **Overlooked OPDS access diversity** - Multiple access methods vs FLUID's single binding
4. **Didn't appreciate business vs technical focus** - They serve different organizational needs

### **Decision Framework:**

**Choose FLUID 0.7.1 if you need:**
- ✅ **End-to-end data pipeline governance**
- ✅ **AI/ML pipeline orchestration** 
- ✅ **Automated quality & lineage tracking**
- ✅ **Multi-environment data mesh architecture**
- ✅ **Agentic AI consumption with contracts**
- ✅ **AI model governance** (NEW: agentPolicy)
- ✅ **Data sovereignty enforcement** (NEW: jurisdiction control)
- ✅ **Provider-first orchestration** (NEW: direct cloud actions)

**Choose OPDS v4.0 if you need:**
- ✅ **Commercial data marketplace**
- ✅ **Legal compliance & licensing frameworks**
- ✅ **Business-oriented data catalogs**
- ✅ **Payment processing & billing integration**
- ✅ **Multi-access method data products**

**Use both together when:**
- ✅ Building **commercial data platforms** with technical governance
- ✅ Need **marketplace capabilities** + **pipeline orchestration**
- ✅ **Hybrid internal/external** data product distribution
- ✅ **Enterprise governance** + **ecosystem monetization**

---

## Why FLUID Is Indispensable in an MCP World

**Can’t a smart AI just “get the data”? Why bother with data products?**

No matter how advanced, an AI agent cannot operate on data it does not understand or trust. Connecting to raw databases is a liability, not an asset. FLUID closes three critical gaps:

- **Semantic Gap:** Without a contract, data is just bits. FLUID’s contract and semantics provide essential context—schema, descriptions, business ontology links.
- **Trust Gap:** How does an agent know data is correct or fresh? FLUID’s quality and SLA blocks provide enforceable guarantees.
- **Governance Gap:** How do we control and audit agent access? FLUID’s accessPolicy and dynamicPolicies create a programmatic access control layer.

**Conclusion:** AI cannot “just get the data.” FLUID provides the machine-readable contracts and policies that transform raw data into safe, trustworthy, and understandable Data Products.

---

## 📈 Why Mandate FLUID?

### 1️⃣ Drastically Reduce Operational Risk & Complexity

- Replace glue code with declarative `.fluid.yml`
- Built-in governance, compliance & versioning

### 2️⃣ Increase Innovation Velocity

- Treat data as products
- Discoverable, composable, contract-driven data

### 3️⃣ Future-Proof for the Agentic Era

- Machine-readable
- Secure
- Ready for AI-first enterprise infrastructure

---

## 🏗️ Core Principles

| Principle               | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| **Data as a Product**   | The core mental model of FLUID is to shift from thinking about "pipelines" to thinking about "products." A pipeline is an imperative process. A product is a versioned asset with a defined interface, quality guarantees, and a clear owner. FLUID files are the specification for these products.                         |
| **Declarative, Not Imperative**         | You define the desired end state of your data product—what it consumes, what it exposes, and the contract it must adhere to. You do not define the step-by-step "how." This is the job of a FLUID-compliant tool, which reads your definition and figures out the best way to implement it.                     |
| **Contracts as Code**   | The contract block is the heart of every data product. It embeds schema, quality rules, and privacy treatments directly into a version-controlled file. This makes governance an automated, proactive part of the development lifecycle, not a reactive, manual process.                          |
| **Federated Ownership** | FLUID is designed for a Data Mesh. .fluid.yml files are intended to be decentralized and co-located with the domain teams that own them. The standard's use of globally unique dataProduct names allows a central orchestrator or catalog to discover these distributed files and weave them into a single, unified data fabric.                       |
| **Compliant Ecosystem** | FLUID is not a monolithic platform. It is a standard that delegates execution to the tools you already use. An orchestrator, a catalog, or an ingestion service becomes "FLUID-aware" by learning to read .fluid.yml files to configure itself. This fosters an open, composable ecosystem rather than creating a new silo.                 |

---

## ✨ FLUID 0.7.1 in Action: Simple Examples

### 🥉 Example 1: Bronze Layer - Raw Data Ingestion

A FLUID data product that ingests payment events with built-in quality controls:

```yaml
# payments.fluid.yml
fluidVersion: "0.7.1"
kind: "DataProduct"
id: "finance.bronze.raw_payments"
name: "Raw Payment Events"

# NEW in v0.7.1: Data sovereignty
sovereignty:
  jurisdiction: "US"
  dataResidency:
    allowedRegions: ["us-central1", "us-east1"]

metadata:
  layer: "Bronze"
  owner:
    team: "data-platform"
    email: "data-platform@company.com"

# What this data product creates
exposes:
  - exposeId: "payment_events"
    kind: "table"
    contract:
      schema:
        - name: "payment_id"
          type: "STRING"
          required: true
          description: "Unique payment identifier"
        - name: "amount"
          type: "NUMERIC"
          required: true
          description: "Payment amount"
        - name: "currency"
          type: "STRING" 
          required: true
          description: "Currency code (USD, EUR, etc.)"
      dq:
        rules:
          - id: "positive_amount"
            type: "valid_values"
            selector: "amount > 0"
            severity: "error"
    binding:
      platform: "gcp"
      format: "bigquery_table"
      location:
        project: "company-data"
        dataset: "bronze_finance"
        table: "payments"

# How it gets built
build:
  engine: "sql"
  pattern: "embedded-logic"
  properties:
    sql: |
      SELECT 
        payment_id,
        amount,
        currency,
        created_at
      FROM raw_source.payments
      WHERE amount > 0
```

### 🥈 Example 2: Silver Layer - Business Logic

A FLUID data product that transforms raw data into business-ready insights:

```yaml
# customer_metrics.fluid.yml
fluidVersion: "0.7.1"
kind: "DataProduct" 
id: "analytics.silver.customer_metrics"
name: "Customer Metrics"

# NEW in v0.7.1: Access control automation
accessPolicy:
  grants:
    - principal: "group:analytics-team@company.com"
      permissions: ["read", "select"]

metadata:
  layer: "Silver"
  owner:
    team: "analytics"
    email: "analytics@company.com"

# What data this consumes
consumes:
  - productId: "finance.bronze.raw_payments"
    exposeId: "payment_events"
  - productId: "crm.bronze.raw_customers"
    exposeId: "customer_data"

# What this creates
exposes:
  - exposeId: "customer_ltv"
    kind: "table"
    contract:
      schema:
        - name: "customer_id"
          type: "STRING"
          required: true
        - name: "total_spent"
          type: "NUMERIC"
          required: true
        - name: "order_count"
          type: "INTEGER"
          required: true
        - name: "avg_order_value"
          type: "NUMERIC"
          required: true
    binding:
      platform: "gcp"
      format: "bigquery_table"
      location:
        project: "company-data"
        dataset: "silver_analytics"
        table: "customer_ltv"

build:
  engine: "dbt"
  pattern: "hybrid-reference"
  properties:
    model: "customer_ltv"
```

### 🥇 Example 3: Gold Layer - AI-Ready Features

A FLUID data product optimized for machine learning consumption:

```yaml
# ml_features.fluid.yml
fluidVersion: "0.7.1"
kind: "DataProduct"
id: "ml.gold.churn_features"
name: "Churn Prediction Features"

# NEW in v0.7.1: AI model governance
agentPolicy:
  allowedModels: ["gpt-4", "claude-3-opus"]
  maxTokensPerRequest: 8192
  allowedUseCases: ["churn-prediction", "customer-analytics"]
  requiresHumanReview: false

metadata:
  layer: "Gold"
  owner:
    team: "ml-engineering"
    email: "ml@company.com"

consumes:
  - productId: "analytics.silver.customer_metrics"
    exposeId: "customer_ltv"

exposes:
  - exposeId: "churn_features"
    kind: "feature_store"
    contract:
      schema:
        - name: "customer_id"
          type: "STRING"
          required: true
          tags: ["identifier"]
        - name: "recency_days"
          type: "INTEGER"
          description: "Days since last purchase"
        - name: "frequency_score"
          type: "FLOAT"
          description: "Purchase frequency score"
        - name: "monetary_score"
          type: "FLOAT"
          description: "Monetary value score"
    policy:
      authn: "iam"
      authz:
        readers: ["ml-agents", "data-scientists"]
    binding:
      platform: "gcp"
      format: "bigquery_table"
      location:
        project: "company-ml"
        dataset: "features"
        table: "churn_v1"

build:
  engine: "python"
  pattern: "embedded-logic"
  properties:
    language: "python"
    sql: |
      SELECT 
        customer_id,
        DATE_DIFF(CURRENT_DATE(), last_order_date, DAY) as recency_days,
        LOG(1 + order_count) as frequency_score,
        LOG(1 + total_spent) as monetary_score
      FROM {{ ref('customer_ltv') }}
```

---

## 🙋‍♀️ FAQ & Critical Review (The Black Hat Perspective)

A specification is only as strong as its ability to withstand scrutiny. Here, we address the toughest questions head-on.

### 1❓Isn't this just more YAML complexity?
**A:** FLUID eliminates complexity by unifying scattered configurations. Instead of separate dbt models, Airflow DAGs, data quality scripts, and access policies, you get one declarative file. Less moving parts = less complexity.

### 2❓Does FLUID replace my existing tools?
**A:** No. FLUID makes your tools work better together. dbt, Airflow, Snowflake, and other tools become "FLUID-aware" by reading the `.fluid.yml` specification to auto-configure themselves. It's the shared language, not a replacement platform.

### 3❓How do I start using FLUID 0.7.1 today?
**A:** Start small:
1. Pick one critical data pipeline
2. Write a `.fluid.yml` file describing it (see examples above)
3. Use FLUID-compliant tools or build adapters for your existing stack
4. Gradually expand to more data products

### 4❓What about complex transformations and custom logic?
**A:** FLUID 0.7.1 supports multiple build patterns:
- **`hybrid-reference`**: For dbt-style transformations
- **`embedded-logic`**: For custom SQL/Python code
- **`multi-stage`**: For complex multi-step orchestration

The `lineage` block maintains full traceability even with custom code.

### 5❓How does this help with AI agents and the "agentic era"?
**A:** AI agents need **contracts**, not chaos. FLUID 0.7.1 provides:
- **Discoverable data**: Agents can find the right data products
- **Trustworthy contracts**: Schema, quality, and freshness guarantees
- **Secure access**: Policy-driven permissions for autonomous systems
- **Rich context**: Business semantics and lineage for better decision-making
- **⭐ AI governance** (NEW): Model whitelisting, usage quotas, and audit trails
- **⭐ Sovereignty controls** (NEW): Automated jurisdictional compliance
- **⭐ Fine-grained permissions** (NEW): Root-level access policies with automated IAM

---

## 📚 Learn More

📖 [FLUID Full Specification](https://github.com/open-data-protocol/fluid/blob/main/specification.md)  
🔗 JSON Schema: [v0.7.3 (latest)](https://github.com/open-data-protocol/fluid/blob/main/schema/fluid-schema-0.7.3.json) · [v0.7.2](https://github.com/open-data-protocol/fluid/blob/main/schema/fluid-schema-0.7.2.json) · [v0.7.1](https://github.com/open-data-protocol/fluid/blob/main/schema/fluid-schema-0.7.1.json)  
📚 Generated Schema Docs: [v0.7.3](https://github.com/open-data-protocol/fluid/blob/main/specs/0.7.3/fluid-spec.html) · [v0.7.2](https://github.com/open-data-protocol/fluid/blob/main/specs/0.7.2/fluid-spec.html) · [v0.7.1](https://github.com/open-data-protocol/fluid/blob/main/specs/0.7.1/fluid-spec.html)  
🧭 [Schema Anatomy](docs/anatomy.md) · 📋 [Schema Cheatsheet](docs/schema-cheatsheet.md)  
🆕 Version Diffs: [0.7.2 → 0.7.3](schema-diffs/diff-0.7.2-to-0.7.3.md) · [0.7.1 → 0.7.2](schema-diffs/diff-0.7.1-to-0.7.2.md) · [0.5.7 → 0.7.1](schema-diffs/diff-0.5.7-to-0.7.1.md)  
🧑‍💻 [FLUID Contribution Guide](https://github.com/open-data-protocol/fluid/blob/main/contribute.md)  
📜 [License (MIT)](LICENSE.md)

---

## 🤝 Join the Movement

FLUID is an open-source standard, and we welcome contributions from the community! Whether you are interested in refining the specification, building compliant tools, or creating new examples, there are many ways to get involved.

- Help build the **agentic data future**
- Contribute examples, tooling, or feedback
- Be part of an open, community-led protocol

---

> **Your agents are only as trustworthy as the data products they consume. Make FLUID your foundation.**

📄 License
This project is licensed under the MIT License - see the LICENSE.md file for details.
