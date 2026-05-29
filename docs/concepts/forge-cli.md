# The Reference Compiler — forge-cli

A capability matrix shows what each spec *covers*. **[`forge-cli`](https://github.com/Agenticstiger/forge-cli)** is what turns a FLUID contract into deployed reality and Bitol-compatible outputs.

[![Repo](https://img.shields.io/badge/Agenticstiger%2Fforge--cli-FF6B35?logo=github&logoColor=white&style=for-the-badge)](https://github.com/Agenticstiger/forge-cli)
[![License Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-1E3A8A?style=for-the-badge)](https://github.com/Agenticstiger/forge-cli/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-forge--docs-A78BFA?style=for-the-badge&logo=readthedocs&logoColor=white)](https://agenticstiger.github.io/forge_docs/)

> **FLUID stands on its own.** A FLUID contract is complete and useful with no compiler at all — you can author, validate, and version it as the single source of truth. `forge-cli` is an **optional adapter**: reach for it once you want compiled Infrastructure-as-Code, generated orchestration DAGs, and catalog-interop outputs.

## What forge-cli does

`forge-cli` consumes a `.fluid.yml` and compiles it to:

- **Infrastructure-as-Code** — OpenTofu / Terraform for BigQuery, Snowflake, AWS, and GCP.
- **Airflow DAGs** (and Dagster / Prefect) generated from the contract's `orchestration` block.
- **Bitol ODPS + ODCS** — for catalog and data-mesh registry interop (DataHub, OpenMetadata, Datamesh Manager).

## Compile stages

It emits the following, stage by stage:

| Stage | Output |
|---|---|
| 🟢 **Bitol export** | `1 ODPS doc + N <contractId>.odcs.yaml` files — Bitol v1.0.0 as the default, center-stage ODPS. |
| 🟠 **Orchestration** | Native **Airflow / Dagster / Prefect** DAGs from the `orchestration` block. |
| 🟣 **Infrastructure** | **OpenTofu / Terraform** IaC for BigQuery / Snowflake / AWS / GCP. |
| 🔵 **Governance** | **IAM bindings** from `accessPolicy.grants[]` + **AI gateway** enforcement of `agentPolicy`. |
| 🔴 **Supply chain** | **Cosign-verified** connector images + **SLSA provenance** checks on ingest. |

> *"What Terraform did for infrastructure, FLUID Forge does for data products."* — [forge-docs](https://agenticstiger.github.io/forge_docs/)

## Learn more

- **Repository:** [github.com/Agenticstiger/forge-cli](https://github.com/Agenticstiger/forge-cli)
- **Documentation:** [agenticstiger.github.io/forge_docs](https://agenticstiger.github.io/forge_docs/)

---

## Where to go next

- **[FLUID vs ODCS / ODPS](/fluid/concepts/comparisons)** — where the Bitol export and ODPS v4 layers fit.
- **[What FLUID Is (and Is Not)](/fluid/concepts/)** — why FLUID delegates execution to FLUID-aware tools.
