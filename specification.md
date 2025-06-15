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


🌊 FLUID: Federated Layered Unified Interchange Definition  
Version 1.0 – Official Specification

---

## Preamble

This document provides the complete, official v1.0 specification for the FLUID (Federated Layered Unified Interchange Definition) protocol. It is intended for data architects, platform engineers, and developers who are building the next generation of data infrastructure, as well as for vendors seeking to make their tools compliant with this open standard.

---

## 1. Specification Root

The FLUID definition is a YAML file (`.fluid.yml`) with the following root-level objects.

| Key            | Type           | Required | Description                                                                 |
|----------------|----------------|----------|-----------------------------------------------------------------------------|
| fluidVersion   | String         | Yes      | The version of the FLUID specification this file adheres to (e.g., 1.0).    |
| kind           | String         | Yes      | The type of data product definition. See section 1.1.                       |
| extends        | String         | No       | Path or URL to a base template FLUID file for standardization.              |
| metadata       | Object         | Yes      | Identification, ownership, and classification information. See section 1.2. |
| exposes        | Object / List  | Yes      | Defines the public output interface(s) of the product. See section 1.3.     |
| consumes       | Object / List  | No       | Defines the input data sources needed to build the product. See section 1.4.|
| build          | Object         | No       | Contains the implementation logic for how the product is built. See 1.5.    |
| accessPolicy   | Object         | No       | Defines the static access control policies for the data product. See 1.6.   |
| dynamicPolicies| Object         | No       | Defines context-aware access policies that adapt at runtime. See 1.7.       |
| operations     | Object         | No       | Defines SLAs, lifecycle, and observability characteristics. See 1.8.        |
| extensions     | Object         | No       | Registers required external plugins. See section 1.9.                       |
| revision       | String         | No       | (Recommended) The Git commit hash, tag, or version for traceability.        |

---

### 1.1 kind Enumeration

The `kind` key specifies the nature of the data product.

- **DataProduct**: A standard, materialized data asset.
- **VirtualDataProduct**: A product that exists only as a logical view or query, without its own physical storage.
- **EgressFlow**: A product specifically designed to export data securely to an external system.

---

### 1.2 metadata Block

| Key           | Type           | Required | Description                                                                 |
|---------------|----------------|----------|-----------------------------------------------------------------------------|
| dataProduct   | String         | Yes      | Globally unique name using dot notation (e.g., finance.gold.balances).      |
| owner         | Object         | Yes      | Ownership details (e.g., { team: 'finance', email: 'finance@company.com' }).|
| description   | String         | No       | Purpose of the product (Markdown supported).                                |
| tags          | Map[String]    | No       | Key-value pairs for categorization (e.g., layer: gold, domain: finance).    |
| classification| String         | Yes      | Default privacy level: public, internal, confidential, restricted.          |
| version       | String         | No       | (Recommended) Semantic version of this data product definition (e.g., 1.0.0).|

---

### 1.3 exposes Block (The Output Port)

Defines the public interface of the data product. This is what consumers interact with.

| Key      | Type   | Required | Description                                                        |
|----------|--------|----------|--------------------------------------------------------------------|
| name     | String | If list  | A unique name for this output port within the product.              |
| location | Object | Yes      | The physical or virtual location where the data product is materialized. See 1.3.1. |
| contract | Object | Yes      | The schema, quality, and privacy promises for this output. See 1.3.2. |

#### 1.3.1 location Object

| Key        | Type   | Required      | Description                                                        |
|------------|--------|--------------|--------------------------------------------------------------------|
| type       | String | Yes           | bigquery, s3, snowflake, gcs, iceberg, api, kafka, or virtual.     |
| connection | String | Yes           | Reference to a secret in a vault (e.g., secret:gcp-prod-dwh-key).  |
| format     | Object | If not virtual| Describes the data format (e.g., { type: 'parquet' }).             |
| properties | Object | Yes           | Technology-specific properties (e.g., project, dataset, table).    |

#### 1.3.2 contract Object

| Key         | Type   | Required      | Description                                                        |
|-------------|--------|--------------|--------------------------------------------------------------------|
| inheritFrom | String | No           | dbt, fluid-product, or openApi. Populates the contract from a source.|
| model / spec| String | If inheriting| The dbt model name or path to the OpenAPI spec file/URL.           |
| schema      | Object | Yes          | Defines the columns and data types. See 1.3.2.1.                   |
| quality     | List   | No           | List of data quality rules to enforce. See 1.3.2.2.                |
| privacy     | List   | No           | List of privacy classifications and treatments. See 1.3.2.3.        |
| semantics   | Object | No           | Adds machine-readable meaning to the data. See 1.3.2.4.            |

##### 1.3.2.1 schema.columns Array

| Key     | Type    | Required | Description                                  |
|---------|---------|----------|----------------------------------------------|
| name    | String  | Yes      | Column name.                                 |
| type    | String  | Yes      | Data type (STRING, INT64, NUMERIC, TIMESTAMP, JSON, BOOLEAN, DATE). |
| nullable| Boolean | No       | true by default.                             |

##### 1.3.2.2 quality Array Item

| Key      | Type   | Required      | Description                                                        |
|----------|--------|--------------|--------------------------------------------------------------------|
| rule     | String | Yes          | not_null, unique, regex_match, in_set, or a custom SQL expression. |
| columns  | List   | If applicable| Column(s) to apply the rule to.                                    |
| pattern/set| String/List|If applicable| Parameters for regex_match or in_set.                         |
| onFailure| Object | Yes          | action (reject_row, quarantine_row, fail_pipeline, alert) and optional notifications. |

##### 1.3.2.3 privacy Array Item

| Key           | Type   | Required      | Description                                                        |
|---------------|--------|--------------|--------------------------------------------------------------------|
| classification| String | No           | PII, SPI, Confidential. Overrides metadata.classification.         |
| columns       | List   | Yes          | Column(s) to apply the treatment to. Can be ['*'].                 |
| treatment     | Object | Yes          | type (hashing, masking, encryption, tokenization) and properties.  |

##### 1.3.2.4 semantics Object

| Key           | Type   | Description                                                        |
|---------------|--------|--------------------------------------------------------------------|
| ontology      | String | Reference to an external ontology (e.g., URL to an OWL or RDF file).|
| classifications| List  | Maps columns to terms in a business glossary or formal ontology.   |

---

### 1.4 consumes Block (The Input Port)

| Key             | Type   | Required      | Description                                                        |
|-----------------|--------|--------------|--------------------------------------------------------------------|
| type            | String | Yes          | gcs, kafka, s3, api, postgres-cdc, sftp, or fluid-product.         |
| name            | String | If type: fluid-product | The dataProduct name of the upstream FLUID definition.      |
| alias           | String | If list      | A local alias to refer to this source in the build block.          |
| onUpstreamChange| String | No           | Action on upstream contract change: fail, alert, triggerRebuild.   |
| connection      | String | If physical type | Reference to a secret in a vault.                             |
| format          | Object | If physical type | Describes the data format (e.g., { type: 'json' }).           |
| properties      | Object | If physical type | Technology-specific properties (e.g., Kafka topic, API endpoint). |

---

### 1.5 build Block (The Implementation)

| Key             | Type   | Required      | Description                                                        |
|-----------------|--------|--------------|--------------------------------------------------------------------|
| transformation  | Object | No           | The core data manipulation logic. See 1.5.1.                       |
| execution       | Object | Yes          | Defines the orchestration, scheduling, and runtime. See 1.5.2.     |
| stateManagement | Object | If incremental/streaming | Defines how the flow's state is persisted. See 1.5.3. |

#### 1.5.1 build.transformation Block

| Key      | Type   | Required | Description                                                        |
|----------|--------|----------|--------------------------------------------------------------------|
| engine   | String | Yes      | The engine to use: sql, python, dbt, dbt-cloud, spark-sql.         |
| properties| Object| Yes      | Engine-specific properties that contain the transformation logic.   |
| lineage  | Object | No       | Explicit column-level lineage declarations for complex or Python transformations. |

#### 1.5.2 build.execution Block

| Key          | Type   | Required | Description                                                        |
|--------------|--------|----------|--------------------------------------------------------------------|
| trigger      | Object | Yes      | Defines how the build is initiated (schedule, event, manual).      |
| runtime      | Object | Yes      | The underlying compute platform where the build will run (airflow, gcp-cloud-run). |
| dependencies | Object | No       | Defines the execution dependencies on other data products.         |
| retries      | Object | No       | Configuration for handling transient failures: count, delay.       |
| notifications| Object | No       | Defines how to send alerts (channel, target) on onSuccess or onFailure. |

#### 1.5.3 build.stateManagement Block

| Key      | Type   | Required | Description                                                        |
|----------|--------|----------|--------------------------------------------------------------------|
| backend  | String | Yes      | The system to store state: gcs, s3, bigquery_table.                |
| properties| Object| Yes      | Connection properties for the chosen backend (e.g., bucket, path). |

---

### 1.6 accessPolicy (Static Access)

| Key        | Type   | Required | Description                                                        |
|------------|--------|----------|--------------------------------------------------------------------|
| visibility | String | No       | Default discoverability: private, internal.                        |
| grants     | List   | Yes      | A list of static, explicit access grants.                          |

#### 1.6.1 grants Array Item

| Key        | Type   | Required | Description                                                        |
|------------|--------|----------|--------------------------------------------------------------------|
| principal  | String | Yes      | The actor receiving the grant. Format: user:<email>, group:<name>, agent:<id>. |
| permissions| List   | Yes      | Rights granted: readData, readMetadata, manage.                    |
| scope      | Object | No       | Fine-grained access. See 1.6.2.                                    |

#### 1.6.2 scope Object

| Key         | Type   | Required | Description                                                        |
|-------------|--------|----------|--------------------------------------------------------------------|
| columns     | List   | No       | Allow-list of columns the principal can view.                      |
| rowFilter   | String | No       | SQL WHERE clause for secure view.                                  |
| privacyView | String | No       | treated (default, views post-privacy data), cleartext (views pre-privacy data). |

---

### 1.7 dynamicPolicies (Adaptive Access)

| Key   | Type | Required | Description                                                        |
|-------|------|----------|--------------------------------------------------------------------|
| rules | List | Yes      | A list of contextual access rules, evaluated in order.              |

#### 1.7.1 rules Array Item

| Key       | Type   | Required | Description                                                        |
|-----------|--------|----------|--------------------------------------------------------------------|
| name      | String | Yes      | A descriptive name for the policy rule.                            |
| condition | String | Yes      | An expression evaluated against the agent's context. Supports interpolation. |
| grant     | Object | Yes      | The permissions and scope to grant if the condition is met.        |

---

### 1.8 operations Block

| Key         | Type   | Required | Description                                                        |
|-------------|--------|----------|--------------------------------------------------------------------|
| sla         | Object | No       | Defines the Service Level Agreements for this product. See 1.8.1.  |
| lifecycle   | Object | No       | Manages data retention and archival policies. See 1.8.2.           |
| observability| Object| No       | Configures logging, alerting, and monitoring. See 1.8.3.           |

#### 1.8.1 sla Object

Defines cost, latency, freshness, accuracy, sustainability, and feedbackSignals.

#### 1.8.2 lifecycle Object

Defines retention (period, condition) and archival (trigger, destination).

#### 1.8.3 observability Object

Defines logging (level, destination) and alerting (onFailure notifications).

---

### 1.9 extensions Block

| Key                  | Type | Description                                                        |
|----------------------|------|--------------------------------------------------------------------|
| customTransformations| List | A list of custom transformation engines the build requires.         |
| policyEngines        | List | A list of external policy engines (e.g., OPA) needed to evaluate policies. |
| observabilityHooks   | List | A list of custom hooks to send metrics and traces to external systems. |



