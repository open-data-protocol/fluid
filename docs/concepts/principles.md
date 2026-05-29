# Core Principles

Five principles shape every FLUID contract. Together they make governance automated, ownership federated, and execution someone else's job.

| Principle | Description |
|---|---|
| **Data as a Product** | FLUID's core mental model shifts from "pipelines" to "products." A pipeline is an imperative process; a product is a versioned asset with a defined interface, quality guarantees, and a clear owner. FLUID files are the specification for these products. |
| **Declarative, Not Imperative** | You define the desired end state of your data product — what it consumes, what it exposes, and the contract it must adhere to. You do not define the step-by-step "how." That is the job of a FLUID-compliant tool, which reads your definition and figures out the best way to implement it. |
| **Contracts as Code** | The `contract` block is the heart of every data product. It embeds schema, quality rules, and privacy treatments directly into a version-controlled file. This makes governance an automated, proactive part of the development lifecycle — not a reactive, manual process. |
| **Federated Ownership** | FLUID is designed for a Data Mesh. `.fluid.yml` files are decentralized and co-located with the domain teams that own them. The standard's use of globally unique data product ids lets a central orchestrator or catalog discover these distributed files and weave them into a single unified data fabric. |
| **Compliant Ecosystem** | FLUID is not a monolithic platform. It is a standard that delegates execution to the tools you already use. An orchestrator, a catalog, or an ingestion service becomes *FLUID-aware* by learning to read `.fluid.yml` files to configure itself. This fosters an open, composable ecosystem rather than creating a new silo. |

---

## Where to go next

- **[What FLUID Is (and Is Not)](/fluid/concepts/)** — the conceptual anchor and the F.L.U.I.D philosophy.
- **[The Agentic-Native Layer](/fluid/concepts/agentic-native)** — how these principles play out for AI agents.
