# Schema Changes: 0.1.1 → 0.2.0

**Total changes:** 40
- ✅ Added: 23
- ❌ Removed: 6
- 📝 Modified: 11

---

## ✅ Added Properties

### `$defs.accessGrant.properties.principal.pattern`
```json
"^(group|user|gcp_service_account|aws_iam_role):.+$"
```

### `$defs.build.properties.engine.examples`
```json
[...13 items...]
```

### `$defs.column.properties.name.pattern`
```json
"^[a-zA-Z0-9_]+$"
```

### `$defs.consume.properties.id.pattern`
```json
"^[a-zA-Z0-9_.-]+$"
```

### `$defs.expose.properties.id.pattern`
```json
"^[a-zA-Z0-9_.-]+$"
```

### `$defs.expose.properties.mappings`
```json
{
  description: "Declarative transformation logic that separates lineage from rules."
  type: "array"
  items: {
    $ref: "#/$defs/mapping"
  }
}
```

### `$defs.expose.properties.type.examples`
```json
[...17 items...]
```

### `$defs.lifecycle.properties.retentionPeriodDays.minimum`
```json
0
```

### `$defs.location.properties.format.examples`
```json
[...6 items...]
```

### `$defs.mapping`
```json
{
  type: "object"
  description: "Defines the transformation for a single target column, explicitly separating source columns for line..."
  properties: {
    target: {
      type: "string"
      description: "The name of the target column in the output schema."
      pattern: "^[a-zA-Z0-9_]+$"
    }
    sources: {
      type: "array"
      items: {
        type: "string"
      }
      description: "An array of input columns used, for automated lineage generation."
    }
    rule: {
      type: "string"
      description: "The transformation logic or function to compute the target column."
    }
  }
  required: ["target", "sources", "rule"]
}
```

### `$defs.runtime.properties.platform.description`
```json
"The runtime platform. Provided examples cover common cloud orchestrators, but any string is valid."
```

### `$defs.runtime.properties.platform.examples`
```json
[...10 items...]
```

### `$defs.security.properties.encryptionAtRest.description`
```json
"Method of at-rest encryption. Examples provided for cloud KMS services."
```

### `$defs.security.properties.encryptionAtRest.examples`
```json
["AES256", "GCP_CMEK", "AWS_KMS"]
```

### `$defs.security.properties.encryptionInTransit.description`
```json
"Method of in-transit encryption."
```

### `$defs.security.properties.encryptionInTransit.examples`
```json
["TLS1.2+", "mTLS"]
```

### `$defs.sla.properties.availabilityPct.maximum`
```json
100
```

### `$defs.sla.properties.availabilityPct.minimum`
```json
0
```

### `$defs.sla.properties.freshnessMinutes.minimum`
```json
0
```

### `$defs.sla.properties.latencyMs.minimum`
```json
0
```

### `properties.domain.pattern`
```json
"^[a-zA-Z0-9_.-]+$"
```

### `properties.id.pattern`
```json
"^[a-zA-Z0-9_.-]+$"
```

### `properties.kind.examples`
```json
[...6 items...]
```

## ❌ Removed Properties

### `$defs.build.properties.engine.enum`
```json
[...6 items...]
```

### `$defs.location.properties.format.enum`
```json
[...5 items...]
```

### `$defs.runtime.properties.platform.enum`
```json
[...5 items...]
```

### `$defs.security.properties.encryptionAtRest.enum`
```json
["None", "AES256", "KMS"]
```

### `$defs.security.properties.encryptionInTransit.enum`
```json
["None", "TLS1.2+", "mTLS"]
```

### `properties.kind.enum`
```json
[...6 items...]
```

## 📝 Modified Properties

### `$defs.accessGrant.properties.principal.description`

**Before:**
```json
"e.g., group:analysts, user:name@company.com"
```

**After:**
```json
"e.g., group:analysts, user:name@company.com, gcp_service_account:..., aws_iam_role:..."
```

### `$defs.build.properties.engine.description`

**Before:**
```json
"The transformation engine used."
```

**After:**
```json
"The transformation engine used. Provided examples cover common cloud services, but any string is val..."
```

### `$defs.build.properties.model.description`

**Before:**
```json
"A reference to the specific model or script (e.g., dbt model path)."
```

**After:**
```json
"A reference to the specific model or script (e.g., dbt model path, git URI to a SQL file)."
```

### `$defs.expose.properties.type.description`

**Before:**
```json
"The physical type of the output (e.g., 'snowflake_table', 'bigquery_view')."
```

**After:**
```json
"The physical type of the output. Provided examples cover common cloud services, but any string is va..."
```

### `$defs.location.properties.properties.description`

**Before:**
```json
"Technology-specific properties (e.g., project, dataset, table)."
```

**After:**
```json
"Technology-specific properties. E.g., for BigQuery: { 'project': '...', 'dataset': '...', 'table': '..."
```

### `$defs.metadata.properties.owner.oneOf`

**Before:**
```json
[{"type": "string", "description": "A contact email address for the owner."}, {"type": "object", "properties": {"team": {"type": "string"}, "email": {"type": "string", "format": "email"}, "slack": {"type": "string"}}, "required": ["team"]}]
```

**After:**
```json
[{"type": "string", "description": "A contact email address for the owner.", "format": "email"}, {"type": "object", "properties": {"team": {"type": "string"}, "email": {"type": "string", "format": "email"}, "slack": {"type": "string"}}, "required": ["team"]}]
```

### `$defs.trigger.oneOf`

**Before:**
```json
[{"properties": {"type": {"const": "schedule"}, "cron": {"type": "string"}}, "required": ["type", "cron"]}, {"properties": {"type": {"const": "event"}, "eventType": {"type": "string"}}, "required": ["type", "eventType"]}, {"properties": {"type": {"const": "manual"}}, "required": ["type"]}]
```

**After:**
```json
[{"properties": {"type": {"const": "schedule"}, "cron": {"type": "string", "description": "A standard cron expression.", "pattern": "^((?:\\*|\\d+(?:-\\d+)?(?:,\\d+(?:-\\d+)?)*)(?:/\\d+)?\\s+){4,5}(?:\\*|\\d+(?:-\\d+)?(?:,\\d+(?:-\\d+)?)*)(?:/\\d+)?$"}}, "required": ["type", "cron"]}, {"properties": {"type": {"const": "event"}, "eventType": {"type": "string"}}, "required": ["type", "eventType"]}, {"properties": {"type": {"const": "manual"}}, "required": ["type"]}]
```

### `$id`

**Before:**
```json
"https://open-data-protocol.org/fluid/fluid.schema.v2.0.json"
```

**After:**
```json
"https://open-data-protocol.org/fluid/fluid.schema.v2.3.json"
```

### `description`

**Before:**
```json
"A comprehensive, production-ready schema for FLUID data product contracts, merging rich operational ..."
```

**After:**
```json
"A comprehensive, production-ready schema for FLUID data product contracts. This version adds stricte..."
```

### `properties.fluidVersion.examples`

**Before:**
```json
["0.1.1"]
```

**After:**
```json
["2.3.0"]
```

### `properties.id.description`

**Before:**
```json
"Globally-unique, versioned data product identifier."
```

**After:**
```json
"Globally-unique, versioned data product identifier. Should be machine-friendly."
```
