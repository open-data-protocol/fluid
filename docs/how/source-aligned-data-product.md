# Example: Source-Aligned Ingestion from On-Prem Oracle to Cloud

This example showcases a core FLUID ecosystem pattern: **Source-Aligned Data Product**. The objective is to create a reliable, governable, and secure mirror of a source system in the cloud’s bronze layer—without altering the data’s meaning.

---

## Scenario

- **Source:** On-premise Oracle database containing critical customer information.
- **Ingestion Framework:** Cloud-native Spark job running on a GCP DataProc cluster.
- **Goal:** Daily batch ingestion of new or updated customer records, enforcing strict quality and privacy rules in-flight, and exposing a trusted, partitioned Parquet dataset in GCS for the customer domain.

---

## The `fluid.yml` Manifest

A single `customer.bronze.raw_oracle_customers.fluid.yml` file drives the entire process—no extra configuration or code required.

```yaml
fluidVersion: "1.0"
kind: DataProduct

# 1. METADATA: Identity of this data product.
metadata:
    dataProduct: customer.bronze.raw_oracle_customers
    owner: { team: 'data-platform-ingestion' }
    description: >
        A daily, incremental ingestion of the core customer table from the on-premise Oracle ERP.
        This product provides the raw, trusted source for all downstream customer data products.
    classification: restricted # Contains PII, access is highly controlled.
    tags: { layer: 'bronze', domain: 'customer', source: 'oracle' }
    version: "1.0.0"

# 2. CONSUMES: Source system definition.
consumes:
    - type: oracle-db
        connection: secret:onprem-oracle-erp-readonly-creds
        properties:
            query: |
                SELECT
                    CUST_ID,
                    F_NAME,
                    L_NAME,
                    CUST_EMAIL_ADDR,
                    PHONE_INTL,
                    COUNTRY_CODE,
                    CREATED_TS,
                    LAST_UPDATED_TS
                FROM ERP.CUSTOMERS
                WHERE LAST_UPDATED_TS > '{{ watermark.last_updated_ts }}'

# 3. EXPOSES: Output interface.
exposes:
    - location:
            type: gcs
            connection: secret:gcp-prod-sa-key
            format: { type: 'parquet' }
            properties:
                bucket: 'prod-customer-landing-zone'
                path: 'raw_oracle_customers/'
                partitionBy: ['load_date']

        # 4. CONTRACT: Governance and enforcement.
        contract:
            schema:
                columns:
                    - { name: 'customer_id', type: 'INT64', nullable: false }
                    - { name: 'first_name_pii', type: 'STRING' }
                    - { name: 'last_name_pii', type: 'STRING' }
                    - { name: 'email_hash', type: 'STRING' }
                    - { name: 'phone_token', type: 'STRING' }
                    - { name: 'country_code', type: 'STRING' }
                    - { name: 'created_ts', type: 'TIMESTAMP' }
                    - { name: 'last_updated_ts', type: 'TIMESTAMP' }
                    - { name: 'load_date', type: 'DATE' }

            quality:
                - rule: not_null
                    columns: [customer_id]
                    onFailure: { action: 'reject_row' }
                - rule: regex_match
                    columns: [CUST_EMAIL_ADDR]
                    pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    onFailure: { action: 'quarantine_row', location: 'gs://prod-customer-quarantine/invalid_emails/' }

            privacy:
                - classification: PII
                    columns: [CUST_EMAIL_ADDR]
                    treatment:
                        type: hashing
                        properties: { algorithm: 'SHA256' }
                        newColumn: 'email_hash'
                - classification: SPI
                    columns: [PHONE_INTL]
                    treatment:
                        type: tokenization
                        properties:
                            vault: 'gcp-dlp-service'
                            keyId: 'customer-phone-key'
                        newColumn: 'phone_token'

# 5. BUILD: Implementation logic.
build:
    transformation:
        engine: spark-sql
        properties:
            query: |
                SELECT
                    CUST_ID AS customer_id,
                    F_NAME AS first_name_pii,
                    L_NAME AS last_name_pii,
                    CUST_EMAIL_ADDR,
                    PHONE_INTL,
                    COUNTRY_CODE as country_code,
                    CREATED_TS as created_ts,
                    LAST_UPDATED_TS as last_updated_ts,
                    current_date() as load_date
                FROM source

    execution:
        trigger:
            type: schedule
            properties: { cron: '0 3 * * *', timezone: 'UTC' }
        runtime:
            type: gcp-dataproc
            connection: secret:gcp-prod-sa-key
            properties:
                clusterName: 'ephemeral-ingestion-cluster-small'
                region: 'us-central1'
                mainJarFileUri: 'gs://prod-dataproc-jars/fluid-ingestion-framework.jar'
                mainClass: 'com.mycorp.fluid.ingestion.JdbcToGcsRunner'
                args:
                    - '--fluid-file=gs://my-fluid-repo/customer.bronze.raw_oracle_customers.fluid.yml'

    stateManagement:
        backend: gcs
        properties:
            bucket: 'fluid-state-prod'
            path: 'customer.bronze.raw_oracle_customers.json'
            watermarkKey: 'last_updated_ts'
```

---

> **Key Takeaways:**
> - **Declarative:** All ingestion, quality, privacy, and execution logic is defined in a single YAML file.
> - **Governed:** Data contracts and privacy rules are enforced in-flight.
> - **Cloud-Native:** Runs on ephemeral, scalable GCP DataProc clusters.
> - **Extensible:** Easily adapted for other sources, targets, or domains.

