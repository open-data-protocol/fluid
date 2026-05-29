import { defineUserConfig } from 'vuepress'
import { defaultTheme } from '@vuepress/theme-default'
import { viteBundler } from '@vuepress/bundler-vite'
import { searchPlugin } from '@vuepress/plugin-search'
import { sitemapPlugin } from '@vuepress/plugin-sitemap'
import { markdownChartPlugin } from '@vuepress/plugin-markdown-chart'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const SITE = 'https://open-data-protocol.github.io/fluid/'

export default defineUserConfig({
  lang: 'en-US',
  title: 'FLUID',
  description: 'The open, declarative standard for Data Products — built for the agentic era.',

  // LOCKED: matches the GitHub Pages project path. Every published schema
  // `$id` (https://open-data-protocol.github.io/fluid/schema/...) depends
  // on this base — do not change without rewriting the schema $id URLs.
  base: '/fluid/',

  clientConfigFile: resolve(__dirname, './client.ts'),
  bundler: viteBundler(),

  // PERF: stop VuePress injecting <link rel="prefetch"> for every async
  // route chunk — the biggest render-blocking win on a multi-page site.
  shouldPrefetch: false,
  shouldPreload: false,

  head: [
    ['link', { rel: 'icon', href: '/fluid/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#050813' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }],

    ['meta', { property: 'og:title', content: 'FLUID — Declarative Data Products for the Agentic Era' }],
    ['meta', { property: 'og:description', content: 'One YAML contract: schema, build, orchestration, agentic governance, sovereignty, and semantics.' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:url', content: SITE }],
    ['meta', { property: 'og:image', content: SITE + 'og-card.png' }],
    ['meta', { property: 'og:image:width', content: '1200' }],
    ['meta', { property: 'og:image:height', content: '630' }],
    ['meta', { property: 'og:site_name', content: 'FLUID' }],

    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:title', content: 'FLUID — Declarative Data Products for the Agentic Era' }],
    ['meta', { name: 'twitter:description', content: 'One YAML contract for trustworthy, governable, agent-ready data products.' }],
    ['meta', { name: 'twitter:image', content: SITE + 'og-card.png' }],

    ['meta', { name: 'keywords', content: 'fluid, data products, data contract, data mesh, ODCS, ODPS, agentic, MCP, semantics, sovereignty, json schema' }],
  ],

  theme: defaultTheme({
    colorMode: 'dark',
    colorModeSwitch: true,
    // Transparent blue mark (cream background removed) — names the brand/home
    // link via its alt text (a11y) and reads well on both dark and light.
    logo: '/logo-mark.png',

    navbar: [
      {
        text: 'Guide',
        children: [
          { text: 'Introduction', link: '/guide/' },
          { text: 'Quickstart', link: '/guide/quickstart' },
          { text: 'Why FLUID', link: '/guide/why-fluid' },
          { text: 'FAQ', link: '/guide/faq' },
        ],
      },
      {
        text: 'Concepts',
        children: [
          { text: 'What FLUID Is', link: '/concepts/' },
          { text: 'Core Principles', link: '/concepts/principles' },
          { text: 'Agentic-Native Layer', link: '/concepts/agentic-native' },
          { text: 'FLUID vs ODCS / ODPS', link: '/concepts/comparisons' },
        ],
      },
      {
        text: 'Schema',
        children: [
          { text: 'Anatomy', link: '/schema/anatomy' },
          { text: 'Cheatsheet', link: '/schema/cheatsheet' },
          { text: 'Full Specification', link: '/schema/specification' },
          { text: 'Versions', link: '/schema/versions' },
          { text: 'JSON Schema 0.7.4 ↗', link: 'https://open-data-protocol.github.io/fluid/schema/fluid-schema-0.7.4.json', target: '_blank' },
          { text: 'Reference (HTML) ↗', link: 'https://open-data-protocol.github.io/fluid/specs/0.7.4/fluid-spec.html', target: '_blank' },
        ],
      },
      { text: 'Examples', link: '/examples/' },
      { text: 'How-to', link: '/how-to/' },
      { text: "What's New", link: '/releases/' },
      { text: 'Deck', link: '/deck/' },
      { text: 'GitHub', link: 'https://github.com/open-data-protocol/fluid' },
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Guide',
          children: [
            '/guide/README.md',
            '/guide/quickstart.md',
            '/guide/why-fluid.md',
            '/guide/in-an-mcp-world.md',
            '/guide/faq.md',
          ],
        },
      ],
      '/concepts/': [
        {
          text: 'Concepts',
          children: [
            '/concepts/README.md',
            '/concepts/principles.md',
            '/concepts/looming-crisis-of-context.md',
            '/concepts/agentic-native.md',
            '/concepts/comparisons.md',
            '/concepts/forge-cli.md',
          ],
        },
      ],
      '/schema/': [
        {
          text: 'Schema Reference',
          children: [
            '/schema/README.md',
            '/schema/anatomy.md',
            '/schema/cheatsheet.md',
            '/schema/specification.md',
            '/schema/minimal-contract.md',
            '/schema/versions.md',
            '/schema/changelog.md',
          ],
        },
      ],
      '/examples/': [
        {
          text: 'Examples',
          children: ['/examples/README.md'],
        },
      ],
      '/how-to/': [
        {
          text: 'How-to Guides',
          children: [
            '/how-to/README.md',
            '/how-to/source-aligned-data-product.md',
            '/how-to/source-aligned-kafka.md',
            '/how-to/dbt.md',
            '/how-to/airflow.md',
            '/how-to/mcp.md',
            '/how-to/datavault.md',
            '/how-to/build-patterns.md',
            '/how-to/advanced.md',
          ],
        },
      ],
      '/releases/': [
        {
          text: "What's New",
          children: [
            '/releases/README.md',
            '/releases/0.7.4.md',
            '/releases/0.7.3.md',
            '/releases/0.7.2.md',
            '/releases/0.7.1.md',
          ],
        },
      ],
      '/vision/': [
        {
          text: 'Vision',
          children: [
            '/vision/README.md',
            '/vision/2030.md',
            '/vision/multi-stakeholder.md',
          ],
        },
      ],
      '/contributing/': [
        {
          text: 'Project',
          children: ['/contributing/README.md'],
        },
      ],
    },

    repo: 'open-data-protocol/fluid',
    docsRepo: 'open-data-protocol/fluid',
    docsDir: 'docs',
    docsBranch: 'main',
    editLink: true,
    editLinkText: 'Edit this page on GitHub',
    lastUpdated: true,
    contributors: true,
  }),

  plugins: [
    searchPlugin({
      maxSuggestions: 12,
      hotKeys: ['s', '/'],
    }),
    sitemapPlugin({
      hostname: SITE,
    }),
    markdownChartPlugin({}),
  ],
})
