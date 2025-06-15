# 🚀 **FLUID by Example: The Ultimate Curated Guide for New Users**

Welcome to the **FLUID** journey! This guide presents **10 foundational `.fluid.yml` examples**, each crafted to help you master the FLUID specification. Examples are ordered from the simplest to the most advanced, building your knowledge step by step.

---

## 📚 **Table of Contents**

1. [Hello, World! – A Basic File Copy](#1-hello-world--a-basic-file-copy)
2. [Adding a Contract – Schema Enforcement](#2-adding-a-contract--schema-enforcement)
3. [Simple Transformation (SQL)](#3-simple-transformation-sql)
4. [Adding Quality Rules](#4-adding-quality-rules)
5. [Layered Product (Consuming another FLUID Product)](#5-layered-product-consuming-another-fluid-product)
6. [Orchestration with dbt](#6-orchestration-with-dbt)
7. [Streaming Ingestion (Kafka)](#7-streaming-ingestion-kafka)
8. [Adding Privacy Treatments](#8-adding-privacy-treatments)
9. [Egress Flow to an External System](#9-egress-flow-to-an-external-system)
10. [Product with Access Policies](#10-product-with-access-policies)

---

## 1. Hello, World! – A Basic File Copy <a name="1-hello-world--a-basic-file-copy"></a>

> **Goal:** Copy files from one cloud storage location to another.  
> **Concepts:** Data product basics, scheduling, state management.

```yaml
# 01-hello-world.fluid.yml
fluidVersion: "1.0"
kind: DataProduct

metadata:
    dataProduct: landing.bronze.raw_user_uploads
    owner: { team: 'data-platform' }

consumes:
    - type: gcs
        connection: secret:gcp-prod-sa-key
        properties:
            bucket: 'acme-user-uploads-raw'
            path: 'daily/*.csv'

exposes:
    - location:
            type: gcs
            connection: secret:gcp-prod-sa-key
            properties:
                bucket: 'acme-bronze-layer'
                path: 'raw_user_uploads/'
        contract:
            schema: { columns: [] } # Schema is unknown/undeclared initially

build:
    execution:
        trigger: { type: 'schedule', properties: { cron: '0 1 * * *' } }
        runtime: { type: 'gcp-storage-copy-job' }
    stateManagement:
        backend: gcs
        properties: { bucket: 'fluid-state-prod', path: 'state/01-hello-world.json' }
```

---

## 2. Adding a Contract – Schema Enforcement <a name="2-adding-a-contract--schema-enforcement"></a>

> **Goal:** Validate source CSV columns before copying.  
> **Concepts:** Schema contracts, format conversion.

```yaml
# 02-with-contract.fluid.yml
fluidVersion: "1.0"
kind: DataProduct
metadata:
    dataProduct: landing.bronze.validated_user_uploads
    owner: { team: 'data-platform' }

consumes:
    - type: gcs
        connection: secret:gcp-prod-sa-key
        format: { type: 'csv', properties: { header: true } }
        properties:
            bucket: 'acme-user-uploads-raw'
            path: 'daily/*.csv'

exposes:
    - location:
            type: gcs
            connection: secret:gcp-prod-sa-key
            format: { type: 'parquet' }
            properties:
                bucket: 'acme-bronze-layer'
                path: 'validated_user_uploads/'
        contract:
            schema:
                columns:
                    - { name: 'user_id', type: 'STRING', nullable: false }
                    - { name: 'email', type: 'STRING' }
                    - { name: 'created_at', type: 'TIMESTAMP' }

build:
    execution:
        trigger: { type: 'schedule', properties: { cron: '0 1 * * *' } }
        runtime: { type: 'gcp-dataflow', properties: { jobTemplate: 'gcs-to-gcs-with-validation' } }
    stateManagement:
        backend: gcs
        properties: { bucket: 'fluid-state-prod', path: 'state/02-with-contract.json' }
```

---

## 3. Simple Transformation (SQL) <a name="3-simple-transformation-sql"></a>

> **Goal:** Transform data with SQL before loading to BigQuery.  
> **Concepts:** SQL transformations, type casting, renaming.

```yaml
# 03-simple-transform.fluid.yml
fluidVersion: "1.0"
kind: DataProduct
metadata:
    dataProduct: landing.bronze.users_table
    owner: { team: 'data-platform' }

consumes:
    - type: gcs
        connection: secret:gcp-prod-sa-key
        format: { type: 'csv', properties: { header: true } }
        properties:
            bucket: 'acme-user-uploads-raw'
            path: 'daily/*.csv'

exposes:
    - location:
            type: bigquery
            connection: secret:gcp-prod-sa-key
            properties:
                project: 'acme-prod-dwh'
                dataset: 'bronze'
                table: 'users'
        contract:
            schema: { columns: [{name: id, type: INT64}, {name: user_email, type: STRING}] }

build:
    transformation:
        engine: sql
        properties:
            query: |
                SELECT
                    CAST(user_id AS INT64) as id,
                    email as user_email
                FROM source
    execution:
        trigger: { type: 'schedule', properties: { cron: '0 2 * * *' } }
        runtime: { type: 'gcp-dataflow' }
    stateManagement:
        backend: gcs
        properties: { bucket: 'fluid-state-prod', path: 'state/03-simple-transform.json' }
```

---

## 4. Adding Quality Rules <a name="4-adding-quality-rules"></a>

> **Goal:** Enforce data quality with validation rules.  
> **Concepts:** Quality block, row rejection, quarantining.

```yaml
# 04-with-quality.fluid.yml
fluidVersion: "1.0"
kind: DataProduct
metadata:
    dataProduct: landing.bronze.quality_checked_users
    owner: { team: 'data-platform' }

consumes: # ... same as example 3 ...

exposes:
    - location:
            type: bigquery
            properties: { project: 'acme-prod-dwh', dataset: 'bronze', table: 'quality_checked_users' }
        contract:
            schema: { columns: [{name: id, type: INT64}, {name: user_email, type: STRING}] }
            quality:
                - rule: not_null
                    columns: [id]
                    onFailure: { action: 'reject_row' }
                - rule: regex_match
                    columns: [user_email]
                    pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    onFailure: { action: 'quarantine_row', location: 'gs://acme-quarantine/invalid_emails/' }

build: # ... same as example 3 ...
```

---

## 5. Layered Product (Consuming another FLUID Product) <a name="5-layered-product-consuming-another-fluid-product"></a>

> **Goal:** Build lineage by consuming another FLUID product.  
> **Concepts:** Logical pointers, data product chaining.

```yaml
# 05-layered-product.fluid.yml
fluidVersion: "1.0"
kind: DataProduct
metadata:
    dataProduct: users.silver.enriched_users
    owner: { team: 'analytics-engineering' }

consumes:
    - type: fluid-product
        name: landing.bronze.quality_checked_users

exposes:
    - location:
            type: bigquery
            properties: { project: 'acme-prod-dwh', dataset: 'silver', table: 'users' }
        contract:
            schema: { columns: [{name: user_id, type: INT64}, {name: email, type: STRING}, {name: domain, type: STRING}] }

build:
    transformation:
        engine: sql
        properties:
            query: |
                SELECT
                    id as user_id,
                    user_email as email,
                    SPLIT(user_email, '@')[SAFE_OFFSET(1)] as domain
                FROM source
    execution:
        trigger: { type: 'schedule', properties: { cron: '0 3 * * *' } }
        runtime: { type: 'bigquery-job' }
    stateManagement:
        backend: gcs
        properties: { bucket: 'fluid-state-prod', path: 'state/05-layered-product.json' }
```

---

## 6. Orchestration with dbt <a name="6-orchestration-with-dbt"></a>

> **Goal:** Orchestrate dbt models with FLUID.  
> **Concepts:** dbt integration, model inheritance.

```yaml
# 06-with-dbt.fluid.yml
fluidVersion: "1.0"
kind: DataProduct
metadata:
    dataProduct: users.silver.dbt_enriched_users
    owner: { team: 'analytics-engineering' }

consumes:
    - type: fluid-product
        name: landing.bronze.quality_checked_users

exposes:
    - location:
            type: bigquery
            properties: { project: 'acme-prod-dwh', dataset: 'silver', table: 'dbt_users' }
        contract:
            inheritFrom: dbt
            model: 'dim_users'

build:
    transformation:
        engine: dbt
        properties:
            projectDir: './dbt/acme_project/'
            command: 'run'
            models: ['dim_users']
    execution:
        trigger: { type: 'schedule', properties: { cron: '0 4 * * *' } }
        runtime: { type: 'airflow' }
    stateManagement: { backend: gcs, properties: { bucket: 'fluid-state-prod' } }
```

---

## 7. Streaming Ingestion (Kafka) <a name="7-streaming-ingestion-kafka"></a>

> **Goal:** Ingest streaming data from Kafka.  
> **Concepts:** Streaming triggers, offset management.

```yaml
# 07-streaming-kafka.fluid.yml
fluidVersion: "1.0"
kind: DataProduct
metadata:
    dataProduct: events.bronze.raw_pageviews
    owner: { team: 'data-platform' }

consumes:
    - type: kafka
        connection: secret:prod-kafka-creds
        format: { type: 'json' }
        properties:
            topic: 'prod.web.pageviews'
            consumerGroup: 'fluid-gcs-sink-v1'

exposes:
    - location:
            type: gcs
            format: { type: 'parquet' }
            properties: { bucket: 'acme-bronze-layer', path: 'raw_pageviews/' }
        contract:
            schema: { columns: [{name: event_id, type: STRING}, {name: url, type: STRING}] }

build:
    execution:
        trigger: { type: 'streaming' }
        runtime: { type: 'gcp-dataflow', properties: { jobTemplate: 'kafka-to-gcs' } }
    stateManagement:
        backend: bigquery_table
        properties: { project: 'acme-prod-dwh', dataset: 'fluid_state', table: 'kafka_offsets' }
```

---

## 8. Adding Privacy Treatments <a name="8-adding-privacy-treatments"></a>

> **Goal:** Automatically hash PII columns.  
> **Concepts:** Privacy block, column transformation.

```yaml
# 08-with-privacy.fluid.yml
fluidVersion: "1.0"
kind: DataProduct
metadata:
    dataProduct: users.bronze.privacy_users
    owner: { team: 'data-platform' }

consumes: # ... same as example 2 ...

exposes:
    - location:
            type: bigquery
            properties: { project: 'acme-prod-dwh', dataset: 'bronze', table: 'privacy_users' }
        contract:
            schema:
                columns:
                    - { name: 'user_id', type: 'STRING' }
                    - { name: 'email_hash', type: 'STRING' }
                    - { name: 'created_at', type: 'TIMESTAMP' }
            privacy:
                - classification: PII
                    columns: [email]
                    treatment:
                        type: hashing
                        properties: { algorithm: 'SHA256' }
                        newColumn: 'email_hash'

build: # ... same as example 2 ...
```

---

## 9. Egress Flow to an External System <a name="9-egress-flow-to-an-external-system"></a>

> **Goal:** Send data to a partner via SFTP.  
> **Concepts:** EgressFlow kind, external destinations.

```yaml
# 09-egress-flow.fluid.yml
fluidVersion: "1.0"
kind: EgressFlow

metadata:
    dataProduct: partners.egress.daily_lead_export
    owner: { team: 'marketing-ops' }

consumes:
    - type: fluid-product
        name: marketing.gold.qualified_leads_for_partners

exposes:
    - location:
            type: sftp
            connection: secret:partner-xyz-sftp-creds
            format: { type: 'csv', properties: { header: true } }
            properties:
                host: 'sftp.partnerxyz.com'
                path: '/uploads/'
                filename: 'acme_leads_{{ execution_date }}.csv'
        contract:
            schema: { columns: [{name: lead_id, type: STRING}, {name: company_name, type: STRING}] }

build:
    transformation:
        engine: sql
        properties: { query: "SELECT id as lead_id, company as company_name FROM source" }
    execution:
        trigger: { type: 'schedule', properties: { cron: '0 8 * * *' } }
        runtime: { type: 'gcp-cloud-run' }
    stateManagement: { backend: gcs, properties: { bucket: 'fluid-state-prod' } }
```

---

## 10. Product with Access Policies <a name="10-product-with-access-policies"></a>

> **Goal:** Define who can access trusted data and under what conditions.  
> **Concepts:** Access policies, privacy views, row-level security.

```yaml
# 10-with-access-policy.fluid.yml
fluidVersion: "1.0"
kind: DataProduct
metadata:
    dataProduct: customers.gold.trusted_customer_view
    owner: { team: 'customer-domain' }

consumes:
    - type: fluid-product
        name: customers.silver.trusted_customers

exposes:
    - location:
            type: bigquery
            properties: { project: 'acme-prod-dwh', dataset: 'gold', table: 'customer_view' }
        contract: # ... contract definition ...
        accessPolicy:
            visibility: internal
            grants:
                - principal: group:analytics@acme.com
                    permissions: [readData]
                    scope: { privacyView: treated }
                - principal: user:support.lead@acme.com
                    permissions: [readData]
                    scope:
                        privacyView: cleartext
                        columns: [customer_id, full_name, email]
                        rowFilter: "status = 'escalated'"

build: # ... build definition ...
```

---

## 🎉 **Congratulations!**

You’ve just explored the **core patterns of FLUID**.  
Use these examples as templates, inspiration, and a launchpad for your own data products!

---

> **💡 Pro Tip:**  
> Mix and match these patterns to create robust, secure, and scalable data pipelines with FLUID!

---

