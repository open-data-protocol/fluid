---
title: The Agentic-Native Layer
description: The four agent failure modes any data product spec must answer before LLMs can safely consume it — tested against each spec's own canonical example.
---

# 🤖 The Agentic-Native Layer

**"Agentic-native"** isn't a marketing label — it's a concrete set of failure modes that any data product spec must address before AI agents can safely consume it at production scale. This page maps those failure modes to spec features, **tests them against each spec's own canonical example file**, and is honest about where FLUID also falls short.

> ⚡ **As of [0.7.4](/fluid/releases/0.7.4), `agentPolicy` is enforced at runtime** — not just declared. When an `exposes[].mcp` block is present, the Fluid MCP gateway enforces `allowedModels` / `deniedModels` / `allowedUseCases` / `deniedUseCases` on every read and redacts PII/PHI values inline. The schema shape is unchanged from 0.7.1; 0.7.4's change is behavioral. See [What's New in 0.7.4](/fluid/releases/0.7.4) and the [MCP how-to](/fluid/how-to/mcp).

## Methodology

Each spec was evaluated against the **canonical example file its maintainers publish**, asking four questions an LLM agent must answer before consuming a data product. Each cell below records whether the spec gives a **deterministic** (✅), **partial** (⚠️), or **silent** (❌) answer.

| Spec | Example file used |
|---|---|
| Bitol ODCS v3.1 | [`full-example.odcs.yaml`](https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/examples/all/full-example.odcs.yaml) (seller/payments contract) |
| Bitol ODPS v1.0 | [`customer-data-product.odps.yaml`](https://github.com/bitol-io/open-data-product-standard/blob/main/docs/examples/customer-data-product.odps.yaml) |
| ODPS v4 | [`urbanpulse_final.yml`](https://github.com/Open-Data-Product-Initiative/v4.0/blob/main/source/examples/Refs/urbanpulse_final.yml) (UrbanPulse Events) |
| FLUID v0.7.3 | [Example 10 (Customers CDC)](/fluid/examples/#10-source-aligned-acquisition) |

## The four agent failure modes

These are the failures that get LLM-driven data products taken offline:

| # | Failure mode | What an agent must determine | Real consequence if undetermined |
|---|---|---|---|
| **F1** | **PII leakage** | Which columns are PII? With what masking strategy? | Agent surfaces customer emails / SSNs in answers → privacy incident |
| **F2** | **Disallowed use** | Am I permitted to use this data for *training*? *RAG*? *Credit scoring*? | Model trained on data with `training: deny` → contract breach, lawsuit |
| **F3** | **Metric hallucination** | What is "revenue"? "MRR"? "MAU"? Can I derive them? | Agent invents a SQL expression → wrong number reported to executive |
| **F4** | **Sovereignty violation** | Where is the data located? Am I (running in `us-east-1`) allowed to read EU-resident PII? | Cross-border PII transfer → GDPR fine |

## Results of the test

Verdict per spec per failure mode (✅ deterministic · ⚠️ partial · ❌ silent). Details in the prose below.

| Failure mode | ODCS | ODPS | v4 | **FLUID** |
|---|---|---|---|---|
| **F1** — PII leakage | ⚠️ tier, no strategy | ❌ | ❌ | ✅ `sensitivity` + `masking[]` |
| **F2** — Disallowed use | ❌ | ❌ | ⚠️ MCP tiers, no policy | ✅ `agentPolicy` controlled vocab |
| **F3** — Metric hallucination | ❌ | ❌ | ❌ | ✅ `semantics.metrics` |
| **F4** — Sovereignty violation | ❌ | ❌ | ⚠️ legal scope only | ✅ `sovereignty.enforcementMode` |

**What each verdict means:**

- **F1 — PII leakage.** ODCS gives a `classification: restricted` per column (a tier label), but no masking strategy — an agent has to guess between hash/tokenize/mask. ODPS is manifest-only; PII lives in the referenced ODCS. v4 delegates to `contract.contractURL`. FLUID's `column.sensitivity` (12-value enum) + `exposes[].policy.privacy.masking[].strategy` (`mask`/`hash`/`tokenize`/`encrypt`/`k_anonymity`) is machine-actionable.
- **F2 — Disallowed use.** No agent-policy fields in ODCS or ODPS. v4 has `pricingPlans` for MCP-agent tiers and an English-prose `license.scope.restrictions`, but no machine-readable use-case allow/deny list. FLUID's `agentPolicy.allowedUseCases` / `deniedUseCases` use the 12-value controlled vocabulary plus token caps and `allowedModels` / `deniedModels`.
- **F3 — Metric hallucination.** No spec other than FLUID defines metrics at the contract level. FLUID's `exposes[].semantics.metrics` with `type: simple` / `derived` / `ratio` and explicit `expr` gives the agent a verbatim definition to use instead of inventing SQL.
- **F4 — Sovereignty violation.** v4's `license.scope.geographicalArea: [EU, US]` indicates *where the data may be used* (legal scope), not *where it may be read from* — agents can over- or under-block. FLUID's `sovereignty.jurisdiction` / `allowedRegions` / `deniedRegions` / `enforcementMode` blocks cross-border bindings at apply time.

## Where FLUID is still maturing — roadmap & honest gaps

The four ✅s above cover the failure modes that matter most for safe agent consumption. Remaining items are operational/tracked-on-roadmap:

- 🛣️ **MCP binding** — `exposes[].binding.mcp` is on the FLUID roadmap. Once landed, FLUID matches ODPS v4's `dataAccess.interface: MCP` for direct LLM tool calls.
- 🛣️ **dbt MetricFlow compatibility** — FLUID's `semantics` block already aligns with the [**OSI (Open Semantic Interchange)**](https://open-semantic-interchange.org/) v1.0 standard (Apache 2.0, Jan 2026); MetricFlow round-trip compatibility is on the roadmap.
- ⚠️ **`purposeLimitation` is free text** — human-readable but not deterministically enforceable without an NLU layer. Shared limitation with every spec that supports purpose clauses.
- ⚠️ **Controlled vocab is mechanism-flavored** — `allowedUseCases: [inference, qa, rag, …]` describes *how* an AI uses the data, not *why*. Business use cases (`credit-scoring`, `marketing-targeting`) live in `purposeLimitation`. A vocabulary extension is under discussion.
- ⚠️ **Semantics is opt-in** — authors who skip the `semantics` block leave F3 (metric hallucination) open. The spec supports it; adoption is the gap.

## What broke when running the tests

Two concrete findings against the canonical examples:

- **F3 — hallucination, against the ODCS example.** Asked *"what was last month's daily transaction volume?"* against the seller/payments contract, a naive LLM agent writes `SELECT txn_ref_dt, COUNT(*) FROM tbl_1 WHERE txn_ref_dt >= DATE_SUB(CURRENT_DATE, 30)`. The contract has no metric defining "transaction volume" and no row-grain documentation, so the SQL is plausible-but-ungrounded. A FLUID `semantics.measures: [{name: transaction_count, agg: count_distinct, expr: txn_id}]` block would have produced a verifiable expression.
- **F4 — sovereignty, against the ODPS v4 example.** UrbanPulse Events declares `license.scope.geographicalArea: [EU, US]`. An agent running in `us-east-1` cannot determine whether that grants *runtime access* or merely *consumer rights of use* — the clause governs the latter. FLUID's `sovereignty.enforcementMode: strict` removes the ambiguity at apply time.

## Complementary protocols worth knowing about

None of these specs replace each other — they live at different layers. Production agentic data products typically combine several:

| Protocol | Layer | What it does | Relationship to FLUID |
|---|---|---|---|
| **[MCP](https://modelcontextprotocol.io/)** (Model Context Protocol) | Access | How an LLM tool calls a data product (JSON-RPC over stdio/SSE). Anthropic-led, broad adoption. | `binding.mcp` on the **FLUID roadmap**. ODPS v4 has it today via `dataAccess.interface: MCP`. |
| **[OSI](https://open-semantic-interchange.org/)** (Open Semantic Interchange) v1.0 | Semantic | Vendor-neutral semantic-layer spec (Snowflake + Databricks + AtScale + Qlik …), Apache 2.0, Jan 2026. | **FLUID `semantics` aligns with OSI** — interoperable with any OSI-compliant BI/AI tool. |
| **[dbt MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow)** / **Snowflake Semantic Views** | Semantic | Engine-specific metric definitions. | FLUID `semantics` is shape-compatible; **MetricFlow round-trip on roadmap**. |
| **[OpenLineage](https://openlineage.io/)** | Lineage events | Runtime lineage events from any tool. | FLUID's `acquisitionPattern.lineage.emit: true` produces OpenLineage events per batch. |
| **[OPA / Rego](https://www.openpolicyagent.org/)** | Policy enforcement | Policy-as-code engine. | An OPA sidecar evaluates FLUID's `accessPolicy` JSONPath selectors at request time. |
| **[Cosign](https://docs.sigstore.dev/cosign/overview/) / [SLSA](https://slsa.dev/)** | Supply chain | Container image signing + provenance. | Required by FLUID's `acquisition.<engine>.image_signature`. |

## Practical conclusion

**FLUID v0.7.3 is the only one of the four specs that gives an LLM deterministic answers to all four agent failure modes today.** That isn't marketing — it's what the test above shows when run against each spec's own canonical example. As of [0.7.4](/fluid/releases/0.7.4), those `agentPolicy` answers are no longer advisory: they are enforced at runtime at the Fluid MCP gateway.

FLUID's scope is deliberately the **operational + governance layer** — contract, build, orchestration, agent policy, sovereignty, semantics, DQ. Commercial layers (pricing, payment, multi-language marketplace) are out of scope on purpose; pair FLUID with ODPS v4 when you need them:

```
  FLUID  (author + agent governance + semantics + sovereignty + multi-layer DQ)
    │
    ├── forge-cli → Bitol ODPS + ODCS    (catalog + data-mesh interop)
    │
    └── ODPS v4 wrapper (optional)        (commercial publishing + MCP access)
                  │
                  └── MCP server          (the LLM-side handle)
```

> **PRs welcome** to add a `binding.mcp` block or extend the `allowedUseCases` vocabulary. The agentic-native layer is still being built in the open — and FLUID is currently leading on the governance dimensions that matter most.

---

→ See [**how FLUID compares to ODCS, Bitol ODPS, and ODPS v4**](/fluid/concepts/comparisons) for the full capability matrix.
