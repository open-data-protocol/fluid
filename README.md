
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
fluidVersion: "0.5.7"
kind: "DataProduct"
id: "analytics.gold.customer_segments"

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
