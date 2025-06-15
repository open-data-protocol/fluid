# Integrating dbt and Airflow with FLUID: A Practical Guide

This guide presents a hands-on approach to integrating the [FLUID specification](https://github.com/open-data-protocol/fluid/blob/main/specification.md) with core data stack tools like **dbt** and **Airflow**. It explains how FLUID bridges the gap between these tools, clarifies their responsibilities, and demonstrates how to orchestrate robust, contract-aware data pipelines.

---

## The Challenge: Disconnected Data Planes

Modern data engineering often means juggling two worlds:

- **dbt World**: SQL transformations, data contracts in `schema.yml`, and sources in `sources.yml`.
- **Airflow World**: Python DAGs orchestrate ingestion and dbt runs, but lack native awareness of dbt’s contracts or lineage.

**Problems:**

- **Brittle Glue Code**: Connections between ingestion and transformation are implicit and fragile (e.g., hardcoded table names).
- **No End-to-End Lineage**: Airflow only sees task dependencies, not the full data lineage inside dbt.
- **Contract-Unaware Orchestration**: Airflow can’t detect if an upstream change will break a dbt model.

---

## The FLUID Solution

**FLUID** introduces a unified, declarative manifest (`.fluid.yml`) that all tools can understand. This eliminates glue code and enables contract-aware orchestration.

---

## Clear Division of Responsibilities

| Component | Responsibilities |
|-----------|------------------|
| **FLUID** | - Defines end-to-end data product lifecycle<br>- Specifies ingestion, exposure, access policies<br>- Declares orchestration and transformation engines |
| **dbt**   | - Owns SQL transformation logic<br>- Maintains transformation contracts (`schema.yml`) |
| **Airflow** | - Acts as runtime engine<br>- Reads `.fluid.yml` to generate DAGs<br>- Translates FLUID build blocks into Airflow tasks |

> **FLUID orchestrates the orchestrator**—providing Airflow with data-awareness it lacks natively.

---

## Building a FLUID-Aware Ecosystem

- **FLUID-Aware Orchestrators**: Airflow can read `.fluid.yml` files and generate DAGs dynamically.
- **FLUID-Aware dbt (Future)**: dbt could resolve sources from FLUID products, enabling seamless dependency management.

*This guide focuses on Airflow integration, which is possible today without modifying dbt-core.*

---

## Example: Orchestrating dbt with Airflow via FLUID

### 1. Project Structure

Organize by data domain. FLUID files live with the dbt project they orchestrate.

```
/
├── data-products/
│   └── customers/
│       ├── bronze_raw_customers/
│       │   └── product.fluid.yml       # Ingestion definition
│       └── silver_stg_customers/
│           ├── product.fluid.yml       # dbt transformation definition
│           └── dbt_project/
│               ├── dbt_project.yml
│               └── models/
│                   └── ...
└── airflow/
    └── dags/
        └── fluid_dag_generator.py      # DAG factory for FLUID files
```

---

### 2. Sample FLUID File

**`silver_stg_customers/product.fluid.yml`**:

```yaml
fluidVersion: 1.0
kind: DataProduct

metadata:
  dataProduct: customers.silver.stg_customers
  owner: { team: 'analytics-engineering' }
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

build:
  transformation:
    engine: dbt
    properties:
      projectDir: './dbt_project/'
      command: 'run'
      models:
        - 'stg_customers'
  execution:
    trigger: { type: 'schedule', properties: { cron: '0 5 * * *' } }
    runtime:
      type: airflow
      properties:
        dag_id: 'fluid_customer_silver_build'
        pool: 'dbt_runs'
        tags: ['fluid', 'dbt', 'customers']
    dependencies:
      dataProducts: ['customers.bronze.raw_customers']
  stateManagement:
    backend: gcs
    properties: { bucket: 'fluid-state-prod', path: 'customers.silver.stg_customers.json' }
```

---

### 3. Airflow DAG Factory

**`fluid_dag_generator.py`** scans for `.fluid.yml` files and generates DAGs for those specifying Airflow as the runtime.

```python
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
import yaml
import glob

FLUID_PRODUCT_PATH = '/usr/local/airflow/data-products'

def create_dag_from_fluid_spec(spec_file_path):
    with open(spec_file_path, 'r') as f:
        spec = yaml.safe_load(f)

    if spec.get('build', {}).get('execution', {}).get('runtime', {}).get('type') != 'airflow':
        return None

    dag_id = spec['build']['execution']['runtime']['properties']['dag_id']
    schedule = spec['build']['execution']['trigger']['properties']['cron']

    @dag(dag_id=dag_id, schedule=schedule, catchup=False, tags=['fluid-generated'])
    def dynamic_dag():
        dependency_sensors = []
        for dep in spec['build']['execution']['dependencies']['dataProducts']:
            upstream_dag_id = f"fluid_{dep.replace('.', '_')}"
            dependency_sensors.append(
                ExternalTaskSensor(task_id=f"wait_for_{dep.replace('.', '_')}", external_dag_id=upstream_dag_id)
            )

        if spec['build']['transformation']['engine'] == 'dbt':
            dbt_props = spec['build']['transformation']['properties']
            project_dir = dbt_props['projectDir']
            models = ' '.join(dbt_props['models'])
            dbt_task = BashOperator(
                task_id='run_dbt_transformation',
                bash_command=f"dbt {dbt_props['command']} --models {models} --project-dir {project_dir}"
            )
            if dependency_sensors:
                dependency_sensors >> dbt_task

    return dynamic_dag()

for spec_file in glob.glob(f"{FLUID_PRODUCT_PATH}/**/*.fluid.yml", recursive=True):
    generated_dag = create_dag_from_fluid_spec(spec_file)
    if generated_dag:
        globals()[generated_dag.dag_id] = generated_dag
```

---

## Why This Matters

- **Decoupling**: Ingestion and analytics teams work independently, each owning their FLUID files and dbt projects.
- **End-to-End Lineage**: FLUID-aware tools can generate complete lineage graphs (e.g., GCS Bucket → bronze → silver).
- **Contract-Aware Orchestration**: Airflow DAGs know their dependencies. CI/CD can validate contracts before running expensive jobs.

---

## Conclusion

By adopting FLUID, you move from implicit, brittle glue code to explicit, version-controlled, contract-aware data products. This is the foundation for a scalable, trustworthy data platform.

