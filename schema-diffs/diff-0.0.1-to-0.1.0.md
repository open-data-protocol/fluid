# Schema Changes: 0.0.1 → 0.1.0

**Total changes:** 176
- ✅ Added: 34
- ❌ Removed: 113
- 📝 Modified: 29

---

## ✅ Added Properties

### `$defs.build.description`
```json
"Describes the logical transformation process and its operational details."
```

### `$defs.build.properties.config`
```json
{
  type: "object"
  description: "Engine-specific configuration key-value pairs."
  additionalProperties: true
}
```

### `$defs.build.properties.engine.description`
```json
"The transformation engine used."
```

### `$defs.build.properties.model`
```json
{
  type: "string"
  description: "A reference to the specific model or script (e.g., dbt model path)."
}
```

### `$defs.column.properties.name.type`
```json
"string"
```

### `$defs.column.properties.tags`
```json
{
  type: "array"
  items: {
    type: "string"
  }
  description: "Semantic tags like 'primary_key', 'foreign_key', 'pii'."
}
```

### `$defs.consume.properties.description`
```json
{
  type: "string"
}
```

### `$defs.consume.properties.id`
```json
{
  type: "string"
  description: "A local alias for the consumed data source."
}
```

### `$defs.consume.properties.ref`
```json
{
  type: "string"
  description: "A reference to another data product (e.g., URN)."
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
}
```

### `$defs.expose.properties.privacy`
```json
{
  description: "A list of privacy treatments applied to columns in this port."
  type: "array"
  items: {
    $ref: "#/$defs/privacyRule"
  }
}
```

### `$defs.expose.properties.quality`
```json
{
  description: "A list of quality rules specific to this port."
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

### `$defs.expose.properties.tags`
```json
{
  type: "object"
  properties: {
    archetype: {
      type: "string"
      enum: [...5 items...]
      description: "The modeling archetype of the port."
    }
    relationships: {
      type: "array"
      items: {
        $ref: "#/$defs/relationship"
      }
    }
  }
}
```

### `$defs.expose.properties.type`
```json
{
  type: "string"
  description: "The physical type of the output (e.g., 'snowflake_table', 'bigquery_view')."
}
```

### `$defs.location.properties.format.enum`
```json
[...5 items...]
```

### `$defs.metadata.properties.owner.description`
```json
"The team or individual responsible for the data product."
```

### `$defs.metadata.properties.owner.oneOf`
```json
[{"type": "string", "description": "A contact email address for the owner."}, {"type": "object", "properties": {"team": {"type": "string"}, "email": {"type": "string", "format": "email"}, "slack": {"type": "string"}}, "required": ["team"]}]
```

### `$defs.metadata.properties.tags.items`
```json
{
  type: "string"
}
```

### `$defs.qualityRule.properties.name`
```json
{
  type: "string"
}
```

### `$defs.relationship`
```json
{
  type: "object"
  properties: {
    to: {
      type: "string"
      description: "The 'id' of the target port for the relationship."
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

### `properties.consumes.items`
```json
{
  $ref: "#/$defs/consume"
}
```

### `properties.consumes.type`
```json
"array"
```

### `properties.exposes.items`
```json
{
  $ref: "#/$defs/expose"
}
```

### `properties.exposes.minItems`
```json
1
```

### `properties.exposes.type`
```json
"array"
```

### `properties.slo`
```json
{
  $ref: "#/$defs/sla"
}
```

## ❌ Removed Properties

### `$defs.accessGrant.additionalProperties`
```json
false
```

### `$defs.accessGrant.properties.permissions.minItems`
```json
1
```

### `$defs.accessGrant.properties.principal.pattern`
```json
"^(user:[^\\s@]+@[^\\s@]+\\.[^\\s@]+|group:[A-Za-z0-9_.-]+|agent:[A-Za-z0-9_.:-]+)$"
```

### `$defs.accessGrant.properties.scope`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    columns: {
      type: "array"
      items: {
        type: "string"
      }
    }
    rowFilter: {
      type: "string"
      description: "SQL WHERE clause."
    }
    privacyView: {
      type: "string"
      enum: ["treated", "cleartext"]
      default: "treated"
    }
  }
}
```

### `$defs.accessPolicy.additionalProperties`
```json
false
```

### `$defs.accessPolicy.properties.auditLog`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    enabled: {
      type: "boolean"
      default: true
    }
    destination: {
      type: "string"
      description: "Log sink or endpoint."
    }
    retentionDays: {
      type: "integer"
      minimum: 1
      default: 365
    }
  }
}
```

### `$defs.accessPolicy.properties.grants.minItems`
```json
1
```

### `$defs.accessPolicy.properties.visibility`
```json
{
  type: "string"
  enum: ["private", "internal"]
  default: "internal"
}
```

### `$defs.accessPolicy.required`
```json
["grants"]
```

### `$defs.build.additionalProperties`
```json
false
```

### `$defs.build.properties.dependencies`
```json
{
  type: "array"
  items: {
    $ref: "#/$defs/dependency"
  }
}
```

### `$defs.build.properties.script`
```json
{
  type: "string"
  description: "Script path, query, or model selector."
}
```

### `$defs.column.additionalProperties`
```json
false
```

### `$defs.column.properties.name.$ref`
```json
"#/$defs/nonEmptyString"
```

### `$defs.column.properties.type.oneOf`
```json
[{"enum": ["STRING", "INT64", "NUMERIC", "TIMESTAMP", "JSON", "BOOLEAN", "DATE", "FLOAT64", "BYTES"]}, {"pattern": "^[A-Za-z]+:[A-Za-z0-9_.-]+$"}]
```

### `$defs.conformance`
```json
{
  type: "string"
  description: "Compliance tier to support graduated adoption."
  enum: ["Core", "Extended", "Enterprise"]
  default: "Core"
}
```

### `$defs.consume.additionalProperties`
```json
false
```

### `$defs.consume.allOf`
```json
[{"if": {"properties": {"type": {"const": "fluid-product"}}}, "then": {"required": ["name"]}}, {"if": {"properties": {"type": {"enum": ["gcs", "kafka", "s3", "api", "postgres-cdc", "sftp", "snowflake", "bigquery"]}}}, "then": {"required": ["connection"]}}]
```

### `$defs.consume.properties.alias`
```json
{
  type: "string"
}
```

### `$defs.consume.properties.connection`
```json
{
  type: "string"
  pattern: "^(secret:).+"
  description: "Vault secret reference (required for physical types)."
}
```

### `$defs.consume.properties.format`
```json
{
  type: "object"
  properties: {
    type: {
      type: "string"
      enum: [...4 items...]
    }
  }
  additionalProperties: true
}
```

### `$defs.consume.properties.name`
```json
{
  type: "string"
  description: "Upstream FLUID product name (required when type=fluid-product)."
}
```

### `$defs.consume.properties.onUpstreamChange`
```json
{
  type: "string"
  enum: ["fail", "alert", "triggerRebuild"]
  default: "alert"
}
```

### `$defs.consume.properties.properties`
```json
{
  type: "object"
  description: "Technology-specific properties (e.g., topic, endpoint, bucket, path)."
  additionalProperties: true
}
```

### `$defs.consume.properties.type`
```json
{
  type: "string"
  enum: [...9 items...]
}
```

### `$defs.contract`
```json
{
  type: "object"
  additionalProperties: false
  required: ["schema"]
  properties: {
    inheritFrom: {
      type: "string"
      enum: ["dbt", "fluid-product", "openApi"]
    }
    model: {
      type: "string"
      description: "dbt model name (if inheritFrom=dbt)."
    }
    spec: {
      type: "string"
      description: "Path/URL to OpenAPI spec (if inheritFrom=openApi)."
    }
    schema: {
      $ref: "#/$defs/schema"
    }
    quality: {
      type: "array"
      items: {
        $ref: "#/$defs/qualityRule"
      }
    }
    ... (2 more)
  }
  allOf: [{"if": {"properties": {"inheritFrom": {"const": "dbt"}}, "required": ["inheritFrom"]}, "then": {"required": ["model"]}}, {"if": {"properties": {"inheritFrom": {"const": "openApi"}}, "required": ["inheritFrom"]}, "then": {"required": ["spec"]}}]
}
```

### `$defs.dependency`
```json
{
  type: "object"
  additionalProperties: false
  required: ["productId"]
  properties: {
    productId: {
      type: "string"
    }
    minVersion: {
      type: "string"
      pattern: "^\\d+\\.\\d+\\.\\d+$"
    }
    maxVersion: {
      type: "string"
      pattern: "^\\d+\\.\\d+\\.\\d+$"
    }
    policy: {
      type: "string"
      enum: ["strict", "compatible"]
      default: "compatible"
    }
  }
}
```

### `$defs.dynamicPolicies`
```json
{
  type: "object"
  additionalProperties: false
  required: ["rules"]
  properties: {
    rules: {
      type: "array"
      minItems: 1
      items: {
        $ref: "#/$defs/policyRule"
      }
    }
    evaluation: {
      type: "string"
      enum: ["firstMatch", "allMatch"]
      default: "firstMatch"
      description: "Evaluation strategy for rules."
    }
  }
}
```

### `$defs.expose.additionalProperties`
```json
false
```

### `$defs.expose.properties.contract`
```json
{
  $ref: "#/$defs/contract"
}
```

### `$defs.expose.properties.name`
```json
{
  type: "string"
  description: "Unique within product."
}
```

### `$defs.extensionRef`
```json
{
  type: "object"
  additionalProperties: false
  required: ["name"]
  properties: {
    name: {
      type: "string"
    }
    version: {
      type: "string"
    }
    config: {
      type: "object"
      additionalProperties: true
    }
  }
}
```

### `$defs.extensions`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    customTransformations: {
      type: "array"
      items: {
        $ref: "#/$defs/extensionRef"
      }
    }
    policyEngines: {
      type: "array"
      items: {
        $ref: "#/$defs/extensionRef"
      }
    }
    observabilityHooks: {
      type: "array"
      items: {
        $ref: "#/$defs/extensionRef"
      }
    }
  }
}
```

### `$defs.governance.additionalProperties`
```json
false
```

### `$defs.governance.description`
```json
"Org-wide rules that must be satisfied by this product."
```

### `$defs.governance.properties.rules.items.additionalProperties`
```json
false
```

### `$defs.governance.properties.rules.items.properties.policyRef`
```json
{
  type: "string"
  description: "Optional reference to external policy (e.g., OPA bundle, Rego package)."
}
```

### `$defs.governance.properties.rules.items.properties.requirement.description`
```json
"Human-readable requirement (e.g., 'Confidential data must have masking')."
```

### `$defs.lifecycle.additionalProperties`
```json
false
```

### `$defs.lifecycle.properties.archival`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    trigger: {
      type: "string"
      enum: ["time", "event"]
    }
    destination: {
      type: "string"
    }
  }
}
```

### `$defs.lifecycle.properties.retentionCondition`
```json
{
  type: "string"
}
```

### `$defs.lifecycle.properties.retentionPeriodDays.minimum`
```json
0
```

### `$defs.location.additionalProperties`
```json
false
```

### `$defs.location.allOf`
```json
[{"if": {"properties": {"type": {"const": "virtual"}}}, "then": {"properties": {"format": {"type": "null"}}, "required": ["type", "connection", "properties"]}, "else": {"required": ["format"]}}]
```

### `$defs.location.properties.connection`
```json
{
  type: "string"
  description: "Reference to secret in a vault. Format recommendation: secret:<name>."
  pattern: "^(secret:).+"
}
```

### `$defs.location.properties.format.additionalProperties`
```json
true
```

### `$defs.location.properties.format.dependentRequired`
```json
{}
```

### `$defs.location.properties.format.description`
```json
"Required if not virtual."
```

### `$defs.location.properties.format.properties`
```json
{
  type: {
    type: "string"
    enum: [...8 items...]
  }
  compression: {
    type: "string"
  }
}
```

### `$defs.location.properties.properties.additionalProperties`
```json
true
```

### `$defs.location.properties.type`
```json
{
  type: "string"
  description: "Physical/virtual storage or interface."
  enum: [...12 items...]
}
```

### `$defs.metadata.additionalProperties`
```json
false
```

### `$defs.metadata.properties.classification`
```json
{
  type: "string"
  description: "Default data classification for the product."
  enum: [...4 items...]
}
```

### `$defs.metadata.properties.cost_center`
```json
{
  type: "string"
}
```

### `$defs.metadata.properties.owner.$ref`
```json
"#/$defs/owner"
```

### `$defs.metadata.properties.purpose`
```json
{
  $ref: "#/$defs/purpose"
}
```

### `$defs.metadata.properties.sensitivity_level`
```json
{
  type: "string"
  enum: [...4 items...]
}
```

### `$defs.metadata.properties.tags.additionalProperties`
```json
{
  type: "string"
}
```

### `$defs.metadata.properties.tags.propertyNames`
```json
{
  pattern: "^[A-Za-z0-9_.-]+$"
}
```

### `$defs.metadata.properties.version`
```json
{
  type: "string"
  description: "Semantic version of this product definition."
  pattern: "^\\d+\\.\\d+\\.\\d+$"
}
```

### `$defs.nonEmptyString`
```json
{
  type: "string"
  minLength: 1
}
```

### `$defs.notification.additionalProperties`
```json
false
```

### `$defs.notification.properties.on`
```json
{
  type: "string"
  enum: [...4 items...]
  default: "onFailure"
}
```

### `$defs.observability`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    logging: {
      type: "object"
      additionalProperties: false
      properties: {
        level: {
          type: "string"
          enum: [...4 items...]
          default: "INFO"
        }
        destination: {
          type: "string"
        }
      }
    }
    metrics: {
      type: "object"
      description: "Standard metric names to emit."
      additionalProperties: {
        type: "string"
        description: "Metric type or description"
      }
    }
    alerting: {
      type: "object"
      additionalProperties: false
      properties: {
        onFailure: {
          type: "array"
          items: {
            $ref: "#/$defs/notification"
          }
        }
        onDegraded: {
          type: "array"
          items: {
            $ref: "#/$defs/notification"
          }
        }
      }
    }
  }
}
```

### `$defs.operations.additionalProperties`
```json
false
```

### `$defs.operations.properties.observability`
```json
{
  $ref: "#/$defs/observability"
}
```

### `$defs.owner`
```json
{
  type: "object"
  additionalProperties: false
  required: ["team"]
  properties: {
    team: {
      $ref: "#/$defs/nonEmptyString"
    }
    email: {
      type: "string"
      format: "email"
      description: "Team contact email."
    }
    slack: {
      type: "string"
      description: "Slack channel or handle."
    }
    pagerduty: {
      type: "string"
      description: "PagerDuty service ID."
    }
  }
}
```

### `$defs.policyRule`
```json
{
  type: "object"
  additionalProperties: false
  required: ["name", "condition", "grant"]
  properties: {
    name: {
      $ref: "#/$defs/nonEmptyString"
    }
    language: {
      type: "string"
      enum: ["CEL", "Rego"]
      default: "CEL"
      description: "Expression language used for `condition`."
    }
    condition: {
      type: "string"
      description: "Boolean expression evaluated against the request/agent context (e.g., CEL: request.user.role == "ana..."
    }
    grant: {
      $ref: "#/$defs/accessGrant"
    }
  }
}
```

### `$defs.privacyRule.additionalProperties`
```json
false
```

### `$defs.privacyRule.properties.classification.description`
```json
"Overrides metadata.classification if provided. Precedence: privacy > metadata."
```

### `$defs.privacyRule.properties.columns.description`
```json
"Use ['*'] for all columns."
```

### `$defs.privacyRule.properties.columns.minItems`
```json
1
```

### `$defs.privacyRule.properties.treatment.additionalProperties`
```json
false
```

### `$defs.privacyRule.properties.treatment.properties.properties`
```json
{
  type: "object"
  additionalProperties: true
}
```

### `$defs.purpose`
```json
{
  type: "object"
  additionalProperties: false
  required: ["business_purpose"]
  properties: {
    business_purpose: {
      $ref: "#/$defs/nonEmptyString"
    }
    use_cases: {
      type: "array"
      items: {
        $ref: "#/$defs/nonEmptyString"
      }
    }
    target_group: {
      type: "array"
      items: {
        $ref: "#/$defs/nonEmptyString"
      }
    }
    limitations: {
      type: "string"
    }
  }
}
```

### `$defs.qualityRule.additionalProperties`
```json
false
```

### `$defs.qualityRule.properties.columns`
```json
{
  type: "array"
  items: {
    type: "string"
  }
}
```

### `$defs.qualityRule.properties.onFailure.additionalProperties`
```json
false
```

### `$defs.qualityRule.properties.onFailure.properties.notifications`
```json
{
  type: "array"
  items: {
    $ref: "#/$defs/notification"
  }
}
```

### `$defs.qualityRule.properties.pattern`
```json
{
  type: "string"
}
```

### `$defs.qualityRule.properties.rule.oneOf`
```json
[{"enum": ["not_null", "unique", "regex_match", "in_set"]}, {"pattern": "^SQL:.*", "flags": "i"}]
```

### `$defs.qualityRule.properties.set`
```json
{
  type: "array"
  items: {
    type: "string"
  }
}
```

### `$defs.retryPolicy.additionalProperties`
```json
false
```

### `$defs.runtime.additionalProperties`
```json
false
```

### `$defs.runtime.properties.entrypoint`
```json
{
  type: "string"
}
```

### `$defs.runtime.properties.env`
```json
{
  type: "object"
  additionalProperties: {
    type: "string"
  }
}
```

### `$defs.runtime.properties.image`
```json
{
  type: "string"
  description: "Container image or runtime image."
}
```

### `$defs.runtime.properties.resources.additionalProperties`
```json
true
```

### `$defs.runtime.properties.resources.description`
```json
"Resource hints (not scheduling guarantees)."
```

### `$defs.runtime.properties.resources.properties.gpu`
```json
{
  type: "string"
}
```

### `$defs.schema`
```json
{
  type: "object"
  additionalProperties: false
  required: ["columns"]
  properties: {
    columns: {
      type: "array"
      minItems: 1
      items: {
        $ref: "#/$defs/column"
      }
    }
    primaryKey: {
      type: "array"
      items: {
        type: "string"
      }
    }
    uniqueKeys: {
      type: "array"
      items: {
        type: "array"
        minItems: 1
        items: {
          type: "string"
        }
      }
    }
    indexes: {
      type: "array"
      items: {
        type: "object"
        additionalProperties: false
        required: ["columns"]
        properties: {
          name: {
            type: "string"
          }
          columns: {
            type: "array"
            minItems: 1
            items: {
              type: "string"
            }
          }
        }
      }
    }
  }
}
```

### `$defs.security.additionalProperties`
```json
false
```

### `$defs.security.allOf`
```json
[{"if": {"properties": {"encryptionAtRest": {"const": "KMS"}}}, "then": {"required": ["kmsKey"]}}]
```

### `$defs.security.properties.kmsKey`
```json
{
  type: "string"
  description: "If encryptionAtRest=KMS, reference key name/ARN/resource."
}
```

### `$defs.semantics.additionalProperties`
```json
false
```

### `$defs.semantics.properties.classifications.description`
```json
"Map column -> ontology/glossary term."
```

### `$defs.semantics.properties.ontology.description`
```json
"URL to ontology (OWL/RDF/etc)."
```

### `$defs.sla.additionalProperties`
```json
false
```

### `$defs.sla.properties.accuracyPct`
```json
{
  type: "number"
  minimum: 0
  maximum: 100
}
```

### `$defs.sla.properties.availabilityPct.maximum`
```json
100
```

### `$defs.sla.properties.availabilityPct.minimum`
```json
0
```

### `$defs.sla.properties.costPerQuery`
```json
{
  type: "number"
  minimum: 0
}
```

### `$defs.sla.properties.feedbackSignals`
```json
{
  type: "array"
  items: {
    type: "string"
  }
}
```

### `$defs.sla.properties.freshnessMinutes.minimum`
```json
0
```

### `$defs.sla.properties.latencyMs.minimum`
```json
0
```

### `$defs.sla.properties.sustainability`
```json
{
  type: "object"
  additionalProperties: false
  properties: {
    emissionsPerRunKgCO2e: {
      type: "number"
      minimum: 0
    }
  }
}
```

### `$defs.trigger.additionalProperties`
```json
false
```

### `examples`
```json
[{"fluidVersion": "1.1.0", "kind": "DataProduct", "id": "marketing.customer360:1.2.0", "name": "Customer 360", "description": "Unified view of customers for analytics and activation.", "domain": "Marketing", "metadata": {"owner": {"team": "marketing-data", "email": "mdt@example.com"}, "layer": "Gold", "status": "Published", "classification": "confidential", "tags": {"subject": "customers", "region": "EU"}, "version": "1.2.0", "purpose": {"business_purpose": "Enable personalization and attribution.", "use_cases": ["segmentation", "LTV modeling"], "target_group": ["analysts", "ml-engineers"]}}, "consumes": [{"type": "kafka", "alias": "events", "connection": "secret:kafka-prod", "properties": {"topic": "events.customer"}}, {"type": "fluid-product", "name": "sales.orders:2.0.0", "alias": "orders", "onUpstreamChange": "triggerRebuild"}], "build": {"engine": "dbt", "script": "models/marts/customers.sql", "trigger": {"type": "schedule", "cron": "0 * * * *", "timezone": "UTC"}, "runtime": {"platform": "dbt-cloud"}, "retries": {"count": 3, "delaySeconds": 60, "backoff": "exponential"}, "notifications": [{"channel": "slack", "target": "#data-alerts", "on": "onFailure"}]}, "exposes": {"name": "warehouse_table", "location": {"type": "bigquery", "connection": "secret:gcp-dwh", "format": {"type": "parquet"}, "properties": {"project": "proj", "dataset": "dwh", "table": "customer360"}}, "contract": {"schema": {"columns": [{"name": "customer_id", "type": "STRING", "nullable": false}, {"name": "email", "type": "STRING"}, {"name": "created_at", "type": "TIMESTAMP"}], "primaryKey": ["customer_id"]}, "quality": [{"rule": "not_null", "columns": ["customer_id"], "onFailure": {"action": "fail_pipeline"}}, {"rule": "regex_match", "columns": ["email"], "pattern": "^[^@]+@[^@]+\\.[^@]+$", "onFailure": {"action": "quarantine_row"}}], "privacy": [{"classification": "PII", "columns": ["email"], "treatment": {"type": "hashing"}}], "semantics": {"ontology": "https://example.org/ontologies/customer.owl", "classifications": {"customer_id": "Customer", "email": "EmailAddress"}}}}, "accessPolicy": {"visibility": "internal", "grants": [{"principal": "group:analysts", "permissions": ["readData", "readMetadata"], "scope": {"privacyView": "treated"}}, {"principal": "user:owner@example.com", "permissions": ["manage", "readData", "readMetadata"]}], "auditLog": {"enabled": true, "destination": "log://central/sec-audit", "retentionDays": 365}}, "dynamicPolicies": {"evaluation": "firstMatch", "rules": [{"name": "Row-level EU filter", "language": "CEL", "condition": "request.user.region == 'EU' && request.purpose == 'analytics'", "grant": {"principal": "group:analysts", "permissions": ["readData"], "scope": {"rowFilter": "region = 'EU'", "privacyView": "treated"}}}]}, "operations": {"sla": {"latencyMs": 60000, "freshnessMinutes": 60, "availabilityPct": 99.5}, "lifecycle": {"retentionPeriodDays": 1095, "deletionPolicy": "anonymize"}, "observability": {"logging": {"level": "INFO", "destination": "log://central/data"}, "alerting": {"onFailure": [{"channel": "pagerduty", "target": "dp-c360"}]}}}, "extensions": {"policyEngines": [{"name": "opa", "version": "0.63.0"}]}, "security": {"encryptionAtRest": "KMS", "kmsKey": "projects/x/locations/y/keyRings/z/cryptoKeys/k"}, "governance": {"rules": [{"name": "Mask PII", "requirement": "All PII columns must have a privacy treatment.", "policyRef": "rego://org/policies/privacy.piimask"}]}, "conformance": "Extended"}]
```

### `properties.conformance`
```json
{
  $ref: "#/$defs/conformance"
}
```

### `properties.consumes.oneOf`
```json
[{"$ref": "#/$defs/consume"}, {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/consume"}}]
```

### `properties.dynamicPolicies`
```json
{
  $ref: "#/$defs/dynamicPolicies"
}
```

### `properties.exposes.oneOf`
```json
[{"$ref": "#/$defs/expose"}, {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/expose"}}]
```

### `properties.extensions`
```json
{
  $ref: "#/$defs/extensions"
}
```

## 📝 Modified Properties

### `$defs.accessGrant.properties.principal.description`

**Before:**
```json
"user:<email>, group:<name>, agent:<id>"
```

**After:**
```json
"e.g., group:analysts, user:name@company.com"
```

### `$defs.build.required`

**Before:**
```json
[...4 items...]
```

**After:**
```json
["engine", "model"]
```

### `$defs.column.properties.semantic.description`

**Before:**
```json
"Reference to ontology term or glossary ID."
```

**After:**
```json
"Reference to an ontology term or glossary ID."
```

### `$defs.column.properties.type.description`

**Before:**
```json
"Logical type. Vendor-specific types allowed via namespacing (e.g., vendor:snowflake.VARIANT)."
```

**After:**
```json
"The physical data type."
```

### `$defs.consume.required`

**Before:**
```json
["type"]
```

**After:**
```json
["id", "ref"]
```

### `$defs.expose.required`

**Before:**
```json
["location", "contract"]
```

**After:**
```json
[...4 items...]
```

### `$defs.location.properties.format.type`

**Before:**
```json
"object"
```

**After:**
```json
"string"
```

### `$defs.location.properties.properties.description`

**Before:**
```json
"Technology-specific properties (e.g., project, dataset, table, topic, endpoint)."
```

**After:**
```json
"Technology-specific properties (e.g., project, dataset, table)."
```

### `$defs.location.required`

**Before:**
```json
["type", "connection", "properties"]
```

**After:**
```json
["properties"]
```

### `$defs.metadata.properties.layer.description`

**Before:**
```json
"Architectural layer."
```

**After:**
```json
"The architectural layer of the data product."
```

### `$defs.metadata.properties.tags.description`

**Before:**
```json
"Arbitrary key/value tags."
```

**After:**
```json
"A list of arbitrary tags for categorization."
```

### `$defs.metadata.properties.tags.type`

**Before:**
```json
"object"
```

**After:**
```json
"array"
```

### `$defs.metadata.required`

**Before:**
```json
["owner", "classification"]
```

**After:**
```json
["layer", "owner"]
```

### `$defs.notification.properties.channel.enum`

**Before:**
```json
[...4 items...]
```

**After:**
```json
[...4 items...]
```

### `$defs.qualityRule.properties.rule.description`

**Before:**
```json
"Rule name or SQL predicate."
```

**After:**
```json
"The rule to be enforced (e.g., 'not_null', 'unique', or a SQL predicate)."
```

### `$defs.qualityRule.required`

**Before:**
```json
["rule", "onFailure"]
```

**After:**
```json
["name", "rule", "onFailure"]
```

### `$defs.runtime.properties.platform.enum`

**Before:**
```json
[...8 items...]
```

**After:**
```json
[...5 items...]
```

### `$defs.trigger.oneOf`

**Before:**
```json
[{"title": "Schedule", "type": "object", "required": ["type", "cron"], "properties": {"type": {"const": "schedule"}, "cron": {"type": "string", "description": "Cron expression (Quartz or UNIX).", "pattern": "^([\\s\\S]+)$"}, "timezone": {"type": "string"}}, "additionalProperties": false}, {"title": "Event", "type": "object", "required": ["type", "eventType"], "properties": {"type": {"const": "event"}, "eventType": {"type": "string"}, "eventSchema": {"type": "object", "description": "JSON Schema for event payload.", "additionalProperties": true}, "source": {"type": "string"}}, "additionalProperties": false}, {"title": "Manual", "type": "object", "required": ["type"], "properties": {"type": {"const": "manual"}}, "additionalProperties": false}]
```

**After:**
```json
[{"properties": {"type": {"const": "schedule"}, "cron": {"type": "string"}}, "required": ["type", "cron"]}, {"properties": {"type": {"const": "event"}, "eventType": {"type": "string"}}, "required": ["type", "eventType"]}, {"properties": {"type": {"const": "manual"}}, "required": ["type"]}]
```

### `$id`

**Before:**
```json
"https://open-data-protocol.org/fluid/fluid.schema.json"
```

**After:**
```json
"https://open-data-protocol.org/fluid/fluid.schema.v2.0.json"
```

### `description`

**Before:**
```json
"Machine-validated schema for FLUID data product contracts. Drafted for production use with strong ty..."
```

**After:**
```json
"A comprehensive, production-ready schema for FLUID data product contracts, merging rich operational ..."
```

### `properties.consumes.description`

**Before:**
```json
"Input sources required to build the product."
```

**After:**
```json
"An optional list of input data sources required to build the product."
```

### `properties.description.description`

**Before:**
```json
"Brief description of the product's purpose."
```

**After:**
```json
"A brief, business-focused description of the product's purpose."
```

### `properties.domain.description`

**Before:**
```json
"Owning business domain (e.g., Marketing, Finance)."
```

**After:**
```json
"The owning business domain (e.g., 'Marketing', 'Finance')."
```

### `properties.exposes.description`

**Before:**
```json
"Public output interface(s)."
```

**After:**
```json
"The public output interfaces (ports) of the data product."
```

### `properties.fluidVersion.description`

**Before:**
```json
"Version of the FLUID spec this contract adheres to (semantic version). Major = breaking, minor = add..."
```

**After:**
```json
"Version of the FLUID spec this contract adheres to."
```

### `properties.fluidVersion.examples`

**Before:**
```json
["1.1.0", "1.2.3"]
```

**After:**
```json
["0.1.0"]
```

### `properties.fluidVersion.pattern`

**Before:**
```json
"^1\\.\\d+\\.\\d+$"
```

**After:**
```json
"^\\d+\\.\\d+(\\.\\d+)?$"
```

### `properties.id.description`

**Before:**
```json
"Globally-unique, versioned data product identifier. Recommended format: <domain>.<name>:<semver> or ..."
```

**After:**
```json
"Globally-unique, versioned data product identifier."
```

### `required`

**Before:**
```json
[...10 items...]
```

**After:**
```json
[...8 items...]
```
