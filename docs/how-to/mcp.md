# Unlocking Governable AI: Agentic Data Access with MCP & FLUID

> ⭐ **As of schema `0.7.4`, the recommended path is the `exposes[].mcp` block.** Add `mcp.sampling` / `mcp.classification` to an output port to opt it into the **Fluid MCP gateway**, where `policy.agentPolicy` (allowed/denied models and use cases) is enforced at runtime on every read and column-level `sensitivity: pii` / `phi` redacts values. See the [**0.7.4 release notes**](/fluid/releases/0.7.4) for the full reference and [**Examples → Agent-consumable output port (MCP)**](/fluid/examples/#_11-agent-consumable-output-port-mcp) for a complete, valid contract.
>
> The walkthrough below explains the *conceptual* request/authorization flow that underpins this gateway. It uses an earlier illustrative manifest shape; treat the YAML as a narrative aid, not a `0.7.4` template.

**Imagine this:**
A sales executive simply asks their AI assistant:
> "Show me our top 5 highest-value customers in Germany who have purchased in the last 90 days."

**What happens next?**
With MCP (Machine-Consumable Protocol) and FLUID, this isn't just possible—it's secure, governable, and enterprise-ready.

---

## Why MCP + FLUID?
- **MCP**: Standardizes how AI agents request and access data—securely, with full context and auditability.
- **FLUID**: Defines data products, access policies, and privacy controls—making sure the right data is delivered to the right agent, every time.

Together, they enable **agentic data access**: AI agents can act on behalf of users, but always within strict, transparent guardrails.

---

## The Data Product: `customers.gold.enriched_customers`

A data engineering team publishes a FLUID data product:

```yaml
fluidVersion: 1.0
kind: DataProduct
metadata:
    dataProduct: customers.gold.enriched_customers
    owner: { team: 'sales-analytics' }
exposes:
    location:
        type: bigquery
        properties:
            project: 'bq-prod-lakehouse'
            dataset: 'gold'
            table: 'enriched_customers'
    contract:
        schema:
            columns:
                - { name: customer_id, type: STRING }
                - { name: full_name, type: STRING }
                - { name: email, type: STRING }
                - { name: country, type: STRING }
                - { name: total_lifetime_value, type: NUMERIC }
                - { name: last_purchase_date, type: DATE }
        privacy:
            - { classification: PII, columns: [full_name, email], treatment: { type: hashing } }
    accessPolicy:
        visibility: internal
        grants:
            # Sales team: see treated PII for their region
            - principal: group:sales-de@company.com
                permissions: [readData]
                scope:
                    privacyView: treated
                    columns: [customer_id, full_name, email, country, total_lifetime_value]
                    rowFilter: "country = 'DE'"
            # Fraud agent: see cleartext PII
            - principal: agent:fraud_investigation_agent_v1
                permissions: [readData]
                scope:
                    privacyView: cleartext
                    columns: [customer_id, full_name, email, last_purchase_date]
            # AI Assistant: limited, read-only access (no PII)
            - principal: agent:ai_assistant_prod
                permissions: [readData]
                scope:
                    privacyView: treated
                    columns: [customer_id, country, total_lifetime_value, last_purchase_date]
```

**Key Takeaway:**
*Every agent and user gets only the data they're allowed—no more, no less. PII is protected by default.*

---

## The MCP Request: Secure, Context-Aware, Auditable

When the AI assistant receives the sales executive's question, it generates a standardized MCP request:

```json
{
    "mcp_version": "1.0",
    "context": {
        "principal": {
            "id": "agent:ai_assistant_prod",
            "on_behalf_of": "user:sales.exec.de@company.com",
            "groups": ["sales-de@company.com", "all-employees@company.com"]
        },
        "intent": {
            "task": "query_data_product",
            "parameters": {
                "dataProduct": "customers.gold.enriched_customers",
                "filters": [
                    { "column": "country", "operator": "=", "value": "DE" },
                    { "column": "last_purchase_date", "operator": ">=", "value": "2025-03-17" }
                ],
                "orderBy": { "column": "total_lifetime_value", "direction": "DESC" },
                "limit": 5
            }
        }
    }
}
```

**Why is this awesome?**
- **Principals & Context:** The request is explicit about *who* is asking, *on behalf of whom*, and *why*.
- **Intent:** The AI's purpose is clear and machine-auditable.

---

## FLUID-Compliant Authorization: Guardrails in Action

1. **Identify Principal:**
     The Data API recognizes the agent (`ai_assistant_prod`) and the user context.

2. **Locate Data Product:**
     It loads the FLUID definition for `customers.gold.enriched_customers`.

3. **Evaluate Access Policy:**
     It matches the agent's grant:
     - Only non-PII columns (`customer_id`, `country`, `total_lifetime_value`, `last_purchase_date`)
     - Treated (hashed) data where required

4. **Construct Secure Query:**
     The Data API *never* blindly passes user filters. Instead, it:
     - Selects only allowed columns
     - Applies all policy-enforced filters
     - Combines user intent with policy guardrails

     **Example SQL:**
     ```sql
     SELECT customer_id, country, total_lifetime_value, last_purchase_date
     FROM bq-prod-lakehouse.gold.enriched_customers
     WHERE country = 'DE' AND last_purchase_date >= '2025-03-17'
     ORDER BY total_lifetime_value DESC
     LIMIT 5
     ```

5. **Execute & Return:**
     The query runs securely. The AI agent receives only the permitted data—never the underlying PII.

---

## The Result: Governable, Agentic Data Access

- **The sales executive gets their answer—instantly.**
- **The AI agent never sees PII, even if the user could.**
- **All access is transparent, auditable, and policy-driven.**

---

## Why This Matters

- **Enterprise-Ready AI:** MCP + FLUID make AI agents safe, governable, and trustworthy.
- **Zero Trust by Default:** Every request is evaluated, every access is justified.
- **Accelerate Innovation:** Empower AI and users—without sacrificing security or compliance.

> **MCP support isn't just a feature—it's the foundation for safe, scalable, agentic AI in the enterprise.**
