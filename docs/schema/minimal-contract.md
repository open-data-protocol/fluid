# Minimal Contract & FLUID at a Glance

Two views of a contract on the latest stable schema, **0.7.5**: the smallest file that validates, and a one-screen map of every top-level block.

## Minimal Valid Contract

The smallest file that passes JSON Schema validation against 0.7.5 — every other block is opt-in:

```yaml
fluidVersion: "0.7.5"
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

It validates against `fluid-schema-0.7.5.json` with any JSON Schema Draft 2020-12 validator, and with the reference implementation (`fluid validate` prints `✅ Valid FLUID contract (schema v0.7.5)`).

**What is required:** the six top-level keys above; inside `metadata`, only `owner` (the schema requires no member of `owner`, but name a `team`); and inside each expose, `exposeId`, `kind`, `contract` (with `schema` or `openapiRef`) and `binding` (with `platform`, `format` and `location`).

See the [**Examples**](/fluid/examples/) for the step-by-step progression from this minimal file to a production source-aligned acquisition product.

---

## FLUID at a Glance

Every top-level block in 0.7.5, with the version each first appeared in (in its current form). `[req]` marks required blocks. This is a **map, not a contract** — the placeholders are not valid values.

```text
fluidVersion: "0.7.5"            [req] the schema version this file declares
kind: DataProduct                [req] DataProduct | MLPipeline
id:   domain.layer.name          [req] globally unique product id
name: "Human-readable name"      [req] display name
description, domain                    business-facing summary, owning domain
tags: [pii, gold-layer]                lower-case categorization tags
labels: { team: analytics }            key/value labels

metadata:                        [req] only metadata.owner is required
  owner: { team, email, slack, oncall }   [req] owner itself; none of its members
  layer, productType, classification, businessContext, …

exposes: [ ... ]                 [req] ports you publish; each requires exposeId, kind, contract, binding
  ├── contract                   [req] schema columns (or openapiRef), dq rules, schemaPolicy
  ├── policy                           authn, authz, privacy, classification, agentPolicy (0.7.1)
  ├── semantics                        entities, measures, dimensions, metrics (0.7.2)
  ├── qos                              availability, freshnessSLO, latencyP95, …
  ├── mcp                              serve the port to AI agents over MCP (0.7.4)
  └── binding                    [req] platform + format + location (+ icebergConfig, vectorConfig, governance)

consumes: [ ... ]                      upstream FLUID products you read
build / builds[]                       how the product is produced
  pattern: hybrid-reference | embedded-logic | multi-stage | acquisition (0.7.3)
  engine:  dbt | dbt-<adapter> | sql | python | spark | glue | custom
           | duckdb | airbyte | meltano | dlt | kafka-connect | debezium (0.7.3)
  properties: { ... }                  shape chosen by pattern

orchestration    { engine, mode, airflow, … }                     (0.7.2, top level)
sovereignty      { jurisdiction, allowedRegions, deniedRegions, … }  (0.7.1)
accessPolicy     { grants: [{ principal, permissions, resources, conditions }] }  (0.7.1)
governance       { lakeFormation: { admins, tagDefinitions } }    (0.7.3)
retention        { runState, runLogs, lineage, dlq }              (0.7.3)
extensions       { ... }                                          (0.7.3)
lineage          { granularity, upstream, downstream }
schemaEvolution  { strategy, compatibility, changePolicy }
machineLearning  { enabled, framework, models }
environments     { dev: {...}, staging: {...}, prod: {...} }
lifecycle        { state, retention, deprecationPolicy }
docs             { homepage, runbook, dictionary, changeLog }

0.7.6 preview only (fluidVersion "0.7.6"):
packaging        { mode, pool, containers }
consumers        [ { name, type, ... } ]
```

Field-level lineage is `lineage.granularity: field_level` with `fieldMappings` on each `upstream[]` entry; there is no `fieldLevel` member.

::: tip `agentPolicy` location
AI/LLM consumption policy lives **per-expose** under `exposes[].policy.agentPolicy` — not at the root; the schema has never accepted it there. See [Anatomy §7](/fluid/schema/anatomy#_7-governance-sovereignty-accesspolicy-governance-and-exposes-policy-agentpolicy) for the shape.
:::

For a one-line-per-field reference with required flags, see the [**Cheatsheet**](/fluid/schema/cheatsheet). For a tour of each block, see the [**Anatomy**](/fluid/schema/anatomy).
