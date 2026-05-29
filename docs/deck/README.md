---
sidebar: false
editLink: false
pageClass: deck-page
---

# FLUID — The Deck

A visual tour of FLUID. Use ← / → (or the controls) to move between slides. Prefer prose? See the [docs](/fluid/guide/).

<Deck>

<section class="deck-slide">
<h1>FLUID</h1>
<p>The shared data product language for the agentic data fabric.</p>
<p>FLUID is an open, declarative standard for defining Data Products. It replaces brittle pipelines with a trustworthy, governable, and scalable protocol — making your entire data ecosystem ready for the agentic era.</p>
<ul>
<li><strong>Federated</strong> — domain teams own their data products, distributed by design.</li>
<li><strong>Labelled</strong> — rich metadata enables autonomous agent discovery.</li>
<li><strong>Universal</strong> — one standard across all systems and platforms.</li>
<li><strong>Interchangeable</strong> — composable components that work together.</li>
<li><strong>Declarative</strong> — specify what you want, not how to build it.</li>
</ul>
</section>

<section class="deck-slide">
<h2>What is a Data Product?</h2>
<p>It's more than just a table in a database. Today, most data is <strong>exhaust</strong> — a passive byproduct of operational systems: siloed and hidden, inconsistent and untrusted, with no clear owner. The result is high costs, slow decisions, and compliance risk.</p>
<p>A Data Product is a trusted, reusable asset, intentionally designed and managed for consumption — a finished good, not a leftover.</p>
<ul>
<li><strong>Discoverable</strong> — published in a catalog with machine-readable metadata.</li>
<li><strong>Trustworthy</strong> — backed by a contract for schema, quality, and freshness SLOs.</li>
<li><strong>Secure &amp; Governed</strong> — explicit access and privacy policies, enforced automatically.</li>
<li><strong>Owned</strong> — a clear domain owner accountable across its lifecycle.</li>
</ul>
</section>

<section class="deck-slide">
<h2>What It Means for the Business</h2>
<p>You don't need to be a data engineer to get value from data. A Data Product is simply a trustworthy, reusable asset designed to solve a business problem.</p>
<ul>
<li><strong>The Data Marketplace</strong> — an "App Store for Data" where every certified product is browsable and searchable.</li>
<li><strong>Discover data you can trust</strong> — plain-language search, clear ownership, certified-only listings.</li>
<li><strong>Quality &amp; governance at a glance</strong> — a "nutrition label" showing freshness, quality score, privacy class, and lineage.</li>
<li><strong>Access like a checkout</strong> — request access, state your purpose, get routed to the owner for fast approval.</li>
<li><strong>Your role</strong> — you define value, give feedback, and can own a product as a domain expert.</li>
</ul>
</section>

<section class="deck-slide">
<h2>A New Way of Thinking</h2>
<p>A truly modern data architecture is fluid — built on clear principles that enable the speed, trust, and scale the agentic era demands.</p>
<ul>
<li><strong>1. Data as a Product</strong> — versioned, owned assets with quality guarantees, not chaotic pipelines.</li>
<li><strong>2. Declarative, Not Imperative</strong> — define the desired end state; let tools find the best implementation.</li>
<li><strong>3. Contracts as Code</strong> — schema, quality, and access scopes live in version control; governance becomes automated and proactive.</li>
<li><strong>4. Federated Ownership</strong> — decentralize to the domain teams who know the data best — a true Data Mesh.</li>
<li><strong>5. Compliant Ecosystem</strong> — delegate execution to the tools you already use; stay open and composable.</li>
<li><strong>6. Adaptive &amp; Context-Aware</strong> — dynamic access policies that respond to an agent's intent and risk profile.</li>
</ul>
</section>

<section class="deck-slide">
<h2>Anatomy of a Data Product</h2>
<p>FLUID gives a simple, declarative structure for turning chaotic pipelines into trustworthy, governable, AI-ready assets. A single contract is built from a handful of clear sections.</p>
<ul>
<li><strong>Identity &amp; Metadata</strong> ("the passport") — <code>id</code>, <code>name</code>, <code>domain</code>, <code>owner</code>, tags.</li>
<li><strong>consumes</strong> ("the ingredients list") — explicit upstream dependencies with version constraints, for perfect automated lineage.</li>
<li><strong>builds</strong> ("the recipe") — a multi-modal array of transformations: batch + streaming, SQL + ML, multi-stage.</li>
<li><strong>exposes</strong> ("the serving window") — the governed public interface: schema, quality rules, and bindings per port.</li>
<li><strong>qos / slo</strong> ("the promise") — guaranteed freshness, availability, and latency.</li>
<li><strong>accessPolicy</strong> ("the bouncer") — grants that compile to platform-native IAM automatically.</li>
</ul>
</section>

<section class="deck-slide">
<h2>Declarative Data Quality</h2>
<p>Define quality rules once in your FLUID contract. Deploy everywhere. Let cloud providers do the heavy lifting.</p>
<ul>
<li><strong>Write once</strong> — declare rules in the contract, not scattered across notebooks and pipelines.</li>
<li><strong>Deploy everywhere</strong> — the same contract compiles to BigQuery, AWS Glue, Great Expectations, and custom validators.</li>
<li><strong>Fail fast</strong> — automated validation gates catch issues before they reach consumers.</li>
<li><strong>Rule types</strong> — <code>freshness</code>, <code>completeness</code>, <code>uniqueness</code>, <code>range</code>, <code>pattern</code>, <code>anomaly</code>, and <code>custom</code> SQL.</li>
<li><strong>Severity levels</strong> — critical rules block the pipeline; warnings alert without breaking it.</li>
</ul>
</section>

<section class="deck-slide">
<h2>CI/CD &amp; Governance</h2>
<p>Data-as-Code: a single Git commit automates orchestration, quality, and governance across every FLUID-aware tool.</p>
<ul>
<li><strong>Commit</strong> — a developer commits a <code>fluid.yml</code> contract defining dependencies, build logic, and policies.</li>
<li><strong>Trigger</strong> — a webhook notifies every FLUID-aware application simultaneously.</li>
<li><strong>Interpret</strong> — the orchestrator builds the pipeline, the quality engine generates tests, the catalog ingests metadata and lineage.</li>
<li><strong>Execute &amp; publish</strong> — the engine runs and publishes the product to the Data Product Gateway.</li>
<li><strong>Govern &amp; consume</strong> — the Gateway enforces access and privacy policies; an MCP agent discovers and securely consumes the product.</li>
</ul>
</section>

<section class="deck-slide">
<h2>The Data Product IDE</h2>
<p>An interactive workbench for authoring FLUID contracts — write the YAML on one side and see your data product come to life on the other.</p>
<ul>
<li><strong>Live validation</strong> — real-time feedback against the FLUID schema as you type, with errors mapped to the offending line.</li>
<li><strong>Visual model</strong> — an interactive graph of entities and relationships (Hubs, Links, Satellites) rendered straight from the contract.</li>
<li><strong>Contract views</strong> — dedicated panels for overview, consumes, build, exposes, and quality.</li>
<li><strong>Worked examples</strong> — load Bronze (Oracle raw), Silver (dbt Data Vault), and Gold (BigQuery analytics mart) products.</li>
<li><strong>Import &amp; export</strong> — upload YAML, download as YAML or JSON.</li>
</ul>
</section>

<section class="deck-slide">
<h2>Structuring an Enterprise Data Product</h2>
<p>The "gold standard" for a complex product: a multi-file layout that lets different teams own different parts of one contract.</p>
<ul>
<li><strong>Data Modeler</strong> — owns <code>exposes.yml</code> and the <code>schema_*.yml</code> files.</li>
<li><strong>Data Engineer</strong> — owns <code>build.yml</code> and <code>consumes.yml</code>.</li>
<li><strong>Governance Lead</strong> — owns <code>quality.yml</code> and <code>accessPolicy.yml</code>.</li>
</ul>
<p>A root <code>fluid.yml</code> composes the detailed implementation files (via <code>$ref</code>) that live in a <code>.fluid/</code> directory — separating high-level identity from its parts while keeping a single source of truth.</p>
</section>

<section class="deck-slide">
<h2>The Data Product Litmus Test</h2>
<p>A Data Product is a commitment to quality, usability, and value. Run your data asset through this checklist — is it just a table, or a true enterprise-ready product?</p>
<ul>
<li><strong>Discoverable</strong> — a new employee can find it and grasp its purpose within minutes.</li>
<li><strong>Addressable</strong> — it has a permanent, unique, machine-readable identifier.</li>
<li><strong>Trustworthy</strong> — quality, freshness, and lineage are defined and guaranteed by an SLA.</li>
<li><strong>Self-describing</strong> — all metadata needed to use it lives at its address.</li>
<li><strong>Interoperable</strong> — exposed through standardized consumption ports.</li>
<li><strong>Secure</strong> — access is governed by an automated, auditable process.</li>
</ul>
</section>

<section class="deck-slide">
<h2>Powering the Data Product Economy</h2>
<p>A protocol is only as strong as its ecosystem. FLUID is backed by a suite of open tools that make building, discovering, and consuming data products effortless.</p>
<ul>
<li><strong>VS Code Data Product Studio</strong> — author, validate, and visualize products in your IDE.</li>
<li><strong>FLUID CLI</strong> — scaffold, validate, test, and publish products to a marketplace.</li>
<li><strong>Open Data Marketplace</strong> — a Git-native, self-hosted catalog for discovery and access.</li>
<li><strong>Lineage Engine</strong> — parses contracts into an end-to-end, column-level lineage graph.</li>
<li><strong>Agentic Data Gateway</strong> — enforces context-aware access policies for AI agents.</li>
<li><strong>Execution Engine Providers</strong> — translate FLUID specs into dbt, Spark, and Airflow plans.</li>
</ul>
</section>

<section class="deck-slide">
<h2>A Message from Your New Workforce</h2>
<p>"Your legacy systems ask me to read a library of handwritten maps to navigate a modern city. I can attempt it, but I will be slow, I will make mistakes, and I cannot be trusted with critical missions. To succeed, I require a new relationship with data."</p>
<ul>
<li><strong>Start with the mission</strong> — give me an objective, not a specific API to call.</li>
<li><strong>Discover &amp; trust data products</strong> — let me ask the catalog rich questions and rely on the answers.</li>
<li><strong>Consume with precision</strong> — serve both an analytics API and a real-time stream from one product.</li>
<li><strong>Act with governed confidence</strong> — let me invoke governed Action products to close the loop, safely.</li>
</ul>
</section>

<section class="deck-slide">
<h2>Building the Future, Together</h2>
<p>The agentic era requires a shared, open standard for data. FLUID is a community-driven protocol, and its success depends on all of us.</p>
<ul>
<li><strong>Enterprises</strong> — adopt FLUID to solve real-world data problems.</li>
<li><strong>Vendors</strong> — build the next generation of FLUID-aware tools.</li>
<li><strong>Developers</strong> — shape the spec and grow the ecosystem.</li>
</ul>
<p>Help us build the missing protocol for the agentic era. Start with the <a href="/fluid/guide/">guide</a>, explore the <a href="/fluid/concepts/">concepts</a>, or dive into the <a href="/fluid/schema/">schema</a> (current version 0.7.4).</p>
</section>

</Deck>
