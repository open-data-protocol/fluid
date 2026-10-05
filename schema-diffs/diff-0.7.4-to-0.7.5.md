# Schema Changes: 0.7.4 → 0.7.5

**Total changes:** 26
- ✅ Added: 18
- ❌ Removed: 0
- 📝 Modified: 8

<!-- HUMAN-NOTE:START -->
> **Note — 0.7.5 re-vendored.** The 0.7.5 schema first published here was the
> reference implementation's pre-GA copy (identical to forge-cli v0.10.0's, from
> while 0.7.5 was still a preview). It has been replaced, byte for byte, by the
> copy forge-cli v0.18.1 ships, and this diff regenerated. Against the earlier
> copy, the GA schema adds the `pgvector` platform, the `pgvector_table` format,
> `binding.vectorConfig`, and the Iceberg catalog-profile (`catalog`,
> `warehouse`, `uri`, `partitionBy`), Redshift Serverless (`namespace`,
> `workgroup`, `iam_role_arn`, `external_schema`, `glue_database`) and Kinesis
> (`stream`) location fields. `scripts/check-compat.py --from 0.7.4 --to 0.7.5`
> reports no narrowing.
<!-- HUMAN-NOTE:END -->

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

### `$defs.binding.properties.vectorConfig`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.5: vector / embeddings output-port configuration (platform 'pgvector', format 'pgvector_..."
  required: ["dimensions"]
  properties: {
    dimensions: {
      type: "integer"
      minimum: 1
      maximum: 16000
      description: "Embedding vector width (e.g. 1536 for OpenAI text-embedding-3-small, 1024 for Cohere embed-english-l..."
    }
    embeddingModel: {
      type: "string"
      description: "Provenance: the embedding model that produces the vectors (e.g. 'text-embedding-3-small'). Recorded ..."
    }
    vectorType: {
      type: "string"
      enum: ["vector", "halfvec"]
      default: "vector"
      description: "pgvector column type: 'vector' (float32, up to 2000 dims) or 'halfvec' (float16, half the storage, u..."
    }
    indexType: {
      type: "string"
      enum: ["hnsw", "ivfflat", "none"]
      default: "hnsw"
      description: "ANN index built on the embedding column. 'hnsw' (higher recall / lower query latency, buildable befo..."
    }
    distanceMetric: {
      type: "string"
      enum: [...4 items...]
      default: "cosine"
      description: "Distance function the index optimises for → pgvector operator class: cosine→vector_cosine_ops, l2→ve..."
    }
    ... (4 more)
  }
}
```

### `$defs.bindingLocation.properties.catalog`
```json
{
  type: "string"
  description: "NEW in v0.7.5: Iceberg catalog kind/profile selector — maps to iceberg.catalog.type (e.g. glue, rest..."
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

### `$defs.bindingLocation.properties.external_schema`
```json
{
  type: "string"
  description: "NEW in v0.7.5: Redshift external (Spectrum) schema name created over a Glue database via the redshif..."
}
```

### `$defs.bindingLocation.properties.glue_database`
```json
{
  type: "string"
  description: "NEW in v0.7.5: Glue Data Catalog database that backs the Redshift external schema."
}
```

### `$defs.bindingLocation.properties.iam_role_arn`
```json
{
  type: "string"
  description: "NEW in v0.7.5: ARN of the IAM role attached to the Redshift Serverless namespace / used by the redsh..."
}
```

### `$defs.bindingLocation.properties.kafka_cluster_id`
```json
{
  type: "string"
  description: "NEW in v0.7.5: Confluent Cloud Kafka cluster id (lkc-xxxxx) the Tableflow topic belongs to."
}
```

### `$defs.bindingLocation.properties.namespace`
```json
{
  type: "string"
  description: "NEW in v0.7.5: Amazon Redshift Serverless namespace name \u2014 maps to aws_redshiftserverless_namespace."
}
```

### `$defs.bindingLocation.properties.partitionBy`
```json
{
  type: "array"
  items: {
    type: "string"
  }
  description: "NEW in v0.7.5: Iceberg partition columns — a FLUID abstraction over the Iceberg PARTITIONED BY / Par..."
}
```

### `$defs.bindingLocation.properties.stream`
```json
{
  type: "string"
  description: "NEW in v0.7.5: AWS Kinesis Data Stream name — maps to aws_kinesis_stream in the streaming IaC emitte..."
}
```

### `$defs.bindingLocation.properties.uri`
```json
{
  type: "string"
  description: "NEW in v0.7.5: REST Iceberg catalog endpoint URL — the canonical Iceberg REST 'uri' property (maps t..."
}
```

### `$defs.bindingLocation.properties.warehouse`
```json
{
  type: "string"
  description: "NEW in v0.7.5: Iceberg warehouse — the canonical Iceberg REST 'warehouse' property (maps to iceberg...."
}
```

### `$defs.bindingLocation.properties.workgroup`
```json
{
  type: "string"
  description: "NEW in v0.7.5: Amazon Redshift Serverless workgroup name \u2014 maps to aws_redshiftserverless_workgroup."
}
```

## 📝 Modified Properties

### `$defs.binding.properties.format.description`

**Before:**
```json
"Binding format. NEW in v0.7.4: 'postgres_table' (PostgreSQL driver), 'athena_table' / 'glue_table' (..."
```

**After:**
```json
"Binding format. NEW in v0.7.5: 'pgvector_table' — a pgvector embeddings table target for the vector ..."
```

### `$defs.binding.properties.format.enum`

**Before:**
```json
[...21 items...]
```

**After:**
```json
[...22 items...]
```

### `$defs.binding.properties.platform.description`

**Before:**
```json
"Target platform. NEW in v0.7.4: 'postgres' for the MCP output-port PostgreSQL driver (AWS Athena use..."
```

**After:**
```json
"Target platform. NEW in v0.7.5: 'pgvector' for the vector/embeddings output port (pgvector-on-Postgr..."
```

### `$defs.binding.properties.platform.enum`

**Before:**
```json
[...10 items...]
```

**After:**
```json
[...12 items...]
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
