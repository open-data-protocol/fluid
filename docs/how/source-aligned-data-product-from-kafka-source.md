# Example: Source-Aligned Ingestion from On-Prem Kafka to Cloud

This example showcases a powerful FLUID pattern: **Source-Aligned Data Product**. The objective is to mirror a source system in the cloud's bronze layer—reliably, securely, and with strong governance—without altering the data's meaning.

---

## Scenario

- **Source:** On-premises Kafka topic streaming raw payment events as JSON.
- **Ingestion Framework:** Cloud-native streaming job on GCP Dataflow.
- **Goal:** Continuously ingest, enforce quality/privacy, and expose trusted Parquet data in GCS for finance.

---

## The `fluid.yml` Manifest

A single `finance.bronze.raw_kafka_payments.fluid.yml` file drives the entire process—no extra code or config needed.

```yaml
fluidVersion: "1.0"
kind: DataProduct

# 1. METADATA: Identity & Catalog Registration
metadata:
    dataProduct: finance.bronze.raw_kafka_payments
    owner: { team: 'data-platform-ingestion' }
    description: >
        Continuous streaming ingestion of payment events from on-prem Kafka.
        Raw source for all real-time financial analysis.
    classification: restricted # Contains PII; access tightly controlled.
    tags: { layer: 'bronze', domain: 'finance', source: 'kafka', pattern: 'streaming' }
    version: "1.0.0"

# 2. CONSUMES: Source System Definition
consumes:
    - type: kafka
        connection: secret:onprem-kafka-cluster-creds
        format: { type: 'json' }
        properties:
            topic: 'prod.financial.payments'
            consumerGroup: 'fluid-gcs-sink-v1'
            # Optional: startingOffsets: 'earliest'

# 3. EXPOSES: Output Interface
exposes:
    - location:
            type: gcs
            connection: secret:gcp-prod-sa-key
            format: { type: 'parquet' }
            properties:
                bucket: 'prod-finance-landing-zone'
                path: 'raw_payments/'
                partitionBy: ['load_date']

        # 4. CONTRACT: Governance & Enforcement
        contract:
            schema:
                columns:
                    - { name: 'payment_id', type: 'STRING', nullable: false }
                    - { name: 'amount', type: 'NUMERIC' }
                    - { name: 'currency', type: 'STRING' }
                    - { name: 'payment_method_token', type: 'STRING' }
                    - { name: 'customer_email_hash', type: 'STRING' }
                    - { name: 'event_timestamp', type: 'TIMESTAMP' }
                    - { name: 'load_date', type: 'DATE' }
            quality:
                - rule: not_null
                    columns: [payment_id, amount]
                    onFailure: { action: 'reject_row' }
                - rule: in_set
                    columns: [currency]
                    set: ['USD', 'EUR', 'GBP', 'JPY']
                    onFailure: { action: 'quarantine_row', location: 'gs://prod-finance-quarantine/invalid_currency/' }
            privacy:
                - classification: PII
                    columns: [user_email]
                    treatment:
                        type: hashing
                        properties: { algorithm: 'SHA256' }
                        newColumn: 'customer_email_hash'
                - classification: SPI
                    columns: [payment_method_details]
                    treatment:
                        type: tokenization
                        properties:
                            vault: 'gcp-dlp-service'
                            keyId: 'payment-method-key'
                        newColumn: 'payment_method_token'

# 5. BUILD: Implementation Logic
build:
    transformation:
        engine: spark-sql
        properties:
            query: |
                SELECT
                    payload.paymentId as payment_id,
                    payload.transaction.amount as amount,
                    payload.transaction.currency as currency,
                    payload.user.email as user_email, -- For privacy engine
                    payload.user.paymentMethod as payment_method_details, -- For privacy engine
                    metadata.timestamp as event_timestamp,
                    current_date() as load_date
                FROM source

    execution:
        trigger:
            type: streaming
        runtime:
            type: gcp-dataflow
            connection: secret:gcp-prod-sa-key
            properties:
                jobName: 'fluid-kafka-to-gcs-payments'
                templateUri: 'gs://prod-dataflow-templates/streaming-ingestion-framework'
                parameters:
                    fluid-spec-uri: 'gs://my-fluid-repo/finance.bronze.raw_kafka_payments.fluid.yml'
                machineType: 'n1-standard-2'

    stateManagement:
        backend: bigquery_table
        properties:
            project: 'bq-prod-lakehouse'
            dataset: 'fluid_state'
            table: 'kafka_consumer_offsets'
```

---

## Key Features

- **Declarative:** All ingestion, quality, privacy, and output logic in one YAML.
- **Governed:** Enforces schema, quality, and privacy in-stream.
- **Cloud-Native:** Runs as a managed, scalable streaming job.
- **Auditable:** State and failures are tracked for compliance.

---

> **Tip:** Use this pattern to bootstrap trusted, analytics-ready data products from any source system—no custom code required!
