# Security Policy

## What "security" means for a specification repository

This repository publishes JSON Schemas, a conformance corpus, and the small
Python tools that check them. It is not a service and holds no user data, so the
realistic threat model is narrower than for an application — but not empty:

- A schema that **fails open** — accepting a contract it should reject — can let
  an unsafe data product through a downstream gate that trusted it.
- A conformance case that **passes for the wrong reason** launders a false
  assurance into every implementation that trusts the corpus.
- The **compatibility gate** or the **conformance runner** silently not doing
  what it claims. A gate that cannot fail is worse than no gate, because it is
  believed. This is why [`tests/meta_test.py`](tests/meta_test.py) exists and
  runs first in CI.
- Anything that would cause a consumer to execute code, exfiltrate data, or
  escalate privilege while processing a published artefact.

If you have found something in those categories, we want to hear about it, even
if you are unsure it qualifies.

## Supported versions

| Schema version | Supported |
|---|---|
| 0.7.5 | ✅ |
| 0.7.3 – 0.7.4 | ✅ |
| ≤ 0.7.2 | ❌ |

Fixes land on the current version. Because the compatibility promise forbids
narrowing, a fix that would reject a previously-valid contract is a version
increment, not a patch to a published schema — a published schema is an
immutable artefact that people validate against by URL.

## Reporting a vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Use GitHub's
[Private Vulnerability Reporting](https://github.com/open-data-protocol/fluid/security/advisories/new).
It keeps the report private until a fix ships, gives us somewhere to draft the
advisory, and lets you follow the fix without leaving GitHub.

If you cannot use that form, email **change@agenticstransformation.com**.

You should get a response within **48 hours**. If you do not, please follow up —
assume the message was lost rather than ignored.

Please include as much as you can:

- What the issue is, and which artefact it affects (schema version, corpus file,
  or tool).
- A contract, corpus case, or command that demonstrates it.
- What you expected to happen and what happened instead.
- Any impact you can see on downstream consumers.

## What happens next

1. We acknowledge within 48 hours.
2. We reproduce it, and tell you if we cannot.
3. We agree a fix and a disclosure timeline with you. We will not sit on a
   confirmed issue quietly; if we disagree on severity we will say so rather
   than let it go silent.
4. We credit you in the advisory unless you would rather we did not.

## Scope

**In scope:** the schemas under `schema/`, the corpus under `tests/`, and the
tools under `conformance/` and `scripts/`.

**Out of scope here, but still worth reporting to their owners:** the reference
implementation ([forge-cli](https://github.com/Agenticstiger/forge-cli)) and any
product built on FLUID. If you are unsure which, report it here and we will route
it.
