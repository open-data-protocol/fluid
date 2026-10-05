---
home: true
title: Home
heroText: FLUID
tagline: One declarative contract for trustworthy, governable, agent-ready data products.
actions:
  - text: Get Started →
    link: /guide/
    type: primary
  - text: Minimal Contract
    link: /schema/minimal-contract
    type: secondary
  - text: FLUID vs ODCS / ODPS
    link: /concepts/comparisons
    type: secondary
features:
  - title: Contract-First
    details: One .fluid.yml is the source of truth — schema, quality, build, lineage, governance. Version-controlled and schema-validated.
  - title: Agentic-Native
    details: agentPolicy, sovereignty, and semantics give LLM agents machine-readable answers to PII, allowed-use, metric, and residency questions — and an MCP gateway can enforce them on every read.
  - title: Operational Superset
    details: Covers build, orchestration and source-aligned acquisition alongside the data contract and its governance.
  - title: Interoperable
    details: Compiles to Bitol ODPS + ODCS via the forge-cli reference implementation for DataHub / OpenMetadata / Datamesh Manager catalog interop.
  - title: Federated by Design
    details: Built for Data Mesh — decentralized ownership, globally unique product ids, one unified fabric.
  - title: Open & Apache 2.0-Licensed
    details: An open specification under the Apache License 2.0, with a public conformance corpus and no CLA.
footer: Licensed under the Apache License 2.0 | Copyright 2025 The FLUID Authors
---

> **Your agents are only as trustworthy as the data products they consume.**

FLUID is one YAML file that describes a data product end to end — **schema, build, orchestration, agentic governance, sovereignty, and semantics**. Write it once; validate it, compile it, and deploy it anywhere.

## The shape of a contract

```yaml
fluidVersion: "0.7.5"
kind: DataProduct
id: demo.bronze.hello_world
name: Hello World
metadata:
  owner:
    team: data-platform
exposes:
  - exposeId: hello
    kind: table
    contract:
      schema:
        - name: id
          type: STRING
          required: true
    binding:
      platform: local
      format: parquet
      location:
        path: ./hello.parquet
```

→ Build it up step by step in **[FLUID by Example](/fluid/examples/)**.

## Where to go next

- **[Guide](/fluid/guide/)** — what FLUID is, the quickstart, and the FAQ.
- **[Concepts](/fluid/concepts/)** — the agentic-native layer and how FLUID compares to ODCS / ODPS.
- **[Schema Reference](/fluid/schema/anatomy)** — every top-level block, a cheatsheet, and the full specification.
- **[What's New in 0.7.5](/fluid/releases/0.7.5)** — the latest stable version: streaming Kafka → Iceberg sink, Confluent Cloud Tableflow, and a pgvector output port.
- **[0.7.6 (preview)](/fluid/releases/0.7.6)** — packaging modes, declared consumers, cross-mesh pins; opt-in, and still subject to change.
- **[See the deck](/fluid/deck/)** — the FLUID story in slides.
- **[Contributing & governance](/fluid/contributing/)** — how the standard is maintained, and how to take part.
