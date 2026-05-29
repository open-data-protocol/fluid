# Schema Changes: 0.7.3 → 0.7.4

**Total changes:** 15
- ✅ Added: 5
- ❌ Removed: 2
- 📝 Modified: 8

<!-- HUMAN-NOTE:START -->
## 🔎 Human summary

**0.7.4 — "Runtime agentPolicy Enforcement at the MCP Gateway."** Fully **additive** and backward-compatible: every valid 0.7.3 contract validates as 0.7.4 unchanged.

### ✅ What's new
- **`exposes[].mcp`** (new `exposeMcp` block) opts an expose into the Fluid MCP gateway, where `policy.agentPolicy` is enforced at runtime on every read. Carries `mcp.sampling.maxRows` (integer ≥ 1, default 100) and `mcp.classification.dataClass` (`public | internal | confidential | restricted`).
- **`binding.platform`** gains `postgres`; **`binding.format`** gains `postgres_table`, `athena_table`, `glue_table` (MCP output-port drivers).
- **`fluidVersion`** goes from `const: "0.7.3"` to `enum: ["0.7.3", "0.7.4"]`, so existing `0.7.3` values still validate.

`policy.agentPolicy`'s schema shape is unchanged from 0.7.1 — 0.7.4's contribution is *runtime enforcement*, not a new field. The `governance` block, Redshift/Athena bindings and runtimes, and the `datamesh_manager`/`opentofu` acquisition options all remain valid in 0.7.4.

> `phi` is not new in 0.7.4 — it has been in the column `sensitivity` enum since 0.7.3.
<!-- HUMAN-NOTE:END -->

---

## ✅ Added Properties

### `$defs.binding.properties.format.description`
```json
"Binding format. NEW in v0.7.4: 'postgres_table' (PostgreSQL driver), 'athena_table' / 'glue_table' (..."
```

### `$defs.binding.properties.platform.description`
```json
"Target platform. NEW in v0.7.4: 'postgres' for the MCP output-port PostgreSQL driver (AWS Athena use..."
```

### `$defs.expose.properties.mcp`
```json
{
  $ref: "#/$defs/exposeMcp"
  description: "NEW in v0.7.4: Declares this expose as agent-consumable over MCP, with per-expose overrides for the ..."
}
```

### `$defs.exposeMcp`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.4: Per-expose overrides for the MCP output-port server — sampling caps + classification...."
  properties: {
    sampling: {
      type: "object"
      additionalProperties: false
      properties: {
        maxRows: {
          type: "integer"
          minimum: 1
          description: "Hard cap for the `sample` MCP tool. Defends against an over-curious agent asking for petabyte-scale ..."
        }
      }
    }
    classification: {
      type: "object"
      additionalProperties: false
      properties: {
        dataClass: {
          type: "string"
          enum: [...4 items...]
          description: "Surfaced on the `describe` tool so consumer agents can declare downstream handling. Advisory; the re..."
        }
      }
    }
  }
}
```

### `properties.fluidVersion.enum`
```json
["0.7.3", "0.7.4"]
```

## ❌ Removed Properties

### `$defs.acquisitionCatalog.properties.register.description`
```json
"Catalog targets the publish stage will auto-register against. ``glue`` and ``snowflake_horizon`` are..."
```

### `properties.fluidVersion.const`
```json
"0.7.3"
```

## 📝 Modified Properties

### `$defs.acquisitionCatalog.properties.register.items.enum`

**Before:**
```json
["datahub", "openmetadata", "datamesh_manager"]
```

**After:**
```json
[...6 items...]
```

### `$defs.binding.properties.format.enum`

**Before:**
```json
[...18 items...]
```

**After:**
```json
[...21 items...]
```

### `$defs.binding.properties.platform.enum`

**Before:**
```json
[...9 items...]
```

**After:**
```json
[...10 items...]
```

### `$id`

**Before:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.3.json"
```

**After:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.4.json"
```

### `description`

**Before:**
```json
"FLUID Data Product contract (v0.7.3). Source-Aligned Acquisition Release:

🔥 NEW in v0.7.3:
• acquis..."
```

**After:**
```json
"FLUID Data Product contract (v0.7.4). Runtime agentPolicy Enforcement Release.

🔥 NEW in v0.7.4:
• M..."
```

### `properties.fluidVersion.description`

**Before:**
```json
"Contract schema version. Must be exactly '0.7.3' for source-aligned data products + acquisition patt..."
```

**After:**
```json
"Contract schema version. Accepts '0.7.3' (source-aligned data products + acquisition pattern + inges..."
```

### `properties.fluidVersion.examples`

**Before:**
```json
["0.7.3"]
```

**After:**
```json
["0.7.4", "0.7.3"]
```

### `title`

**Before:**
```json
"FLUID 0.7.3 \u2014 Source-Aligned Data Products"
```

**After:**
```json
"FLUID 0.7.4 \u2014 Runtime agentPolicy Enforcement at the MCP Gateway"
```
