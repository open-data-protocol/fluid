# Quickstart

A FLUID contract is **one YAML file**. This page shows the smallest file that validates against FLUID **0.7.5**, explains each required block, and shows how to validate it.

## The smallest valid contract

Every block below is required. Every other top-level block — `description`, `domain`, `tags`, `labels`, `consumes`, `build`, `orchestration`, governance (`agentPolicy`, `sovereignty`, `accessPolicy`, `retention`), `lineage`, `lifecycle`, `environments`, `docs` — is opt-in and layered on as you need it.

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

## What each required block does

| Block | Required | Meaning |
|---|---|---|
| `fluidVersion` | ✅ | Which contract version this file targets. Use `"0.7.5"` for the latest schema. |
| `kind` | ✅ | `DataProduct` or `MLPipeline`. |
| `id` | ✅ | Globally unique product id. Convention: `domain.layer.name`. |
| `name` | ✅ | Human-readable display name. |
| `metadata` | ✅ | Only `metadata.owner` is required; by convention `owner.team` is the one truly required field. |
| `exposes` | ✅ | The ports you publish. Each entry requires `exposeId`, `kind`, `contract`, and `binding`. |

Inside each `exposes[]` entry:

- **`contract`** — the schema columns (or an `openapiRef`) plus optional data-quality rules.
- **`binding`** — where the data physically lives: `platform` + `format` + `location`.

> **0.7.5 note.** The `kafka-connect` acquisition pattern gains an opt-in Iceberg streaming sink (`iceberg_sink_enabled`, `streamingSink`, `sink_topics`), and `binding.platform` adds `confluent` (Confluent Cloud Tableflow). 0.7.5 is **additive and fully backward-compatible** — every valid 0.7.4 contract still validates, so bumping `fluidVersion` is all it takes.

## Validate it

Validate any `.fluid.yml` against the published JSON Schema for 0.7.5:

```
https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.5.json
```

Point any JSON-Schema validator (for example `ajv`, `check-jsonschema`, or your CI's schema step) at that URL.

### Editor autocomplete & inline validation

Add this line as the **first line** of your `.fluid.yml` so the [YAML Language Server](https://github.com/redhat-developer/yaml-language-server) (bundled with the VS Code YAML extension) gives you live completion and validation:

```yaml
# yaml-language-server: $schema=https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.5.json
fluidVersion: "0.7.5"
kind: DataProduct
# ...
```

## Next steps

- **[FLUID by Example](/fluid/examples/)** — the step-by-step build-up from this minimal file to a production source-aligned acquisition product.
- **[Schema Anatomy](/fluid/schema/anatomy)** — the full tour of every top-level block with deep-dive links.
