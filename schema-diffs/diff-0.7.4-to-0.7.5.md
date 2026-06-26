# Schema Changes: 0.7.4 → 0.7.5

**Total changes:** 13
- ✅ Added: 7
- ❌ Removed: 0
- 📝 Modified: 6

---

## ✅ Added Properties

### `$defs.acquisitionPattern.properties.kafka-connect.properties.iceberg_catalog_overrides`
```json
{
  type: "object"
  additionalProperties: {
    type: "string"
  }
  description: "Operator escape hatch: connector config keys merged LAST over the derived Iceberg sink config."
}
```

### `$defs.acquisitionPattern.properties.kafka-connect.properties.iceberg_sink_enabled`
```json
{
  type: "boolean"
  description: "Opt-in: derive the Iceberg sink connector config. Defaults OFF when a hand-written sink_connector_co..."
}
```

### `$defs.acquisitionPattern.properties.kafka-connect.properties.sink_topics`
```json
{
  type: "array"
  items: {
    type: "string"
  }
  description: "Explicit topics the derived Iceberg sink consumes (else derived from source streams)."
}
```

### `$defs.acquisitionPattern.properties.kafka-connect.properties.streamingSink`
```json
{
  type: "object"
  additionalProperties: false
  description: "Optional Iceberg streaming-sink tuning (RFC \u00a76.2). All keys optional."
  properties: {
    commitIntervalMs: {
      type: "integer"
      minimum: 1
    }
    routeField: {
      type: "string"
    }
    dynamicEnabled: {
      type: "boolean"
    }
    autoCreate: {
      type: "boolean"
    }
    evolveSchema: {
      type: "boolean"
    }
    ... (2 more)
  }
}
```

### `$defs.bindingLocation.properties.confluent_role_arn`
```json
{
  type: "string"
  description: "NEW in v0.7.5: ARN of the pre-created AWS IAM role Confluent Tableflow assumes (byob_aws). Its trust..."
}
```

### `$defs.bindingLocation.properties.environment_id`
```json
{
  type: "string"
  description: "NEW in v0.7.5: Confluent Cloud environment id (env-xxxxx) for the Tableflow emitter."
}
```

### `$defs.bindingLocation.properties.kafka_cluster_id`
```json
{
  type: "string"
  description: "NEW in v0.7.5: Confluent Cloud Kafka cluster id (lkc-xxxxx) the Tableflow topic belongs to."
}
```

## 📝 Modified Properties

### `$defs.binding.properties.platform.description`

**Before:**
```json
"Target platform. NEW in v0.7.4: 'postgres' for the MCP output-port PostgreSQL driver (AWS Athena use..."
```

**After:**
```json
"Target platform. NEW in v0.7.5: 'confluent' for the Confluent Cloud Tableflow managed Kafka→Iceberg ..."
```

### `$defs.binding.properties.platform.enum`

**Before:**
```json
[...10 items...]
```

**After:**
```json
[...11 items...]
```

### `$id`

**Before:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.4.json"
```

**After:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.5.json"
```

### `description`

**Before:**
```json
"FLUID Data Product contract (v0.7.4). Runtime agentPolicy Enforcement Release.

🔥 NEW in v0.7.4:
• M..."
```

**After:**
```json
"FLUID Data Product contract (v0.7.5). Streaming Kafka→Iceberg Sink & Confluent Tableflow Release.

🔥..."
```

### `properties.fluidVersion.enum`

**Before:**
```json
["0.7.3", "0.7.4"]
```

**After:**
```json
["0.7.3", "0.7.4", "0.7.5"]
```

### `title`

**Before:**
```json
"FLUID 0.7.4 \u2014 Runtime agentPolicy Enforcement at the MCP Gateway"
```

**After:**
```json
"FLUID 0.7.5 \u2014 Streaming Kafka\u2192Iceberg Sink & Confluent Tableflow"
```
