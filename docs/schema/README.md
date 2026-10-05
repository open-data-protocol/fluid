# Schema Reference

Everything you need to read, write, and validate a FLUID contract. **The latest stable schema is 0.7.5; 0.7.6 is a preview** (see [Versions](/fluid/schema/versions#stable-and-preview-versions)).

| Page | Use it for |
|---|---|
| [**Anatomy**](/fluid/schema/anatomy) | A guided tour of every top-level block, in authoring order, with a "what / when / why" per block. Start here if you've never written a contract. |
| [**Cheatsheet**](/fluid/schema/cheatsheet) | One row per field — meaning, required flag, and version added. The fast lookup table while you author. |
| [**Minimal Valid Contract**](/fluid/schema/minimal-contract) | The smallest file that validates, plus a glance at every top-level block. |
| [**Specification**](/fluid/schema/specification) | Validation semantics, document structure, and how multi-file composition relates to validity. |
| [**Versions**](/fluid/schema/versions) | Every published schema version and its status, how to choose `fluidVersion`, and known caveats. |
| [**Changelog**](/fluid/schema/changelog) | What changed between consecutive versions, including the pre-0.7.1 breaking changes and the one narrowing in 0.7.2. |

## Machine-readable artifacts

- **JSON Schema (0.7.5, stable):** [`/fluid/schema/fluid-schema-0.7.5.json`](/fluid/schema/fluid-schema-0.7.5.json) — point your validator here.
- **Generated HTML reference (0.7.5):** [`/fluid/specs/0.7.5/fluid-spec.html`](/fluid/specs/0.7.5/fluid-spec.html) — every type, enum and validation rule, rendered from the schema.
- **Preview (0.7.6):** [`fluid-schema-0.7.6.json`](/fluid/schema/fluid-schema-0.7.6.json) · [`specs/0.7.6/fluid-spec.html`](/fluid/specs/0.7.6/fluid-spec.html).

Validate a document against the schema of the `fluidVersion` it declares. For older versions, see [**Versions**](/fluid/schema/versions).
