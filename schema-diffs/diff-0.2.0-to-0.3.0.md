# Schema Changes: 0.2.0 → 0.3.0

**Total changes:** 53
- ✅ Added: 14
- ❌ Removed: 32
- 📝 Modified: 7

---

## ✅ Added Properties

### `$defs.declarativePattern`
```json
{
  type: "object"
  properties: {
    from: {
      type: "string"
    }
    joins: {
      type: "array"
      items: {
        $ref: "#/$defs/join"
      }
    }
    filters: {
      type: "array"
      items: {
        type: "string"
      }
    }
    select: {
      type: "array"
      items: {
        $ref: "#/$defs/select"
      }
    }
  }
}
```

### `$defs.embeddedLogicPattern`
```json
{
  type: "object"
  properties: {
    sql: {
      type: "string"
    }
    language: {
      type: "string"
      enum: [...4 items...]
    }
  }
  required: ["sql"]
}
```

### `$defs.expose.properties.mappings.readOnly`
```json
true
```

### `$defs.governance.properties.lineage`
```json
{
  type: "string"
}
```

### `$defs.governance.properties.regulatory`
```json
{
  type: "array"
  items: {
    type: "string"
    enum: [...4 items...]
  }
}
```

### `$defs.governance.properties.stewardship`
```json
{
  type: "object"
  properties: {
    steward: {
      type: "string"
    }
    email: {
      type: "string"
      format: "email"
    }
  }
}
```

### `$defs.hybridReferencePattern`
```json
{
  type: "object"
  properties: {
    model: {
      type: "string"
    }
    vars: {
      type: "object"
      additionalProperties: true
    }
  }
  required: ["model"]
}
```

### `$defs.join`
```json
{
  type: "object"
  properties: {
    type: {
      type: "string"
      enum: [...4 items...]
    }
    left: {
      type: "string"
    }
    right: {
      type: "string"
    }
    on: {
      type: "string"
    }
  }
  required: [...4 items...]
}
```

### `$defs.logicalMappingPattern`
```json
{
  type: "object"
  properties: {
    sources: {
      type: "array"
      items: {
        type: "string"
      }
    }
    steps: {
      type: "array"
      items: {
        $ref: "#/$defs/step"
      }
    }
  }
}
```

### `$defs.select`
```json
{
  type: "object"
  properties: {
    name: {
      type: "string"
    }
    source: {
      type: "string"
    }
    expression: {
      type: "string"
    }
  }
  required: ["name"]
}
```

### `$defs.step`
```json
{
  type: "object"
  properties: {
    type: {
      type: "string"
      enum: [...4 items...]
    }
    source: {
      type: "string"
    }
    condition: {
      type: "string"
    }
    output: {
      type: "string"
    }
  }
  required: ["type"]
}
```

### `properties.build.description`
```json
"Describes the logical transformation process and its operational details."
```

### `properties.build.properties`
```json
{
  transformation: {
    type: "object"
    properties: {
      pattern: {
        type: "string"
        enum: [...4 items...]
        default: "hybrid-reference"
        description: "The transformation build pattern used."
      }
      engine: {
        type: "string"
        description: "The transformation engine used."
      }
      properties: {
        type: "object"
        description: "Pattern-specific properties for the build transformation."
        oneOf: [...4 items...]
      }
    }
    required: ["pattern", "engine", "properties"]
  }
  execution: {
    type: "object"
    properties: {
      trigger: {
        $ref: "#/$defs/trigger"
      }
      runtime: {
        $ref: "#/$defs/runtime"
      }
      retries: {
        $ref: "#/$defs/retryPolicy"
      }
      notifications: {
        type: "array"
        items: {
          $ref: "#/$defs/notification"
        }
      }
    }
  }
}
```

### `properties.build.type`
```json
"object"
```

## ❌ Removed Properties

### `$defs.accessGrant.properties.principal.description`
```json
"e.g., group:analysts, user:name@company.com, gcp_service_account:..., aws_iam_role:..."
```

### `$defs.accessGrant.properties.principal.pattern`
```json
"^(group|user|gcp_service_account|aws_iam_role):.+$"
```

### `$defs.accessGrant.required`
```json
[]
```

### `$defs.build`
```json
{
  type: "object"
  description: "Describes the logical transformation process and its operational details."
  properties: {
    engine: {
      type: "string"
      description: "The transformation engine used. Provided examples cover common cloud services, but any string is val..."
      examples: [...13 items...]
    }
    model: {
      type: "string"
      description: "A reference to the specific model or script (e.g., dbt model path, git URI to a SQL file)."
    }
    config: {
      type: "object"
      description: "Engine-specific configuration key-value pairs."
      additionalProperties: true
    }
    trigger: {
      $ref: "#/$defs/trigger"
    }
    runtime: {
      $ref: "#/$defs/runtime"
    }
    ... (2 more)
  }
  required: ["engine", "model"]
}
```

### `$defs.column.properties.semantic.description`
```json
"Reference to an ontology term or glossary ID."
```

### `$defs.column.properties.tags.description`
```json
"Semantic tags like 'primary_key', 'foreign_key', 'pii'."
```

### `$defs.column.properties.type.description`
```json
"The physical data type."
```

### `$defs.expose.properties.privacy.description`
```json
"A list of privacy treatments applied to columns in this port."
```

### `$defs.expose.properties.quality.description`
```json
"A list of quality rules specific to this port."
```

### `$defs.expose.properties.tags.properties.archetype.description`
```json
"The modeling archetype of the port."
```

### `$defs.expose.properties.type.examples`
```json
[...17 items...]
```

### `$defs.governance.properties.rules`
```json
{
  type: "array"
  items: {
    type: "object"
    properties: {
      name: {
        type: "string"
      }
      requirement: {
        type: "string"
      }
    }
    required: ["name", "requirement"]
  }
}
```

### `$defs.location.properties.format.examples`
```json
[...6 items...]
```

### `$defs.mapping.description`
```json
"Defines the transformation for a single target column, explicitly separating source columns for line..."
```

### `$defs.mapping.properties.rule.description`
```json
"The transformation logic or function to compute the target column."
```

### `$defs.mapping.properties.sources.description`
```json
"An array of input columns used, for automated lineage generation."
```

### `$defs.mapping.properties.target.description`
```json
"The name of the target column in the output schema."
```

### `$defs.notification.required`
```json
[]
```

### `$defs.qualityRule.properties.rule.description`
```json
"The rule to be enforced (e.g., 'not_null', 'unique', or a SQL predicate)."
```

### `$defs.relationship.properties.to.description`
```json
"The 'id' of the target port for the relationship."
```

### `$defs.runtime.properties.platform.description`
```json
"The runtime platform. Provided examples cover common cloud orchestrators, but any string is valid."
```

### `$defs.runtime.properties.platform.examples`
```json
[...10 items...]
```

### `$defs.runtime.required`
```json
[]
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

### `$defs.sla.description`
```json
"Defines the Service Level Objectives for the entire data product."
```

### `$defs.sla.properties.availabilityPct.description`
```json
"Expected uptime percentage."
```

### `$defs.sla.properties.freshnessMinutes.description`
```json
"Maximum data latency in minutes."
```

### `$defs.sla.properties.latencyMs.description`
```json
"Maximum query latency in milliseconds."
```

### `properties.build.$ref`
```json
"#/$defs/build"
```

## 📝 Modified Properties

### `$defs.expose.properties.mappings.description`

**Before:**
```json
"Declarative transformation logic that separates lineage from rules."
```

**After:**
```json
"OPTIONAL. Column-level lineage and rules for governance. SHOULD be generated from build.transformati..."
```

### `$defs.expose.properties.type.description`

**Before:**
```json
"The physical type of the output. Provided examples cover common cloud services, but any string is va..."
```

**After:**
```json
"The physical type of the output."
```

### `$defs.location.properties.properties.description`

**Before:**
```json
"Technology-specific properties. E.g., for BigQuery: { 'project': '...', 'dataset': '...', 'table': '..."
```

**After:**
```json
"Technology-specific properties (e.g., dataset, table, bucket)."
```

### `$defs.trigger.oneOf`

**Before:**
```json
[{"properties": {"type": {"const": "schedule"}, "cron": {"type": "string", "description": "A standard cron expression.", "pattern": "^((?:\\*|\\d+(?:-\\d+)?(?:,\\d+(?:-\\d+)?)*)(?:/\\d+)?\\s+){4,5}(?:\\*|\\d+(?:-\\d+)?(?:,\\d+(?:-\\d+)?)*)(?:/\\d+)?$"}}, "required": ["type", "cron"]}, {"properties": {"type": {"const": "event"}, "eventType": {"type": "string"}}, "required": ["type", "eventType"]}, {"properties": {"type": {"const": "manual"}}, "required": ["type"]}]
```

**After:**
```json
[{"properties": {"type": {"const": "schedule"}, "cron": {"type": "string"}}, "required": ["type", "cron"]}, {"properties": {"type": {"const": "event"}, "eventType": {"type": "string"}}, "required": ["type", "eventType"]}, {"properties": {"type": {"const": "manual"}}, "required": ["type"]}]
```

### `$id`

**Before:**
```json
"https://open-data-protocol.org/fluid/fluid.schema.v2.3.json"
```

**After:**
```json
"https://open-data-protocol.org/fluid/fluid.schema.v0.3.0.json"
```

### `description`

**Before:**
```json
"A comprehensive, production-ready schema for FLUID data product contracts. This version adds stricte..."
```

**After:**
```json
"A comprehensive, production-ready schema for FLUID data product contracts. Version 0.3.0 introduces ..."
```

### `properties.fluidVersion.examples`

**Before:**
```json
["2.3.0"]
```

**After:**
```json
["0.3.0"]
```
