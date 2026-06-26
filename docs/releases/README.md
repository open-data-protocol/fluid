# What's New

Release notes for the FLUID specification, newest first. Each entry links to the full page and the auto-generated schema diff.

| Version | Codename | Compatibility | Summary |
|---|---|---|---|
| **[0.7.5](/fluid/releases/0.7.5)** *(latest)* | Streaming Kafka → Iceberg Sink & Confluent Tableflow | ✅ Additive over 0.7.4 | Adds an opt-in Iceberg streaming sink on the `kafka-connect` acquisition pattern (`iceberg_sink_enabled`, `streamingSink`, `sink_topics`, `iceberg_catalog_overrides`) and the `confluent` Cloud Tableflow binding platform (`environment_id` / `kafka_cluster_id` / `confluent_role_arn`). |
| **[0.7.4](/fluid/releases/0.7.4)** | Runtime agentPolicy Enforcement at the MCP Gateway | ✅ Additive over 0.7.3 | Makes an expose agent-consumable over MCP and turns `policy.agentPolicy` into a gate the MCP output-port gateway enforces on every read. Adds the optional `exposes[].mcp` block, the `postgres` binding platform, and the `postgres_table` / `athena_table` / `glue_table` formats. |
| **[0.7.3](/fluid/releases/0.7.3)** | Source-Aligned Acquisition | ✅ Additive over 0.7.2 | Ingestion becomes a first-class FLUID concept: the `acquisition` build pattern, six ingestion engines, delivery guarantees + DLQ, schema-evolution policy, supply-chain image signing, and a top-level `retention` block. |
| **[0.7.2](/fluid/releases/0.7.2)** | Semantic Truth Engine | ✅ Additive over 0.7.1 | A per-expose `semantics` block (entities, measures, dimensions, metrics) gives agents and BI tools a verbatim metric definition, plus `binding.icebergConfig` for Iceberg table specifics. |
| **[0.7.1](/fluid/releases/0.7.1)** | Agentic Governance + Provider-First Orchestration | ✅ Additive over 0.5.7 | `agentPolicy`, `sovereignty`, root-level `accessPolicy`, and provider-first orchestration tasks. |

---

## Reading the compatibility column

The 0.7.1 → 0.7.5 line is strictly **additive**: bump `fluidVersion` and every prior contract still validates.

**0.7.5 continues that streak.** It only adds optional fields, enum values, and a wider `engine` shape, so every valid 0.7.4 contract validates as 0.7.5 unchanged. See [What's New in 0.7.5](/fluid/releases/0.7.5#backward-compatibility-fully-additive) for the details.

For the field-by-field machine diff of every version, see the [**Schema Changelog**](/fluid/schema/changelog).
