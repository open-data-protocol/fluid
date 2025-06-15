# A Practical Guide to Integrating Data Vault 2.0

This guide presents a hands-on proposal for integrating the [FLUID specification](https://github.com/your-org/fluid-spec) with core data stack tools like **dbt** and **datavault 2.0**. It explains how this integration streamlines data engineering workflows, clarifies tool responsibilities, and solves common pain points in modern data platforms.

## Example : Building a Data Vault 2.0 Product

**Goal:**  
Model "Customers" from CRM and e-commerce sources using Data Vault 2.0 in BigQuery with dbt.

### Data Vault Components

- **hub_customer:** Unique business key for a customer
- **sat_customer_details_crm:** CRM attributes
- **sat_customer_details_ecommerce:** E-commerce attributes

**Folder Structure:**
```
/
├── data-products/
│   └── datavault/
│       ├── customer_hub/
│       │   └── product.fluid.yml
│       ├── crm_satellite/
│       │   └── product.fluid.yml
│       ├── ecommerce_satellite/
│       │   └── product.fluid.yml
│       └── dbt_datavault_project/
│           ├── dbt_project.yml
│           └── models/
│               ├── staging/
│               │   ├── stg_crm_customers.sql
│               │   └── stg_ecommerce_users.sql
│               └── marts/
│                   ├── hub_customer.sql
│                   ├── sat_customer_details_crm.sql
│                   └── sat_customer_details_ecommerce.sql
└── airflow/
        └── dags/
                └── fluid_dag_generator.py
```

### Example dbt Model (`stg_crm_customers.sql`)
```sql
{% set source_model = "raw_crm_customers" %}
{% set src_pk = "CUSTOMER_HK" %}
{% set src_hashdiff = "CUSTOMER_HASHDIFF" %}
{% set src_payload = ["FULL_NAME", "EMAIL_ADDRESS", "CREATED_AT"] %}
{% set src_ldts = "LOAD_TS" %}
{% set src_source = "RECORD_SOURCE" %}

WITH source_data AS (
        SELECT * FROM {{ source('bronze', source_model) }}
)
SELECT
        {{ dbtvault.hub_hash(src_pk, 'CUSTOMER_ID') }},
        {{ dbtvault.satellite_hashdiff(src_hashdiff, src_payload) }},
        {{ src_payload | join(', ') }},
        {{ src_ldts }},
        {{ src_source }}
FROM source_data
```

### FLUID Files

**1. Hub Data Product (`customer_hub/product.fluid.yml`):**
```yaml
fluidVersion: 1.0
kind: DataProduct
metadata:
    dataProduct: datavault.silver.hub_customer
    owner: { team: 'data-architecture' }
consumes:
    - type: dbt-model
        name: stg_crm_customers
    - type: dbt-model
        name: stg_ecommerce_users
exposes:
    location:
        type: bigquery
        properties:
            project: 'bq-prod-lakehouse'
            dataset: 'datavault_silver'
            table: 'hub_customer'
    contract:
        inheritFrom: dbt
        model: 'hub_customer'
build:
    transformation:
        engine: dbt
        properties:
            projectDir: '../dbt_datavault_project/'
            command: 'run'
            models: ['hub_customer']
    execution:
        trigger: { type: 'schedule', properties: { cron: '0 1 * * *' } }
        runtime: { type: 'airflow' }
        dependencies:
            dataProducts: ['crm.bronze.raw_customers', 'ecommerce.bronze.raw_users']
```

**2. Satellite Data Product (`crm_satellite/product.fluid.yml`):**
```yaml
fluidVersion: 1.0
kind: DataProduct
metadata:
    dataProduct: datavault.silver.sat_customer_details_crm
    owner: { team: 'data-architecture' }
consumes:
    type: fluid-product
    name: datavault.silver.hub_customer
# ... exposes and build blocks ...
build:
    transformation:
        engine: dbt
        properties:
            projectDir: '../dbt_datavault_project/'
            command: 'run'
            models: ['sat_customer_details_crm']
    execution:
        dependencies:
            dataProducts: ['datavault.silver.hub_customer']
```

*The e-commerce satellite is structured similarly, depending on the hub.*

---

## How FLUID-Aware Orchestration Works

The Airflow DAG factory (`fluid_dag_generator.py`) reads all FLUID files and builds the dependency graph:

1. **ExternalTaskSensor:** Waits for raw data products (`crm.bronze.raw_customers`, `ecommerce.bronze.raw_users`).
2. **BashOperator:** Runs `dbt run --models hub_customer`.
3. **TaskGroup:** Runs satellites in parallel:  
     - `dbt run --models sat_customer_details_crm`  
     - `dbt run --models sat_customer_details_ecommerce`

**Result:**  
Engineers declare dependencies in FLUID files; the orchestrator builds and maintains the complex DAG automatically. This dramatically simplifies and hardens the creation of sophisticated semantic models.

---

> **FLUID + dbt + Airflow = Declarative, contract-aware, and maintainable data pipelines.**
