<p align="center">
  <img src="fluid-logo.png" width="200" alt="FLUID Logo"/>
</p>

## 📚 Fluid Protocol Specification (v1.0)

This document provides the complete, official v1.0 specification for the FLUID (Federated Layered Unified Interchange Definition) protocol. It is intended for data architects, platform engineers, and developers who are building the next generation of data infrastructure, as well as for vendors seeking to make their tools compliant with this open standard.

### The Strategic Imperative: A Protocol for the Agentic Era
The contemporary enterprise is shifting from process automation to an Agentic Ecosystem, where autonomous AI agents drive operations with unprecedented speed and intelligence. This paradigm shift, enabled by communication standards like the Model Context Protocol (MCP), exposes a foundational vulnerability in modern data architecture: the lack of a common language for defining, governing, and interacting with data assets.

Today's data landscape is a fragmented collection of imperative pipelines, siloed tool configurations, and implicit knowledge. This static, brittle foundation cannot support the dynamic, real-time demands of an agentic workforce. Agents require a data fabric that is not only accessible but also discoverable, trustworthy, and context-aware.

FLUID is the standard designed to create this fabric. It addresses this challenge by providing a declarative, universal protocol for defining Data Products. It is the missing piece of the puzzle, serving as the foundational layer that makes an organization truly MCP-ready. While MCP standardizes how agents communicate, FLUID standardizes the trustworthy Data Products they communicate with.

### What is FLUID?
FLUID is an open, declarative specification, written in YAML and managed in version control. It is not a platform or a single tool, but a shared language that enables a decentralized ecosystem of compliant tools to work in concert.

It re-frames the data lifecycle around the concept of a Data Product: a versioned, autonomous asset with a clearly defined interface, contract, and implementation. By unifying the definition of what a data product consumes (its dependencies), what it exposes (its public interface), and how it is built (its implementation logic), FLUID provides a holistic, auditable, and machine-readable blueprint for every data asset in the enterprise.

This document details the full specification for this protocol, providing the technical foundation required to build the governable, scalable, and agent-ready data ecosystems of the future.

## **1.0 Root Object**

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

### **1.1 `metadata` Block**

| Key         | Type         | Required | Description                                   |
|-------------|--------------|----------|-----------------------------------------------|
| dataProduct | String       | Yes      | Globally unique name (e.g., sales.silver.clean_orders) |
| owner       | Object       | Yes      | Team/individual responsible                   |
| description | String       | No       | Markdown-supported description                |
| tags        | Map[String]  | No       | Key-value pairs for categorization            |
| version     | String       | No       | Semantic version                              |

---

### **1.2 `exposes` Block (Output Port)**

| Key         | Type         | Required | Description                                   |
|-------------|--------------|----------|-----------------------------------------------|
| name        | String       | If list  | Unique name for output port                   |
| location    | Object       | Yes      | Where data is materialized                    |
| contract    | Object       | Yes      | Schema, quality, privacy promises             |
| accessPolicy| Object       | No       | Who can access and under what conditions      |

#### **1.2.1 `location` Object**

| Key        | Type     | Required | Description                                   |
|------------|----------|----------|-----------------------------------------------|
| type       | String   | Yes      | bigquery, s3, snowflake, gcs, iceberg, virtual|
| connection | String   | Yes      | Reference to secret in vault                  |
| format     | Object   | If not virtual | Data format (e.g., parquet)              |
| properties | Object   | Yes      | Technology-specific properties                |

---

### **1.3 `consumes` Block (Input Port)**

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

### **1.2.3 `contract` Block**

| Key         | Type     | Required | Description                                   |
|-------------|----------|----------|-----------------------------------------------|
| inheritFrom | String   | No       | dbt, fluid-product, openApi                   |
| model/spec  | String   | If inheriting | dbt model name or OpenAPI spec path/URL  |
| schema      | Object   | Yes      | Columns and data types                        |
| quality     | List     | No       | Data quality rules                            |
| privacy     | List     | No       | Privacy classifications/treatments            |
| semantics   | Object   | No       | Machine-readable meaning                      |

#### **1.2.3.1 `contract.schema.columns` Array**

| Key      | Type    | Required | Description                |
|----------|---------|----------|----------------------------|
| name     | String  | Yes      | Column name                |
| type     | String  | Yes      | STRING, INT64, etc.        |
| nullable | Boolean | No       | true by default            |

#### **1.2.3.2 `contract.quality` Array**

| Key      | Type    | Description                                   |
|----------|---------|-----------------------------------------------|
| rule     | String  | not_null, unique, regex_match, in_set, custom |
| columns  | List    | Columns to apply rule to                      |
| pattern/set | String/List | Regex or set for validation           |
| onFailure| Object  | Action (reject_row, quarantine_row, etc.)     |

#### **1.2.3.3 `contract.privacy` Array**

| Key           | Type    | Description                                   |
|---------------|---------|-----------------------------------------------|
| classification| String  | PII, SPI, Confidential                        |
| columns       | List    | Columns to treat (can be ['*'])               |
| treatment     | Object  | Type (hashing, masking, etc.), properties     |

---

### **1.4 `build` Block (Implementation)**

| Key             | Type     | Required | Description                                   |
|-----------------|----------|----------|-----------------------------------------------|
| transformation  | Object   | No       | Core data manipulation logic                  |
| execution       | Object   | Yes      | Orchestration, scheduling, runtime            |
| stateManagement | Object   | Yes      | How incremental/streaming state is persisted  |

#### **1.4.1 `build.transformation` Block**

| Key        | Type    | Required | Description                                   |
|------------|---------|----------|-----------------------------------------------|
| engine     | String  | Yes      | sql, python, dbt, dbt-cloud, spark-sql        |
| properties | Object  | Yes      | Engine-specific logic                         |

#### **1.4.2 `build.execution` Block**

| Key           | Type    | Required | Description                                   |
|---------------|---------|----------|-----------------------------------------------|
| trigger       | Object  | Yes      | How build is initiated                        |
| runtime       | Object  | Yes      | Compute platform                              |
| dependencies  | Object  | No       | Execution dependencies                        |
| retries       | Object  | No       | Retry config                                  |
| notifications | Object  | No       | Alerts on success/failure                     |

#### **1.4.3 `build.stateManagement` Block**

| Key        | Type    | Required | Description                                   |
|------------|---------|----------|-----------------------------------------------|
| backend    | String  | Yes      | gcs, s3, bigquery_table                       |
| properties | Object  | Yes      | Connection properties                         |

---

### **1.5 `accessPolicy` and `dynamicPolicies` Blocks**

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
