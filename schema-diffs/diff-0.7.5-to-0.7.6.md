# Schema Changes: 0.7.5 → 0.7.6

**Total changes:** 40
- ✅ Added: 27
- ❌ Removed: 0
- 📝 Modified: 13

<!-- HUMAN-NOTE:START -->
> **Note — 0.7.6 is a preview.** 0.7.5 is the latest stable version. A contract
> opts in to 0.7.6 by declaring `fluidVersion: "0.7.6"`; the reference
> implementation (data-product-forge 0.18.1) never picks a preview as the
> default for a contract that omits `fluidVersion`. A preview can still change
> before it becomes stable, so this diff describes the copy vendored from
> forge-cli v0.18.1. `scripts/check-compat.py --from 0.7.5
> --to 0.7.6` reports no narrowing.
<!-- HUMAN-NOTE:END -->

---

## ✅ Added Properties

### `$defs.acquisitionSink.properties.catalogAuth`
```json
{
  type: "object"
  description: "NEW in v0.7.6: How the Iceberg sink config forge-cli DERIVES (kafka-connect with sink.format iceberg..."
  additionalProperties: false
  required: ["type"]
  properties: {
    type: {
      type: "string"
      enum: ["oauth2", "bearer"]
      description: "oauth2: OAuth2 client credentials against oauth2ServerUri. bearer: a static bearer token."
    }
    credentialEnv: {
      type: "string"
      pattern: "^[A-Za-z_][A-Za-z0-9_]*(?![\\s\\S])"
      not: {
        pattern: "(?:^|_)(?=[A-Za-z]*[0-9])[A-Za-z0-9]{20,}(?:_|$)"
      }
      description: "type oauth2: the NAME of the environment variable holding client_id:client_secret (Iceberg splits it..."
    }
    oauth2ServerUri: {
      type: "string"
      pattern: "^https?://[^\\s/?#@]+(?:[/?#]\\S*)?$"
      not: {
        pattern: "\\$\\{|[\\x00-\\x1f\\x7f]|^\\s*env:"
      }
      description: "type oauth2: absolute URL starting with a lowercase http:// or https:// of the identity provider's t..."
    }
    scope: {
      type: "string"
      minLength: 1
      not: {
        pattern: "\\$\\{|[\\x00-\\x1f\\x7f]|^\\s*env:"
      }
      description: "type oauth2: the OAuth2 scope to request (Iceberg's default, catalog, is not one most identity provi..."
    }
    audience: {
      type: "string"
      minLength: 1
      not: {
        pattern: "\\$\\{|[\\x00-\\x1f\\x7f]|^\\s*env:"
      }
      description: "type oauth2, optional: sent as the audience parameter on the token request."
    }
    ... (2 more)
  }
  ... (1 more)
}
```

### `$defs.binding.allOf`
```json
[{"if": {"properties": {"platform": {"const": "gcp"}}, "required": ["platform"]}, "then": {"properties": {"encryption": {"properties": {"kms": {"not": {"pattern": "^(alias/|arn:)"}}}}, "principals": {"additionalProperties": {"anyOf": [{"type": "string", "pattern": "^(user|group|serviceAccount|domain):.+$"}, {"type": "array", "items": {"type": "string", "pattern": "^(user|group|serviceAccount|domain):.+$"}}]}}}}}, {"if": {"properties": {"platform": {"const": "aws"}}, "required": ["platform"]}, "then": {"properties": {"encryption": {"properties": {"kms": {"not": {"pattern": "^projects/"}}}}, "principals": {"additionalProperties": {"anyOf": [{"type": "string", "pattern": "^arn:aws[a-z0-9-]*:iam::"}, {"type": "array", "items": {"type": "string", "pattern": "^arn:aws[a-z0-9-]*:iam::"}}]}}}}}]
```

### `$defs.binding.properties.encryption`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.6: Encryption at rest for an AWS S3 binding or a GCP BigQuery binding. Absent: nothing i..."
  properties: {
    kms: {
      type: "string"
      default: "product"
      anyOf: [...4 items...]
      description: "NEW in v0.7.6: The KMS key the bucket's objects are encrypted with (SSE-KMS with an S3 Bucket Key). ..."
    }
  }
}
```

### `$defs.binding.properties.packaging`
```json
{
  $ref: "#/$defs/packaging"
  description: "NEW in v0.7.6: Per-exposure packaging override — key-wise precedence over the contract-wide top-leve..."
}
```

### `$defs.binding.properties.principals`
```json
{
  type: "object"
  description: "NEW in v0.7.6: Maps the contract's LOGICAL principals (accessPolicy.grants[].principal and exposes[]..."
  propertyNames: {
    minLength: 1
  }
  additionalProperties: {
    anyOf: [{"type": "string", "minLength": 1}, {"type": "array", "items": {"type": "string", "minLength": 1}, "uniqueItems": true}]
  }
}
```

### `$defs.bindingGovernance.properties.lakeFormation.properties.bucketPolicy`
```json
{
  type: "string"
  enum: ["cross-account", "none", "all-grantees"]
  default: "cross-account"
  description: "NEW in v0.7.6: Which grants[] principals get a statement in the aws_s3_bucket_policy emitted beside ..."
}
```

### `$defs.bindingGovernance.properties.lakeFormation.properties.maskedViews`
```json
{
  type: "object"
  additionalProperties: false
  required: ["definer", "validationConnection"]
  description: "Where the protected Glue Data Catalog views of the expose's masked columns come from (NEW in v0.7.6)..."
  properties: {
    definer: {
      type: "string"
      description: "ARN of the IAM role the views are defined as: Glue and Lake Formation must be allowed to assume it (..."
    }
    validationConnection: {
      type: "string"
      description: "The Glue connection of type VIEW_VALIDATION_ATHENA (WORKGROUP_NAME) Glue validates each view's SQL t..."
    }
  }
}
```

### `$defs.consumeRef.dependentRequired`
```json
{
  upstreamWorkspace: ["upstreamDigest"]
}
```

### `$defs.consumeRef.properties.upstreamDigest`
```json
{
  type: "string"
  pattern: "^sha256:[0-9a-f]{64}$"
  description: "Cross-mesh only. The contract digest this product was composed against, as sha256:<64 hex>. `fluid a..."
}
```

### `$defs.consumeRef.properties.upstreamWorkspace`
```json
{
  type: "string"
  minLength: 1
  description: "Cross-mesh only. Id of the federated workspace that owns this upstream, as declared in federation/up..."
}
```

### `$defs.consumerRef`
```json
{
  type: "object"
  additionalProperties: false
  required: ["name", "type"]
  $comment: "dbt-exposures-shaped (name/label/type/owner/url/maturity/description); exposeIds is the FLUID-native..."
  properties: {
    name: {
      $ref: "#/$defs/identifier"
      description: "Stable identifier for this consumer (unique within the contract)."
    }
    label: {
      type: "string"
      description: "Human-facing display name, e.g. \"Weekly Revenue Dashboard\"."
    }
    type: {
      type: "string"
      enum: [...5 items...]
      description: "What kind of artifact consumes this product."
    }
    owner: {
      type: "object"
      additionalProperties: false
      $comment: "Mirrors metadata.owner's vocabulary so 'owner' means one thing across the standard: team is the rout..."
      properties: {
        team: {
          type: "string"
          description: "Owning team for this consumer (routable identity, as in metadata.owner)."
        }
        email: {
          type: "string"
          format: "email"
          description: "Contact address for the consumer's owner."
        }
      }
    }
    url: {
      type: "string"
      description: "Link to the live artifact (dashboard URL, notebook, app)."
    }
    ... (3 more)
  }
}
```

### `$defs.exposeLifecycle`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    state: {
      $ref: "#/$defs/lifecycleState"
      description: "Unified lifecycle state vocabulary."
    }
    retention: {
      $ref: "#/$defs/isoDuration"
      description: "How long this expose's data is kept (ISO-8601 duration, e.g. P30D, P7Y). A declaration unless `expir..."
    }
    expire: {
      type: "boolean"
      default: false
      description: "NEW in v0.7.6: Delete stored data once it is older than `retention`. Default false, so a contract th..."
    }
    deprecationPolicy: {
      type: "object"
      additionalProperties: false
      properties: {
        noticePeriod: {
          $ref: "#/$defs/isoDuration"
        }
        contact: {
          type: "string"
        }
        replacement: {
          type: "string"
          description: "Reference to replacement data product or expose."
        }
        tags: {
          $ref: "#/$defs/tags"
          description: "Deprecation policy tags."
        }
        labels: {
          $ref: "#/$defs/labels"
          description: "Deprecation policy labels."
        }
      }
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Lifecycle tags for automation."
    }
    ... (1 more)
  }
  description: "NEW in v0.7.6: An expose's lifecycle. The same fields as the contract-root lifecycle, plus `expire`,..."
}
```

### `$defs.exposePolicy.properties.authz.properties.columnRestrictions.items.allOf`
```json
[{"if": {"properties": {"access": {"const": "mask"}}, "required": ["access"]}, "then": {"required": ["mask"]}}, {"if": {"required": ["mask"]}, "then": {"properties": {"access": {"const": "mask"}}, "required": ["access"]}}]
```

### `$defs.exposePolicy.properties.authz.properties.columnRestrictions.items.properties.access.description`
```json
"deny: the principal may not read the columns. allow: only the principals an allow names may read the..."
```

### `$defs.exposePolicy.properties.authz.properties.columnRestrictions.items.properties.columns.description`
```json
"Columns of this expose's schema."
```

### `$defs.exposePolicy.properties.authz.properties.columnRestrictions.items.properties.mask`
```json
{
  type: "string"
  enum: ["last_four", "first_four", "nullify"]
  description: "The masking rule an access: mask restriction applies, required with it and refused without it. last_..."
}
```

### `$defs.exposePolicy.properties.authz.properties.columnRestrictions.items.properties.principal.description`
```json
"Logical principal the restriction applies to, written as in accessPolicy (e.g. group:analysts@compan..."
```

### `$defs.exposePolicy.properties.authz.properties.rowFilters`
```json
{
  type: "array"
  description: "Row-level access control (NEW in v0.7.6). Each filter lets its principal read only the rows its wher..."
  items: {
    type: "object"
    additionalProperties: false
    required: ["principal", "where"]
    properties: {
      principal: {
        type: "string"
        description: "Logical principal the filter applies to, written as in accessPolicy; binding.principals maps it per ..."
      }
      name: {
        type: "string"
        pattern: "^[a-z][a-z0-9_]{0,62}$"
        description: "The filter's name on the platform (the row access policy or data cells filter); derived from the pri..."
      }
      where: {
        type: "string"
        minLength: 1
        description: "One SQL boolean expression over the expose's columns, e.g. consent_data_analytics = true AND is_supp..."
      }
      description: {
        type: "string"
      }
    }
  }
}
```

### `$defs.exposePolicy.properties.privacy.properties.masking.description`
```json
"Columns to treat before they land. The DuckDB acquisition runner rewrites each named column inside t..."
```

### `$defs.exposePolicy.properties.privacy.properties.masking.items.properties.params.description`
```json
"Strategy parameters. The runner accepts exactly these keys and refuses any other, including a litera..."
```

### `$defs.exposePolicy.properties.privacy.properties.masking.items.properties.params.properties`
```json
{
  saltEnv: {
    type: "string"
    pattern: "^[A-Z_][A-Z0-9_]{0,127}$"
    default: "FLUID_PII_HASH_SECRET"
    description: "NEW in v0.7.6: hash only. The environment variable holding the salt, at least 16 bytes. Unset or emp..."
  }
  keyEnv: {
    type: "string"
    pattern: "^[A-Z_][A-Z0-9_]{0,127}$"
    description: "NEW in v0.7.6: tokenize and encrypt. The environment variable holding the key. tokenize defaults to ..."
  }
  keepFirst: {
    type: "integer"
    minimum: 0
    maximum: 64
    default: 0
    description: "NEW in v0.7.6: mask only. Leading characters left as they are."
  }
  keepLast: {
    type: "integer"
    minimum: 0
    maximum: 64
    default: 4
    description: "NEW in v0.7.6: mask only. Trailing characters left as they are, so +46701234567 lands as ********456..."
  }
}
```

### `$defs.exposePolicy.properties.privacy.properties.masking.items.properties.strategy.description`
```json
"hash: lowercase hex SHA-256 of salt || value, deterministic so joins work (64 hex characters). mask:..."
```

### `$defs.packaging`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.6: Declarative packaging mode — per-container ownership for the OpenTofu IaC emit (RFC-p..."
  properties: {
    mode: {
      type: "string"
      enum: ["isolated", "shared"]
      description: "NEW in v0.7.6: Blanket ownership mode for every container kind. Default when the block is present: '..."
    }
    pool: {
      type: "string"
      minLength: 1
      description: "NEW in v0.7.6: Pool id of the platform-owned tenant pool this product writes into. REQUIRED (enforce..."
    }
    poolManifest: {
      type: "string"
      minLength: 1
      description: "NEW in v0.7.6: Optional path to the platform team's pool manifest file; snapshotted into the bundle ..."
    }
    containers: {
      type: "object"
      additionalProperties: false
      description: "NEW in v0.7.6: Per-container-kind ownership overrides — each key wins over `mode` for that kind, yie..."
      properties: {
        bucket: {
          $ref: "#/$defs/packagingContainerMode"
          description: "NEW in v0.7.6: Ownership of the object-store bucket (aws_s3_bucket / google_storage_bucket)."
        }
        database: {
          $ref: "#/$defs/packagingContainerMode"
          description: "NEW in v0.7.6: Ownership of the database container — covers Snowflake `database` AND AWS `glue_datab..."
        }
        dataset: {
          $ref: "#/$defs/packagingContainerMode"
          description: "NEW in v0.7.6: Ownership of the BigQuery dataset (google_bigquery_dataset)."
        }
        schema: {
          $ref: "#/$defs/packagingContainerMode"
          description: "NEW in v0.7.6: Ownership of the Snowflake schema (snowflake_schema)."
        }
        warehouse: {
          $ref: "#/$defs/packagingContainerMode"
          description: "NEW in v0.7.6: Ownership of the Snowflake warehouse (snowflake_warehouse) — isolated gives per-produ..."
        }
        ... (1 more)
      }
    }
  }
}
```

### `$defs.packagingContainerMode`
```json
{
  type: "string"
  enum: ["isolated", "shared"]
  description: "NEW in v0.7.6: Per-container ownership — 'isolated' (this product creates and owns it) or 'shared' (..."
}
```

### `$defs.semanticModel.properties.measures.items.properties.aggParams`
```json
{
  type: "object"
  additionalProperties: false
  description: "Aggregation parameters (mirrors dbt-semantic-interfaces agg_params). Currently used by agg=percentil..."
  properties: {
    percentile: {
      type: "number"
      minimum: 0
      maximum: 1
      description: "Percentile in [0, 1] for agg=percentile (0.5 = median). Consumers default to 0.5 when omitted."
    }
    useDiscretePercentile: {
      type: "boolean"
      description: "Use the discrete percentile (PERCENTILE_DISC / use_discrete_percentile) instead of continuous interp..."
    }
  }
}
```

### `properties.consumers`
```json
{
  type: "array"
  description: "NEW in v0.7.6: Declared downstream consumers of this data product — the business artifacts built on ..."
  items: {
    $ref: "#/$defs/consumerRef"
  }
}
```

### `properties.packaging`
```json
{
  $ref: "#/$defs/packaging"
  description: "NEW in v0.7.6: Contract-wide packaging default — declarative container ownership (isolated = this pr..."
}
```

## 📝 Modified Properties

### `$defs.acquisitionSink.properties.catalog.enum`

**Before:**
```json
[...6 items...]
```

**After:**
```json
[...8 items...]
```

### `$defs.bindingLocation.properties.catalog.description`

**Before:**
```json
"NEW in v0.7.5: Iceberg catalog kind/profile selector — maps to iceberg.catalog.type (e.g. glue, rest..."
```

**After:**
```json
"NEW in v0.7.5: The Iceberg catalog that owns this table: glue, rest, lakekeeper, polaris, unity, nes..."
```

### `$defs.bindingLocation.properties.partitionBy.description`

**Before:**
```json
"NEW in v0.7.5: Iceberg partition columns — a FLUID abstraction over the Iceberg PARTITIONED BY / Par..."
```

**After:**
```json
"NEW in v0.7.5: Iceberg partition columns — a FLUID abstraction over the Iceberg PARTITIONED BY / Par..."
```

### `$defs.build.properties.engine.anyOf`

**Before:**
```json
[{"enum": ["dbt", "sql", "python", "spark", "glue", "custom", "duckdb", "airbyte", "meltano", "dlt", "kafka-connect", "debezium"]}, {"pattern": "^dbt-[a-z0-9]+([_-][a-z0-9]+)*$"}]
```

**After:**
```json
[{"enum": ["dbt", "sql", "python", "spark", "glue", "custom", "duckdb", "airbyte", "meltano", "dlt", "kafka-connect", "debezium", "flink"]}, {"pattern": "^dbt-[a-z0-9]+([_-][a-z0-9]+)*$"}]
```

### `$defs.build.properties.engine.description`

**Before:**
```json
"Build/ingestion engine. Transformation engines: dbt, sql, python, spark, glue, custom. Adapter-quali..."
```

**After:**
```json
"Build/ingestion engine. Transformation engines: dbt, sql, python, spark, glue, custom. Adapter-quali..."
```

### `$defs.expose.properties.lifecycle.$ref`

**Before:**
```json
"#/$defs/lifecycle"
```

**After:**
```json
"#/$defs/exposeLifecycle"
```

### `$defs.exposePolicy.properties.authz.properties.columnRestrictions.description`

**Before:**
```json
"Column-level access control."
```

**After:**
```json
"Column-level access control. A column named in any restriction is restricted. 'deny': the principal ..."
```

### `$defs.exposePolicy.properties.authz.properties.columnRestrictions.items.properties.access.enum`

**Before:**
```json
["allow", "deny"]
```

**After:**
```json
["allow", "deny", "mask"]
```

### `$id`

**Before:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.5.json"
```

**After:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.6.json"
```

### `description`

**Before:**
```json
"FLUID Data Product contract (v0.7.5). Streaming Kafka→Iceberg Sink & Confluent Tableflow Release.

🔥..."
```

**After:**
```json
"FLUID contract schema 0.7.6 — the current PREVIEW version, opened when 0.7.5 was promoted to stable...."
```

### `properties.fluidVersion.description`

**Before:**
```json
"Contract schema version. Accepts '0.7.3' (source-aligned data products + acquisition pattern + inges..."
```

**After:**
```json
"Contract schema version. Accepts '0.7.3' (source-aligned data products + acquisition pattern + inges..."
```

### `properties.fluidVersion.enum`

**Before:**
```json
["0.7.3", "0.7.4", "0.7.5"]
```

**After:**
```json
[...4 items...]
```

### `title`

**Before:**
```json
"FLUID 0.7.5 \u2014 Streaming Kafka\u2192Iceberg Sink & Confluent Tableflow"
```

**After:**
```json
"FLUID 0.7.6 \u2014 Declarative Packaging Modes (preview)"
```
