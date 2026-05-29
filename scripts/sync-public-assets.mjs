// =====================================================================
// sync-public-assets.mjs
// =====================================================================
// Mirrors the canonical schema/ and specs/ directories into
// docs/.vuepress/public/ so the published site serves them under the
// site base — e.g. https://open-data-protocol.github.io/fluid/schema/
// fluid-schema-0.7.4.json — keeping every schema `$id` URL resolvable
// byte-for-byte.
//
// The canonical copies stay at the repo root (untouched by the Python
// generators and the schema-sync CI). These public/ mirrors are
// git-ignored and rebuilt on every `npm run docs:dev` / `docs:build`
// via the npm "sync:assets" prebuild step.
// =====================================================================

import { cpSync, rmSync, existsSync, mkdirSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const publicDir = resolve(root, 'docs/.vuepress/public')

for (const dir of ['schema', 'specs']) {
  const src = resolve(root, dir)
  const dest = resolve(publicDir, dir)
  if (!existsSync(src)) {
    console.warn(`[sync-assets] source missing: ${src} — skipping`)
    continue
  }
  rmSync(dest, { recursive: true, force: true })
  mkdirSync(dirname(dest), { recursive: true })
  cpSync(src, dest, { recursive: true })
  console.log(`[sync-assets] ${dir}/ -> docs/.vuepress/public/${dir}/`)
}
