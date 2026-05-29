# FAQ & Critical Review

*The black-hat perspective.* A specification is only as strong as its ability to withstand scrutiny. Here we address the toughest questions head-on.

## Isn't this just more YAML complexity?

FLUID *eliminates* complexity by unifying scattered configurations. Instead of separate dbt models, Airflow DAGs, data-quality scripts, and access policies, you get one declarative file. Fewer moving parts means less complexity, not more.

## Does FLUID replace my existing tools?

No. FLUID makes your tools work better together. dbt, Airflow, Snowflake, and others become "FLUID-aware" by reading the `.fluid.yml` specification to auto-configure themselves. FLUID is the shared language, not a replacement platform.

## How do I start using FLUID today?

Start small:

1. Pick one critical data pipeline.
2. Write a `.fluid.yml` file describing it — see the [Quickstart](/fluid/guide/quickstart) and [FLUID by Example](/fluid/examples/).
3. Use FLUID-compliant tools, or build adapters for your existing stack.
4. Gradually expand to more data products.

## What about complex transformations and custom logic?

FLUID supports multiple build patterns:

- **`hybrid-reference`** — for dbt-style transformations.
- **`embedded-logic`** — for custom SQL / Python code.
- **`multi-stage`** — for complex multi-step orchestration.
- **`acquisition`** — for source-aligned ingestion from external systems.

The `lineage` block maintains full traceability even with custom code.

## How does this help with AI agents and the "agentic era"?

AI agents need **contracts**, not chaos. FLUID provides:

- **Discoverable data** — agents can find the right data products.
- **Trustworthy contracts** — schema, quality, and freshness guarantees.
- **Secure access** — policy-driven permissions for autonomous systems.
- **Rich context** — business semantics and lineage for better decisions.
- **AI governance** — model whitelisting, usage quotas, and audit trails via `agentPolicy`, enforced at runtime at the MCP gateway.
- **Sovereignty controls** — automated jurisdictional compliance.
- **Fine-grained permissions** — root-level access policies with automated IAM.

> Want to go deeper on where FLUID is honest about its gaps? See the [Agentic-Native Layer](/fluid/concepts/agentic-native), which tests each spec against its own canonical example.
