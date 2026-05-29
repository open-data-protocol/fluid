# What FLUID Is (and Is Not)

FLUID — **Federated Layered Unified Interchange Definition** — is a **declarative specification** (YAML/JSON, version-controlled) that defines a data product's complete lifecycle. It is not an execution engine. It is a universal contract language for the data ecosystem.

One `.fluid.yml` separates **interface** (what you get) from **implementation** (how it's built) — making reliable data ecosystems possible for both humans and AI agents.

---

## What FLUID Is: A Declarative Protocol for Data Products

A FLUID contract describes a data product end to end: its schema, build logic, dependencies, quality rules, orchestration, and governance — all in a single, machine-readable file. Tools read that file and configure themselves; FLUID itself runs nothing.

### Core philosophy (F.L.U.I.D)

| Letter | Pillar | Meaning |
|---|---|---|
| **F** | **Federated** | Distributed ownership and governance. Domain teams own their data products while participating in a unified ecosystem. No central bottlenecks — each team controls its own data destiny. |
| **L** | **Labeled** | Rich metadata and semantic tagging throughout the spec, making data products discoverable, categorizable, and governable at scale. Every asset carries its context. |
| **U** | **Unifying** | A single declarative contract consolidates interface definitions, dependencies, build logic, quality rules, and access policies. One source of truth eliminates scattered configuration. |
| **I** | **Instructional** | Clear, executable specifications tell tools exactly how to build, deploy, and manage data products. The contract is the implementation blueprint. |
| **D** | **Declaration** | Declarative-first: you specify *what* you want, not *how* to achieve it. Tools interpret the spec to determine the optimal execution strategy. |

### Key components

| Block | What it declares |
|---|---|
| **`exposes`** | What data this product provides — schema, location, quality guarantees, and (since 0.7.2) semantics. |
| **`consumes`** | What data this product depends on — other FLUID products or external sources. |
| **`build`** | How the data gets created — dbt, SQL, Python, multi-stage pipelines, or source-aligned acquisition. |
| **`metadata`** | Ownership, business context, and governance information. |
| **`agentPolicy`** | AI/LLM usage governance and control (per-expose, under `exposes[].policy.agentPolicy`). |
| **`sovereignty`** | Data residency and jurisdictional compliance. |
| **`accessPolicy`** | Root-level access control with automated IAM binding generation. |
| **`orchestration`** | Provider-first task orchestration (Airflow, Dagster, Prefect, Kubeflow). |

This structure separates **interface** (what you get) from **implementation** (how it's built), enabling reliable data ecosystems ready for both humans and AI agents.

> The latest schema version is **0.7.4**, which adds runtime `agentPolicy` enforcement at the MCP gateway. Like the 0.7.1 → 0.7.3 line, **0.7.4 is additive and fully backward-compatible** — every valid 0.7.3 contract still validates. See the release notes for details.

---

## What FLUID Is Not: A Monolithic Executor

FLUID is **not** a new central tool or platform. It does not replace Airflow, dbt, or Snowflake. It does **not** require a monolithic "Agentic Executor."

Instead, FLUID fosters a **decentralized, compliant ecosystem**. Tools become *FLUID-aware*: Airflow dynamically generates DAGs from FLUID files, data catalogs ingest lineage from FLUID repositories, and ingestion services configure themselves from the contract. FLUID is the shared language, not the central brain.

---

## Where to go next

- **[Core Principles](/fluid/concepts/principles)** — the five principles that shape every FLUID contract.
- **[The Agentic-Native Layer](/fluid/concepts/agentic-native)** — the four agent failure modes FLUID is built to answer deterministically.
- **[FLUID vs ODCS / ODPS](/fluid/concepts/comparisons)** — how FLUID relates to the adjacent open data product specs.
