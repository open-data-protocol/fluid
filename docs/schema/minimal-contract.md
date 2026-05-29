# Minimal Contract & FLUID at a Glance

Two views of the contract for v0.7.4: the smallest file that validates, and a one-screen map of every top-level block.

## FLUID at a Glance

A FLUID contract is one YAML file. The shape below shows **every top-level block** in v0.7.4, with one-line meaning and the version each was introduced. Required blocks are marked `[req]`; everything else is opt-in.

```yaml
fluidVersion: "0.7.4"            # [req] which contract version this file targets
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
  └── mcp                        #         ⭐ 0.7.4 — opt this expose into the MCP output-port gateway
  └── binding                    # [req] where it lives (platform + format + location, + icebergConfig*)

build:                           #       how the product is produced
  pattern: hybrid-reference      #       | embedded-logic | multi-stage | acquisition (⭐ 0.7.3)
  engine:  dbt | sql | python | spark | glue | custom        # transformation engines
           | duckdb | airbyte | meltano | dlt | kafka-connect | debezium   # ⭐ 0.7.3 acquisition
  properties: { ... }            #       pattern-specific (⭐ 0.7.3: acquisitionPattern)

orchestration: { engine: airflow | dagster | prefect | kubeflow | custom | none, tasks: [...] }   # ⭐ 0.7.0+
sovereignty:   { jurisdiction, allowedRegions, deniedRegions, enforcementMode, … }   # ⭐ 0.7.1
accessPolicy:  { grants: [{ principal, permissions, resources, conditions }] }       # ⭐ 0.7.1
retention:     { runState, runLogs, lineage, dlq }                                   # ⭐ 0.7.3
lineage:       { upstream, downstream, fieldLevel }
schemaEvolution: { strategy, compatibility }
machineLearning: { ... }
environments:  { dev: {...}, staging: {...}, prod: {...} }
lifecycle:     { state: preview | active | deprecated | retired }
docs:          { ... }
```

::: tip `agentPolicy` location
AI/LLM consumption policy lives **per-expose** under `exposes[].policy.agentPolicy` — not at the root. (Earlier release notes show it at the top level; the schema has never accepted it there.) As of 0.7.4, when an expose also carries an `mcp` block, that `agentPolicy` is enforced at runtime by the Fluid MCP gateway on every read. See [Anatomy §7](/fluid/schema/anatomy#_7-governance-sovereignty-accesspolicy-and-exposes-policy-agentpolicy) for the correct shape.
:::

For a one-line-per-field reference with required/optional flags, see the [**Cheatsheet**](/fluid/schema/cheatsheet). For a tour of each block with deep-dive links, see the [**Anatomy**](/fluid/schema/anatomy).

---

## Minimal Valid Contract

The smallest file that passes JSON Schema validation against v0.7.4 — every other top-level block is opt-in:

```yaml
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

**What you can drop:** `description`, `domain`, `tags`, `labels`, `consumes`, `build`, `orchestration`, all governance blocks (`agentPolicy`, `sovereignty`, `accessPolicy`, `retention`), `exposes[].mcp`, `lineage`, `lifecycle`, `environments`, `docs`. Everything else is layered on as you need it.

See the [**Examples**](/fluid/examples/) for the step-by-step progression from this minimal file to a production source-aligned acquisition product.
