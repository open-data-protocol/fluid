# Schema Changes: 0.7.2 → 0.7.3

**Total changes:** 40
- ✅ Added: 25
- ❌ Removed: 0
- 📝 Modified: 15

---

## ✅ Added Properties

### `$defs.acquisitionCatalog`
```json
{
  type: "object"
  description: "Catalog auto-registration on first apply."
  additionalProperties: false
  properties: {
    register: {
      type: "array"
      items: {
        type: "string"
        enum: ["datahub", "openmetadata", "datamesh_manager"]
      }
      description: "Catalog targets the publish stage will auto-register against. ``glue`` and ``snowflake_horizon`` are..."
    }
    documentation: {
      type: "string"
      enum: ["auto", "manual", "none"]
      default: "auto"
    }
  }
}
```

### `$defs.acquisitionConcurrency`
```json
{
  type: "object"
  description: "Single-flight concurrency control."
  additionalProperties: false
  properties: {
    lock: {
      type: "object"
      additionalProperties: false
      properties: {
        scope: {
          type: "string"
          enum: ["product", "build"]
          default: "product"
        }
        timeout: {
          $ref: "#/$defs/isoDuration"
        }
        onContended: {
          type: "string"
          enum: ["abort", "queue", "replace"]
          default: "abort"
        }
      }
    }
  }
}
```

### `$defs.acquisitionCost`
```json
{
  type: "object"
  description: "Cost tracking + budget enforcement."
  additionalProperties: false
  properties: {
    budget: {
      type: "object"
      additionalProperties: false
      properties: {
        monthly: {
          type: "object"
          additionalProperties: false
          properties: {
            rows: {
              type: "integer"
              minimum: 0
            }
            bytes: {
              type: "string"
              description: "Human-readable size with unit suffix (e.g., '50GB', '500MB')."
            }
            computeMinutes: {
              type: "integer"
              minimum: 0
            }
          }
        }
        onExceed: {
          type: "string"
          enum: ["warn", "abort"]
          default: "warn"
        }
      }
    }
    chargeback: {
      type: "object"
      additionalProperties: true
      properties: {
        team: {
          type: "string"
        }
        project: {
          type: "string"
        }
        costCenter: {
          type: "string"
        }
      }
    }
  }
}
```

### `$defs.acquisitionDelivery`
```json
{
  type: "object"
  description: "Delivery semantics + idempotency + DLQ configuration."
  additionalProperties: false
  properties: {
    guarantee: {
      type: "string"
      enum: ["at_most_once", "at_least_once", "exactly_once"]
      default: "at_least_once"
    }
    idempotencyKey: {
      type: "string"
      description: "Template for the idempotency key. Default: {run_id}:{stream}:{record_pk}"
      default: "{run_id}:{stream}:{record_pk}"
    }
    dlq: {
      type: "object"
      additionalProperties: false
      properties: {
        enabled: {
          type: "boolean"
          default: true
        }
        sink: {
          type: "object"
          additionalProperties: false
          properties: {
            format: {
              type: "string"
              enum: ["parquet", "json", "ndjson"]
            }
            location: {
              type: "string"
            }
          }
        }
        maxRecordsBeforeAbort: {
          type: "integer"
          minimum: 0
          default: 10000
        }
        alertOn: {
          type: "array"
          items: {
            type: "string"
            enum: [...4 items...]
          }
        }
      }
    }
  }
}
```

### `$defs.acquisitionDeployment`
```json
{
  type: "object"
  description: "Engine deployment mode and target."
  additionalProperties: false
  required: ["mode"]
  properties: {
    mode: {
      type: "string"
      enum: ["embedded", "bring-your-own", "managed"]
      default: "embedded"
    }
    server_url: {
      type: "string"
      description: "URL for bring-your-own mode."
    }
    auth: {
      type: "object"
      additionalProperties: true
      properties: {
        secretRef: {
          type: "string"
        }
      }
    }
    managed: {
      type: "object"
      additionalProperties: false
      required: ["target"]
      properties: {
        target: {
          type: "string"
          enum: [...4 items...]
        }
        profile: {
          type: "string"
          enum: ["small", "medium", "large"]
          default: "small"
        }
        chart: {
          type: "object"
          additionalProperties: true
          properties: {
            repo: {
              type: "string"
            }
            name: {
              type: "string"
            }
            version: {
              type: "string"
            }
          }
        }
        values_overlay: {
          type: "object"
          additionalProperties: true
        }
        secrets: {
          type: "array"
          items: {
            type: "object"
            additionalProperties: false
            properties: {
              name: {
                type: "string"
              }
              ref: {
                type: "string"
              }
            }
          }
        }
        ... (1 more)
      }
    }
  }
}
```

### `$defs.acquisitionImageSignature`
```json
{
  type: "object"
  description: "Connector image supply-chain verification."
  additionalProperties: false
  properties: {
    verifier: {
      type: "string"
      enum: ["cosign"]
      default: "cosign"
    }
    publicKey: {
      type: "string"
    }
    slsaProvenance: {
      type: "string"
      enum: ["required", "optional", "disabled"]
      default: "optional"
    }
  }
}
```

### `$defs.acquisitionPattern`
```json
{
  type: "object"
  description: "NEW in v0.7.3: Source-aligned acquisition pattern. The build ingests data from an external system (n..."
  additionalProperties: false
  required: ["source"]
  properties: {
    source: {
      $ref: "#/$defs/acquisitionSource"
    }
    sink: {
      $ref: "#/$defs/acquisitionSink"
    }
    delivery: {
      $ref: "#/$defs/acquisitionDelivery"
    }
    schemaEvolution: {
      $ref: "#/$defs/acquisitionSchemaEvolution"
    }
    preLand: {
      type: "array"
      description: "Pre-land hook chain - runs on each batch before destination write."
      items: {
        type: "string"
        enum: [...4 items...]
      }
    }
    ... (11 more)
  }
}
```

### `$defs.acquisitionQuality`
```json
{
  type: "object"
  description: "Pre-land quality gates + anomaly signals."
  additionalProperties: false
  properties: {
    gates: {
      type: "array"
      items: {
        type: "object"
        additionalProperties: true
        required: ["rule", "severity"]
        properties: {
          rule: {
            type: "string"
            enum: [...6 items...]
          }
          columns: {
            type: "array"
            items: {
              type: "string"
            }
          }
          column: {
            type: "string"
          }
          pattern: {
            type: "string"
          }
          min: {
            type: "number"
          }
          ... (4 more)
        }
      }
    }
    onError: {
      type: "string"
      enum: ["route_to_dlq", "abort_run", "best_effort"]
      default: "route_to_dlq"
    }
    anomalies: {
      type: "array"
      items: {
        type: "object"
        additionalProperties: false
        required: ["signal", "severity"]
        properties: {
          signal: {
            type: "string"
            enum: [...7 items...]
          }
          algorithm: {
            type: "string"
            enum: ["ewma", "iqr", "exact"]
          }
          sensitivity: {
            type: "number"
          }
          severity: {
            type: "string"
            enum: ["info", "warn", "error"]
          }
        }
      }
    }
  }
}
```

### `$defs.acquisitionSchemaEvolution`
```json
{
  type: "object"
  description: "Schema evolution behavior. Stricter-wins between policy and per-change overrides."
  additionalProperties: false
  properties: {
    policy: {
      type: "string"
      enum: [...4 items...]
      default: "strict"
    }
    onAddedColumn: {
      type: "string"
      enum: ["include", "warn", "fail"]
    }
    onRemovedColumn: {
      type: "string"
      enum: ["drop", "warn", "fail"]
    }
    onTypeChange: {
      type: "string"
      enum: ["cast", "warn", "fail"]
    }
    sourceFingerprint: {
      type: "string"
      enum: ["required", "optional", "disabled"]
      default: "required"
    }
  }
}
```

### `$defs.acquisitionSink`
```json
{
  type: "object"
  description: "Destination format for ingested data. binding.platform on the expose remains the source of truth for..."
  additionalProperties: false
  properties: {
    format: {
      type: "string"
      enum: [...9 items...]
    }
    catalog: {
      type: "string"
      enum: [...6 items...]
    }
    partitionBy: {
      type: "array"
      items: {
        type: "string"
      }
    }
  }
}
```

### `$defs.acquisitionSource`
```json
{
  type: "object"
  description: "External source system specification."
  additionalProperties: false
  required: ["kind", "mode"]
  properties: {
    kind: {
      type: "string"
      description: "Source system kind: filesystem, postgres, mysql, sqlite, http, salesforce, stripe, github, kafka, et..."
    }
    connection: {
      type: "object"
      description: "Connection details. Use ${VAR} placeholders for env values; use secretRef for credentials. Inline se..."
      additionalProperties: true
      properties: {
        uri: {
          type: "string"
        }
        host: {
          type: "string"
        }
        port: {
          oneOf: [{"type": "integer"}, {"type": "string", "description": "Allows ${ENV_VAR} placeholders that resolve to an integer at runtime."}]
        }
        database: {
          type: "string"
        }
        instance_url: {
          type: "string"
        }
        ... (4 more)
      }
    }
    mode: {
      type: "string"
      enum: [...6 items...]
    }
    cursor_field: {
      type: "string"
      description: "Column used for incremental cursor (e.g., updated_at, SystemModstamp)."
    }
    watermark: {
      type: "object"
      additionalProperties: false
      properties: {
        strategy: {
          type: "string"
          enum: ["high_water_mark", "log_position", "lsn"]
        }
        allowedLateness: {
          $ref: "#/$defs/isoDuration"
        }
      }
    }
    ... (2 more)
  }
}
```

### `$defs.binding.properties.governance`
```json
{
  $ref: "#/$defs/bindingGovernance"
  description: "Per-resource governance: registerLocation, principal grants, tag associations, row/column filters. A..."
}
```

### `$defs.bindingGovernance`
```json
{
  type: "object"
  description: "Per-resource (per-exposure) governance. Currently scoped to AWS Lake Formation; future cloud-specifi..."
  additionalProperties: false
  properties: {
    lakeFormation: {
      type: "object"
      additionalProperties: false
      description: "Per-resource LF settings: location registration, principal grants, LF-tag associations, row/column f..."
      properties: {
        registerLocation: {
          type: "boolean"
          default: false
          description: "When true, emit aws_lakeformation_resource that registers the binding's S3 path with Lake Formation...."
        }
        grants: {
          type: "array"
          description: "Principal-based LF grants on this exposure's database/table. Each entry maps a principal to a permis..."
          items: {
            type: "object"
            additionalProperties: false
            required: ["principal", "permissions"]
            properties: {
              principal: {
                type: "string"
                description: "IAM principal ARN (role or user) receiving the grant."
                pattern: "^arn:aws[a-z0-9-]*:iam::"
              }
              permissions: {
                type: "array"
                description: "LF permissions granted. Valid values per the hashicorp/aws aws_lakeformation_permissions resource."
                items: {
                  type: "string"
                  enum: [...10 items...]
                }
                uniqueItems: true
                minItems: 1
              }
              permissionsWithGrantOption: {
                type: "array"
                description: "Subset of permissions the principal can re-grant. Maps to aws_lakeformation_permissions.permissions_..."
                items: {
                  type: "string"
                }
                uniqueItems: true
              }
              columns: {
                type: "array"
                description: "Optional column-level restriction. When set, the grant is emitted against aws_lakeformation_permissi..."
                items: {
                  type: "string"
                }
                uniqueItems: true
              }
              excludedColumns: {
                type: "array"
                description: "Opposite of columns: every column EXCEPT these is granted. Maps to table_with_columns.excluded_colum..."
                items: {
                  type: "string"
                }
                uniqueItems: true
              }
            }
          }
        }
        tags: {
          type: "object"
          description: "LF-tag (TBAC) associations applied to this table. Keys must reference tag definitions declared in th..."
          additionalProperties: {
            type: "string"
          }
        }
        rowFilter: {
          type: "object"
          additionalProperties: false
          description: "Row-level (and optionally column-level) filter applied to all reads of this table via LF. Emitted as..."
          properties: {
            name: {
              type: "string"
              description: "Filter name (must be unique per table)."
            }
            rowExpression: {
              type: "string"
              description: "PartiQL-flavoured row predicate. ``ALL`` lets every row through (use when only column filtering is i..."
            }
            columnNames: {
              type: "array"
              description: "Columns visible through the filter. Mutually exclusive with allColumns / excludedColumnNames."
              items: {
                type: "string"
              }
              uniqueItems: true
            }
            excludedColumnNames: {
              type: "array"
              description: "Columns hidden through the filter (everything else is visible)."
              items: {
                type: "string"
              }
              uniqueItems: true
            }
            allColumns: {
              type: "boolean"
              default: false
              description: "Convenience for the LF column-wildcard form (every column visible). When true, columnNames / exclude..."
            }
          }
          required: ["name", "rowExpression"]
        }
      }
    }
  }
}
```

### `$defs.build.properties.capabilities`
```json
{
  type: "array"
  description: "Capabilities the build asks for (acquisition pattern). Validation enforces capabilities ⊆ runner.dec..."
  items: {
    type: "string"
    enum: [...12 items...]
  }
  uniqueItems: true
}
```

### `$defs.build.properties.engine.description`
```json
"Build/ingestion engine. Transformation engines: dbt, sql, python, spark, glue, custom. Ingestion eng..."
```

### `$defs.exposeContract.properties.schemaPolicy`
```json
{
  type: "string"
  enum: [...4 items...]
  default: "strict"
  description: "NEW in v0.7.3: Schema evolution policy. strict = fail on any schema change; discover_and_freeze = ca..."
}
```

### `$defs.governance`
```json
{
  type: "object"
  description: "Account/project-wide governance settings. Today only the lakeFormation block is supported; future cl..."
  additionalProperties: false
  properties: {
    lakeFormation: {
      type: "object"
      additionalProperties: false
      description: "AWS Lake Formation account-wide settings: data-lake admins and LF-tag (TBAC) definitions. Applies to..."
      properties: {
        admins: {
          type: "array"
          description: "IAM principal ARNs (roles or users) granted Lake Formation admin privileges. Emitted as aws_lakeform..."
          items: {
            type: "string"
            pattern: "^arn:aws[a-z0-9-]*:iam::"
          }
          uniqueItems: true
        }
        tagDefinitions: {
          type: "object"
          description: "LF-TBAC tag-key definitions. Each entry is a tag key mapped to its allowed string values. Emitted as..."
          additionalProperties: {
            type: "array"
            items: {
              type: "string"
            }
            uniqueItems: true
            minItems: 1
          }
        }
      }
    }
  }
}
```

### `$defs.observability.properties.alert`
```json
{
  type: "object"
  additionalProperties: false
  description: "Alert dispatcher config consumed by the acquisition Alerter (DLQ overflow, schema-fingerprint change..."
  properties: {
    channels: {
      type: "array"
      items: {
        type: "object"
        additionalProperties: false
        required: ["kind"]
        properties: {
          kind: {
            type: "string"
            enum: ["log", "file", "webhook"]
          }
          path: {
            type: "string"
            description: "For kind=file: NDJSON sink path (env-vars expanded)."
          }
          url: {
            type: "string"
            format: "uri"
            description: "For kind=webhook: Slack-compatible incoming webhook URL. Validated against the SSRF guard at constru..."
          }
        }
      }
    }
  }
}
```

### `$defs.retention`
```json
{
  type: "object"
  description: "NEW in v0.7.3: Retention durations (ISO-8601). Defaults: runState=P30D, runLogs=P90D, lineage=P365D,..."
  additionalProperties: false
  properties: {
    runState: {
      $ref: "#/$defs/isoDuration"
    }
    runLogs: {
      $ref: "#/$defs/isoDuration"
    }
    lineage: {
      $ref: "#/$defs/isoDuration"
    }
    dlq: {
      $ref: "#/$defs/isoDuration"
    }
  }
}
```

### `properties.extensions`
```json
{
  type: "object"
  additionalProperties: true
  description: "Vendor / plugin-namespaced configuration. Each plugin claims a single sub-key (e.g. customScaffold, ..."
}
```

### `properties.governance`
```json
{
  $ref: "#/$defs/governance"
  description: "Contract-level governance: account/project-wide settings (e.g. AWS Lake Formation admins and LF-tag ..."
}
```

### `properties.metadata.properties.classification`
```json
{
  type: "string"
  enum: [...4 items...]
  description: "NEW in v0.7.3: Data classification label propagated to catalog + access policy enforcement."
}
```

### `properties.metadata.properties.experimental`
```json
{
  type: "array"
  description: "NEW in v0.7.3: Feature gates the contract opts into (e.g., 'acquisition' while Bronze acquisition is..."
  items: {
    type: "string"
  }
  uniqueItems: true
}
```

### `properties.metadata.properties.productType`
```json
{
  type: "string"
  enum: ["SDP", "ADP", "CDP"]
  description: "NEW in v0.7.3: Data Mesh data-product type. SDP = Source-Aligned Data Product (raw ingestion from ex..."
}
```

### `properties.retention`
```json
{
  $ref: "#/$defs/retention"
  description: "NEW in v0.7.3: Retention durations for run state, run logs, lineage events, and DLQ records. Honored..."
}
```

## 📝 Modified Properties

### `$defs.binding.properties.format.enum`

**Before:**
```json
[...14 items...]
```

**After:**
```json
[...18 items...]
```

### `$defs.build.allOf`

**Before:**
```json
[{"if": {"properties": {"pattern": {"const": "hybrid-reference"}}}, "then": {"properties": {"properties": {"$ref": "#/$defs/hybridReferencePattern"}}}}, {"if": {"properties": {"pattern": {"const": "embedded-logic"}}}, "then": {"properties": {"properties": {"$ref": "#/$defs/embeddedLogicPattern"}}}}, {"if": {"properties": {"pattern": {"const": "multi-stage"}}}, "then": {"properties": {"properties": {"$ref": "#/$defs/multiStagePattern"}}}}]
```

**After:**
```json
[...4 items...]
```

### `$defs.build.properties.engine.enum`

**Before:**
```json
[...6 items...]
```

**After:**
```json
[...12 items...]
```

### `$defs.build.properties.pattern.description`

**Before:**
```json
"Build pattern: hybrid-reference (dbt-style), embedded-logic (raw SQL/code), or multi-stage (complex ..."
```

**After:**
```json
"Build pattern: hybrid-reference (dbt-style), embedded-logic (raw SQL/code), multi-stage (complex pip..."
```

### `$defs.build.properties.pattern.enum`

**Before:**
```json
["hybrid-reference", "embedded-logic", "multi-stage"]
```

**After:**
```json
[...4 items...]
```

### `$defs.identifier.description`

**Before:**
```json
"Unified identifier pattern: starts/ends with alphanumeric or underscore, allows dots and hyphens in ..."
```

**After:**
```json
"Unified identifier pattern: starts/ends with alphanumeric or underscore, allows dots and hyphens in ..."
```

### `$defs.identifier.pattern`

**Before:**
```json
"^[a-z0-9_][a-z0-9_.-]*[a-z0-9_]$|^[a-z0-9_]$"
```

**After:**
```json
"^[A-Za-z0-9_][A-Za-z0-9_.-]*[A-Za-z0-9_]$|^[A-Za-z0-9_]$"
```

### `$defs.runtime.properties.platform.enum`

**Before:**
```json
[...9 items...]
```

**After:**
```json
[...12 items...]
```

### `$id`

**Before:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.2.json"
```

**After:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.3.json"
```

### `description`

**Before:**
```json
"FLUID Data Product contract (v0.7.2). Semantic Truth Engine Release:

🔥 NEW in v0.7.2:
• Semantic mo..."
```

**After:**
```json
"FLUID Data Product contract (v0.7.3). Source-Aligned Acquisition Release:

🔥 NEW in v0.7.3:
• acquis..."
```

### `properties.fluidVersion.const`

**Before:**
```json
"0.7.2"
```

**After:**
```json
"0.7.3"
```

### `properties.fluidVersion.description`

**Before:**
```json
"Contract schema version. Must be exactly '0.7.2' for semantic truth engine + agentic governance + pr..."
```

**After:**
```json
"Contract schema version. Must be exactly '0.7.3' for source-aligned data products + acquisition patt..."
```

### `properties.fluidVersion.examples`

**Before:**
```json
["0.7.2"]
```

**After:**
```json
["0.7.3"]
```

### `properties.metadata.properties.layer.description`

**Before:**
```json
"Data layer label (e.g., Bronze/Silver/Gold). Free-form."
```

**After:**
```json
"Data layer label (e.g., Bronze/Silver/Gold). Free-form. When set together with `productType`, the tw..."
```

### `title`

**Before:**
```json
"FLUID 0.7.2 \u2014 Semantic Truth Engine"
```

**After:**
```json
"FLUID 0.7.3 \u2014 Source-Aligned Data Products"
```
