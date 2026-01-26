# Schema Changes: 0.5.7 → 0.7.1

**Total changes:** 27
- ✅ Added: 20
- ❌ Removed: 0
- 📝 Modified: 7

---

## ✅ Added Properties

### `$defs.accessPolicy`
```json
{
  type: "object"
  description: "Root-level access control policy for automated IAM binding generation. Defines who can access this d..."
  additionalProperties: false
  properties: {
    grants: {
      type: "array"
      description: "List of access grants to principals (users, groups, service accounts)."
      items: {
        type: "object"
        required: ["principal"]
        additionalProperties: false
        properties: {
          principal: {
            type: "string"
            description: "Identity receiving access. Format: 'user:email@domain.com', 'group:name@domain.com', 'serviceAccount..."
            examples: ["group:data-analytics@company.com", "serviceAccount:pipeline@project.iam.gserviceaccount.com", "user:analyst@company.com"]
          }
          permissions: {
            type: "array"
            description: "Permissions to grant. Will be mapped to provider-specific roles (e.g., BigQuery roles)."
            items: {
              type: "string"
              enum: [...9 items...]
            }
            uniqueItems: true
            examples: [["read", "select"], ["write", "insert", "update"]]
          }
          resources: {
            type: "array"
            description: "Resources this grant applies to. JSONPath expressions referencing exposes[] items. If omitted, appli..."
            items: {
              type: "string"
            }
            examples: ["$.exposes[?(@.exposeId=='customer_table')]", "$.exposes[?(@.kind=='table')]"]
          }
          conditions: {
            type: "object"
            description: "Optional conditions for conditional access (e.g., IP restrictions, time windows)."
            additionalProperties: true
          }
        }
      }
    }
  }
  examples: [{"grants": [{"principal": "group:data-analytics@company.com", "permissions": ["read", "select", "query"]}, {"principal": "serviceAccount:pipeline@project.iam.gserviceaccount.com", "permissions": ["write", "insert", "update", "delete"]}]}]
}
```

### `$defs.agentPolicy`
```json
{
  type: "object"
  description: "NEW in v0.7.1: AI/LLM usage governance. Controls which AI models can consume data and defines usage ..."
  additionalProperties: false
  properties: {
    allowedModels: {
      type: "array"
      description: "Whitelist of AI models permitted to consume this data. Examples: ['gpt-4', 'claude-3-opus', 'gemini-..."
      items: {
        type: "string"
        pattern: "^[a-z0-9][a-z0-9-_.]*[a-z0-9]$|^[a-z0-9]$"
        examples: [...7 items...]
      }
      uniqueItems: true
    }
    deniedModels: {
      type: "array"
      description: "Blacklist of AI models explicitly prohibited from consuming this data. Takes precedence over allowed..."
      items: {
        type: "string"
      }
      uniqueItems: true
    }
    maxTokensPerRequest: {
      type: "integer"
      minimum: 1
      description: "Maximum tokens per AI request. Prevents excessive data exposure in single queries."
      examples: [4096, 8192, 16384]
    }
    maxTokensPerDay: {
      type: "integer"
      minimum: 1
      description: "Daily token limit for AI consumption. Enforces usage quotas."
    }
    allowedUseCases: {
      type: "array"
      description: "Permitted AI use cases. Controls whether data can be used for training, inference, reasoning, etc."
      items: {
        type: "string"
        enum: [...12 items...]
      }
      uniqueItems: true
      examples: [["inference", "reasoning", "summarization"], ["search", "qa", "rag"]]
    }
    ... (8 more)
  }
}
```

### `$defs.airflowOrchestration`
```json
{
  type: "object"
  required: ["dagId"]
  properties: {
    dagId: {
      type: "string"
      pattern: "^[a-z0-9_][a-z0-9_.-]*[a-z0-9_]$|^[a-z0-9_]$"
    }
    dagConfig: {
      type: "object"
      properties: {
        description: {
          type: "string"
        }
        schedule: {
          type: "string"
        }
        startDate: {
          type: "string"
        }
        endDate: {
          type: "string"
        }
        catchup: {
          type: "boolean"
          default: false
        }
        ... (7 more)
      }
    }
    taskDefaults: {
      type: "object"
      description: "Default configuration for all tasks (can be overridden per task)"
      properties: {
        retries: {
          type: "integer"
          minimum: 0
        }
        retryDelay: {
          $ref: "#/$defs/isoDuration"
        }
        executionTimeout: {
          $ref: "#/$defs/isoDuration"
        }
        pool: {
          type: "string"
        }
        queue: {
          type: "string"
        }
        ... (3 more)
      }
    }
    tasks: {
      type: "array"
      minItems: 1
      items: {
        $ref: "#/$defs/airflowTask"
      }
    }
    sensors: {
      type: "array"
      items: {
        $ref: "#/$defs/airflowSensor"
      }
    }
    ... (1 more)
  }
}
```

### `$defs.airflowSensor`
```json
{
  type: "object"
  required: ["taskId", "sensorType"]
  properties: {
    taskId: {
      type: "string"
    }
    sensorType: {
      type: "string"
      enum: [...7 items...]
    }
    params: {
      type: "object"
    }
    pokInterval: {
      type: "integer"
      minimum: 1
      default: 60
    }
    timeout: {
      type: "integer"
      minimum: 1
      default: 3600
    }
    ... (2 more)
  }
}
```

### `$defs.airflowTask`
```json
{
  type: "object"
  required: ["taskId"]
  properties: {
    taskId: {
      type: "string"
      pattern: "^[a-z0-9_][a-z0-9_.-]*[a-z0-9_]$|^[a-z0-9_]$"
    }
    type: {
      type: "string"
      description: "NEW in v0.7.0: Simplified task type taxonomy. Replaces 'operator' field (backward compatible). Types..."
      enum: [...19 items...]
    }
    operator: {
      type: "string"
      description: "DEPRECATED in v0.7.0: Use 'type' instead. Maintained for backward compatibility with v0.6.1 contract..."
    }
    provider: {
      type: "string"
      description: "NEW in v0.7.0: Provider name when type=provider_action. Examples: aws, gcp, azure, snowflake, databr..."
      enum: [...9 items...]
    }
    action: {
      type: "string"
      pattern: "^[a-z0-9_]+\\.[a-z0-9_]+$"
      description: "NEW in v0.7.0: Provider action when type=provider_action. Format: service.operation (e.g., s3.ensure..."
      examples: [...6 items...]
    }
    ... (13 more)
  }
  allOf: [...5 items...]
}
```

### `$defs.buildExecution.properties.orchestration`
```json
{
  type: "object"
  required: ["engine"]
  properties: {
    engine: {
      type: "string"
      enum: [...6 items...]
    }
    mode: {
      type: "string"
      enum: ["generated", "manual", "hybrid"]
      default: "generated"
    }
    generateOnChange: {
      type: "boolean"
      default: true
    }
    airflow: {
      $ref: "#/$defs/airflowOrchestration"
    }
    dagster: {
      type: "object"
    }
    ... (1 more)
  }
}
```

### `$defs.exposePolicy.properties.agentPolicy`
```json
{
  $ref: "#/$defs/agentPolicy"
  description: "NEW in v0.7.1: AI/LLM usage governance - controls which AI models can consume this data and for what..."
}
```

### `$defs.orchestration`
```json
{
  type: "object"
  required: ["engine"]
  properties: {
    engine: {
      type: "string"
      enum: [...6 items...]
    }
    mode: {
      type: "string"
      enum: ["generated", "manual", "hybrid"]
      default: "generated"
    }
    generateOnChange: {
      type: "boolean"
      default: true
    }
    airflow: {
      $ref: "#/$defs/airflowOrchestration"
    }
    dagster: {
      type: "object"
    }
    ... (1 more)
  }
}
```

### `$defs.runtime.properties.executor`
```json
{
  type: "string"
  enum: [...4 items...]
}
```

### `$defs.runtime.properties.image`
```json
{
  type: "string"
  description: "Container image for execution"
}
```

### `$defs.runtime.properties.platform`
```json
{
  type: "string"
  enum: [...9 items...]
}
```

### `$defs.runtime.properties.serviceAccount`
```json
{
  type: "string"
  description: "Service account for cloud execution"
}
```

### `$defs.sovereignty`
```json
{
  type: "object"
  description: "NEW in v0.7.1: Data sovereignty and jurisdiction requirements. Declares WHERE data must reside and e..."
  additionalProperties: false
  properties: {
    jurisdiction: {
      type: "string"
      description: "Required legal jurisdiction for data storage and processing. Used to validate binding.location match..."
      enum: [...11 items...]
      examples: ["EU", "US", "Global"]
    }
    allowedRegions: {
      type: "array"
      description: "Explicit list of allowed cloud regions. Example: ['eu-west-1', 'eu-central-1'] for EU-only."
      items: {
        type: "string"
      }
      uniqueItems: true
      examples: [["eu-west-1", "eu-central-1"], ["us-east-1", "us-west-2"]]
    }
    deniedRegions: {
      type: "array"
      description: "Explicit list of prohibited cloud regions. Takes precedence over allowedRegions."
      items: {
        type: "string"
      }
      uniqueItems: true
    }
    dataResidency: {
      type: "boolean"
      default: true
      description: "Whether data must remain within jurisdiction boundaries at rest and in transit. True = strict reside..."
    }
    crossBorderTransfer: {
      type: "boolean"
      default: false
      description: "Whether cross-border data transfer is permitted. False = data never leaves jurisdiction."
    }
    ... (6 more)
  }
  examples: [{"jurisdiction": "EU", "allowedRegions": ["eu-west-1", "eu-central-1"], "dataResidency": true, "crossBorderTransfer": false, "regulatoryFramework": ["GDPR"], "enforcementMode": "strict"}, {"jurisdiction": "US", "allowedRegions": ["us-east-1", "us-west-2"], "dataResidency": true, "regulatoryFramework": ["CCPA", "HIPAA"], "enforcementMode": "strict"}]
}
```

### `$defs.trigger.properties.cron`
```json
{
  type: "string"
  description: "Cron expression for schedule trigger"
}
```

### `$defs.trigger.properties.datasets`
```json
{
  type: "array"
  description: "NEW in v0.7.0: Can reference data products directly via exposeRef for strong typing and auto-URI gen..."
  items: {
    oneOf: [{"type": "string", "description": "Raw dataset URI (legacy, e.g., 'dataset://gcp/project/dataset/table')"}, {"type": "object", "description": "NEW in v0.7.0: Data product reference with strong typing", "required": ["productId", "exposeId"], "properties": {"productId": {"$ref": "#/$defs/identifier", "description": "Data product ID to depend on"}, "exposeId": {"$ref": "#/$defs/identifier", "description": "Expose ID within the data product"}, "versionConstraint": {"$ref": "#/$defs/semverRange", "description": "Optional version constraint (e.g., '^2.0.0')"}}}]
  }
}
```

### `$defs.trigger.properties.datasetsOperator`
```json
{
  type: "string"
  enum: ["any", "all"]
  default: "all"
}
```

### `$defs.trigger.properties.timetable`
```json
{
  type: "object"
  description: "Custom timetable configuration"
}
```

### `$defs.trigger.properties.timezone`
```json
{
  type: "string"
  default: "UTC"
}
```

### `properties.accessPolicy`
```json
{
  $ref: "#/$defs/accessPolicy"
  description: "Root-level access policy for automated IAM binding generation. Defines principals, permissions, and ..."
}
```

### `properties.sovereignty`
```json
{
  $ref: "#/$defs/sovereignty"
  description: "NEW in v0.7.1: Jurisdiction and data residency requirements for compliance enforcement."
}
```

## 📝 Modified Properties

### `$defs.trigger.properties.type.enum`

**Before:**
```json
[...4 items...]
```

**After:**
```json
[...7 items...]
```

### `$id`

**Before:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.5.7.json"
```

**After:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.1.json"
```

### `description`

**Before:**
```json
"FLUID Data Product contract (v0.5.7). Enhanced build section with:
• Multiple build objects for mult..."
```

**After:**
```json
"FLUID Data Product contract (v0.7.1). Provider-First Orchestration + Agentic Governance Release:

🔥 ..."
```

### `properties.fluidVersion.const`

**Before:**
```json
"0.5.7"
```

**After:**
```json
"0.7.1"
```

### `properties.fluidVersion.description`

**Before:**
```json
"Contract schema version. Must be exactly '0.5.7' for this schema."
```

**After:**
```json
"Contract schema version. Must be exactly '0.7.1' for agentic governance + provider-first orchestrati..."
```

### `properties.fluidVersion.examples`

**Before:**
```json
["0.5.7"]
```

**After:**
```json
["0.7.1"]
```

### `title`

**Before:**
```json
"FLUID 0.5.7 \u2014 Data Product Contract"
```

**After:**
```json
"FLUID 0.7.1 \u2014 Provider-First Orchestration + Agentic Governance"
```
