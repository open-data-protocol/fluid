# Advanced FLUID Examples: The Art of the Possible

Explore the full power and extensibility of the FLUID specification with these advanced, real-world use cases.

---

## 11. Multi-Tenant Data Product with Dynamic Policies

**Scenario:**  
Serve different data to different partners, enforcing dynamic, context-aware access policies at query time. The product is a secure, virtual view—no static access policy.

<details>
<summary><strong>YAML: <code>11-dynamic-policies.fluid.yml</code></strong></summary>

```yaml
fluidVersion: "1.0"
kind: VirtualDataProduct

metadata:
    dataProduct: partners.api.live_stock_check
    owner: { team: 'partner-engineering' }
    description: "Provides secure, real-time API access for partners to check stock levels for products they are authorized to see."

consumes:
    - type: fluid-product
        name: inventory.gold.live_stock_by_warehouse

exposes:
    - location: { type: 'virtual' }
        contract:
            schema:
                columns:
                    - { name: product_sku, type: STRING }
                    - { name: quantity_on_hand, type: INT64 }

dynamicPolicies:
    rules:
        - name: "Allow authorized partners based on JWT claim"
            condition: "agent.jwt.claims.can_access_stock_api == true"
            grant:
                permissions: [readData]
                scope:
                    rowFilter: "partner_id = '{{ agent.jwt.claims.partner_id }}'"

build:
    execution: { trigger: { type: 'manual' } }
    stateManagement: { backend: gcs, properties: { bucket: 'fluid-state-prod' } }
```
</details>

---

## 12. AI/ML Feature Store Integration

**Scenario:**  
Bridge data engineering and MLOps by delivering features directly to a feature store for ML models.

<details>
<summary><strong>YAML: <code>12-feature-store.fluid.yml</code></strong></summary>

```yaml
fluidVersion: "1.0"
kind: DataProduct

metadata:
    dataProduct: features.customer_churn_propensity
    owner: { team: 'ml-engineering' }
    description: "Computes and backfills customer features (RFM scores) and registers them in the central feature store."
    tags: { layer: 'feature', domain: 'mlops' }

consumes:
    - type: fluid-product
        name: customers.silver.trusted_customers

exposes:
    - location:
            type: redis
            connection: secret:ml-feature-store-redis-creds
            properties:
                keyPrefix: 'customer_churn_features'
        contract:
            schema:
                columns:
                    - { name: 'customer_id', type: 'STRING' }
                    - { name: 'recency_days', type: 'INT64' }
                    - { name: 'frequency_30d', type: 'INT64' }
                    - { name: 'last_updated_ts', type: 'TIMESTAMP' }

build:
    transformation:
        engine: python
        properties:
            entrypoint: 'feature_engineering/churn.py:calculate_rfm_features'
            requirements: 'feature_engineering/requirements.txt'
    execution:
        trigger: { type: 'schedule', properties: { cron: '0 1 * * *' } }
        runtime: { type: 'gcp-dataflow' }
    stateManagement: { backend: gcs, properties: { bucket: 'fluid-state-prod' } }
```
</details>

---

## 13. Active Metadata & Self-Monitoring Product

**Scenario:**  
Centralize observability by consuming execution logs from all FLUID products, powering dashboards, catalogs, and lineage graphs.

<details>
<summary><strong>YAML: <code>13-active-metadata.fluid.yml</code></strong></summary>

```yaml
fluidVersion: "1.0"
kind: DataProduct

metadata:
    dataProduct: platform.gold.observability_dashboard
    owner: { team: 'data-platform-governance' }
    description: "A structured data product built from the execution logs of all FLUID flows. Powers the data catalog, lineage graphs, and operational monitoring."
    tags: { layer: 'observability', domain: 'platform' }

consumes:
    - type: gcs
        connection: secret:gcp-prod-sa-key
        format: { type: 'jsonl' }
        properties:
            bucket: 'fluid-execution-logs-prod'
            path: 'runs/'

exposes:
    - location:
            type: bigquery
            properties: { project: 'acme-prod-dwh', dataset: 'observability', table: 'fluid_runs' }
        contract:
            schema:
                columns:
                    - { name: 'run_id', type: 'STRING' }
                    - { name: 'data_product_name', type: 'STRING' }
                    - { name: 'status', type: 'STRING' }
                    - { name: 'start_time', type: 'TIMESTAMP' }
                    - { name: 'duration_ms', type: 'INT64' }
                    - { name: 'rows_written', type: 'INT64' }
                    - { name: 'error_message', type: 'STRING' }
            quality:
                - rule: in_set
                    columns: [status]
                    set: ['SUCCESS', 'FAILED', 'QUARANTINED']
                    onFailure:
                        action: 'alert'
                        notifications:
                            - { channel: 'slack', target: '#platform-alerts' }

build:
    execution: { trigger: { type: 'streaming' }, runtime: { type: 'gcp-cloud-run' } }
    stateManagement: { backend: gcs, properties: { bucket: 'fluid-state-prod' } }
```
</details>

---

## 14. Semantic Data Product with Ontology Links

**Scenario:**  
Enrich a Gold-layer product with formal semantic meaning from an external ontology, making it machine-understandable for AI agents.

<details>
<summary><strong>YAML: <code>14-semantic-product.fluid.yml</code></strong></summary>

```yaml
fluidVersion: "1.0"
kind: DataProduct

metadata:
    dataProduct: products.gold.catalog_master
    owner: { team: 'product-domain' }
    description: "The master, unified view of the product catalog, enriched with semantic meaning."
    tags: { layer: 'gold', domain: 'product', semantics: 'true' }

consumes:
    - type: fluid-product
        name: products.silver.cleaned_catalog

exposes:
    - location:
            type: bigquery
            properties: { project: 'acme-prod-dwh', dataset: 'gold', table: 'product_catalog' }
        contract:
            schema:
                columns:
                    - { name: 'product_id', type: 'STRING' }
                    - { name: 'name', type: 'STRING' }
                    - { name: 'description', type: 'STRING' }
                    - { name: 'price', type: 'NUMERIC' }
            semantics:
                ontology: "https://schema.org/docs/schema_org_rdfa.html"
                classifications:
                    - column: product_id
                        term: "schema:sku"
                    - column: name
                        term: "schema:name"
                    - column: description
                        term: "schema:description"
                    - column: price
                        term: "schema:price"

build: # ... build definition ...
```
</details>

---

## 15. Ephemeral Product for a Chat-Agent Session

**Scenario:**  
Create a temporary, virtual data product for a single user conversation. Joins multiple sources on-the-fly with a strict 15-minute lifecycle.

<details>
<summary><strong>YAML: <code>15-ephemeral-product.fluid.yml</code></strong></summary>

```yaml
fluidVersion: "1.0"
kind: VirtualDataProduct

metadata:
    dataProduct: agent_session.temp.user_order_analysis_12345
    owner: { team: 'agentic-applications' }
    description: "Ephemeral data product for analyzing a user's order history during a chat session. TTL is 15 minutes."

consumes:
    - type: fluid-product
        name: sales.silver.clean_orders
        alias: orders
    - type: fluid-product
        name: customers.silver.trusted_customers
        alias: customers

exposes:
    - location: { type: 'virtual' }
        contract:
            schema:
                columns:
                    - { name: order_id, type: STRING }
                    - { name: order_total, type: NUMERIC }

build:
    transformation:
        engine: sql
        properties:
            query: |
                SELECT o.order_id, o.order_total
                FROM {{ consumes.orders }} o
                JOIN {{ consumes.customers }} c ON o.customer_id = c.customer_id
                WHERE c.email = '{{ agent.user_context.email }}'
                    AND o.order_date > '{{ agent.user_context.date_filter }}'
    execution:
        trigger: { type: 'manual' }
        lifecycle:
            ttl: '15m'
    stateManagement: { backend: gcs, properties: { bucket: 'fluid-state-prod' } }
```
</details>

---
