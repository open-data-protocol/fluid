<!--
  <Deck> — a dependency-free slide engine (no reveal.js, no external lib).
  Async-loaded via client.ts, so its JS ships ONLY on the /deck/ route and
  0 bytes on every docs page.

  Authoring: wrap each slide in <section class="deck-slide"> … </section>
  inside <Deck> … </Deck> on the deck page. The engine shows one slide at a
  time with prev/next, dot nav, a counter, keyboard control (←/→/space,
  Home/End), and an expand-to-fullscreen toggle. Respects
  prefers-reduced-motion.
-->

<template>
  <div
    ref="root"
    class="ff-deck"
    :class="{ 'is-full': full }"
    tabindex="0"
    role="group"
    aria-roledescription="carousel"
    aria-label="FLUID slide deck"
    @keydown="onKey"
  >
    <div class="ff-deck__stage"><slot /></div>

    <div class="ff-deck__bar">
      <button class="ff-deck__nav" type="button" :disabled="i === 0" aria-label="Previous slide" @click="prev">‹</button>

      <div class="ff-deck__dots" role="group" aria-label="Slides">
        <button
          v-for="n in count"
          :key="n"
          class="ff-deck__dot"
          :class="{ active: n - 1 === i }"
          type="button"
          :aria-label="`Go to slide ${n}`"
          :aria-current="n - 1 === i ? 'true' : undefined"
          @click="go(n - 1)"
        />
      </div>

      <span class="ff-deck__count" aria-live="polite">{{ count ? i + 1 : 0 }} / {{ count }}</span>

      <button class="ff-deck__nav" type="button" :disabled="i >= count - 1" aria-label="Next slide" @click="next">›</button>
      <button class="ff-deck__full" type="button" :aria-pressed="full" aria-label="Toggle fullscreen" @click="toggleFull">
        {{ full ? '✕' : '⤢' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'

const root = ref<HTMLElement | null>(null)
const slides = ref<HTMLElement[]>([])
const count = ref(0)
const i = ref(0)
const full = ref(false)

function render() {
  slides.value.forEach((el, n) => {
    el.style.display = n === i.value ? '' : 'none'
  })
}
function go(n: number) {
  if (!count.value) return
  i.value = Math.max(0, Math.min(count.value - 1, n))
  render()
}
function next() { go(i.value + 1) }
function prev() { go(i.value - 1) }

function syncScroll() {
  if (typeof document !== 'undefined') document.body.style.overflow = full.value ? 'hidden' : ''
}
function toggleFull() { full.value = !full.value; syncScroll() }

function onKey(e: KeyboardEvent) {
  switch (e.key) {
    case 'ArrowRight':
    case 'PageDown':
    case ' ': e.preventDefault(); next(); break
    case 'ArrowLeft':
    case 'PageUp': e.preventDefault(); prev(); break
    case 'Home': e.preventDefault(); go(0); break
    case 'End': e.preventDefault(); go(count.value - 1); break
    case 'Escape': if (full.value) { full.value = false; syncScroll() } break
  }
}

onMounted(async () => {
  await nextTick()
  if (!root.value) return
  slides.value = Array.from(root.value.querySelectorAll<HTMLElement>('.deck-slide'))
  count.value = slides.value.length
  render()
})
onBeforeUnmount(() => {
  if (typeof document !== 'undefined') document.body.style.overflow = ''
})
</script>

<style lang="scss" scoped>
.ff-deck {
  position: relative;
  margin: 1.5rem 0 2rem;
  border: 1px solid var(--vp-c-border);
  border-radius: 16px;
  background: var(--ff-hero-gradient-soft);
  outline: none;

  &__stage {
    position: relative;
    min-height: 440px;
    padding: clamp(1.5rem, 4vw, 3.25rem);
    display: flex;

    // Each authored slide.
    :deep(.deck-slide) {
      flex: 1;
      animation: ff-deck-in .32s ease;

      h1, h2 {
        border-bottom: 0;
        margin-top: 0;
        background: var(--ff-text-gradient);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
      }
    }
  }

  &__bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 0.9rem;
    border-top: 1px solid var(--vp-c-border);
    background: var(--ff-glass-bg);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    border-radius: 0 0 16px 16px;
  }

  &__nav,
  &__full {
    width: 34px;
    height: 34px;
    border-radius: 999px;
    border: 1px solid var(--vp-c-border);
    background: transparent;
    color: var(--vp-c-text);
    font-size: 1.1rem;
    line-height: 1;
    cursor: pointer;
    transition: border-color .15s ease, color .15s ease, background .15s ease;

    &:hover:not(:disabled) { border-color: var(--vp-c-accent); color: var(--vp-c-accent); }
    &:disabled { opacity: .35; cursor: default; }
  }
  &__full { margin-left: auto; }

  &__dots {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    justify-content: center;
    flex: 1;
  }
  &__dot {
    // 24px hit target (WCAG target-size) with a small visible dot drawn via ::before
    width: 24px;
    height: 24px;
    padding: 0;
    border: 0;
    background: transparent;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;

    &::before {
      content: "";
      width: 9px;
      height: 9px;
      border-radius: 999px;
      background: var(--vp-c-border-hard);
      transition: background .15s ease, transform .15s ease;
    }
    &.active::before { background: var(--vp-c-accent); transform: scale(1.25); }
    &:hover::before { background: var(--vp-c-accent-hover); }
  }

  &__count {
    font-family: var(--ff-font-mono);
    font-size: 0.78rem;
    color: var(--vp-c-text-mute);
    white-space: nowrap;
  }

  &.is-full {
    position: fixed;
    inset: 0;
    z-index: 200;
    margin: 0;
    border-radius: 0;
    display: flex;
    flex-direction: column;

    .ff-deck__stage { flex: 1; align-items: center; }
    .ff-deck__bar { border-radius: 0; }
  }
}

@keyframes ff-deck-in {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: none; }
}

@media (prefers-reduced-motion: reduce) {
  .ff-deck__stage :deep(.deck-slide) { animation: none; }
}
</style>
