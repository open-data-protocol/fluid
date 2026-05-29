<!--
  FLUID — branded 404 page
  ============================================================
  Registered as a custom layout named "NotFound" (via client.ts),
  overriding the stock "There's nothing here." page. After the docs
  reorg, inbound links to old README anchors / file paths may be stale;
  this routes visitors to the destinations they most likely wanted.
  ============================================================
-->

<template>
  <div class="ff-404">
    <div class="ff-404__hero">
      <div class="ff-404__sigil">404</div>
      <h1 class="ff-404__title">This page took a wrong turn.</h1>
      <p class="ff-404__lede">
        The link you followed might be stale, the page may have moved during the docs
        reorganization, or the URL might just be a typo. Here are the routes most visitors want:
      </p>
    </div>

    <nav class="ff-404__cards" aria-label="Suggested destinations">
      <a class="ff-404__card" href="/fluid/">
        <span class="ff-404__card-eyebrow">Start here</span>
        <strong>Home</strong>
        <span class="ff-404__card-detail">What FLUID is, in 60 seconds.</span>
      </a>
      <a class="ff-404__card" href="/fluid/guide/">
        <span class="ff-404__card-eyebrow">Quickstart</span>
        <strong>Guide</strong>
        <span class="ff-404__card-detail">The minimal contract and your first steps.</span>
      </a>
      <a class="ff-404__card" href="/fluid/schema/anatomy">
        <span class="ff-404__card-eyebrow">Reference</span>
        <strong>Schema Anatomy</strong>
        <span class="ff-404__card-detail">Every top-level block, what / when / why.</span>
      </a>
      <a class="ff-404__card" href="/fluid/examples/">
        <span class="ff-404__card-eyebrow">Hands-on</span>
        <strong>Examples</strong>
        <span class="ff-404__card-detail">Ten steps from hello-world to production.</span>
      </a>
    </nav>

    <p class="ff-404__report">
      Found a true broken link? Please
      <a href="https://github.com/open-data-protocol/fluid/issues/new" rel="noopener">open an issue</a>
      so it doesn't trip the next visitor.
    </p>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
onMounted(() => {
  if (typeof document === 'undefined') return
  const existing = document.querySelector('meta[name="robots"]')
  if (existing) {
    existing.setAttribute('content', 'noindex,follow')
  } else {
    const meta = document.createElement('meta')
    meta.name = 'robots'
    meta.content = 'noindex,follow'
    document.head.appendChild(meta)
  }
})
</script>

<style lang="scss" scoped>
.ff-404 {
  max-width: 760px;
  margin: 0 auto;
  padding: 64px 24px 96px;

  &__hero {
    background: var(--ff-hero-gradient-soft);
    border-radius: 16px;
    padding: 56px 32px 48px;
    text-align: center;
    margin-bottom: 32px;
  }

  &__sigil {
    font-family: var(--ff-font-mono);
    font-size: 6rem;
    font-weight: 700;
    line-height: 1;
    background: var(--ff-hero-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    letter-spacing: -0.04em;
    margin-bottom: 16px;
  }

  &__title {
    font-size: 1.75rem;
    font-weight: 600;
    margin: 0 0 12px;
    color: var(--vp-c-text);
    border: 0;
    padding: 0;
  }

  &__lede {
    font-size: 1rem;
    line-height: 1.6;
    color: var(--vp-c-text-mute);
    max-width: 520px;
    margin: 0 auto;
  }

  &__cards {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;

    @media (max-width: 600px) {
      grid-template-columns: 1fr;
    }
  }

  &__card {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 18px 20px;
    background: var(--vp-c-bg-alt);
    border: 1px solid var(--vp-c-border);
    border-radius: 10px;
    text-decoration: none;
    color: var(--vp-c-text);
    transition: border-color 120ms ease, transform 120ms ease, box-shadow 120ms ease;

    &:hover {
      border-color: var(--vp-c-accent);
      transform: translateY(-1px);
      box-shadow: 0 6px 18px -10px rgba(37, 99, 235, 0.4);
      text-decoration: none;
    }

    strong {
      font-size: 1.1rem;
      color: var(--vp-c-text);
    }
  }

  &__card-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--vp-c-accent);
  }

  &__card-detail {
    font-size: 0.875rem;
    color: var(--vp-c-text-mute);
    line-height: 1.4;
  }

  &__report {
    text-align: center;
    margin-top: 32px;
    color: var(--vp-c-text-subtle);
    font-size: 0.9rem;

    a {
      color: var(--vp-c-accent);
      font-weight: 500;
    }
  }
}
</style>
