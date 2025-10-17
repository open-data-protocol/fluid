
<p align="center">
  <img src="./logo.png" width="400" alt="FLUID Logo"/>
</p>

# Federated Layered Unified Interchange Definition (FLUID)

> **The open, declarative standard for Data Products.**  
> FLUID provides the foundational protocol for building trustworthy, governable, and scalable data ecosystems—ready for the agentic era.

**Quick Start:**
- 📖 [FLUID v0.5.7 Specification](https://github.com/open-data-protocol/fluid/blob/main/specification.md)
- 🔗 [JSON Schema v0.5.7](https://github.com/open-data-protocol/fluid/blob/main/schema/fluid-schema-0.5.7.json)
- 🚀 [Examples in Action](https://github.com/open-data-protocol/fluid/blob/main/examples.md)
- 🤝 [Contributing Guide](https://github.com/open-data-protocol/fluid/blob/main/contribute.md)

---

## Comparison with Open Data Product Specification (ODPS) v4.0

While both FLUID and ODPS aim to standardize data product specifications, they serve different purposes and contexts:

### Philosophy & Approach
- **FLUID**: Infrastructure-first approach focusing on data pipeline automation, build patterns, and technical implementation
- **ODPS**: Business-first approach emphasizing data product packaging, monetization, and governance for marketplaces

### Core Purpose
- **FLUID**: Enable automated data product development with standardized build patterns and ML integration
- **ODPS**: Facilitate data product discovery, pricing, and commercial exchange between organizations

### Structure & Components

#### FLUID Core Elements:
- **fluidVersion**: Version tracking with regex validation
- **build**: Comprehensive automation patterns (dbt, Airflow, ML workflows)
- **metadata**: Technical documentation and lineage
- **dependencies**: System and data requirements

#### ODPS Core Elements:
- **product.details**: Business metadata (name, description, visibility, status)
- **pricingPlans**: 12 standardized pricing models with payment gateways
- **SLA**: Service level agreements with monitoring dimensions
- **dataQuality**: Quality profiles with Everything-as-Code monitoring
- **dataAccess**: Multiple access methods (API, file, AI agent via MCP)
- **license**: Legal terms and IPR management
- **dataHolder**: Organization metadata

### Target Personas
- **FLUID**: Data engineers, MLOps teams, platform developers building data products
- **ODPS**: Data product managers, marketplace operators, business stakeholders selling/buying data

### Key Differentiators

| Feature | FLUID v0.5.7 | ODPS v4.0 |
|---------|--------------|-----------|
| **Build Automation** | ✅ Comprehensive patterns (dbt, Airflow, ML) | ❌ Not included |
| **Pricing & Monetization** | ❌ Not included | ✅ 12 pricing models + payment gateways |
| **SLA Management** | ❌ Not included | ✅ 11 standardized dimensions + monitoring |
| **Data Quality** | ❌ Not included | ✅ 8 quality dimensions + validation tools |
| **Legal Framework** | ❌ Not included | ✅ Licensing, IPR, governance |
| **Multi-language Support** | ❌ Not included | ✅ ISO 639-1 language codes |
| **AI Agent Integration** | ⚡ Basic support | ✅ Native MCP protocol support |
| **Technical Focus** | ✅ Infrastructure & automation | ⚡ Business metadata & access |
| **Schema Complexity** | 📦 Minimal (engineering-focused) | 📦 Comprehensive (business-focused) |
| **Referencing System** | ❌ Not included | ✅ Internal & external $ref support |
| **Everything-as-Code** | ✅ Build patterns | ✅ SLA + Quality monitoring |

### Complementary Use Cases

These specifications can work together:
1. **FLUID** for technical implementation and automation
2. **ODPS** for business packaging and marketplace distribution

A data product could use FLUID for development/deployment and ODPS for commercialization and external distribution.

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

### What FLUID 0.5.7 Is: A Declarative Protocol for Data Products

FLUID is a **declarative specification** (YAML/JSON, version-controlled) that defines a data product's complete lifecycle. It's not an execution engine, but a universal contract language for the data ecosystem.

**Core Philosophy (F.L.U.I.D):**
- **Federated:** Distributed ownership and governance, enabling domain teams to own their data products while participating in a unified ecosystem. No central bottlenecks—each team controls their data destiny.
- **Labeled:** Rich metadata and semantic tagging throughout the specification, making data products discoverable, categorizable, and governable at scale. Every asset carries its context.
- **Unifying:** Single declarative contract that consolidates interface definitions, dependencies, build logic, quality rules, and access policies. One source of truth eliminates scattered configurations.
- **Instructional:** Clear, executable specifications that tell tools exactly how to build, deploy, and manage data products. The contract becomes the implementation blueprint.
- **Declaration:** Declarative-first approach where you specify *what* you want, not *how* to achieve it. Tools interpret the specification to determine optimal execution strategies.

**Key Components in v0.5.7:**
- **`exposes`**: What data this product provides (schema, location, quality guarantees)
- **`consumes`**: What data this product depends on (other FLUID products or external sources)  
- **`build`**: How the data gets created (dbt, SQL, Python, multi-stage pipelines)
- **`metadata`**: Ownership, business context, and governance information
- **Enhanced Features**: Multi-modal builds, improved lineage, ML pipeline support

This structure separates **interface** (what you get) from **implementation** (how it's built), enabling reliable data ecosystems ready for both humans and AI agents.

### What It Is Not: A Monolithic Executor

FLUID is **not** a new central tool or platform. It does not replace Airflow, dbt, or Snowflake. It does **not** require a monolithic "Agentic Executor."

Instead, FLUID fosters a **decentralized, compliant ecosystem**. Tools become "FLUID-aware"—for example, Airflow dynamically generates DAGs from FLUID files, and data catalogs ingest lineage from FLUID repositories. FLUID is the shared language, not the central brain.

---

## 🔄 FLUID vs. OpenAPI Data Specification (OPDS) v4

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

| **Aspect** | **FLUID 0.5.7** | **OPDS v4** |
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
fluidVersion: "0.5.7"
kind: "DataProduct"
id: "finance.gold.risk_metrics"

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
fluidVersion: "0.5.7"
kind: "DataProduct"
id: "customer.api.profiles_v1"

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

### **Revised Concept Mapping: FLUID 0.5.7 ↔ OPDS v4.0**

Let me provide a more accurate comparison based on careful analysis of both specifications:

| **Concept Domain** | **FLUID 0.5.7** | **OPDS v4.0** | **Analysis** |
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

### **Corrected Strength Analysis:**

#### **🎯 OPDS v4.0 Actually Excels At:**
- **Production SLA Management**: Comprehensive monitoring-as-code with industry tools
- **Business Product Management**: Value propositions, use cases, product series
- **Commercial Operations**: Complete pricing, billing, legal, and payment frameworks  
- **Multi-Access Patterns**: Supporting diverse consumption methods per product
- **Quality Tooling**: Integration with enterprise DQ tools (SodaCL, Montecarlo, DQOps)
- **Lifecycle Granularity**: Detailed business process states

#### **� FLUID 0.5.7 Actually Excels At:**
- **Data Engineering**: Complete pipeline orchestration and transformation logic
- **Technical Governance**: Embedded contracts, lineage tracking, schema evolution
- **AI/ML Workflows**: Native support for ML pipelines and agentic consumption
- **Dependency Management**: Formal inter-product relationships with version constraints
- **Multi-Environment**: Environment-specific configurations (dev/staging/prod)
- **Developer Experience**: Unified specification for technical teams

#### **🤔 Where I Was Wrong Initially:**
1. **Underestimated OPDS quality management** - It's actually more comprehensive with tool integrations
2. **Missed OPDS SLA sophistication** - It's production-grade with monitoring-as-code
3. **Overlooked OPDS access diversity** - Multiple access methods vs FLUID's single binding
4. **Didn't appreciate business vs technical focus** - They serve different organizational needs

### **Decision Framework:**

**Choose FLUID 0.5.7 if you need:**
- ✅ **End-to-end data pipeline governance**
- ✅ **AI/ML pipeline orchestration** 
- ✅ **Automated quality & lineage tracking**
- ✅ **Multi-environment data mesh architecture**
- ✅ **Agentic AI consumption with contracts**

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

## ✨ FLUID 0.5.7 in Action: Simple Examples

### 🥉 Example 1: Bronze Layer - Raw Data Ingestion

A FLUID data product that ingests payment events with built-in quality controls:

```yaml
# payments.fluid.yml
fluidVersion: "0.5.7"
kind: "DataProduct"
id: "finance.bronze.raw_payments"
name: "Raw Payment Events"

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
fluidVersion: "0.5.7"
kind: "DataProduct" 
id: "analytics.silver.customer_metrics"
name: "Customer Metrics"

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
fluidVersion: "0.5.7"
kind: "DataProduct"
id: "ml.gold.churn_features"
name: "Churn Prediction Features"

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

### 3❓How do I start using FLUID 0.5.7 today?
**A:** Start small:
1. Pick one critical data pipeline
2. Write a `.fluid.yml` file describing it (see examples above)
3. Use FLUID-compliant tools or build adapters for your existing stack
4. Gradually expand to more data products

### 4❓What about complex transformations and custom logic?
**A:** FLUID 0.5.7 supports multiple build patterns:
- **`hybrid-reference`**: For dbt-style transformations
- **`embedded-logic`**: For custom SQL/Python code
- **`multi-stage`**: For complex multi-step orchestration

The `lineage` block maintains full traceability even with custom code.

### 5❓How does this help with AI agents and the "agentic era"?
**A:** AI agents need **contracts**, not chaos. FLUID provides:
- **Discoverable data**: Agents can find the right data products
- **Trustworthy contracts**: Schema, quality, and freshness guarantees
- **Secure access**: Policy-driven permissions for autonomous systems
- **Rich context**: Business semantics and lineage for better decision-making

---

## 📚 Learn More

📖 [FLUID v0.5.7 Full Specification](https://github.com/open-data-protocol/fluid/blob/main/specification.md)  
🔗 [JSON Schema v0.5.7](https://github.com/open-data-protocol/fluid/blob/main/schema/fluid-schema-0.5.7.json)  
📚 [Generated Schema Documentation](https://github.com/open-data-protocol/fluid/blob/main/specs/0.5.7/fluid-spec.html)  
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
