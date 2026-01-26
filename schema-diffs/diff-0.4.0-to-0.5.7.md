# Schema Changes: 0.4.0 → 0.5.7

**Total changes:** 177
- ✅ Added: 102
- ❌ Removed: 62
- 📝 Modified: 13

---

## ✅ Added Properties

### `$defs.availabilityPct`
```json
{
  type: "string"
  pattern: "^(100(\\.0+)?|\\d{2}(\\.\\d+)?|\\d{1}\\d(\\.\\d+)?)%$"
  description: "Availability percentage (e.g., 99.9%)."
}
```

### `$defs.binding`
```json
{
  type: "object"
  additionalProperties: false
  required: ["platform", "format", "location"]
  properties: {
    platform: {
      type: "string"
      enum: [...9 items...]
    }
    format: {
      type: "string"
      enum: [...13 items...]
    }
    location: {
      $ref: "#/$defs/bindingLocation"
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Binding configuration tags for infrastructure."
    }
    labels: {
      $ref: "#/$defs/labels"
      description: "Binding configuration labels for automation."
    }
  }
}
```

### `$defs.bindingLocation`
```json
{
  type: "object"
  description: "Provider-native addressing with tightened structure for better interop."
  additionalProperties: false
  properties: {
    account: {
      type: "string"
      description: "Cloud account ID"
    }
    project: {
      type: "string"
      description: "GCP project ID"
    }
    dataset: {
      type: "string"
      description: "BigQuery dataset or database name"
    }
    database: {
      type: "string"
      description: "Database name"
    }
    schema: {
      type: "string"
      description: "Schema name"
    }
    ... (9 more)
  }
}
```

### `$defs.build`
```json
{
  type: "object"
  description: "Enhanced build configuration supporting v0.4.0 patterns with v0.5.5 improvements."
  additionalProperties: false
  properties: {
    id: {
      $ref: "#/$defs/identifier"
      description: "Build identifier for multi-build scenarios (e.g., 'batch-processing', 'ml-training')."
    }
    description: {
      type: "string"
      description: "Human-readable description of this build configuration."
    }
    pattern: {
      type: "string"
      enum: ["hybrid-reference", "embedded-logic", "multi-stage"]
      default: "hybrid-reference"
      description: "Build pattern: hybrid-reference (dbt-style), embedded-logic (raw SQL/code), or multi-stage (complex ..."
    }
    engine: {
      type: "string"
      enum: [...5 items...]
      default: "dbt"
    }
    repository: {
      type: "string"
    }
    ... (7 more)
  }
  allOf: [{"if": {"properties": {"pattern": {"const": "hybrid-reference"}}}, "then": {"properties": {"properties": {"$ref": "#/$defs/hybridReferencePattern"}}}}, {"if": {"properties": {"pattern": {"const": "embedded-logic"}}}, "then": {"properties": {"properties": {"$ref": "#/$defs/embeddedLogicPattern"}}}}, {"if": {"properties": {"pattern": {"const": "multi-stage"}}}, "then": {"properties": {"properties": {"$ref": "#/$defs/multiStagePattern"}}}}]
}
```

### `$defs.buildExecution`
```json
{
  type: "object"
  description: "Build execution configuration from v0.4.0 enhanced."
  additionalProperties: false
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
```

### `$defs.buildProperties`
```json
{
  type: "object"
  description: "Base properties for all build patterns."
}
```

### `$defs.column.additionalProperties`
```json
false
```

### `$defs.column.properties.businessDefinition`
```json
{
  type: "string"
  description: "Business definition and meaning of this field."
}
```

### `$defs.column.properties.businessName`
```json
{
  type: "string"
  description: "Business-friendly name for this field."
}
```

### `$defs.column.properties.labels`
```json
{
  $ref: "#/$defs/labels"
  description: "Field-level labels for metadata and automation."
}
```

### `$defs.column.properties.name.minLength`
```json
1
```

### `$defs.column.properties.required`
```json
{
  type: "boolean"
}
```

### `$defs.column.properties.semanticType`
```json
{
  type: "string"
  description: "Semantic meaning (e.g., 'email', 'phone', 'identifier')."
}
```

### `$defs.column.properties.sensitivity`
```json
{
  $ref: "#/$defs/sensitivityLevel"
  description: "Field-level sensitivity classification for improved policy ergonomics."
}
```

### `$defs.column.properties.tags.$ref`
```json
"#/$defs/tags"
```

### `$defs.column.properties.tags.description`
```json
"Field-level tags for categorization and data governance."
```

### `$defs.column.properties.type.minLength`
```json
1
```

### `$defs.column.properties.validationRules`
```json
{
  type: "array"
  description: "Field-level validation constraints."
  items: {
    type: "object"
    additionalProperties: false
    properties: {
      type: {
        type: "string"
        enum: [...4 items...]
      }
      constraint: {
        type: "string"
      }
      message: {
        type: "string"
      }
    }
  }
}
```

### `$defs.consumeRef`
```json
{
  type: "object"
  additionalProperties: false
  required: ["productId", "exposeId"]
  $comment: "productId identifies data product (renamed from 'provider' for clarity)"
  properties: {
    productId: {
      $ref: "#/$defs/identifier"
      description: "Upstream data product identifier (e.g., 'silver.hr.people_v2'). Renamed from 'provider' for clarity."
    }
    exposeId: {
      $ref: "#/$defs/identifier"
      description: "The upstream exposeId being consumed."
    }
    versionConstraint: {
      $ref: "#/$defs/semverRange"
    }
    qosExpectations: {
      type: "object"
      additionalProperties: false
      properties: {
        freshnessMax: {
          $ref: "#/$defs/isoDuration"
        }
        maxStaleness: {
          $ref: "#/$defs/isoDuration"
          description: "Maximum acceptable staleness for consumed data."
        }
        minCompleteness: {
          type: "number"
          minimum: 0
          maximum: 1
          description: "Minimum completeness expectation."
        }
        tags: {
          $ref: "#/$defs/tags"
          description: "QoS expectation tags."
        }
        labels: {
          $ref: "#/$defs/labels"
          description: "QoS expectation labels."
        }
      }
    }
    requiredPolicies: {
      type: "array"
      items: {
        type: "string"
      }
    }
    ... (3 more)
  }
}
```

### `$defs.defaultSLIs`
```json
{
  type: "object"
  description: "Default SLI trio that CLI can auto-generate based on expose kind."
  additionalProperties: false
  properties: {
    enabled: {
      type: "boolean"
      default: true
      description: "Enable auto-generation of default SLIs."
    }
    freshness: {
      type: "object"
      description: "Default freshness SLI configuration."
      additionalProperties: false
      properties: {
        enabled: {
          type: "boolean"
          default: true
        }
        threshold: {
          $ref: "#/$defs/isoDuration"
          description: "Freshness threshold (auto-set by kind: table=PT6H, stream=PT1M, api=PT1S)"
        }
        severity: {
          type: "string"
          enum: ["info", "warning", "critical"]
          default: "warning"
        }
        tags: {
          $ref: "#/$defs/tags"
          description: "Freshness SLI tags."
        }
        labels: {
          $ref: "#/$defs/labels"
          description: "Freshness SLI labels."
        }
      }
    }
    completeness: {
      type: "object"
      description: "Default completeness SLI configuration."
      additionalProperties: false
      properties: {
        enabled: {
          type: "boolean"
          default: true
        }
        threshold: {
          type: "number"
          minimum: 0
          maximum: 1
          default: 0.95
          description: "Completeness threshold (auto-set by kind: table=0.95, stream=0.99)"
        }
        severity: {
          type: "string"
          enum: ["info", "warning", "critical"]
          default: "warning"
        }
        tags: {
          $ref: "#/$defs/tags"
          description: "Completeness SLI tags."
        }
        labels: {
          $ref: "#/$defs/labels"
          description: "Completeness SLI labels."
        }
      }
    }
    latency: {
      type: "object"
      description: "Default latency SLI configuration."
      additionalProperties: false
      properties: {
        enabled: {
          type: "boolean"
          default: true
        }
        threshold: {
          $ref: "#/$defs/isoDuration"
          description: "P95 latency threshold (auto-set by kind: api=PT200MS, table=PT5S, stream=PT100MS)"
        }
        percentile: {
          type: "number"
          minimum: 0
          maximum: 100
          default: 95
          description: "Latency percentile to measure."
        }
        severity: {
          type: "string"
          enum: ["info", "warning", "critical"]
          default: "warning"
        }
        tags: {
          $ref: "#/$defs/tags"
          description: "Latency SLI tags."
        }
        ... (1 more)
      }
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Default SLI configuration tags."
    }
    ... (1 more)
  }
}
```

### `$defs.docs`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    homepage: {
      type: "string"
      format: "uri"
    }
    runbook: {
      type: "string"
      format: "uri"
    }
    dictionary: {
      type: "string"
      format: "uri"
    }
    changeLog: {
      type: "string"
      format: "uri"
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Documentation tags for organization."
    }
    ... (1 more)
  }
}
```

### `$defs.dqRule`
```json
{
  type: "object"
  additionalProperties: false
  required: ["id", "type", "severity"]
  properties: {
    id: {
      type: "string"
    }
    type: {
      type: "string"
      enum: [...8 items...]
    }
    selector: {
      type: "string"
    }
    threshold: {
      type: "number"
    }
    operator: {
      type: "string"
      enum: [...6 items...]
    }
    ... (5 more)
  }
}
```

### `$defs.dqSpec`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    rules: {
      type: "array"
      items: {
        $ref: "#/$defs/dqRule"
      }
    }
    monitoring: {
      type: "object"
      additionalProperties: false
      properties: {
        enabled: {
          type: "boolean"
          default: true
        }
        window: {
          $ref: "#/$defs/isoDuration"
        }
        owner: {
          type: "string"
        }
      }
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Data quality specification tags."
    }
    labels: {
      $ref: "#/$defs/labels"
      description: "Data quality specification labels."
    }
  }
}
```

### `$defs.embeddedLogicPattern.additionalProperties`
```json
false
```

### `$defs.embeddedLogicPattern.description`
```json
"Embedded logic pattern from v0.4.0."
```

### `$defs.embeddedLogicPattern.properties.labels`
```json
{
  $ref: "#/$defs/labels"
}
```

### `$defs.embeddedLogicPattern.properties.parameters`
```json
{
  type: "object"
  additionalProperties: true
}
```

### `$defs.embeddedLogicPattern.properties.tags`
```json
{
  $ref: "#/$defs/tags"
}
```

### `$defs.environmentConfig`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    metadata: {
      type: "object"
      description: "Environment-specific metadata overrides."
      additionalProperties: false
      properties: {
        owner: {
          type: "object"
          additionalProperties: false
          properties: {
            team: {
              type: "string"
            }
            email: {
              type: "string"
            }
            slack: {
              type: "string"
            }
          }
        }
        tags: {
          $ref: "#/$defs/tags"
          description: "Environment-specific metadata tags."
        }
        labels: {
          $ref: "#/$defs/labels"
          description: "Environment-specific metadata labels."
        }
      }
    }
    exposes: {
      type: "array"
      description: "Environment-specific expose overrides."
      items: {
        type: "object"
        additionalProperties: false
        properties: {
          exposeId: {
            $ref: "#/$defs/identifier"
          }
          binding: {
            $ref: "#/$defs/binding"
          }
          qos: {
            $ref: "#/$defs/exposeQoS"
          }
          tags: {
            $ref: "#/$defs/tags"
            description: "Environment-specific expose tags."
          }
          labels: {
            $ref: "#/$defs/labels"
            description: "Environment-specific expose labels."
          }
        }
      }
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Environment configuration tags."
    }
    labels: {
      $ref: "#/$defs/labels"
      description: "Environment configuration labels."
    }
  }
}
```

### `$defs.expose.additionalProperties`
```json
false
```

### `$defs.expose.examples`
```json
[{"exposeId": "customer_profiles", "title": "Customer Profiles Table", "kind": "table", "tags": ["pii", "customer-facing", "analytical"], "labels": {"sensitivity": "high", "retention": "7-years", "team": "customer-analytics"}, "contract": {"schema": [{"name": "customer_id", "type": "STRING", "required": true, "sensitivity": "cleartext", "tags": ["identifier", "primary-key"], "labels": {"business-name": "Customer ID", "data-category": "identifier"}}]}, "binding": {"platform": "gcp", "format": "bigquery_table", "location": {"project": "company-data", "dataset": "customer", "table": "profiles"}}}]
```

### `$defs.expose.properties.binding`
```json
{
  $ref: "#/$defs/binding"
}
```

### `$defs.expose.properties.contract`
```json
{
  $ref: "#/$defs/exposeContract"
}
```

### `$defs.expose.properties.docs`
```json
{
  $ref: "#/$defs/docs"
}
```

### `$defs.expose.properties.exposeId`
```json
{
  $ref: "#/$defs/identifier"
  description: "Stable interface handle (used by consumers & build.outputs)."
}
```

### `$defs.expose.properties.kind`
```json
{
  type: "string"
  enum: [...12 items...]
}
```

### `$defs.expose.properties.labels`
```json
{
  $ref: "#/$defs/labels"
  description: "Expose-level labels for metadata and automation."
}
```

### `$defs.expose.properties.lifecycle`
```json
{
  $ref: "#/$defs/lifecycle"
}
```

### `$defs.expose.properties.observability`
```json
{
  $ref: "#/$defs/observability"
}
```

### `$defs.expose.properties.policy`
```json
{
  $ref: "#/$defs/exposePolicy"
}
```

### `$defs.expose.properties.qos`
```json
{
  $ref: "#/$defs/exposeQoS"
}
```

### `$defs.expose.properties.tags.$ref`
```json
"#/$defs/tags"
```

### `$defs.expose.properties.tags.description`
```json
"Expose-level tags for categorization and routing."
```

### `$defs.expose.properties.title`
```json
{
  type: "string"
}
```

### `$defs.expose.properties.version`
```json
{
  $ref: "#/$defs/semver"
}
```

### `$defs.exposeContract`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    schemaSignature: {
      type: "string"
      pattern: "^sha256:[0-9a-fA-F]{64}$"
      description: "Hash of canonical schema/OpenAPI. Used by contract-tests gates."
    }
    schema: {
      type: "array"
      items: {
        $ref: "#/$defs/column"
      }
      description: "Tabular schema (for table/view/file)."
    }
    openapiRef: {
      type: "string"
      format: "uri"
      description: "OpenAPI document URL (for APIs)."
    }
    guarantees: {
      type: "object"
      additionalProperties: false
      properties: {
        compatibility: {
          type: "string"
          enum: [...6 items...]
          description: "Compatibility promise for non-breaking evolution."
        }
        evolution: {
          type: "array"
          items: {
            type: "string"
            enum: [...6 items...]
          }
        }
      }
    }
    dq: {
      $ref: "#/$defs/dqSpec"
      description: "Enhanced data quality rules including anomaly detection."
    }
    ... (2 more)
  }
  anyOf: [{"required": ["schema"]}, {"required": ["openapiRef"]}]
}
```

### `$defs.exposePolicy`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    authn: {
      type: "string"
      enum: [...7 items...]
    }
    authz: {
      type: "object"
      additionalProperties: false
      properties: {
        readers: {
          type: "array"
          items: {
            type: "string"
          }
        }
        writers: {
          type: "array"
          items: {
            type: "string"
          }
        }
        columnRestrictions: {
          type: "array"
          description: "Column-level access control."
          items: {
            type: "object"
            additionalProperties: false
            properties: {
              principal: {
                type: "string"
              }
              columns: {
                type: "array"
                items: {
                  type: "string"
                }
              }
              access: {
                type: "string"
                enum: ["allow", "deny"]
              }
              tags: {
                $ref: "#/$defs/tags"
                description: "Access control rule tags."
              }
              labels: {
                $ref: "#/$defs/labels"
                description: "Access control rule labels."
              }
            }
          }
        }
        tags: {
          $ref: "#/$defs/tags"
          description: "Authorization policy tags."
        }
        labels: {
          $ref: "#/$defs/labels"
          description: "Authorization policy labels."
        }
      }
    }
    privacy: {
      type: "object"
      additionalProperties: false
      properties: {
        masking: {
          type: "array"
          items: {
            type: "object"
            additionalProperties: false
            required: ["column", "strategy"]
            properties: {
              column: {
                type: "string"
              }
              strategy: {
                type: "string"
                enum: [...5 items...]
              }
              params: {
                type: "object"
                additionalProperties: true
              }
              tags: {
                $ref: "#/$defs/tags"
                description: "Privacy masking rule tags."
              }
              labels: {
                $ref: "#/$defs/labels"
                description: "Privacy masking rule labels."
              }
            }
          }
        }
        rowLevelPolicy: {
          type: "object"
          additionalProperties: false
          required: ["expression"]
          properties: {
            expression: {
              type: "string"
              description: "Provider-specific predicate"
            }
            tags: {
              $ref: "#/$defs/tags"
              description: "Row-level policy tags."
            }
            labels: {
              $ref: "#/$defs/labels"
              description: "Row-level policy labels."
            }
          }
        }
        tags: {
          $ref: "#/$defs/tags"
          description: "Privacy policy tags."
        }
        labels: {
          $ref: "#/$defs/labels"
          description: "Privacy policy labels."
        }
      }
    }
    classification: {
      type: "string"
      enum: [...4 items...]
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Policy-level tags for governance."
    }
    ... (1 more)
  }
}
```

### `$defs.exposeQoS`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    availability: {
      $ref: "#/$defs/availabilityPct"
    }
    freshnessSLO: {
      $ref: "#/$defs/isoDuration"
    }
    dataLossSLO: {
      type: "string"
      description: "e.g., '0 rows'"
    }
    latencyP95: {
      $ref: "#/$defs/isoDuration"
    }
    completenessTarget: {
      type: "number"
      minimum: 0
      maximum: 1
      description: "Target completeness ratio (0.0 to 1.0)."
    }
    ... (3 more)
  }
}
```

### `$defs.hybridReferencePattern.additionalProperties`
```json
false
```

### `$defs.hybridReferencePattern.description`
```json
"Hybrid-reference pattern from v0.4.0 (dbt-style)."
```

### `$defs.hybridReferencePattern.properties.labels`
```json
{
  $ref: "#/$defs/labels"
}
```

### `$defs.hybridReferencePattern.properties.materializations`
```json
{
  type: "object"
  additionalProperties: {
    type: "string"
    enum: [...4 items...]
  }
}
```

### `$defs.hybridReferencePattern.properties.tags`
```json
{
  $ref: "#/$defs/tags"
}
```

### `$defs.identifier`
```json
{
  type: "string"
  pattern: "^[a-z0-9_][a-z0-9_.-]*[a-z0-9_]$|^[a-z0-9_]$"
  description: "Unified identifier pattern: starts/ends with alphanumeric or underscore, allows dots and hyphens in ..."
}
```

### `$defs.isoDuration`
```json
{
  type: "string"
  pattern: "^P(?!$)(\\d+Y)?(\\d+M)?(\\d+W)?(\\d+D)?(T(\\d+H)?(\\d+M)?(\\d+S)?)?$"
  description: "ISO-8601 duration (e.g., P1D, PT15M, P2Y6M)."
}
```

### `$defs.labels`
```json
{
  type: "object"
  description: "Key-value labels for structured metadata and automation. Consistent pattern used throughout FLUID ob..."
  additionalProperties: {
    type: "string"
    description: "Label values are always strings for consistency and tooling compatibility."
  }
  examples: [{"team": "customer-analytics", "criticality": "high", "cost-center": "engineering", "retention": "7-years", "region": "us-central1", "business-name": "Customer Profiles", "data-category": "analytical"}]
}
```

### `$defs.lifecycle.additionalProperties`
```json
false
```

### `$defs.lifecycle.properties.deprecationPolicy`
```json
{
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
```

### `$defs.lifecycle.properties.labels`
```json
{
  $ref: "#/$defs/labels"
  description: "Lifecycle labels for governance."
}
```

### `$defs.lifecycle.properties.retention`
```json
{
  $ref: "#/$defs/isoDuration"
}
```

### `$defs.lifecycle.properties.state`
```json
{
  $ref: "#/$defs/lifecycleState"
  description: "Unified lifecycle state vocabulary."
}
```

### `$defs.lifecycle.properties.tags`
```json
{
  $ref: "#/$defs/tags"
  description: "Lifecycle tags for automation."
}
```

### `$defs.lifecycleState`
```json
{
  type: "string"
  enum: [...4 items...]
  description: "Unified lifecycle state vocabulary."
}
```

### `$defs.lineage`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    granularity: {
      type: "string"
      enum: ["table_level", "field_level"]
      default: "table_level"
      description: "Level of lineage tracking granularity."
    }
    upstream: {
      type: "array"
      description: "Upstream dependencies and their field mappings."
      items: {
        type: "object"
        additionalProperties: false
        required: ["productId", "exposeId"]
        properties: {
          productId: {
            $ref: "#/$defs/identifier"
            description: "Upstream data product ID."
          }
          exposeId: {
            $ref: "#/$defs/identifier"
            description: "Upstream expose ID being consumed."
          }
          fieldMappings: {
            type: "array"
            description: "Field-level lineage mappings (optional)."
            items: {
              type: "object"
              additionalProperties: false
              required: ["sourceField", "targetField"]
              properties: {
                sourceField: {
                  type: "string"
                }
                targetField: {
                  type: "string"
                }
                transformation: {
                  type: "object"
                  additionalProperties: false
                  properties: {
                    type: {
                      type: "string"
                      enum: [...4 items...]
                    }
                    expression: {
                      type: "string"
                      description: "Transformation logic or SQL expression."
                    }
                    tags: {
                      $ref: "#/$defs/tags"
                      description: "Transformation tags."
                    }
                    labels: {
                      $ref: "#/$defs/labels"
                      description: "Transformation labels."
                    }
                  }
                }
                tags: {
                  $ref: "#/$defs/tags"
                  description: "Field mapping tags."
                }
                labels: {
                  $ref: "#/$defs/labels"
                  description: "Field mapping labels."
                }
              }
            }
          }
          relationship: {
            type: "string"
            enum: ["direct_consumption", "lookup_enrichment", "aggregation"]
            description: "Type of data relationship."
          }
          tags: {
            $ref: "#/$defs/tags"
            description: "Upstream relationship tags."
          }
          ... (1 more)
        }
      }
    }
    downstream: {
      type: "array"
      description: "Known downstream consumers (optional)."
      items: {
        type: "object"
        additionalProperties: false
        properties: {
          consumer: {
            $ref: "#/$defs/identifier"
            description: "Downstream data product ID."
          }
          impact: {
            type: "string"
            enum: [...4 items...]
            description: "Impact level if this data product changes."
          }
          tags: {
            $ref: "#/$defs/tags"
            description: "Downstream relationship tags."
          }
          labels: {
            $ref: "#/$defs/labels"
            description: "Downstream relationship labels."
          }
        }
      }
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Lineage configuration tags."
    }
    labels: {
      $ref: "#/$defs/labels"
      description: "Lineage configuration labels."
    }
  }
}
```

### `$defs.machineLearning`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    enabled: {
      type: "boolean"
      default: false
    }
    framework: {
      type: "string"
      enum: [...5 items...]
    }
    models: {
      type: "array"
      items: {
        type: "object"
        additionalProperties: false
        required: ["name", "version", "type"]
        properties: {
          name: {
            type: "string"
          }
          version: {
            $ref: "#/$defs/semver"
          }
          type: {
            type: "string"
            enum: [...5 items...]
          }
          algorithm: {
            type: "string"
          }
          features: {
            type: "array"
            description: "List of feature names used by this model."
            items: {
              type: "string"
            }
          }
          ... (4 more)
        }
      }
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "ML configuration tags."
    }
    labels: {
      $ref: "#/$defs/labels"
      description: "ML configuration labels."
    }
  }
}
```

### `$defs.multiStagePattern`
```json
{
  type: "object"
  description: "NEW in v0.5.5: Multi-stage orchestration pattern."
  additionalProperties: false
  properties: {
    stages: {
      type: "array"
      items: {
        type: "object"
        additionalProperties: false
        properties: {
          name: {
            type: "string"
          }
          pattern: {
            type: "string"
            enum: ["hybrid-reference", "embedded-logic"]
            default: "hybrid-reference"
          }
          properties: {
            $ref: "#/$defs/buildProperties"
          }
          dependsOn: {
            type: "array"
            items: {
              type: "string"
            }
          }
          outputs: {
            type: "array"
            items: {
              $ref: "#/$defs/identifier"
            }
          }
          ... (2 more)
        }
      }
    }
    orchestration: {
      type: "object"
      properties: {
        parallelism: {
          type: "integer"
          minimum: 1
        }
        retryPolicy: {
          $ref: "#/$defs/retryPolicy"
        }
      }
    }
    tags: {
      $ref: "#/$defs/tags"
    }
    labels: {
      $ref: "#/$defs/labels"
    }
  }
}
```

### `$defs.notification.properties.condition`
```json
{
  type: "string"
  enum: ["success", "failure", "always"]
}
```

### `$defs.notification.properties.type`
```json
{
  type: "string"
  enum: [...4 items...]
}
```

### `$defs.observability`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    metrics: {
      type: "array"
      items: {
        type: "object"
        additionalProperties: false
        required: ["name", "source"]
        properties: {
          name: {
            type: "string"
          }
          source: {
            type: "string"
          }
          sli: {
            type: "string"
            description: "Human/machine-readable SLI check description"
          }
        }
      }
    }
    onBreach: {
      type: "array"
      items: {
        type: "object"
        additionalProperties: false
        required: ["type"]
        properties: {
          type: {
            type: "string"
            enum: [...5 items...]
          }
          channel: {
            type: "string"
          }
          target: {
            type: "string"
          }
          url: {
            type: "string"
            format: "uri"
          }
          severity: {
            type: "string"
            enum: ["info", "warning", "critical"]
          }
          ... (2 more)
        }
      }
    }
    defaultSLIs: {
      $ref: "#/$defs/defaultSLIs"
      description: "Default SLI trio (freshness, completeness, latency) by kind."
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Observability configuration tags."
    }
    labels: {
      $ref: "#/$defs/labels"
      description: "Observability configuration labels."
    }
  }
}
```

### `$defs.retryPolicy.properties.backoffStrategy`
```json
{
  type: "string"
  enum: ["fixed", "exponential", "linear"]
}
```

### `$defs.retryPolicy.properties.initialDelay`
```json
{
  type: "string"
}
```

### `$defs.retryPolicy.properties.maxAttempts`
```json
{
  type: "integer"
  minimum: 1
}
```

### `$defs.retryPolicy.properties.maxDelay`
```json
{
  type: "string"
}
```

### `$defs.runtime.properties.environment`
```json
{
  type: "object"
  additionalProperties: {
    type: "string"
  }
}
```

### `$defs.runtime.properties.resources.properties.disk`
```json
{
  type: "string"
}
```

### `$defs.runtime.properties.timeout`
```json
{
  type: "string"
}
```

### `$defs.schemaEvolution`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    strategy: {
      type: "string"
      enum: ["semantic_versioning", "date_based", "sequential"]
      description: "Versioning strategy for schema changes."
    }
    compatibility: {
      type: "string"
      enum: [...4 items...]
      description: "Compatibility approach for schema evolution."
    }
    changePolicy: {
      type: "object"
      additionalProperties: false
      properties: {
        changeWindowDays: {
          type: "integer"
          minimum: 0
          description: "Advance notice period for breaking changes."
        }
        approvalRequired: {
          type: "boolean"
          description: "Whether schema changes require approval."
        }
        approvers: {
          type: "array"
          items: {
            type: "string"
          }
          description: "List of approvers for schema changes."
        }
        tags: {
          $ref: "#/$defs/tags"
          description: "Change policy tags."
        }
        labels: {
          $ref: "#/$defs/labels"
          description: "Change policy labels."
        }
      }
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Schema evolution tags."
    }
    labels: {
      $ref: "#/$defs/labels"
      description: "Schema evolution labels."
    }
  }
}
```

### `$defs.semver`
```json
{
  type: "string"
  pattern: "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-[0-9A-Za-z.-]+)?(?:\\+[0-9A-Za-z.-]+)?$"
  description: "Semantic version (semver.org)."
}
```

### `$defs.semverRange`
```json
{
  type: "string"
  description: "Semver range (e.g., ^1.2, ~1.4, >=1.0.0). Not strictly validated by regex; tooling enforces."
}
```

### `$defs.sensitivityLevel`
```json
{
  type: "string"
  enum: [...11 items...]
  description: "Unified data sensitivity classification."
}
```

### `$defs.tags`
```json
{
  type: "array"
  description: "Simple string tags for categorization, discovery, and automation. Consistent pattern used throughout..."
  items: {
    type: "string"
    pattern: "^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$"
    description: "Tag format: lowercase alphanumeric with hyphens, e.g., 'customer-data', 'pii', 'real-time'"
  }
  uniqueItems: true
}
```

### `$defs.transformation`
```json
{
  type: "object"
  additionalProperties: false
  required: ["name"]
  properties: {
    name: {
      type: "string"
    }
    model: {
      type: "string"
      description: "Path/script identifier (dbt model, sql file, etc.)"
    }
    outputs: {
      type: "array"
      description: "List of exposeIds materialized by this step. VALIDATION: Tools must validate that every output exist..."
      items: {
        $ref: "#/$defs/identifier"
      }
    }
    tags: {
      $ref: "#/$defs/tags"
      description: "Transformation step tags."
    }
    labels: {
      $ref: "#/$defs/labels"
      description: "Transformation step labels."
    }
  }
}
```

### `$defs.trigger.properties`
```json
{
  type: {
    type: "string"
    enum: [...4 items...]
  }
  schedule: {
    type: "string"
  }
  event: {
    type: "string"
  }
  condition: {
    type: "string"
  }
}
```

### `examples`
```json
[{"fluidVersion": "0.5.7", "kind": "DataProduct", "id": "gold.customer.analytics_360_v1", "name": "Customer 360 Analytics", "description": "Unified customer profiles with ML-driven insights", "domain": "Customer Experience", "tags": ["customer-data", "analytics", "gold-layer"], "labels": {"team": "customer-analytics", "criticality": "high", "cost-center": "engineering"}, "metadata": {"layer": "Gold", "owner": {"team": "customer-analytics", "email": "customer-analytics@company.com"}, "businessContext": {"domain": "Customer Experience", "subdomain": "Customer Intelligence"}}, "exposes": [{"exposeId": "customer_profiles", "title": "Unified Customer Profiles", "version": "2.1.0", "kind": "table", "tags": ["pii", "customer-facing", "real-time"], "labels": {"sensitivity": "high", "retention": "7-years", "region": "us-central1"}, "contract": {"schema": [{"name": "customer_id", "type": "STRING", "required": true, "description": "Unique customer identifier", "sensitivity": "cleartext", "tags": ["identifier", "primary-key"], "labels": {"business-name": "Customer ID", "data-category": "identifier"}}]}, "binding": {"platform": "gcp", "format": "bigquery_table", "location": {"project": "company-data", "dataset": "gold_customer", "table": "profiles_v1"}}}]}]
```

### `properties.build.$ref`
```json
"#/$defs/build"
```

### `properties.builds`
```json
{
  type: "array"
  description: "NEW in v0.5.5: Multiple build configurations for multi-modal data products (e.g., batch + streaming,..."
  items: {
    $ref: "#/$defs/build"
  }
}
```

### `properties.docs`
```json
{
  $ref: "#/$defs/docs"
}
```

### `properties.environments`
```json
{
  type: "object"
  description: "Optional environment-specific overrides (dev, staging, prod)."
  additionalProperties: {
    $ref: "#/$defs/environmentConfig"
  }
}
```

### `properties.fluidVersion.const`
```json
"0.5.7"
```

### `properties.id.$ref`
```json
"#/$defs/identifier"
```

### `properties.kind.enum`
```json
["DataProduct", "MLPipeline"]
```

### `properties.labels`
```json
{
  $ref: "#/$defs/labels"
  description: "Product-level labels for metadata and automation."
}
```

### `properties.lifecycle`
```json
{
  $ref: "#/$defs/lifecycle"
}
```

### `properties.lineage`
```json
{
  $ref: "#/$defs/lineage"
  description: "Optional lineage tracking for better data governance."
}
```

### `properties.machineLearning`
```json
{
  $ref: "#/$defs/machineLearning"
  description: "Optional ML model specifications for MLPipeline kind."
}
```

### `properties.metadata.additionalProperties`
```json
false
```

### `properties.metadata.properties`
```json
{
  layer: {
    type: "string"
    description: "Data layer label (e.g., Bronze/Silver/Gold). Free-form."
  }
  owner: {
    type: "object"
    additionalProperties: false
    properties: {
      team: {
        type: "string"
      }
      email: {
        type: "string"
        format: "email"
      }
      slack: {
        type: "string"
      }
      oncall: {
        type: "string"
        description: "Oncall rotation or contact for operational issues."
      }
    }
  }
  createdAt: {
    type: "string"
    format: "date-time"
  }
  businessContext: {
    type: "object"
    description: "Business alignment information for data mesh organization."
    additionalProperties: false
    properties: {
      domain: {
        type: "string"
        description: "Business domain this product belongs to."
      }
      subdomain: {
        type: "string"
        description: "Business subdomain for more granular organization."
      }
      businessCapability: {
        type: "string"
        description: "Business capability this product supports."
      }
      valueStream: {
        type: "string"
        description: "Value stream this product participates in."
      }
    }
  }
}
```

### `properties.metadata.required`
```json
["owner"]
```

### `properties.metadata.type`
```json
"object"
```

### `properties.name.minLength`
```json
1
```

### `properties.schemaEvolution`
```json
{
  $ref: "#/$defs/schemaEvolution"
  description: "Optional schema evolution strategy for managing changes."
}
```

### `properties.tags`
```json
{
  $ref: "#/$defs/tags"
  description: "Product-level tags for categorization and discovery."
}
```

## ❌ Removed Properties

### `$defs.accessGrant`
```json
{
  type: "object"
  properties: {
    principal: {
      type: "string"
    }
    permissions: {
      type: "array"
      items: {
        type: "string"
        enum: ["readData", "readMetadata", "manage"]
      }
    }
  }
}
```

### `$defs.accessPolicy`
```json
{
  type: "object"
  properties: {
    grants: {
      type: "array"
      items: {
        $ref: "#/$defs/accessGrant"
      }
    }
  }
}
```

### `$defs.column.properties.name.pattern`
```json
"^[a-zA-Z0-9_]+$"
```

### `$defs.column.properties.nullable`
```json
{
  type: "boolean"
  default: true
}
```

### `$defs.column.properties.semantic`
```json
{
  type: "string"
}
```

### `$defs.column.properties.tags.items`
```json
{
  type: "string"
}
```

### `$defs.column.properties.tags.type`
```json
"array"
```

### `$defs.consume`
```json
{
  type: "object"
  properties: {
    id: {
      type: "string"
      description: "A local alias for the consumed data source."
      pattern: "^[a-zA-Z0-9_.-]+$"
    }
    ref: {
      type: "string"
      description: "A reference to another data product (e.g., URN)."
    }
    description: {
      type: "string"
    }
  }
  required: ["id", "ref"]
}
```

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

### `$defs.expose.description`
```json
"A single output port of the data product."
```

### `$defs.expose.properties.description`
```json
{
  type: "string"
}
```

### `$defs.expose.properties.id`
```json
{
  type: "string"
  description: "The unique identifier for this output port."
  pattern: "^[a-zA-Z0-9_.-]+$"
}
```

### `$defs.expose.properties.location`
```json
{
  $ref: "#/$defs/location"
}
```

### `$defs.expose.properties.mappings`
```json
{
  description: "OPTIONAL. Column-level lineage and rules for governance. SHOULD be generated from build.transformati..."
  type: "array"
  items: {
    $ref: "#/$defs/mapping"
  }
  readOnly: true
}
```

### `$defs.expose.properties.privacy`
```json
{
  type: "array"
  items: {
    $ref: "#/$defs/privacyRule"
  }
}
```

### `$defs.expose.properties.quality`
```json
{
  type: "array"
  items: {
    $ref: "#/$defs/qualityRule"
  }
}
```

### `$defs.expose.properties.schema`
```json
{
  type: "array"
  items: {
    $ref: "#/$defs/column"
  }
}
```

### `$defs.expose.properties.semantics`
```json
{
  $ref: "#/$defs/semantics"
}
```

### `$defs.expose.properties.tags.properties`
```json
{
  archetype: {
    type: "string"
    enum: [...5 items...]
  }
  relationships: {
    type: "array"
    items: {
      $ref: "#/$defs/relationship"
    }
  }
}
```

### `$defs.expose.properties.tags.type`
```json
"object"
```

### `$defs.expose.properties.type`
```json
{
  type: "string"
  description: "The physical type of the output."
}
```

### `$defs.governance`
```json
{
  type: "object"
  properties: {
    lineage: {
      type: "string"
    }
    regulatory: {
      type: "array"
      items: {
        type: "string"
        enum: [...4 items...]
      }
    }
    stewardship: {
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
  }
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

### `$defs.lifecycle.properties.deletionPolicy`
```json
{
  type: "string"
  enum: ["hard-delete", "soft-delete", "anonymize"]
}
```

### `$defs.lifecycle.properties.retentionPeriodDays`
```json
{
  type: "integer"
  minimum: 0
}
```

### `$defs.location`
```json
{
  type: "object"
  properties: {
    format: {
      type: "string"
    }
    properties: {
      type: "object"
      description: "Technology-specific properties (e.g., dataset, table, bucket)."
    }
  }
  required: ["properties"]
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

### `$defs.mapping`
```json
{
  type: "object"
  properties: {
    target: {
      type: "string"
      pattern: "^[a-zA-Z0-9_]+$"
    }
    sources: {
      type: "array"
      items: {
        type: "string"
      }
    }
    rule: {
      type: "string"
    }
  }
  required: ["target", "sources", "rule"]
}
```

### `$defs.metadata`
```json
{
  type: "object"
  properties: {
    layer: {
      type: "string"
      enum: [...4 items...]
      description: "The architectural layer of the data product."
    }
    owner: {
      description: "The team or individual responsible for the data product."
      oneOf: [{"type": "string", "description": "A contact email address for the owner.", "format": "email"}, {"type": "object", "properties": {"team": {"type": "string"}, "email": {"type": "string", "format": "email"}, "slack": {"type": "string"}}, "required": ["team"]}]
    }
    status: {
      type: "string"
      enum: ["Development", "Published", "Deprecated"]
      default: "Development"
    }
    tags: {
      type: "array"
      items: {
        type: "string"
      }
      description: "A list of arbitrary tags for categorization."
    }
  }
  required: ["layer", "owner"]
}
```

### `$defs.notification.properties.channel`
```json
{
  type: "string"
  enum: [...4 items...]
}
```

### `$defs.operations`
```json
{
  type: "object"
  properties: {
    sla: {
      $ref: "#/$defs/sla"
    }
    lifecycle: {
      $ref: "#/$defs/lifecycle"
    }
  }
}
```

### `$defs.privacyRule`
```json
{
  type: "object"
  properties: {
    classification: {
      type: "string"
      enum: ["PII", "SPI", "Confidential"]
    }
    columns: {
      type: "array"
      items: {
        type: "string"
      }
    }
    treatment: {
      type: "object"
      properties: {
        type: {
          type: "string"
          enum: [...4 items...]
        }
      }
      required: ["type"]
    }
  }
  required: ["columns", "treatment"]
}
```

### `$defs.qualityRule`
```json
{
  type: "object"
  properties: {
    name: {
      type: "string"
    }
    rule: {
      type: "string"
    }
    onFailure: {
      type: "object"
      properties: {
        action: {
          type: "string"
          enum: [...4 items...]
        }
      }
      required: ["action"]
    }
  }
  required: ["name", "rule", "onFailure"]
}
```

### `$defs.relationship`
```json
{
  type: "object"
  properties: {
    to: {
      type: "string"
    }
    cardinality: {
      type: "string"
      enum: [...4 items...]
    }
    description: {
      type: "string"
    }
  }
  required: ["to", "cardinality"]
}
```

### `$defs.retryPolicy.properties.backoff`
```json
{
  type: "string"
  enum: ["none", "exponential"]
  default: "none"
}
```

### `$defs.retryPolicy.properties.count`
```json
{
  type: "integer"
  minimum: 0
  default: 0
}
```

### `$defs.retryPolicy.properties.delaySeconds`
```json
{
  type: "integer"
  minimum: 0
  default: 0
}
```

### `$defs.runtime.properties.platform`
```json
{
  type: "string"
}
```

### `$defs.security`
```json
{
  type: "object"
  properties: {
    encryptionAtRest: {
      type: "string"
      default: "AES256"
    }
    encryptionInTransit: {
      type: "string"
      default: "TLS1.2+"
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

### `$defs.semantics`
```json
{
  type: "object"
  properties: {
    ontology: {
      type: "string"
      format: "uri"
    }
    classifications: {
      type: "object"
      additionalProperties: {
        type: "string"
      }
    }
  }
}
```

### `$defs.sla`
```json
{
  type: "object"
  properties: {
    latencyMs: {
      type: "integer"
      minimum: 0
    }
    freshnessMinutes: {
      type: "integer"
      minimum: 0
    }
    availabilityPct: {
      type: "number"
      minimum: 0
      maximum: 100
    }
  }
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

### `$defs.trigger.description`
```json
"Defines how the build is initiated."
```

### `$defs.trigger.oneOf`
```json
[{"properties": {"type": {"const": "schedule"}, "cron": {"type": "string"}}, "required": ["type", "cron"]}, {"properties": {"type": {"const": "event"}, "eventType": {"type": "string"}}, "required": ["type", "eventType"]}, {"properties": {"type": {"const": "manual"}}, "required": ["type"]}]
```

### `properties.accessPolicy`
```json
{
  $ref: "#/$defs/accessPolicy"
}
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
      }
    }
    required: ["pattern", "engine", "properties"]
    allOf: [...4 items...]
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

### `properties.consumes.description`
```json
"An optional list of input data sources required to build the product."
```

### `properties.description.description`
```json
"A brief, business-focused description of the product's purpose."
```

### `properties.domain.pattern`
```json
"^[a-zA-Z0-9_.-]+$"
```

### `properties.exposes.description`
```json
"The public output interfaces (ports) of the data product."
```

### `properties.governance`
```json
{
  $ref: "#/$defs/governance"
}
```

### `properties.id.minLength`
```json
1
```

### `properties.id.pattern`
```json
"^[a-zA-Z0-9_.-]+$"
```

### `properties.id.type`
```json
"string"
```

### `properties.kind.examples`
```json
[...6 items...]
```

### `properties.metadata.$ref`
```json
"#/$defs/metadata"
```

### `properties.name.description`
```json
"Human-readable product name."
```

### `properties.operations`
```json
{
  $ref: "#/$defs/operations"
}
```

### `properties.security`
```json
{
  $ref: "#/$defs/security"
}
```

### `properties.slo`
```json
{
  $ref: "#/$defs/sla"
}
```

## 📝 Modified Properties

### `$defs.embeddedLogicPattern.properties.language.enum`

**Before:**
```json
[...4 items...]
```

**After:**
```json
[...6 items...]
```

### `$defs.expose.required`

**Before:**
```json
[...4 items...]
```

**After:**
```json
[...4 items...]
```

### `$id`

**Before:**
```json
"https://open-data-protocol.org/fluid/fluid.schema.v0.4.0.json"
```

**After:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.5.7.json"
```

### `description`

**Before:**
```json
"A comprehensive, production-ready schema for FLUID data product contracts. Version 0.4.0 replaces th..."
```

**After:**
```json
"FLUID Data Product contract (v0.5.7). Enhanced build section with:
• Multiple build objects for mult..."
```

### `properties.build.description`

**Before:**
```json
"Describes the logical transformation process and its operational details."
```

**After:**
```json
"Single build configuration (legacy). Use 'builds' array for multi-modal."
```

### `properties.consumes.items.$ref`

**Before:**
```json
"#/$defs/consume"
```

**After:**
```json
"#/$defs/consumeRef"
```

### `properties.domain.description`

**Before:**
```json
"The owning business domain (e.g., 'Marketing', 'Finance')."
```

**After:**
```json
"Business domain/mesh domain (e.g., 'HR', 'Finance')."
```

### `properties.fluidVersion.description`

**Before:**
```json
"Version of the FLUID spec this contract adheres to."
```

**After:**
```json
"Contract schema version. Must be exactly '0.5.7' for this schema."
```

### `properties.fluidVersion.examples`

**Before:**
```json
["0.4.0"]
```

**After:**
```json
["0.5.7"]
```

### `properties.id.description`

**Before:**
```json
"Globally-unique, versioned data product identifier. Should be machine-friendly."
```

**After:**
```json
"Stable product identifier, e.g. 'gold.hr.employee_360_v1'."
```

### `properties.kind.description`

**Before:**
```json
"The type of data product definition."
```

**After:**
```json
"Kind of contract. 'MLPipeline' added for basic ML support."
```

### `required`

**Before:**
```json
[...8 items...]
```

**After:**
```json
[...6 items...]
```

### `title`

**Before:**
```json
"FLUID (Federated Layered Unified Interchange Definition) Specification"
```

**After:**
```json
"FLUID 0.5.7 \u2014 Data Product Contract"
```
