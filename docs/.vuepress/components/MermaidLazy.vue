<!--
  <MermaidLazy> — a wrapper around a build-time-rendered Mermaid diagram
  (the markdown-chart plugin emits inline SVG, so no client-side mermaid.js
  ships). Adds a horizontal-scroll container + an expand-to-fullscreen
  affordance so large diagrams stay readable on mobile without forcing a
  tiny render on the page. Usage in markdown:

      <MermaidLazy>

      ```mermaid
      flowchart LR
        ...
      ```

      </MermaidLazy>
-->

<template>
  <figure ref="root" class="ff-diagram" :class="{ 'is-full': full }">
    <div class="ff-diagram__scroll"><slot /></div>
    <button class="ff-diagram__btn" type="button" :aria-pressed="full" @click="toggle">
      {{ full ? '✕ Close' : '⤢ Expand' }}
    </button>
  </figure>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount } from 'vue'

const full = ref(false)
const root = ref<HTMLElement | null>(null)

function onKey(e: KeyboardEvent) {
  if (e.key === 'Escape') close()
}
function open() {
  full.value = true
  if (typeof document !== 'undefined') {
    document.body.style.overflow = 'hidden'
    document.addEventListener('keydown', onKey)
  }
}
function close() {
  full.value = false
  if (typeof document !== 'undefined') {
    document.body.style.overflow = ''
    document.removeEventListener('keydown', onKey)
  }
}
function toggle() {
  full.value ? close() : open()
}
onBeforeUnmount(close)
</script>

<style lang="scss" scoped>
.ff-diagram {
  position: relative;
  margin: 1.5rem 0;
  padding: 0;

  &__scroll {
    overflow-x: auto;
    border: 1px solid var(--vp-c-border);
    border-radius: 12px;
    background: var(--vp-c-bg-alt);
    padding: 1rem;

    :deep(svg) {
      max-width: 100%;
      height: auto;
    }
  }

  &__btn {
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 0.35rem 0.7rem;
    font-family: var(--ff-font-mono);
    font-size: 0.72rem;
    border-radius: 999px;
    border: 1px solid var(--vp-c-border);
    background: var(--ff-glass-bg);
    -webkit-backdrop-filter: blur(8px);
    backdrop-filter: blur(8px);
    color: var(--vp-c-text-mute);
    cursor: pointer;
    transition: color .15s ease, border-color .15s ease;

    &:hover {
      color: var(--vp-c-accent);
      border-color: var(--vp-c-accent);
    }
  }

  &.is-full {
    position: fixed;
    inset: 0;
    z-index: 200;
    margin: 0;
    background: rgba(5, 8, 19, .94);
    display: flex;
    align-items: center;
    justify-content: center;

    .ff-diagram__scroll {
      max-width: 96vw;
      max-height: 92vh;
      overflow: auto;

      :deep(svg) {
        max-width: none;
      }
    }
  }
}
</style>
