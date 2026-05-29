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
    details: agentPolicy, sovereignty, and semantics give LLM agents deterministic answers to PII, allowed-use, metric, and residency questions — enforced at the MCP gateway.
  - title: Operational Superset
    details: The only open spec covering build + orchestration + source-aligned acquisition alongside contract and governance.
  - title: Interoperable
    details: Compiles to Bitol ODPS + ODCS via the forge-cli reference compiler for DataHub / OpenMetadata / Datamesh Manager catalog interop.
  - title: Federated by Design
    details: Built for Data Mesh — decentralized ownership, globally unique product ids, one unified fabric.
  - title: Open & MIT-Licensed
    details: A community-led protocol. Good ideas backed by real use cases get in.
footer: MIT Licensed | © open-data-protocol — Federated Layered Unified Interchange Definition
---

> **Your agents are only as trustworthy as the data products they consume.**

FLUID is one YAML file that describes a data product end to end — **schema, build, orchestration, agentic governance, sovereignty, and semantics**. Write it once; validate it, compile it, and deploy it anywhere.

## The shape of a contract

```yaml
fluidVersion: "0.7.4"
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
- **[What's New in 0.7.4](/fluid/releases/0.7.4)** — runtime agentPolicy enforcement at the MCP gateway.
- **[See the deck](/fluid/deck/)** — the FLUID story in slides.
