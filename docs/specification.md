## 📚 Fluid Protocol Specification (v1.0)

### **Root Object**

| Key             | Type           | Required | Description                                                        |
|-----------------|---------------|----------|--------------------------------------------------------------------|
| `fluidVersion`  | String        | Yes      | FLUID spec version (e.g., 1.0)                                     |
| `extends`       | String        | No       | Path/URL to base template FLUID file                               |
| `kind`          | String        | Yes      | DataProduct, VirtualDataProduct, EgressFlow                        |
| `metadata`      | Object        | Yes      | Identification, ownership, lineage                                 |
| `exposes`       | Object/List   | Yes      | Public output interface(s)                                         |
| `consumes`      | Object/List   | No       | Input data sources/upstream products                               |
| `build`         | Object        | No       | Implementation logic                                               |
| `accessPolicy`  | Object        | No       | Static access control policies                                     |
| `dynamicPolicies`| Object       | No       | Context-aware access policies                                      |
| `sla`           | Object        | No       | Service level agreements                                           |
| `extensions`    | Object        | No       | External plugins                                                   |
| `revision`      | String        | No       | Git commit hash/tag/version                                        |

---

### **4.2 `metadata` Block**

| Key         | Type         | Required | Description                                   |
|-------------|--------------|----------|-----------------------------------------------|
| dataProduct | String       | Yes      | Globally unique name (e.g., sales.silver.clean_orders) |
| owner       | Object       | Yes      | Team/individual responsible                   |
| description | String       | No       | Markdown-supported description                |
| tags        | Map[String]  | No       | Key-value pairs for categorization            |
| version     | String       | No       | Semantic version                              |

---

### **4.3 `exposes` Block (Output Port)**

| Key         | Type         | Required | Description                                   |
|-------------|--------------|----------|-----------------------------------------------|
| name        | String       | If list  | Unique name for output port                   |
| location    | Object       | Yes      | Where data is materialized                    |
| contract    | Object       | Yes      | Schema, quality, privacy promises             |
| accessPolicy| Object       | No       | Who can access and under what conditions      |

#### **4.3.1 `location` Object**

| Key        | Type     | Required | Description                                   |
|------------|----------|----------|-----------------------------------------------|
| type       | String   | Yes      | bigquery, s3, snowflake, gcs, iceberg, virtual|
| connection | String   | Yes      | Reference to secret in vault                  |
| format     | Object   | If not virtual | Data format (e.g., parquet)              |
| properties | Object   | Yes      | Technology-specific properties                |

---

### **4.4 `consumes` Block (Input Port)**

| Key             | Type     | Required | Description                                   |
|-----------------|----------|----------|-----------------------------------------------|
| type            | String   | Yes      | gcs, kafka, s3, postgres-cdc, sftp, api, fluid-product |
| name            | String   | If type: fluid-product | Upstream FLUID dataProduct name      |
| alias           | String   | If list  | Local alias for build block                   |
| onUpstreamChange| String   | No       | Action on upstream contract change            |
| connection      | String   | If physical type | Reference to secret in vault            |
| format          | Object   | If physical type | Data format (e.g., json)                |
| properties      | Object   | If physical type | Tech-specific properties                 |

---

### **4.5 `contract` Block**

| Key         | Type     | Required | Description                                   |
|-------------|----------|----------|-----------------------------------------------|
| inheritFrom | String   | No       | dbt, fluid-product, openApi                   |
| model/spec  | String   | If inheriting | dbt model name or OpenAPI spec path/URL  |
| schema      | Object   | Yes      | Columns and data types                        |
| quality     | List     | No       | Data quality rules                            |
| privacy     | List     | No       | Privacy classifications/treatments            |
| semantics   | Object   | No       | Machine-readable meaning                      |

#### **4.5.1 `contract.schema.columns` Array**

| Key      | Type    | Required | Description                |
|----------|---------|----------|----------------------------|
| name     | String  | Yes      | Column name                |
| type     | String  | Yes      | STRING, INT64, etc.        |
| nullable | Boolean | No       | true by default            |

#### **4.5.2 `contract.quality` Array**

| Key      | Type    | Description                                   |
|----------|---------|-----------------------------------------------|
| rule     | String  | not_null, unique, regex_match, in_set, custom |
| columns  | List    | Columns to apply rule to                      |
| pattern/set | String/List | Regex or set for validation           |
| onFailure| Object  | Action (reject_row, quarantine_row, etc.)     |

#### **4.5.3 `contract.privacy` Array**

| Key           | Type    | Description                                   |
|---------------|---------|-----------------------------------------------|
| classification| String  | PII, SPI, Confidential                        |
| columns       | List    | Columns to treat (can be ['*'])               |
| treatment     | Object  | Type (hashing, masking, etc.), properties     |

---

### **4.6 `build` Block (Implementation)**

| Key             | Type     | Required | Description                                   |
|-----------------|----------|----------|-----------------------------------------------|
| transformation  | Object   | No       | Core data manipulation logic                  |
| execution       | Object   | Yes      | Orchestration, scheduling, runtime            |
| stateManagement | Object   | Yes      | How incremental/streaming state is persisted  |

#### **4.6.1 `build.transformation` Block**

| Key        | Type    | Required | Description                                   |
|------------|---------|----------|-----------------------------------------------|
| engine     | String  | Yes      | sql, python, dbt, dbt-cloud, spark-sql        |
| properties | Object  | Yes      | Engine-specific logic                         |

#### **4.6.2 `build.execution` Block**

| Key           | Type    | Required | Description                                   |
|---------------|---------|----------|-----------------------------------------------|
| trigger       | Object  | Yes      | How build is initiated                        |
| runtime       | Object  | Yes      | Compute platform                              |
| dependencies  | Object  | No       | Execution dependencies                        |
| retries       | Object  | No       | Retry config                                  |
| notifications | Object  | No       | Alerts on success/failure                     |

#### **4.6.3 `build.stateManagement` Block**

| Key        | Type    | Required | Description                                   |
|------------|---------|----------|-----------------------------------------------|
| backend    | String  | Yes      | gcs, s3, bigquery_table                       |
| properties | Object  | Yes      | Connection properties                         |

---

### **4.7 `accessPolicy` and `dynamicPolicies` Blocks**

- **accessPolicy**: Static permissions for known principals.
- **dynamicPolicies**: Rules evaluated at query time based on agent context.

#### **accessPolicy.grants Array Item**

| Key        | Type    | Required | Description                                   |
|------------|---------|----------|-----------------------------------------------|
| principal  | String  | Yes      | user:<email>, group:<name>, agent:<id>        |
| permissions| List    | Yes      | readData, readMetadata, manage                |
| scope      | Object  | No       | Fine-grained access                           |

#### **dynamicPolicies.rules Array Item**

| Key        | Type    | Required | Description                                   |
|------------|---------|----------|-----------------------------------------------|
| name       | String  | Yes      | Policy rule name                              |
| condition  | String  | Yes      | Expression evaluated against agent context    |
| grant      | Object  | Yes      | Permissions and scope if condition is met     |

#### **scope Object**

| Key         | Type    | Required | Description                                   |
|-------------|---------|----------|-----------------------------------------------|
| columns     | List    | No       | Allow-list of columns                         |
| rowFilter   | String  | No       | SQL WHERE clause                              |
| privacyView | String  | No       | treated (default), cleartext                  |

---
