# 📘 FLUID Build Cookbook

*A Practical Guide to Build Patterns for FLUID v0.3.0*

---

## 🔑 Introduction

The **Build Block** is the *engine room* of the FLUID specification.

* It translates the **“what”** of the contract into the **“how”** of execution.
* It enables teams to choose the right level of abstraction for their data product.
* Different teams, tools, and workloads benefit from different patterns.

This guide explores **four canonical Build Patterns**, complete with real-world examples for tools like **dbt, BigQuery, Spark, Airflow, Data Vault 2.0, and Iceberg**.

---

## 🟨 Pattern 1: Declarative Pattern

**Best for:**

* Clear, governable products.
* Teams who want **auto-generated SQL** or transformations.
* Common analytics & segmentation pipelines.

💡 *Think of this as the “golden path” — high-level configuration, no hand-written SQL.*

---

### Example: High-Value Customers in BigQuery

```yaml
fluidVersion: "0.3.0"
kind: DataProduct
id: marketing.high_value_customers:1.0.0
name: "High-Value Active Customers"
description: "Active customers with high spend over the last 90 days."
domain: "Marketing"

metadata:
  owner:
    team: "Marketing Analytics"
    email: "marketing@company.com"
  layer: "Gold"

consumes:
  - id: profiles
    ref: "crm.clean_customers:1.2.0"
  - id: transactions
    ref: "finance.transactions_daily:2.1.0"

exposes:
  - id: bq_customer_view
    type: bigquery_table
    location:
      format: "bigquery"
      properties:
        project: "dwh-prod"
        dataset: "marketing_products"
        table: "high_value_customers"
    schema:
      - name: customer_id
        type: STRING
      - name: email_hash
        type: STRING
      - name: total_spend_90d
        type: NUMERIC

build:
  transformation:
    pattern: declarative
    engine: sql-generator
    properties:
      from: profiles
      joins:
        - type: left
          left: profiles
          right: transactions
          on: "profiles.customer_id = transactions.customer_id"
      filters:
        - "profiles.account_status = 'active'"
        - "transactions.transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)"
      select:
        - name: customer_id
          source: profiles.customer_id
        - name: email_hash
          expression: "SHA256(profiles.email)"
        - name: total_spend_90d
          expression: "SUM(transactions.amount)"
  execution:
    trigger:
      type: schedule
      cron: "0 4 * * *"
    runtime:
      platform: airflow
```

---

**Pros ✅**

* Human-readable, compact, self-documenting.
* Auto-enforceable governance.
* Easy for business analysts.

**Cons ⚠️**

* Limited flexibility for very complex logic.
* Dependent on the FLUID runtime’s SQL generator.

---

## 🟦 Pattern 2: Hybrid Reference Pattern

**Best for:**

* Reusing **existing codebases** (dbt, SQL, Spark scripts).
* Complex, business-critical logic that can’t be abstracted away.
* Enterprise governance without re-engineering.

🚀 *This is the “workhorse” for enterprises.*

---

### Example: Quarterly Financial Report with dbt + Snowflake

```yaml
fluidVersion: "0.3.0"
kind: DataProduct
id: finance.quarterly_reporting:3.0.0
name: "Quarterly Financial Report"
description: "The official, audited quarterly financial report for leadership."
domain: "Finance"

metadata:
  owner:
    team: "Financial Reporting"
    email: "fin-reporting@company.com"
  layer: "Platinum"

consumes:
  - id: ledger
    ref: "finance.general_ledger:1.5.0"
  - id: salaries
    ref: "hr.employee_salaries:1.1.0"

exposes:
  - id: quarterly_report
    type: snowflake_table
    location:
      format: "table"
      properties:
        database: "FINANCE_PROD"
        schema: "REPORTS"
        table: "QUARTERLY_FINANCIALS_V3"
    schema:
      - name: account_id
        type: STRING
      - name: amount
        type: NUMERIC

build:
  transformation:
    pattern: hybrid-reference
    engine: dbt
    properties:
      model: "+quarterly_financial_report"
      vars:
        reporting_quarter_end_date: "{{ ds }}"
  execution:
    trigger:
      type: schedule
      cron: "0 1 1 1,4,7,10 *"
    runtime:
      platform: airflow
```

---

**Pros ✅**

* Leverages existing assets (dbt, scripts).
* Maximum flexibility.
* Natural fit for complex, multi-step pipelines.

**Cons ⚠️**

* Logic not fully visible in the FLUID file.
* Governance depends on external repo practices.

---

## 🟩 Pattern 3: Embedded Logic Pattern

**Best for:**

* **Portable, self-contained** data products.
* Real-time or streaming transformations.
* Lightweight deployments (single-file).

⚡ *Great for “deploy once, run anywhere” products.*

---

### Example: Spark Structured Streaming (5G Latency Alerts)

```yaml
fluidVersion: "0.3.0"
kind: DataProduct
id: network.high_latency_alerts:1.0.0
name: "High Latency Alerts"
description: "Real-time stream of 5G events with latency > 200ms."
domain: "Network"

metadata:
  owner:
    team: "Core Network SRE"
  layer: "Bronze"

consumes:
  - id: raw
    ref: "kafka.prod.5g.raw_telemetry"

exposes:
  - id: latency_alerts
    type: kafka_topic
    location:
      format: "kafka"
      properties:
        topic: "prod.alerts.high_latency"
    schema:
      - name: cell_tower_id
        type: STRING
      - name: latency_ms
        type: INT
      - name: event_timestamp
        type: TIMESTAMP

build:
  transformation:
    pattern: embedded-logic
    engine: spark-sql
    properties:
      sql: |
        SELECT
          cell_tower_id,
          latency_ms,
          event_timestamp
        FROM {{ consumes.raw }}
        WHERE latency_ms > 200
  execution:
    trigger:
      type: event
      eventType: "stream"
    runtime:
      platform: databricks
```

---

**Pros ✅**

* Entire product (contract + logic) is self-contained.
* Easy to port between environments.
* Transparent for auditors.

**Cons ⚠️**

* Harder to reuse across multiple products.
* Can get verbose for big SQL scripts.

---

## 🟥 Pattern 4: Logical Mapping Pattern

**Best for:**

* **Design-first workflows** (business analysts, data architects).
* Feeding an **AI code generator**.
* Data Vault 2.0 and ontology-driven designs.

🤖 *This is the “AI-ready” pattern.*

---

### Example: Data Vault 2.0 Model with Iceberg

```yaml
fluidVersion: "0.3.0"
kind: DataProduct
id: supply_chain.dv2_orders:1.0.0
name: "Orders Data Vault 2.0 Model"
description: "Data Vault 2.0 model for Orders domain, stored in Iceberg."
domain: "SupplyChain"

metadata:
  owner:
    team: "Supply Chain Engineering"
    email: "scm-eng@company.com"
  layer: "Silver"

consumes:
  - id: orders_raw
    ref: "erp.orders_raw:1.0.0"
  - id: customers_raw
    ref: "crm.customers_raw:2.0.0"

exposes:
  - id: dv2_orders
    type: iceberg_table
    location:
      format: "iceberg"
      properties:
        bucket: "s3://datalake/supply_chain/orders_dv2"
    schema:
      - name: hub_order_id
        type: STRING
      - name: sat_order_details
        type: JSON
      - name: link_customer
        type: STRING

build:
  transformation:
    pattern: logical-mapping
    engine: sql-generator
    properties:
      logical_plan:
        sources:
          - orders_raw
          - customers_raw
        steps:
          - type: project
            source: orders_raw
            output: hub_orders
            columns:
              - name: hub_order_id
                source: order_id
          - type: join
            left: orders_raw
            right: customers_raw
            on: "orders_raw.customer_id = customers_raw.customer_id"
            output: link_orders_customers
          - type: project
            source: link_orders_customers
            columns:
              - name: link_customer
                source: customers_raw.customer_id
  execution:
    trigger:
      type: schedule
      cron: "0 2 * * *"
    runtime:
      platform: airflow
```

---

**Pros ✅**

* Business-readable, even without SQL skills.
* Perfect for AI or compiler-driven transformation.
* Encourages consistency and reusability.

**Cons ⚠️**

* Needs a smart FLUID runtime to compile into SQL/Spark.
* Less direct for engineers who prefer explicit SQL.

---

## 📊 Pattern Comparison

| Pattern          | Best For                          | Transparency | Flexibility | AI/Automation Ready |
| ---------------- | --------------------------------- | ------------ | ----------- | ------------------- |
| Declarative      | Simplicity, governance            | High         | Medium      | Medium              |
| Hybrid Reference | Complex, existing pipelines       | Medium       | High        | Low                 |
| Embedded Logic   | Portable, self-contained products | High         | Medium      | Medium              |
| Logical Mapping  | Design-first, AI-generated code   | High         | Medium      | High                |

---

## 🚀 Conclusion

The **FLUID Build Block** is intentionally flexible:

* Declarative → simplicity.
* Hybrid → pragmatism.
* Embedded → portability.
* Logical Mapping → AI-native future.

By picking the right **pattern for the job**, enterprises can future-proof their **data fabric** and scale both governance and innovation.