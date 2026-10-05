# Quickstart

A FLUID contract is **one YAML file**. This page shows the smallest file that validates against FLUID **0.7.5** — the latest stable version — explains each required block, and shows how to validate it.

## The smallest valid contract

Every block below is required. Every other top-level block — `description`, `domain`, `tags`, `labels`, `consumes`, `build` / `builds`, `orchestration`, `sovereignty`, `accessPolicy`, `governance`, `retention`, `lineage`, `lifecycle`, `environments`, `docs`, `extensions` — is opt-in and layered on as you need it. (`agentPolicy` is opt-in too, but it lives inside an expose, under `exposes[].policy`.)

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
| `fluidVersion` | ✅ | The schema version this file declares; it is validated against that version's schema. Use `"0.7.5"`, the latest stable version. |
| `kind` | ✅ | `DataProduct` or `MLPipeline`. |
| `id` | ✅ | Globally unique product id. Convention: `domain.layer.name`. |
| `name` | ✅ | Human-readable display name. |
| `metadata` | ✅ | Only `metadata.owner` is required. The schema requires none of `owner`'s members, but name a `team`: it is how tools route ownership and alerts. |
| `exposes` | ✅ | The ports you publish. Each entry requires `exposeId`, `kind`, `contract`, and `binding`. |

Inside each `exposes[]` entry:

- **`contract`** — the schema columns (or an `openapiRef`) plus optional data-quality rules.
- **`binding`** — where the data physically lives: `platform` + `format` + `location`.

> **0.7.5 note.** 0.7.5 adds an opt-in Iceberg streaming sink on the `kafka-connect` acquisition engine, the `confluent` (Tableflow) and `pgvector` platforms, and new location fields — see [What's New in 0.7.5](/fluid/releases/0.7.5). It is additive: a valid 0.7.4 contract stays valid when it declares `"0.7.5"`, and declaring `"0.7.5"` is what lets a contract use the new fields.
>
> **0.7.6 is a preview.** Use it only if you need one of its fields, by declaring `fluidVersion: "0.7.6"`; it can still change. See [0.7.6 (preview)](/fluid/releases/0.7.6).

## Validate it

Validate a contract against the published JSON Schema **of the version it declares** — for this file, 0.7.5:

```
https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.5.json
```

Use a validator that supports JSON Schema Draft 2020-12, which every FLUID schema declares. Validators that compile `pattern` as an ECMA-262 regular expression, as JavaScript-based ones typically do, may refuse one pattern in the 0.7.2–0.7.6 schemas; see the [known interoperability issue](/fluid/schema/specification#known-interoperability-issue-one-pattern-is-not-an-ecma-262-regular-expression). Python's `jsonschema`, which this repository's conformance tooling uses, validates them.

Or use the reference implementation, which validates against the declared version and adds its own provider checks:

```bash
pip install data-product-forge
fluid validate contract.fluid.yaml     # ✅ Valid FLUID contract (schema v0.7.5)
```

### Editor autocomplete & inline validation

Add this line as the **first line** of your contract file so the [YAML Language Server](https://github.com/redhat-developer/yaml-language-server) (bundled with the VS Code YAML extension) gives you live completion and validation. Use the URL of the version the file declares; pointing a 0.7.4 file at the 0.7.5 schema would hide 0.7.5-only fields that its own schema rejects.

```yaml
# yaml-language-server: $schema=https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.5.json
fluidVersion: "0.7.5"
kind: DataProduct
# ...
```

## Next steps

- **[FLUID by Example](/fluid/examples/)** — the step-by-step build-up from this minimal file to a production source-aligned acquisition product.
- **[Schema Anatomy](/fluid/schema/anatomy)** — the full tour of every top-level block with deep-dive links.
