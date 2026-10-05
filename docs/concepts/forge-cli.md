# The Reference Implementation — forge-cli

A capability matrix shows what each spec *covers*. **[`forge-cli`](https://github.com/Agenticstiger/forge-cli)** is the reference implementation of FLUID: it validates FLUID contracts and turns them into deployed infrastructure, generated orchestration and catalog-interop documents.

[![Repo](https://img.shields.io/badge/Agenticstiger%2Fforge--cli-FF6B35?logo=github&logoColor=white&style=for-the-badge)](https://github.com/Agenticstiger/forge-cli)
[![License Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-1E3A8A?style=for-the-badge)](https://github.com/Agenticstiger/forge-cli/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-forge--docs-A78BFA?style=for-the-badge&logo=readthedocs&logoColor=white)](https://agenticstiger.github.io/forge_docs/)

> **FLUID stands on its own.** A FLUID contract is complete and useful with no compiler at all — you can author, validate and version it with any JSON Schema validator. forge-cli is **one implementation**, not the referee: what makes a document valid FLUID is the published schema and the [conformance corpus](https://github.com/open-data-protocol/fluid/blob/main/tests/README.md), and forge-cli is implementation #1 under test against them ([GOVERNANCE.md](https://github.com/open-data-protocol/fluid/blob/main/GOVERNANCE.md)).

## Install

```bash
pip install data-product-forge
fluid --version
```

- The package is **`data-product-forge`** on PyPI; the command it installs is `fluid`, and the Python import module is `fluid_build`.
- The older distribution name **`fluid-forge`** is frozen at 0.7.9; `pip install fluid-forge` installs that old line, not the current one.
- forge-cli is licensed under Apache 2.0, like this specification.

## Which FLUID versions it supports

The JSON Schemas are authored in forge-cli and published here (see [CONTRIBUTING.md](https://github.com/open-data-protocol/fluid/blob/main/CONTRIBUTING.md#the-schemas-are-not-authored-here)). As of data-product-forge 0.18.1:

- It **bundles** the schemas for 0.7.1 to 0.7.6 and validates a contract against the schema of the `fluidVersion` it declares (`fluid validate --list-versions` lists them).
- **0.7.5 is its default** — the newest stable version — and `fluid init --quickstart` writes `fluidVersion: 0.7.5`.
- **0.7.6 is a preview**: validated when a contract declares it, never chosen by default. See [Stable and preview versions](/fluid/schema/versions#stable-and-preview-versions).
- For an older version it does not bundle, it fetches the schema from this repository and caches it (`--offline` restricts it to bundled and cached schemas).
- Its bundled 0.7.1 is a different document from the published 0.7.1 under the same `$id`; see [Versions](/fluid/schema/versions#_0-7-1-two-documents-share-one-id).

`fluid validate` also applies rules the schema cannot express — for example, a `confluent` binding must use `format: iceberg` and name its environment, cluster, bucket and role. Those are the implementation's own checks: a document can be schema-valid and still be refused by `fluid validate`.

## What it does with a contract

| Area | What forge-cli produces |
|---|---|
| **Validation** | `fluid validate` — the declared version's schema plus provider rules. |
| **Infrastructure** | OpenTofu / Terraform for the binding's platform (`fluid plan`, `fluid apply`), and `fluid verify` to check the deployed result. |
| **Orchestration** | Airflow, Dagster and Prefect workflows (`fluid generate schedule`). |
| **Standards** | Bitol ODPS and ODCS documents, and Linux Foundation ODPS v4.1 on request (`fluid generate standard`), for catalog interop. |
| **Governance** | Cloud access grants and governance resources derived from the contract (which ones depend on the platform), and an MCP output-port gateway that enforces `agentPolicy` on exposes that carry an `mcp` block. |

## Composing a contract from several files

FLUID defines one document; how a contract may be split across files is implementation-defined (see [Specification → Composing a document from several files](/fluid/schema/specification#composing-a-document-from-several-files)). forge-cli's mechanism:

```bash
fluid split  contract.fluid.yaml   # write fragments/ and replace blocks with $ref nodes
fluid bundle contract.fluid.yaml   # resolve every $ref back into one document
```

`fluid validate`, `plan` and `apply` resolve `$ref` nodes before anything else. Since 0.18, refs are confined to the root contract's directory tree — URLs, absolute paths and escapes through `..` or symlinks are refused — and `FLUID_REF_ROOT` widens that root for monorepos. See [Composing a contract from fragments](https://agenticstiger.github.io/forge_docs/concepts/contract-refs.html), [`fluid split`](https://agenticstiger.github.io/forge_docs/cli/split.html) and [`fluid bundle`](https://agenticstiger.github.io/forge_docs/cli/bundle.html).

## Checking forge-cli against the corpus

This repository's [`conformance/check_reference.py`](https://github.com/open-data-protocol/fluid/blob/main/conformance/check_reference.py) runs every corpus case through forge-cli and reports any case where its verdict differs from the corpus:

```bash
pip install data-product-forge
python3 conformance/check_reference.py
```

## Learn more

- **Repository:** [github.com/Agenticstiger/forge-cli](https://github.com/Agenticstiger/forge-cli)
- **Documentation:** [agenticstiger.github.io/forge_docs](https://agenticstiger.github.io/forge_docs/)

---

## Where to go next

- **[FLUID vs ODCS / ODPS](/fluid/concepts/comparisons)** — where the Bitol export and ODPS v4 layers fit.
- **[What FLUID Is (and Is Not)](/fluid/concepts/)** — why FLUID delegates execution to FLUID-aware tools.
