# 🚀 A Practical Guide to Integrating **dbt** with **FLUID**

> **Unlock seamless, contract-aware data engineering with FLUID and dbt.**

---

## 🧩 The Problem: The Disconnected DAG

Modern analytics engineering is split between two worlds:

- **The dbt World:**  
    - SQL transformations  
    - Contracts in `schema.yml`  
    - Sources in `sources.yml`  
    - Lineage *within* the dbt project

- **The Orchestration World (e.g., Airflow):**  
    - Python DAGs trigger `dbt run`  
    - No native understanding of dbt contracts or sources

**This disconnect leads to:**

- ❌ *Brittle Glue Code*: Manual, fragile connections between ingestion and dbt
- ❌ *No End-to-End Lineage*: Orchestrator can’t see inside dbt
- ❌ *Contract-Unaware Orchestration*: No way to know if upstream changes break dbt models

---

## 🦄 The Solution: **FLUID**

**FLUID** introduces a unified, declarative manifest that both orchestrators and dbt can understand.

- **No more glue code**
- **End-to-end, contract-aware orchestration**
- **Explicit, version-controlled data products**

---

## ⚖️ Where FLUID Stops and dbt Begins

| Responsibility | FLUID | dbt |
|---|---|---|
| **Ingestion** | ✅ | ❌ |
| **Physical location & access** | ✅ | ❌ |
| **Orchestration** | ✅ | ❌ |
| **SQL transformation logic** | ❌ | ✅ |
| **Transformation contracts** | Inherits from dbt | ✅ (source of truth) |

> **FLUID orchestrates dbt as a best-in-class transformation engine. It does not replace it.**

---

## 🌱 Pathways to a FLUID-Aware dbt Ecosystem

1. **FLUID-Aware Orchestrators**  
     - Orchestrators (e.g., Airflow, CI/CD) read `.fluid.yml`  
     - See `engine: dbt` → run dbt with specified properties  
     - **_Can be done today!_**

2. **FLUID-Aware dbt (Future)**  
     - dbt-core enhanced to accept `fluid-product` as a source  
     - dbt resolves upstream dependencies via FLUID files

> _This guide focuses on #1: FLUID-aware orchestration with dbt as-is._

---

## 🛠️ Worked Example: Building a Silver Customer Product

### **Goal:**  
Ingest raw customer data from GCS → Load to "bronze" table → Use dbt to transform into clean "silver" `stg_customers` model.

---

### 1️⃣ Federated Folder Structure

```
/data-products/customers/
│
├── bronze_raw_customers/
│   └── product.fluid.yml       # FLUID for ingestion (Step 1)
│
└── silver_stg_customers/
        ├── product.fluid.yml       # FLUID orchestrates dbt (Step 2)
        │
        └── dbt_project/            # Standard dbt project
                ├── dbt_project.yml
                └── models/
                        ├── staging/
                        │   ├── stg_customers.sql
                        │   └── schema.yml
                        └── sources.yml
```

---

### 2️⃣ The FLUID Files

#### **File 1: `bronze_raw_customers/product.fluid.yml`**  
*Ingest raw data from GCS into BigQuery.*

```yaml
fluidVersion: 1.0
kind: DataProduct

metadata:
    dataProduct: customers.bronze.raw_customers
    owner: { team: 'data-platform' }

consumes:
    type: gcs
    connection: secret:gcp-prod-sa-key
    format: { type: 'jsonl' }
    properties:
        bucket: 'prod-crm-uploads'
        path: 'customers/daily/'

exposes:
    location:
        type: bigquery
        properties:
            project: 'bq-prod-lakehouse'
            dataset: 'bronze'
            table: 'raw_customers'
    contract:
        schema:
            columns:
                - { name: data, type: JSON }
                - { name: loaded_at, type: TIMESTAMP }

build:
    execution:
        trigger: { type: 'event', properties: { topic: 'gcs-new-customer-file' } }
        runtime: { type: 'gcp-cloud-run' }
    stateManagement:
        backend: gcs
        properties: { bucket: 'fluid-state-prod', path: 'customers.bronze.raw_customers.json' }
```

---

#### **File 2: `silver_stg_customers/product.fluid.yml`**  
*Orchestrate dbt to build the silver product.*

```yaml
fluidVersion: 1.0
kind: DataProduct

metadata:
    dataProduct: customers.silver.stg_customers
    owner: { team: 'analytics-engineering' }
    description: "Cleansed and standardized customer data."
    tags: { layer: 'silver', tool: 'dbt' }

consumes:
    type: fluid-product
    name: customers.bronze.raw_customers

exposes:
    location:
        type: bigquery
        properties:
            project: 'bq-prod-lakehouse'
            dataset: 'silver'
            table: 'stg_customers'
    contract:
        inheritFrom: dbt
        model: 'stg_customers'
    accessPolicy:
        visibility: internal

build:
    transformation:
        engine: dbt
        properties:
            projectDir: './dbt_project/'
            profile: 'gcp_prod'
            target: 'prod'
            command: 'run'
            models:
                - 'stg_customers'
    execution:
        trigger: { type: 'schedule', properties: { cron: '0 5 * * *' } }
        runtime: { type: 'airflow' }
        dependencies:
            dataProducts: ['customers.bronze.raw_customers']
    stateManagement:
        backend: gcs
        properties: { bucket: 'fluid-state-prod', path: 'customers.silver.stg_customers.json' }
```

---

### 3️⃣ The dbt Project Files

#### **File 3: `models/sources.yml`**  
*Define the source for dbt, pointing to the bronze table.*

```yaml
version: 2
sources:
    - name: staging
        database: bq-prod-lakehouse
        schema: bronze
        tables:
            - name: raw_customers
```

---

#### **File 4: `models/staging/stg_customers.sql`**  
*Standard dbt model.*

```sql
with source as (
        select * from {{ source('staging', 'raw_customers') }}
)

select
        json_extract_scalar(data, '$.id') as customer_id,
        json_extract_scalar(data, '$.first_name') as first_name,
        json_extract_scalar(data, '$.last_name') as last_name,
        loaded_at as created_at
from source
```

---

#### **File 5: `models/staging/schema.yml`**  
*dbt contract inherited by FLUID.*

```yaml
version: 2
models:
    - name: stg_customers
        description: "Cleansed customer records from raw source."
        columns:
            - name: customer_id
                description: "The unique customer identifier."
                tests:
                    - not_null
                    - unique
            - name: first_name
                description: "Customer's first name."
            - name: last_name
                description: "Customer's last name."
            - name: created_at
                description: "Timestamp when the record was ingested."
                tests:
                    - not_null
```

---

## 🎯 **Conclusion: What Problem Is Solved?**

- **Decoupling:**  
    - Ingestion and analytics teams work independently  
    - No need to understand each other's implementation details

- **End-to-End Lineage:**  
    - FLUID-aware tools generate lineage:  
        `GCS Bucket → bronze.raw_customers → silver.stg_customers`

- **Contract-Aware Orchestration:**  
    - Orchestrator knows dependencies and contracts  
    - CI/CD can fail fast on breaking changes

---

> **By adopting FLUID, you move from a world of implicit, brittle glue code to explicit, version-controlled, contract-aware data products. This is the foundation for a scalable, trustworthy data fabric.**

---
