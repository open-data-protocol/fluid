# Schema Changes: 0.7.1 → 0.7.2

**Total changes:** 27
- ✅ Added: 14
- ❌ Removed: 2
- 📝 Modified: 11

---

## ✅ Added Properties

### `$defs.binding.properties.icebergConfig`
```json
{
  type: "object"
  description: "Apache Iceberg table format configuration"
  additionalProperties: false
  properties: {
    writeVersion: {
      type: "integer"
      enum: [1, 2]
      description: "Iceberg table format version"
    }
    fileFormat: {
      type: "string"
      enum: ["parquet", "orc", "avro"]
      description: "Underlying file format for data files"
    }
    partitionSpec: {
      type: "array"
      description: "Partition transformation specifications"
      items: {
        type: "object"
        required: ["sourceColumn", "transform"]
        properties: {
          name: {
            type: "string"
            description: "Partition field name"
          }
          sourceColumn: {
            type: "string"
            description: "Source column for partitioning"
          }
          transform: {
            type: "string"
            enum: [...7 items...]
            description: "Partition transform function"
          }
          numBuckets: {
            type: "integer"
            description: "Number of buckets (for bucket transform)"
          }
          width: {
            type: "integer"
            description: "Truncate width (for truncate transform)"
          }
        }
      }
    }
    sortOrder: {
      type: "array"
      description: "Sort order specifications for data files"
      items: {
        type: "object"
        required: ["column"]
        properties: {
          column: {
            type: "string"
            description: "Column to sort by"
          }
          direction: {
            type: "string"
            enum: ["asc", "desc"]
            description: "Sort direction"
          }
          nullOrder: {
            type: "string"
            enum: ["nulls-first", "nulls-last"]
            description: "NULL value ordering"
          }
        }
      }
    }
    properties: {
      type: "object"
      description: "Iceberg table properties"
      additionalProperties: {
        type: "string"
      }
    }
  }
}
```

### `$defs.binding.properties.properties`
```json
{
  type: "object"
  description: "Provider-specific binding properties (e.g., cluster_by, comment for Snowflake)."
  additionalProperties: true
}
```

### `$defs.column.properties.type.anyOf`
```json
[{"type": "string", "enum": ["string", "text", "varchar", "varchar2", "nvarchar", "char", "nchar", "character", "clob", "int", "integer", "int2", "int4", "int8", "int16", "int32", "int64", "tinyint", "smallint", "mediumint", "bigint", "long", "longint", "serial", "bigserial", "float", "float4", "float8", "float32", "float64", "double", "real", "decimal", "dec", "numeric", "number", "bignumeric", "money", "boolean", "bool", "bit", "date", "time", "datetime", "datetime2", "smalldatetime", "timestamp", "timestamptz", "timestamp_tz", "timestamp_ntz", "timestamp_ltz", "timestampntz", "interval", "year", "variant", "object", "array", "struct", "map", "record", "row", "json", "jsonb", "super", "binary", "varbinary", "bytes", "blob", "bytea", "raw", "geography", "geometry", "geom", "point", "uuid", "uniqueidentifier", "guid", "enum", "hll"]}, {"type": "string", "pattern": "(?i)^\\s*(string|text|varchar|varchar2|nvarchar|char|nchar|character|clob|int|integer|int2|int4|int8|int16|int32|int64|tinyint|smallint|mediumint|bigint|long|longint|serial|bigserial|float|float4|float8|float32|float64|double|real|double\\s+precision|decimal|dec|numeric|number|bignumeric|money|boolean|bool|bit|date|time|datetime|datetime2|smalldatetime|timestamp|timestamptz|timestamp_tz|timestamp_ntz|timestamp_ltz|timestampntz|timestamp\\s+with(out)?\\s+time\\s+zone|interval|year|variant|object|array|struct|map|record|row|json|jsonb|super|binary|varbinary|bytes|blob|bytea|raw|geography|geometry|geom|point|uuid|uniqueidentifier|guid|enum|hll)\\s*(\\(\\s*[0-9A-Za-z_,\\s'\\\"-]*\\s*\\))?\\s*$"}]
```

### `$defs.column.properties.type.description`
```json
"Column data type. Accepts a canonical FLUID/SQL type name (case-insensitive) or a parameterized form..."
```

### `$defs.expose.properties.crawler`
```json
{
  type: "object"
  description: "AWS Glue crawler configuration for auto-discovery of schema from S3 paths."
  properties: {
    name: {
      type: "string"
      description: "Glue crawler name."
    }
    role: {
      type: "string"
      description: "IAM role ARN for the crawler."
    }
    schedule: {
      type: "string"
      description: "Cron schedule expression (e.g., 'cron(0 6 * * ? *)')."
    }
    classifiers: {
      type: "array"
      description: "Custom classifier names to apply."
      items: {
        type: "string"
      }
    }
    schemaChangePolicy: {
      type: "object"
      description: "Policy for schema changes detected by the crawler."
      properties: {
        updateBehavior: {
          type: "string"
          enum: ["UPDATE_IN_DATABASE", "LOG"]
        }
        deleteBehavior: {
          type: "string"
          enum: ["LOG", "DELETE_FROM_DATABASE", "DEPRECATE_IN_DATABASE"]
        }
      }
    }
  }
}
```

### `$defs.expose.properties.description`
```json
{
  type: "string"
  description: "Detailed description of the exposed resource."
}
```

### `$defs.expose.properties.iceberg`
```json
{
  type: "object"
  description: "AWS Glue Iceberg table management configuration (snapshots, compaction)."
  properties: {
    writeFormat: {
      type: "string"
      enum: ["parquet", "orc", "avro"]
      description: "Underlying file format for Iceberg data files."
    }
    snapshotRetention: {
      type: "object"
      description: "Snapshot retention policy."
      properties: {
        maxSnapshotAgeMs: {
          type: "integer"
          description: "Maximum age of snapshots in milliseconds."
        }
        minSnapshotsToKeep: {
          type: "integer"
          description: "Minimum number of snapshots to retain."
        }
      }
    }
    compaction: {
      type: "object"
      description: "Iceberg compaction settings."
      properties: {
        enabled: {
          type: "boolean"
        }
        targetFileSizeMb: {
          type: "integer"
          description: "Target file size in MB after compaction."
        }
      }
    }
  }
}
```

### `$defs.expose.properties.semantics`
```json
{
  $ref: "#/$defs/semanticModel"
  description: "NEW in v0.7.2: Semantic model definition mapping physical columns to business concepts. Defines enti..."
}
```

### `$defs.exposeContract.properties.quality`
```json
{
  type: "array"
  description: "Simplified SQL-expression data quality rules (alternate form of dq.rules for inline assertions)."
  items: {
    type: "object"
    required: ["rule", "expression", "severity"]
    properties: {
      rule: {
        type: "string"
        description: "Rule identifier."
      }
      expression: {
        type: "string"
        description: "SQL or boolean expression that must evaluate to true."
      }
      severity: {
        type: "string"
        enum: ["error", "warning", "info"]
        description: "Severity when the rule fails."
      }
    }
  }
}
```

### `$defs.notification.additionalProperties`
```json
false
```

### `$defs.semanticModel`
```json
{
  type: "object"
  description: "NEW in v0.7.2: Semantic model definition for an exposed interface. Maps physical columns to business..."
  additionalProperties: false
  properties: {
    name: {
      type: "string"
      description: "Human-readable name for this semantic model."
    }
    description: {
      type: "string"
      description: "Business context explaining what this semantic model represents."
    }
    defaultAggTimeDimension: {
      type: "string"
      description: "Default time dimension used for measure aggregation. Can be overridden per-measure."
    }
    entities: {
      type: "array"
      description: "Join keys with type annotations. Entities connect this table to others in the semantic graph."
      items: {
        type: "object"
        additionalProperties: false
        required: ["name", "type"]
        properties: {
          name: {
            type: "string"
            description: "Entity name (e.g., 'order', 'customer')."
          }
          type: {
            type: "string"
            enum: [...4 items...]
            description: "Entity key type: primary (unique, complete), foreign (references another table), unique (unique, pos..."
          }
          expr: {
            type: "string"
            description: "Column expression. Defaults to entity name if omitted."
          }
          description: {
            type: "string"
          }
        }
      }
    }
    measures: {
      type: "array"
      description: "Aggregatable column expressions. Measures are the atomic building blocks from which metrics are comp..."
      items: {
        type: "object"
        additionalProperties: false
        required: ["name", "agg"]
        properties: {
          name: {
            type: "string"
            description: "Measure name (e.g., 'total_amount', 'order_count')."
          }
          description: {
            type: "string"
          }
          agg: {
            type: "string"
            enum: [...8 items...]
            description: "Aggregation function applied to the expression."
          }
          expr: {
            type: "string"
            description: "SQL expression to aggregate. Defaults to measure name if omitted."
          }
          aggTimeDimension: {
            type: "string"
            description: "Override the model-level default time dimension for this measure."
          }
          ... (2 more)
        }
      }
    }
    ... (4 more)
  }
  examples: [{"name": "orders_revenue_model", "description": "Canonical semantic model for revenue analytics", "defaultAggTimeDimension": "order_date", "entities": [{"name": "order", "type": "primary", "expr": "order_id"}, {"name": "customer", "type": "foreign", "expr": "customer_id"}], "measures": [{"name": "order_amount", "agg": "sum", "expr": "amount", "description": "Sum of all order amounts"}, {"name": "order_count", "agg": "count_distinct", "expr": "order_id", "createMetric": true}], "dimensions": [{"name": "order_date", "type": "time", "expr": "completed_at", "typeParams": {"timeGranularity": "day"}}, {"name": "region", "type": "categorical"}], "metrics": [{"name": "net_revenue", "description": "GAAP-compliant net revenue: completed orders minus discounts, excluding refunds", "type": "derived", "inputMetrics": ["gross_revenue", "total_discounts"], "expr": "gross_revenue - total_discounts", "owner": "finance-data@company.com"}, {"name": "gross_revenue", "description": "Total value of completed orders", "type": "simple", "measure": "order_amount", "filter": "status = 'completed'"}]}]
}
```

### `properties.metadata.properties.provenance`
```json
{
  type: "object"
  description: "Generation envelope injected by `fluid forge` / `fluid init` — records how, when and by which tool/c..."
  properties: {
    schema_version: {
      type: "integer"
      description: "Envelope schema version."
    }
    kind: {
      type: "string"
      description: "Envelope discriminator, e.g. 'ContractMetadata'."
    }
    generated_at: {
      type: "string"
      format: "date-time"
      description: "ISO 8601 UTC timestamp of generation."
    }
    generated_by: {
      type: "object"
      description: "Tool, version and command that generated the contract."
      properties: {
        tool: {
          type: "string"
        }
        version: {
          type: "string"
        }
        command: {
          type: "string"
        }
      }
    }
  }
}
```

### `properties.metadata.properties.tags`
```json
{
  $ref: "#/$defs/tags"
  description: "Product-level tags on metadata for discovery and categorization."
}
```

### `properties.orchestration`
```json
{
  $ref: "#/$defs/orchestration"
  description: "Top-level orchestration configuration for scheduling and workflow engines."
}
```

## ❌ Removed Properties

### `$defs.column.properties.type.minLength`
```json
1
```

### `$defs.column.properties.type.type`
```json
"string"
```

## 📝 Modified Properties

### `$defs.accessPolicy.properties.grants.items.properties.permissions.items.enum`

**Before:**
```json
[...9 items...]
```

**After:**
```json
[...10 items...]
```

### `$defs.binding.properties.format.enum`

**Before:**
```json
[...13 items...]
```

**After:**
```json
[...14 items...]
```

### `$defs.build.properties.engine.enum`

**Before:**
```json
[...5 items...]
```

**After:**
```json
[...6 items...]
```

### `$defs.sensitivityLevel.enum`

**Before:**
```json
[...11 items...]
```

**After:**
```json
[...12 items...]
```

### `$id`

**Before:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.1.json"
```

**After:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.2.json"
```

### `description`

**Before:**
```json
"FLUID Data Product contract (v0.7.1). Provider-First Orchestration + Agentic Governance Release:

🔥 ..."
```

**After:**
```json
"FLUID Data Product contract (v0.7.2). Semantic Truth Engine Release:

🔥 NEW in v0.7.2:
• Semantic mo..."
```

### `examples`

**Before:**
```json
[{"fluidVersion": "0.7.1", "kind": "DataProduct", "id": "gold.customer.analytics_360_v1", "name": "Customer 360 Analytics", "description": "Unified customer profiles with ML-driven insights", "domain": "Customer Experience", "tags": ["customer-data", "analytics", "gold-layer"], "labels": {"team": "customer-analytics", "criticality": "high", "cost-center": "engineering"}, "metadata": {"layer": "Gold", "owner": {"team": "customer-analytics", "email": "customer-analytics@company.com"}, "businessContext": {"domain": "Customer Experience", "subdomain": "Customer Intelligence"}}, "exposes": [{"exposeId": "customer_profiles", "title": "Unified Customer Profiles", "version": "2.1.0", "kind": "table", "tags": ["pii", "customer-facing", "real-time"], "labels": {"sensitivity": "high", "retention": "7-years", "region": "us-central1"}, "contract": {"schema": [{"name": "customer_id", "type": "STRING", "required": true, "description": "Unique customer identifier", "sensitivity": "cleartext", "tags": ["identifier", "primary-key"], "labels": {"business-name": "Customer ID", "data-category": "identifier"}}]}, "binding": {"platform": "gcp", "format": "bigquery_table", "location": {"project": "company-data", "dataset": "gold_customer", "table": "profiles_v1"}}}]}]
```

**After:**
```json
[{"fluidVersion": "0.5.7", "kind": "DataProduct", "id": "gold.customer.analytics_360_v1", "name": "Customer 360 Analytics", "description": "Unified customer profiles with ML-driven insights", "domain": "Customer Experience", "tags": ["customer-data", "analytics", "gold-layer"], "labels": {"team": "customer-analytics", "criticality": "high", "cost-center": "engineering"}, "metadata": {"layer": "Gold", "owner": {"team": "customer-analytics", "email": "customer-analytics@company.com"}, "businessContext": {"domain": "Customer Experience", "subdomain": "Customer Intelligence"}}, "exposes": [{"exposeId": "customer_profiles", "title": "Unified Customer Profiles", "version": "2.1.0", "kind": "table", "tags": ["pii", "customer-facing", "real-time"], "labels": {"sensitivity": "high", "retention": "7-years", "region": "us-central1"}, "contract": {"schema": [{"name": "customer_id", "type": "STRING", "required": true, "description": "Unique customer identifier", "sensitivity": "cleartext", "tags": ["identifier", "primary-key"], "labels": {"business-name": "Customer ID", "data-category": "identifier"}}]}, "binding": {"platform": "gcp", "format": "bigquery_table", "location": {"project": "company-data", "dataset": "gold_customer", "table": "profiles_v1"}}}]}]
```

### `properties.fluidVersion.const`

**Before:**
```json
"0.7.1"
```

**After:**
```json
"0.7.2"
```

### `properties.fluidVersion.description`

**Before:**
```json
"Contract schema version. Must be exactly '0.7.1' for agentic governance + provider-first orchestrati..."
```

**After:**
```json
"Contract schema version. Must be exactly '0.7.2' for semantic truth engine + agentic governance + pr..."
```

### `properties.fluidVersion.examples`

**Before:**
```json
["0.7.1"]
```

**After:**
```json
["0.7.2"]
```

### `title`

**Before:**
```json
"FLUID 0.7.1 \u2014 Provider-First Orchestration + Agentic Governance"
```

**After:**
```json
"FLUID 0.7.2 \u2014 Semantic Truth Engine"
```
