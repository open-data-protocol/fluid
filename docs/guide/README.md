# Introduction

**FLUID** — the **Federated Layered Unified Interchange Definition** — is the open, declarative standard for **Data Products**. It is one version-controlled YAML file that describes a data product end to end: schema, build, orchestration, agentic governance, sovereignty, and semantics.

FLUID provides the foundational protocol for building trustworthy, governable, and scalable data ecosystems — ready for the agentic era.

## The problem: scattered, partial specs

A single data product is rarely described in one place. Its shape lives in a dbt model, its orchestration in an Airflow DAG, its quality rules in ad-hoc scripts, its access policy in cloud IAM consoles, and its meaning in tribal knowledge. Each artifact is partial, and none of them is the source of truth.

That fragmentation is manageable by humans who know where the bodies are buried. It becomes a liability the moment AI agents — capable of autonomous tool use — become the primary consumers of enterprise data. An agent has three questions no scattered config can answer reliably:

- **Can I trust this data?** Is it correct, fresh, and within SLA?
- **How do I discover the right product?** Which one of thousands is canonical?
- **Am I allowed to use it — and how?** What does governance permit for this principal, this model, this use case?

## The value prop: one contract

FLUID replaces the scattered artifacts with **one declarative contract**. A `.fluid.yml` file consolidates interface, dependencies, build logic, quality rules, semantics, and policy into a single source of truth that is:

- **Version-controlled** — lives in Git, reviewed like code.
- **Schema-validated** — checked against a published JSON Schema before it ships.
- **Machine-readable** — tools and agents read the same file to configure themselves.
- **Decentralized** — co-located with the domain team that owns the product, woven into one fabric by globally unique product ids.

FLUID separates **interface** (what you get) from **implementation** (how it's built). It is the shared contract language — not a new central platform — so your existing tools (dbt, Airflow, Snowflake, BigQuery) become "FLUID-aware" rather than replaced.

## Who it's for

- **Data platform & domain teams** standardizing data products across a Data Mesh.
- **Governance, security, and compliance** owners who need policy, sovereignty, and access expressed as code.
- **AI / platform engineers** exposing data products to LLM agents and MCP gateways safely.
- **Tool builders** writing FLUID-aware orchestrators, catalogs, and ingestion services.

## Next steps

- **[Quickstart](/fluid/guide/quickstart)** — the smallest valid `.fluid.yml` and how to validate it.
- **[Concepts](/fluid/concepts/)** — what FLUID is and is not, the agentic-native layer, and how it compares to ODCS / ODPS.
- **[Schema Anatomy](/fluid/schema/anatomy)** — a tour of every top-level block.
- **[FLUID by Example](/fluid/examples/)** — build a production contract up step by step.
