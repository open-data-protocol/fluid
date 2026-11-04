# Schema Changes: 0.7.6 → 0.7.7

**Total changes:** 22
- ✅ Added: 16
- ❌ Removed: 1
- 📝 Modified: 5

---

## ✅ Added Properties

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

### `$defs.column.properties.key`
```json
{
  $ref: "#/$defs/nestedType"
}
```

### `$defs.column.properties.value`
```json
{
  $ref: "#/$defs/nestedType"
}
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
    required: ["stream", "parameters"]
    properties: {
      parameters: {
        required: ["flink"]
        properties: {
          flink: {
            required: ["management"]
          }
        }
      }
    }
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
  }
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
    ... (1 more)
  }
}
```

## ❌ Removed Properties

### `$defs.embeddedLogicPattern.required`
```json
["sql"]
```

## 📝 Modified Properties

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
"Opt-in preview. Adds recursive struct fields, array elements and map key/value types. Stable 0.7.6 i..."
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
