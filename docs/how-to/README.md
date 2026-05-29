# How-to Guides

Task-focused walkthroughs that show FLUID working alongside the tools you already run — ingestion sources, transformation engines, orchestrators, and AI agents. Each guide is self-contained; start with the one closest to your problem.

For a step-by-step tour of the schema itself, see [**Examples**](/fluid/examples/). For field-level reference, see the [**Cheatsheet**](/fluid/schema/cheatsheet).

| Guide | What it covers |
|---|---|
| [Source-aligned data product](/fluid/how-to/source-aligned-data-product) | Mirror an on-prem Oracle database into a governed cloud bronze layer with in-flight quality and privacy rules. |
| [Source-aligned from Kafka](/fluid/how-to/source-aligned-kafka) | Continuously ingest a Kafka topic into trusted Parquet, enforcing schema, quality, and PII treatment in-stream. |
| [dbt integration](/fluid/how-to/dbt) | Orchestrate dbt as a transformation engine and inherit its model contracts into FLUID. |
| [Airflow integration](/fluid/how-to/airflow) | Generate contract-aware Airflow DAGs from `.fluid.yml` files, with no glue code. |
| [Agentic access with MCP](/fluid/how-to/mcp) | Serve governable, auditable data to AI agents — including the 0.7.4 `exposes[].mcp` gateway path. |
| [Data Vault 2.0](/fluid/how-to/datavault) | Model hubs and satellites with dbt + FLUID, letting the orchestrator build the dependency DAG. |
| [Build patterns](/fluid/how-to/build-patterns) | Tour of the canonical build-pattern styles (declarative, hybrid-reference, embedded, logical-mapping). |
| [Advanced examples](/fluid/how-to/advanced) | The art of the possible — multi-tenant policies, feature stores, ephemeral agent products, and more. |
