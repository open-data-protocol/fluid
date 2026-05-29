// =====================================================================
// FLUID — VuePress 2 client config
// =====================================================================
// Globally registers components so any markdown page can embed them
// without per-page imports, and overrides the theme's default 404 with
// the branded NotFound layout.
//
// Both components are async-loaded so they land in their own JS chunks
// and only download on the pages that use them — <MermaidLazy> on the
// few diagram-heavy pages, <Deck> on the /deck/ route. Every other doc
// page (home, concepts, schema reference, examples) loads neither, which
// keeps their bundles lean.
// =====================================================================

import { defineClientConfig } from 'vuepress/client'
import { defineAsyncComponent } from 'vue'
import NotFound from './layouts/NotFound.vue'

const MermaidLazy = defineAsyncComponent(
  () => import('./components/MermaidLazy.vue'),
)

const Deck = defineAsyncComponent(
  () => import('./components/Deck.vue'),
)

export default defineClientConfig({
  enhance({ app }) {
    app.component('MermaidLazy', MermaidLazy)
    app.component('Deck', Deck)
  },
  layouts: {
    NotFound,
  },
})
