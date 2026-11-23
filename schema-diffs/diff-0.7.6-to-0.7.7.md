# Schema Changes: 0.7.6 → 0.7.7

**Total changes:** 85
- ✅ Added: 64
- ❌ Removed: 6
- 📝 Modified: 15

---

## ✅ Added Properties

### `$defs.acquisitionDeployment.properties.auth.properties.secretRef.$ref`
```json
"#/$defs/secretRef"
```

### `$defs.acquisitionDeployment.properties.auth.properties.token`
```json
{
  type: "string"
  writeOnly: true
  description: "Write-only: a contract may not hold this value. Name the secret with secretRef instead."
}
```

### `$defs.acquisitionPattern.properties.kafka-connect.properties.schema_registry.properties.auth.properties.secretRef.$ref`
```json
"#/$defs/secretRef"
```

### `$defs.acquisitionSource.properties.connection.properties.password`
```json
{
  type: "string"
  writeOnly: true
  description: "Write-only: a contract may not hold this value. Name the secret with secretRef instead."
}
```

### `$defs.acquisitionSource.properties.connection.properties.secretRef.$ref`
```json
"#/$defs/secretRef"
```

### `$defs.airflowOrchestration.properties.dagId.description`
```json
"The Airflow DAG id, exactly as Airflow spells it. The ASCII part of Airflow's rule: letters (either ..."
```

### `$defs.airflowOrchestration.properties.dagId.maxLength`
```json
250
```

### `$defs.airflowOrchestration.properties.dagId.minLength`
```json
1
```

### `$defs.airflowOrchestration.properties.poolPerOutputTable`
```json
{
  type: "boolean"
  default: false
  description: "NEW in v0.7.7: When true, the generated DAG puts each task that writes an output table in a one-slot..."
}
```

### `$defs.airflowTask.properties.taskId.description`
```json
"The Airflow task id, exactly as Airflow spells it. The ASCII part of Airflow's rule: letters (either..."
```

### `$defs.airflowTask.properties.taskId.maxLength`
```json
250
```

### `$defs.airflowTask.properties.taskId.minLength`
```json
1
```

### `$defs.alertRoute`
```json
{
  type: "object"
  additionalProperties: false
  required: ["name", "kind"]
  description: "NEW in v0.7.7: One alert route. A route carries no secret: connection names the scheduler connection..."
  properties: {
    name: {
      type: "string"
      pattern: "^[A-Za-z_][A-Za-z0-9_-]{0,63}$"
    }
    kind: {
      type: "string"
      pattern: "^[a-z][a-z0-9_-]{0,63}$"
      description: "email (SmtpNotifier), slack (SlackWebhookNotifier), webhook (HttpNotifier, see format), pagerduty (P..."
    }
    events: {
      type: "array"
      minItems: 1
      uniqueItems: true
      items: {
        enum: [...4 items...]
      }
      default: ["failure"]
      ... (1 more)
    }
    connection: {
      type: "string"
      pattern: "^[A-Za-z0-9_][A-Za-z0-9_.-]{0,249}$"
      description: "The Airflow connection id that holds the address, URL or key: the scheduler's secrets backend serves..."
    }
    to: {
      type: "array"
      minItems: 1
      maxItems: 50
      items: {
        type: "string"
        pattern: "^[A-Za-z0-9._+-]{1,64}@[A-Za-z0-9-]{1,63}(\\.[A-Za-z0-9-]{1,63})+$"
      }
      description: "email only: the addresses to send to."
    }
    ... (4 more)
  }
}
```

### `$defs.alerts`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7: The alert routes of the product's DAGs. The Airflow DAG renderers put each route's no..."
  properties: {
    sla: {
      type: "string"
      pattern: "^P(?=\\d|T\\d)(\\d{1,7}W)?(\\d{1,7}D)?(T(?=\\d)(\\d{1,7}H)?(\\d{1,7}M)?(\\d{1,7}S)?)?$"
      description: "How long a run may take before its sla_miss routes alert, as an ISO-8601 duration in weeks, days, ho..."
    }
    defaults: {
      type: "boolean"
      default: true
      description: "Whether the product takes the default routes of the organisation's installed packs (the fluid_build...."
    }
    routes: {
      type: "array"
      maxItems: 20
      items: {
        $ref: "#/$defs/alertRoute"
      }
    }
  }
}
```

### `$defs.binding.properties.properties.properties`
```json
{
  registry: {
    $ref: "#/$defs/schemaRegistry"
    description: "NEW in v0.7.7 (preview): The registry a produced topic's subject is registered in, on a Kafka bindin..."
  }
}
```

### `$defs.column.properties.element`
```json
{
  $ref: "#/$defs/nestedType"
}
```

### `$defs.column.properties.fields`
```json
{
  type: "array"
  minItems: 1
  items: {
    $ref: "#/$defs/column"
  }
  description: "Typed child columns of a struct/row/record."
}
```

### `$defs.column.properties.identifierFormat`
```json
{
  type: "array"
  minItems: 1
  description: "NEW in v0.7.7 (preview): The identifier formats of this string column (RFC-data-rules.md section 3),..."
  items: {
    type: "object"
    additionalProperties: false
    required: ["mask"]
    properties: {
      prefixes: {
        type: "array"
        minItems: 1
        uniqueItems: true
        items: {
          type: "string"
          pattern: "^[ -~]*$"
        }
        description: "Literal prefixes, printable ASCII. One empty prefix when left out."
      }
      mask: {
        type: "string"
        minLength: 1
        maxLength: 64
        description: "COBOL PICTURE style: 9 is a digit, A an upper-case ASCII letter, X an upper-case ASCII letter or a d..."
      }
    }
  }
  examples: [[{"prefixes": ["MSC", "TWR"], "mask": "99999"}, {"prefixes": ["LEGACY-"], "mask": "A9-99AA"}]]
}
```

### `$defs.column.properties.key`
```json
{
  $ref: "#/$defs/nestedType"
}
```

### `$defs.column.properties.placeholders`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): Placeholder values of this string column: stand-ins for a real value that i..."
  properties: {
    values: {
      type: "array"
      minItems: 1
      uniqueItems: true
      items: {
        type: "string"
        minLength: 1
      }
      description: "Whole values that are placeholders."
    }
    prefixes: {
      type: "array"
      minItems: 1
      uniqueItems: true
      items: {
        type: "string"
        minLength: 1
      }
      description: "A value that starts with one of these is a placeholder."
    }
    mustBe: {
      $ref: "#/$defs/violationBound"
      description: "Exactly this many placeholder rows."
    }
    mustBeLessThan: {
      $ref: "#/$defs/violationBound"
      description: "Fewer placeholder rows than this."
    }
    mustBeLessOrEqualTo: {
      $ref: "#/$defs/violationBound"
      description: "At most this many placeholder rows."
    }
    ... (4 more)
  }
  examples: [{"values": ["XXXXX"], "prefixes": ["TBD_"], "mustBeLessOrEqualTo": 1, "unit": "percent"}]
}
```

### `$defs.column.properties.protobuf`
```json
{
  type: "object"
  additionalProperties: false
  required: ["field"]
  properties: {
    field: {
      type: "integer"
      minimum: 1
      maximum: 536870911
      not: {
        minimum: 19000
        maximum: 19999
      }
      description: "The column's field number in the .proto forge generates when the topic's value is Protobuf (binding...."
    }
  }
  description: "NEW in v0.7.7 (preview): How this column is written when the topic's value is Protobuf (binding.seri..."
}
```

### `$defs.column.properties.sharedAttribute`
```json
{
  type: "string"
  pattern: "^[A-Za-z][A-Za-z0-9_.]*$"
  description: "NEW in v0.7.7 (preview): The attribute this column carries with every other column of the contract t..."
}
```

### `$defs.column.properties.value`
```json
{
  $ref: "#/$defs/nestedType"
}
```

### `$defs.embeddedLogicPattern.allOf`
```json
[{"if": {"required": ["package"]}, "then": {"required": ["parameters"], "properties": {"language": {"const": "pyspark"}, "parameters": {"required": ["spark"], "properties": {"spark": {"properties": {"mode": {"const": "batch"}}}}}}, "not": {"anyOf": [{"required": ["sql"]}, {"required": ["mapping"]}, {"required": ["stream"]}]}, "description": "a package runs PySpark in a batch Spark build (parameters.spark), in place of sql, mapping and stream"}}]
```

### `$defs.embeddedLogicPattern.dependentRequired`
```json
{
  mapping: ["stream"]
}
```

### `$defs.embeddedLogicPattern.if`
```json
{
  not: {
    anyOf: [{"required": ["stream", "parameters"], "properties": {"parameters": {"required": ["flink"], "properties": {"flink": {"required": ["management"]}}}}}, {"required": ["stream", "mapping", "parameters"], "properties": {"parameters": {"required": ["spark"]}}}, {"required": ["package", "parameters"], "properties": {"parameters": {"required": ["spark"]}}}]
  }
}
```

### `$defs.embeddedLogicPattern.properties.mapping`
```json
{
  $ref: "#/$defs/recordMapping"
  description: "NEW in v0.7.7 (preview): How the stream's records become the output's rows. Requires stream, and rep..."
}
```

### `$defs.embeddedLogicPattern.properties.package`
```json
{
  $ref: "#/$defs/sparkPackage"
  description: "NEW in v0.7.7 (preview): A prebuilt PySpark package a batch Spark build runs by its sha256 digest, i..."
}
```

### `$defs.embeddedLogicPattern.properties.parameters.properties`
```json
{
  spark: {
    $ref: "#/$defs/sparkParameters"
    description: "NEW in v0.7.7 (preview): Where and how a Spark build runs."
  }
}
```

### `$defs.embeddedLogicPattern.properties.stream`
```json
{
  $ref: "#/$defs/streamSource"
  description: "NEW in v0.7.7 (preview): The stream the build reads. On a managed Flink build (parameters.flink.mana..."
}
```

### `$defs.embeddedLogicPattern.then`
```json
{
  required: ["sql"]
}
```

### `$defs.expose.properties.iceberg.properties.maintenance`
```json
{
  $ref: "#/$defs/icebergMaintenance"
  description: "NEW in v0.7.7: The table's maintenance: compaction, manifests, snapshot expiry, orphan files and a p..."
}
```

### `$defs.exposeContract.properties.invariants`
```json
{
  type: "array"
  description: "NEW in v0.7.7 (preview): Rules about valid data (RFC-data-rules.md): checks, derived columns, summar..."
  items: {
    $ref: "#/$defs/invariant"
  }
}
```

### `$defs.fluidSqlText`
```json
{
  type: "string"
  minLength: 1
  description: "NEW in v0.7.7 (preview): A FLUID SQL/1 text (RFC-data-rules.md section 2): a closed SQL expression s..."
}
```

### `$defs.icebergMaintenance`
```json
{
  type: "object"
  additionalProperties: false
  not: {
    required: ["build", "runtime"]
  }
  description: "NEW in v0.7.7: What keeps the Iceberg table healthy, run on a schedule. backend spark (the default) ..."
  properties: {
    backend: {
      type: "string"
      enum: ["spark", "glue"]
      default: "spark"
      description: "spark: forge's Spark runner, on the writer build's runtime. glue: the Glue Data Catalog's table opti..."
    }
    schedule: {
      type: "string"
      minLength: 1
      description: "backend spark, required: the cron (or Airflow preset) the table's maintenance DAG runs on."
    }
    timezone: {
      type: "string"
      minLength: 1
      default: "UTC"
      description: "backend spark: the IANA zone the schedule is read in."
    }
    build: {
      type: "string"
      minLength: 1
      description: "backend spark: the id of the engine: spark build whose output this expose is, when more than one is;..."
    }
    runtime: {
      $ref: "#/$defs/sparkRuntime"
    }
    ... (7 more)
  }
}
```

### `$defs.icebergMaintenanceAction`
```json
{
  type: "object"
  additionalProperties: false
  required: ["name", "kind"]
  description: "NEW in v0.7.7: One maintenance action of a package's kind, such as a GDPR erasure. When fluid plan c..."
  properties: {
    name: {
      type: "string"
      pattern: "^[A-Za-z_][A-Za-z0-9_-]{0,63}$"
      description: "The action's name, unique on the table; its commits are stamped with it."
    }
    kind: {
      type: "string"
      pattern: "^[a-z][a-z0-9_-]{0,63}$"
      description: "The kind's name under the fluid_build.maintenance_actions entry points."
    }
    options: {
      type: "object"
      description: "JSON values the kind reads. No secret: a kind reads its own."
    }
  }
}
```

### `$defs.icebergMaintenanceCompaction`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7: Rewrite small files into larger ones (Iceberg's rewrite_data_files with partial progr..."
  properties: {
    enabled: {
      type: "boolean"
      default: true
      description: "false declares the block and runs nothing."
    }
    strategy: {
      type: "string"
      enum: ["binpack", "sort", "z-order"]
      default: "binpack"
      description: "sort orders by the table's sort order; z-order is backend glue's."
    }
    targetFileSizeMb: {
      type: "integer"
      minimum: 1
      maximum: 1048576
      description: "backend spark: the size files are rewritten to; default iceberg.compaction.targetFileSizeMb, else th..."
    }
    minInputFiles: {
      type: "integer"
      minimum: 1
      maximum: 1000000
      description: "The fewest files a group must hold to be rewritten."
    }
    deleteFileThreshold: {
      type: "integer"
      minimum: 1
      maximum: 1000000
      description: "The delete files that make a data file worth rewriting."
    }
    ... (2 more)
  }
}
```

### `$defs.invariant`
```json
{
  type: "object"
  description: "NEW in v0.7.7 (preview): A rule about valid data (RFC-data-rules.md section 1). Exactly one form: ch..."
  additionalProperties: false
  required: ["id"]
  properties: {
    id: {
      type: "string"
      pattern: "^[A-Za-z][A-Za-z0-9_]*$"
      description: "Unique within the contract, across every expose and kind, and against dq.rules[].id and contract.qua..."
    }
    description: {
      type: "string"
    }
    check: {
      $ref: "#/$defs/fluidSqlText"
      description: "A FLUID SQL/1 predicate over the row."
    }
    derive: {
      type: "string"
      minLength: 1
      description: "The column this invariant determines, with exactly one of expr and aggregate. Several derives of one..."
    }
    expr: {
      $ref: "#/$defs/fluidSqlText"
      description: "With derive: the column's value, a FLUID SQL/1 expression of the column's type whose static scale fi..."
    }
    ... (11 more)
  }
  ... (2 more)
}
```

### `$defs.invariantAggregate`
```json
{
  type: "object"
  description: "NEW in v0.7.7 (preview): A summary over child rows (RFC-data-rules.md section 1.2): SQL's aggregate,..."
  additionalProperties: false
  required: ["function", "from", "via"]
  properties: {
    function: {
      type: "string"
      enum: [...4 items...]
    }
    column: {
      type: "string"
      minLength: 1
      description: "The child column summarized: none for count, a number of bounded scale for sum, any orderable type f..."
    }
    from: {
      $ref: "#/$defs/identifier"
      description: "The child expose, an exposeId of this contract."
    }
    via: {
      type: "string"
      minLength: 1
      description: "A relationship the child declares (its semantics.relationships[].name) whose to is this expose."
    }
    filter: {
      $ref: "#/$defs/fluidSqlText"
      description: "A FLUID SQL/1 predicate over the child row: only children for which it is TRUE count, as in SUM(x) F..."
    }
    ... (1 more)
  }
}
```

### `$defs.invariantDependency`
```json
{
  type: "object"
  description: "NEW in v0.7.7 (preview): A functional dependency (RFC-data-rules.md section 1.2): equal values in fr..."
  additionalProperties: false
  required: ["from", "to"]
  properties: {
    from: {
      type: "array"
      minItems: 1
      uniqueItems: true
      items: {
        type: "string"
        minLength: 1
      }
    }
    to: {
      type: "array"
      minItems: 1
      uniqueItems: true
      items: {
        type: "string"
        minLength: 1
      }
    }
    bothWays: {
      type: "boolean"
      default: false
    }
  }
}
```

### `$defs.nestedType`
```json
{
  type: "object"
  additionalProperties: false
  required: ["type"]
  properties: {
    type: {
      $ref: "#/$defs/column/properties/type"
    }
    required: {
      type: "boolean"
    }
    fields: {
      type: "array"
      minItems: 1
      items: {
        $ref: "#/$defs/column"
      }
    }
    element: {
      $ref: "#/$defs/nestedType"
    }
    key: {
      $ref: "#/$defs/nestedType"
    }
    ... (1 more)
  }
}
```

### `$defs.packaging.properties.containers.properties.athenaWorkgroup`
```json
{
  $ref: "#/$defs/packagingContainerMode"
  description: "NEW in v0.7.7 (preview): Ownership of the Athena workgroup (aws_athena_workgroup) the product's quer..."
}
```

### `$defs.packaging.properties.containers.properties.emrApplication`
```json
{
  $ref: "#/$defs/packagingContainerMode"
  description: "NEW in v0.7.7 (preview): Ownership of the EMR Serverless application (aws_emrserverless_application)..."
}
```

### `$defs.packaging.properties.containers.properties.kmsKey`
```json
{
  $ref: "#/$defs/packagingContainerMode"
  description: "NEW in v0.7.7 (preview): Ownership of the KMS key (aws_kms_key) that encrypts the product's data, ch..."
}
```

### `$defs.packaging.properties.containers.properties.lfTagVocabulary`
```json
{
  $ref: "#/$defs/packagingContainerMode"
  description: "NEW in v0.7.7 (preview): Ownership of the Lake Formation tag vocabulary (aws_lakeformation_lf_tag). ..."
}
```

### `$defs.packaging.properties.containers.properties.mwaaEnvironment`
```json
{
  const: "shared"
  description: "NEW in v0.7.7 (preview): The MWAA environment (aws_mwaa_environment) is the platform team's, so shar..."
}
```

### `$defs.packaging.properties.containers.properties.schemaRegistry`
```json
{
  $ref: "#/$defs/packagingContainerMode"
  description: "NEW in v0.7.7 (preview): Ownership of the Glue schema registry (aws_glue_registry) that holds produc..."
}
```

### `$defs.recordExplode`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): One output row per element of an array. A record whose array is null or emp..."
  required: ["path", "as"]
  properties: {
    path: {
      type: "string"
      pattern: "^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*|\['[^'\\\u0000-\u001f\u007f]{1,256}'\])*(?![\s\S]..."
      description: "The array: a stream column or a nested field, such as items or order.lines."
    }
    as: {
      type: "string"
      pattern: "^[A-Za-z_][A-Za-z0-9_]*(?![\\s\\S])"
      description: "The element's name in mapping paths: item.sku for a field of a struct element, item for a scalar ele..."
    }
  }
}
```

### `$defs.recordMapping`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): How the stream's records become the output's rows. An output column the map..."
  properties: {
    explode: {
      $ref: "#/$defs/recordExplode"
    }
    columns: {
      type: "array"
      minItems: 1
      items: {
        $ref: "#/$defs/recordMappingColumn"
      }
      description: "Output columns, or nested fields of them, that are read from another path, renamed or converted."
    }
  }
}
```

### `$defs.recordMappingColumn`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): Where one output column, or one nested field of one, is read from."
  required: ["name", "from"]
  properties: {
    name: {
      type: "string"
      pattern: "^[A-Za-z_][A-Za-z0-9_]*(?:\\.[A-Za-z_][A-Za-z0-9_]*)*(?![\\s\\S])"
      description: "The output column, or a field of a struct output column as a dotted path (customer.id). Mapping a ne..."
    }
    from: {
      type: "string"
      pattern: "^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*|\['[^'\\\u0000-\u001f\u007f]{1,256}'\])*(?![\s\S]..."
      description: "The source: a stream column (value, key or metadata), a nested field (customer.address.country), a m..."
    }
    cast: {
      $ref: "#/$defs/column/properties/type"
      description: "Convert the source to this type: binary to string (UTF-8), or a widening (int to long, float to doub..."
    }
    description: {
      type: "string"
    }
    maskAtIngest: {
      enum: ["hash"]
      description: "NEW in v0.7.7 (preview): Mask the value before it lands. hash = HMAC-SHA256 keyed by parameters.spar..."
    }
  }
}
```

### `$defs.schemaRegistry`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): The schema registry that holds a topic's record schema, one definition for ..."
  required: ["kind"]
  properties: {
    kind: {
      enum: ["glue", "confluent"]
      description: "glue: AWS Glue Schema Registry. confluent: Confluent Schema Registry REST API."
    }
    url: {
      type: "string"
      format: "uri"
      pattern: "^https?://[^/?#@\\s]+(?:/[^?#\\s]*)?(?![\\s\\S])"
      description: "kind confluent only, and required there: the registry's REST endpoint, http or https, with no creden..."
    }
    registryName: {
      type: "string"
      pattern: "^[A-Za-z0-9_$#.-]{1,255}(?![\\s\\S])"
      description: "kind glue only: the Glue registry's name. Absent: default-registry, the registry Glue uses when none..."
    }
    subject: {
      type: "string"
      pattern: "^[^\\u0000-\\u001f\\u007f]{1,255}(?![\\s\\S])"
      description: "The subject (confluent) or schema name (glue) that holds the record value's schema. Absent: <topic>-..."
    }
    version: {
      oneOf: [{"const": "latest"}, {"type": "integer", "minimum": 1}]
      default: "latest"
      description: "The schema version to verify against or read with: latest, or a version number from 1."
    }
    ... (3 more)
  }
  ... (1 more)
}
```

### `$defs.secretRef`
```json
{
  type: "string"
  description: "NEW in v0.7.7: A reference to a secret held in a store, never the secret itself: a contract names a ..."
  anyOf: [...7 items...]
}
```

### `$defs.semanticModel.properties.dimensions.items.properties.typeParams.properties.validityParams`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): Marks this time dimension as one bound of the validity window of a type II ..."
  properties: {
    isStart: {
      type: "boolean"
      description: "This dimension holds the time each version starts to apply."
    }
    isEnd: {
      type: "boolean"
      description: "This dimension holds the time each version stops applying."
    }
  }
}
```

### `$defs.semanticModel.properties.relationships`
```json
{
  type: "array"
  description: "NEW in v0.7.7 (preview): Named joins from this expose to an expose of the same contract, declared on..."
  items: {
    $ref: "#/$defs/semanticRelationship"
  }
}
```

### `$defs.semanticRelationship`
```json
{
  type: "object"
  description: "NEW in v0.7.7 (preview): One foreign key, from the expose that declares it (the many side) to an exp..."
  additionalProperties: false
  required: [...5 items...]
  properties: {
    name: {
      type: "string"
      description: "Relationship name, unique within the expose (e.g., 'orders_to_customers')."
    }
    to: {
      $ref: "#/$defs/identifier"
      description: "exposeId of the target expose, in the same contract. It may be the declaring expose itself, for a se..."
    }
    fromColumns: {
      type: "array"
      minItems: 1
      items: {
        type: "string"
      }
      description: "Foreign-key columns of the declaring expose, in key order."
    }
    toColumns: {
      type: "array"
      minItems: 1
      items: {
        type: "string"
      }
      description: "Key columns of the target expose, in the order of fromColumns."
    }
    cardinality: {
      type: "string"
      enum: ["many_to_one", "one_to_one"]
      description: "many_to_one: many rows of the declaring expose can match one target row (an ordinary foreign key). o..."
    }
    ... (2 more)
  }
  ... (1 more)
}
```

### `$defs.sparkPackage`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): A prebuilt PySpark package a Spark build runs in place of sql or a mapping,..."
  required: ["uri", "sha256", "entryPoint"]
  properties: {
    uri: {
      type: "string"
      pattern: "^(?:s3://[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]/|file:///)(?:(?!\.{1,2}/)[A-Za-z0-9._=+-]+/)*[A-Za-z0-9._=..."
      maxLength: 1024
      description: "The package as its team published it, a .whl or a .zip: s3://<bucket>/<key> for the AWS runtimes, fi..."
    }
    sha256: {
      type: "string"
      pattern: "^[0-9a-f]{64}(?![\\s\\S])"
      description: "The package's sha256, as sha256sum prints it: 64 lowercase hex characters. The run refuses any other..."
    }
    entryPoint: {
      type: "string"
      pattern: "^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*:[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_..."
      maxLength: 512
      description: "The function the runner calls, as an entry-point object reference, <module>:<attribute>[.<attribute>..."
    }
    arguments: {
      type: "object"
      maxProperties: 64
      propertyNames: {
        pattern: "^[A-Za-z_][A-Za-z0-9_.-]{0,127}(?![\\s\\S])"
      }
      additionalProperties: {
        type: "string"
        maxLength: 4096
      }
      description: "Strings the function reads as context.arguments, name to value (source: commerce.orders_raw)."
    }
    deadLetter: {
      $ref: "#/$defs/sparkPackageDeadLetter"
    }
  }
}
```

### `$defs.sparkPackageDeadLetter`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): What forge's Spark runner does with a row of a package's output that fails ..."
  properties: {
    enabled: {
      type: "boolean"
      default: true
      description: "false: no dead letters; a row that fails the checks fails the run (an overlay can switch it off per ..."
    }
    table: {
      type: "string"
      pattern: "^[A-Za-z_][A-Za-z0-9_]{0,254}(?![\\s\\S])"
      description: "The table's name in the output's database. Absent: <output table>__dead_letter."
    }
    maxRecordsBeforeAbort: {
      type: "integer"
      minimum: 0
      default: 10000
      description: "The run fails, after its dead letters have landed and before the output is written, once more rows t..."
    }
  }
}
```

### `$defs.sparkParameters`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): Where and how a Spark build runs, at builds[].properties.parameters.spark o..."
  required: ["runtime"]
  properties: {
    runtime: {
      enum: [...5 items...]
      description: "Where the job runs: EMR Serverless, EMR on EC2, EMR on EKS, an AWS Glue Spark job, or local, a spark..."
    }
    mode: {
      enum: ["streaming", "batch"]
      description: "streaming: a long-running Structured Streaming job. batch: a job that runs to completion. Absent: st..."
    }
    applicationId: {
      type: "string"
      pattern: "^[0-9a-z]{1,64}(?![\\s\\S])"
      description: "emr-serverless only (runtime local ignores it): an existing EMR Serverless application. Absent: the ..."
    }
    clusterId: {
      type: "string"
      pattern: "^j-[0-9A-Za-z]{1,254}(?![\\s\\S])"
      description: "emr-ec2 only (runtime local ignores it): a running EMR cluster (j-...). Absent: a transient cluster ..."
    }
    virtualClusterId: {
      type: "string"
      pattern: "^[0-9a-z]{1,64}(?![\\s\\S])"
      description: "emr-eks only, and required there (runtime local ignores it): the EMR on EKS virtual cluster."
    }
    ... (6 more)
  }
  ... (1 more)
}
```

### `$defs.sparkRuntime`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): The runtime that maintains an Iceberg table no forge build writes (exposes[..."
  required: ["runtime"]
  properties: {
    runtime: {
      enum: [...4 items...]
      description: "The runtime the maintenance runs on: an existing EMR Serverless application (applicationId), a runni..."
    }
    applicationId: {
      $ref: "#/$defs/sparkParameters/properties/applicationId"
      description: "With runtime emr-serverless, required: the EMR Serverless application the team's own runner uses. fo..."
    }
    clusterId: {
      $ref: "#/$defs/sparkParameters/properties/clusterId"
      description: "With runtime emr-ec2, required: the running EMR cluster (j-...) the maintenance steps go to. forge s..."
    }
    virtualClusterId: {
      $ref: "#/$defs/sparkParameters/properties/virtualClusterId"
      description: "With runtime emr-eks, required: the EMR on EKS virtual cluster."
    }
    releaseLabel: {
      $ref: "#/$defs/sparkParameters/properties/releaseLabel"
    }
    ... (2 more)
  }
  ... (1 more)
}
```

### `$defs.streamKey`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): The record key, read as columns next to the value's. A record without a key..."
  required: ["format", "schema"]
  properties: {
    format: {
      enum: ["raw", "json", "avro-confluent"]
      description: "raw: the key's bytes as one column, of type string (UTF-8) or binary. json and avro-confluent: a key..."
    }
    schema: {
      type: "array"
      minItems: 1
      items: {
        $ref: "#/$defs/column"
      }
      description: "The key's fields, as columns: exactly one for raw."
    }
    prefix: {
      type: "string"
      pattern: "^[A-Za-z_][A-Za-z0-9_]*(?![\\s\\S])"
      description: "Put in front of every key column's name, so a key field can share its name with a value field (a Deb..."
    }
  }
}
```

### `$defs.streamMetadataColumn`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): One piece of Kafka record metadata, read as a column. Its type is fixed by ..."
  required: ["name", "from"]
  properties: {
    name: {
      type: "string"
      minLength: 1
      description: "The column's name, unique among the stream's value, key and metadata columns."
    }
    from: {
      enum: [...7 items...]
      description: "The metadata the column reads."
    }
    description: {
      type: "string"
    }
  }
}
```

### `$defs.streamSource`
```json
{
  type: "object"
  additionalProperties: false
  description: "NEW in v0.7.7 (preview): The Kafka records a streaming build reads, described apart from the engine ..."
  required: [...4 items...]
  properties: {
    kind: {
      const: "kafka"
      description: "The streaming system. Only kafka in this preview."
    }
    topic: {
      type: "string"
      pattern: "^(?!\\.\\.?(?![\\s\\S]))[A-Za-z0-9._-]{1,249}(?![\\s\\S])"
      description: "One Kafka topic, by name: Kafka's legal characters (not . or ..), no pattern and no list."
    }
    format: {
      enum: ["json", "avro-confluent"]
      description: "How record values are encoded. json: one JSON object per record; a field the schema does not declare..."
    }
    schema: {
      type: "array"
      minItems: 1
      items: {
        $ref: "#/$defs/column"
      }
      description: "The record value's fields, as columns. Nested data uses fields (struct), element (array) and key/val..."
    }
    key: {
      $ref: "#/$defs/streamKey"
    }
    ... (8 more)
  }
}
```

### `$defs.violationBound`
```json
{
  type: "number"
  minimum: 0
  description: "NEW in v0.7.7 (preview): A number of rows, or a percentage (unit), read as an exact decimal from its..."
}
```

### `properties.alerts`
```json
{
  $ref: "#/$defs/alerts"
  description: "NEW in v0.7.7: Who hears about the failures, retries, successes and missed SLAs of the DAGs forge ge..."
}
```

## ❌ Removed Properties

### `$defs.acquisitionDeployment.properties.auth.properties.secretRef.type`
```json
"string"
```

### `$defs.acquisitionPattern.properties.kafka-connect.properties.schema_registry.properties.auth.properties.secretRef.type`
```json
"string"
```

### `$defs.acquisitionSource.properties.connection.properties.secretRef.pattern`
```json
"^[a-z][a-z0-9_+.-]*://.+"
```

### `$defs.acquisitionSource.properties.connection.properties.secretRef.type`
```json
"string"
```

### `$defs.airflowOrchestration.required`
```json
["dagId"]
```

### `$defs.embeddedLogicPattern.required`
```json
["sql"]
```

## 📝 Modified Properties

### `$defs.acquisitionSource.properties.connection.properties.secretRef.description`

**Before:**
```json
"Reference to a secret in the configured backend (vault://, aws://, gcp://, azure://, env://)."
```

**After:**
```json
"Reference to the connection's secret in the configured store, e.g. vault://kv/orgs/acme/pg#password ..."
```

### `$defs.acquisitionSource.properties.connection.properties.user.description`

**Before:**
```json
"NEW in v0.7.3: Username/principal for SQL- or REST-style sources. Required by most database drivers ..."
```

**After:**
```json
"NEW in v0.7.3: Username/principal for SQL- or REST-style sources. Required by most database drivers ..."
```

### `$defs.airflowOrchestration.properties.dagId.pattern`

**Before:**
```json
"^[a-z0-9_][a-z0-9_.-]*[a-z0-9_]$|^[a-z0-9_]$"
```

**After:**
```json
"^[A-Za-z0-9_.-]+(?![\\s\\S])"
```

### `$defs.airflowTask.properties.taskId.pattern`

**Before:**
```json
"^[a-z0-9_][a-z0-9_.-]*[a-z0-9_]$|^[a-z0-9_]$"
```

**After:**
```json
"^[A-Za-z0-9_.-]+(?![\\s\\S])"
```

### `$defs.build.properties.engine.anyOf`

**Before:**
```json
[{"enum": ["dbt", "sql", "python", "spark", "glue", "custom", "duckdb", "airbyte", "meltano", "dlt", "kafka-connect", "debezium", "flink"]}, {"pattern": "^dbt-[a-z0-9]+([_-][a-z0-9]+)*$"}]
```

**After:**
```json
[{"enum": ["dbt", "sql", "python", "spark", "glue", "custom", "duckdb", "airbyte", "meltano", "dlt", "kafka-connect", "debezium", "flink", "lakeflow"]}, {"pattern": "^dbt-[a-z0-9]+([_-][a-z0-9]+)*$"}]
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

### `$defs.column.properties.type.anyOf`

**Before:**
```json
[{"type": "string", "enum": ["string", "text", "varchar", "varchar2", "nvarchar", "char", "nchar", "character", "clob", "int", "integer", "int2", "int4", "int8", "int16", "int32", "int64", "tinyint", "smallint", "mediumint", "bigint", "long", "longint", "serial", "bigserial", "float", "float4", "float8", "float32", "float64", "double", "real", "decimal", "dec", "numeric", "number", "bignumeric", "money", "boolean", "bool", "bit", "date", "time", "datetime", "datetime2", "smalldatetime", "timestamp", "timestamptz", "timestamp_tz", "timestamp_ntz", "timestamp_ltz", "timestampntz", "interval", "year", "variant", "object", "array", "struct", "map", "record", "row", "json", "jsonb", "super", "binary", "varbinary", "bytes", "blob", "bytea", "raw", "geography", "geometry", "geom", "point", "uuid", "uniqueidentifier", "guid", "enum", "hll"]}, {"type": "string", "pattern": "(?i)^\\s*(string|text|varchar|varchar2|nvarchar|char|nchar|character|clob|int|integer|int2|int4|int8|int16|int32|int64|tinyint|smallint|mediumint|bigint|long|longint|serial|bigserial|float|float4|float8|float32|float64|double|real|double\\s+precision|decimal|dec|numeric|number|bignumeric|money|boolean|bool|bit|date|time|datetime|datetime2|smalldatetime|timestamp|timestamptz|timestamp_tz|timestamp_ntz|timestamp_ltz|timestampntz|timestamp\\s+with(out)?\\s+time\\s+zone|interval|year|variant|object|array|struct|map|record|row|json|jsonb|super|binary|varbinary|bytes|blob|bytea|raw|geography|geometry|geom|point|uuid|uniqueidentifier|guid|enum|hll)\\s*(\\(\\s*[0-9A-Za-z_,\\s'\\\"-]*\\s*\\))?\\s*$"}]
```

**After:**
```json
[{"type": "string", "enum": ["string", "text", "varchar", "varchar2", "nvarchar", "char", "nchar", "character", "clob", "int", "integer", "int2", "int4", "int8", "int16", "int32", "int64", "tinyint", "smallint", "mediumint", "bigint", "long", "longint", "serial", "bigserial", "float", "float4", "float8", "float32", "float64", "double", "real", "decimal", "dec", "numeric", "number", "bignumeric", "money", "boolean", "bool", "bit", "date", "time", "datetime", "datetime2", "smalldatetime", "timestamp", "timestamptz", "timestamp_tz", "timestamp_ntz", "timestamp_ltz", "timestampntz", "interval", "year", "variant", "object", "array", "struct", "map", "record", "row", "json", "jsonb", "super", "binary", "varbinary", "bytes", "blob", "bytea", "raw", "geography", "geometry", "geom", "point", "uuid", "uniqueidentifier", "guid", "enum", "hll"]}, {"type": "string", "pattern": "(?i)^\\s*(?:enum\\s*\\(\\s*(?:(?:'(?:[^'\\x00-\\x1f\\x7f-\\x9f]|'')*'|\"(?:[^\"\\x00-\\x1f\\x7f-\\x9f]|\"\")*\"|[0-9A-Za-z_-]+(?:\\s+[0-9A-Za-z_-]+)*)\\s*(?:,\\s*(?:'(?:[^'\\x00-\\x1f\\x7f-\\x9f]|'')*'|\"(?:[^\"\\x00-\\x1f\\x7f-\\x9f]|\"\")*\"|[0-9A-Za-z_-]+(?:\\s+[0-9A-Za-z_-]+)*)\\s*)*)?\\)|(?!enum\\s*\\()(string|text|varchar|varchar2|nvarchar|char|nchar|character|clob|int|integer|int2|int4|int8|int16|int32|int64|tinyint|smallint|mediumint|bigint|long|longint|serial|bigserial|float|float4|float8|float32|float64|double|real|double\\s+precision|decimal|dec|numeric|number|bignumeric|money|boolean|bool|bit|date|time|datetime|datetime2|smalldatetime|timestamp|timestamptz|timestamp_tz|timestamp_ntz|timestamp_ltz|timestampntz|timestamp\\s+with(out)?\\s+time\\s+zone|interval|year|variant|object|array|struct|map|record|row|json|jsonb|super|binary|varbinary|bytes|blob|bytea|raw|geography|geometry|geom|point|uuid|uniqueidentifier|guid|enum|hll)(\\s*\\([0-9A-Za-z_,\\s'\\\"-]*\\))?)\\s*$"}]
```

### `$defs.column.properties.type.description`

**Before:**
```json
"Column data type. Accepts a canonical FLUID/SQL type name (case-insensitive) or a parameterized form..."
```

**After:**
```json
"Column data type. Accepts a canonical FLUID/SQL type name (case-insensitive) or a parameterized form..."
```

### `$defs.packaging.properties.containers.description`

**Before:**
```json
"NEW in v0.7.6: Per-container-kind ownership overrides — each key wins over `mode` for that kind, yie..."
```

**After:**
```json
"NEW in v0.7.6: Per-container-kind ownership overrides — each key wins over `mode` for that kind, yie..."
```

### `$defs.semanticModel.properties.entities.items.properties.type.description`

**Before:**
```json
"Entity key type: primary (unique, complete), foreign (references another table), unique (unique, pos..."
```

**After:**
```json
"Entity key type: primary (unique, complete), foreign (references another table), unique (unique, pos..."
```

### `$id`

**Before:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.6.json"
```

**After:**
```json
"https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.7.json"
```

### `description`

**Before:**
```json
"FLUID contract schema 0.7.6 — opened as the preview when 0.7.5 was promoted to stable, and stable it..."
```

**After:**
```json
"Opt-in preview. Adds recursive struct fields, array elements and map key/value types, the lakeflow b..."
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
[...4 items...]
```

**After:**
```json
[...5 items...]
```

### `title`

**Before:**
```json
"FLUID 0.7.6 \u2014 Declarative Packaging Modes"
```

**After:**
```json
"FLUID 0.7.7 \u2014 Preview: recursive streaming types"
```
