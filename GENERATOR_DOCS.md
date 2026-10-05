# Generated files: the HTML reference and the schema diffs

Two directories in this repository are generated from `schema/` and committed:

| Directory | Generator | What it holds |
|---|---|---|
| `specs/<version>/` | `generate-docs.py` | `fluid-spec.html`, the field-by-field HTML reference for one schema version, with its `schema_doc.css` and `schema_doc.min.js` |
| `schema-diffs/` | `generate-schema-diffs.py` | one Markdown diff per pair of consecutive schema versions, and an index |

Neither is edited by hand. The `generated` job in
`.github/workflows/conformance.yml` regenerates both on every pull request and
fails if the committed files differ from a fresh run.

Nothing else may sit beside them. `generate-docs.py --check` also accounts for
every file under `schema/` and `specs/`: each is either generated for a synced
version (or, under `schema/`, a synced schema, which the drift check compares
with the reference implementation) or listed with its sha256 in the `frozen`
map of `scripts/schema-versions.json`. A file that is neither, a frozen file
whose bytes changed, and a frozen file that is gone all fail the check. The
frozen files are the schemas before 0.7.2 and the HTML pages earlier renderer
releases produced for them; changing one is a deliberate edit to `frozen`.

## The version record

`scripts/schema-versions.json` says which schema versions are **synced** with
the reference implementation, which one is the latest **stable** version, and
which are **previews**, and it records which reference implementation release
they were vendored from (`upstream.ref` and `upstream.commit`, the release
`scripts/check-schema-drift.py` compares with) and the `frozen` files described
above. Both generators and the drift check read it.

The latest stable version is recorded on its own, not derived from the
highest version number, because a preview has the higher number. Nothing
should link a preview as "latest":

```bash
python3 generate-docs.py --print-latest-stable    # prints the stable version
```

`generate-docs.py` refuses to run if the record is inconsistent: a version
listed as both stable and preview, a stable version that is not synced, or a
synced non-preview version higher than the recorded stable one.

## `generate-docs.py`

```bash
pip install --require-hashes -r scripts/requirements-docs.lock

python3 generate-docs.py                  # every synced version
python3 generate-docs.py --all            # the same, spelled out
python3 generate-docs.py --version 0.7.6  # one version; repeat the flag for more
python3 generate-docs.py --check          # render to a temporary directory and
                                          # exit 1 if specs/ differs, or if a
                                          # file under schema/ or specs/ is not
                                          # accounted for
python3 generate-docs.py --check-files    # only the offline half of --check;
                                          # needs no renderer
```

It renders with [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans),
in-process, using its default configuration with the footer timestamp turned
off, so the same schema and the same renderer produce the same bytes. The
renderer and the libraries that shape its output are pinned exactly in
`scripts/requirements-docs.txt`, and the script exits with an error naming the
mismatch if any other version is installed. That file is the input; what CI and
the docs deploy install is `scripts/requirements-docs.lock`, the same pins plus
every transitive dependency, each with its hashes, installed with
`--require-hashes` so that a package replaced on PyPI afterwards is refused.
`--check` fails if the two files disagree. To move a pin, change it in
`requirements-docs.txt`, recompile the lock, run `python3 generate-docs.py`, and
commit the lock and the regenerated `specs/` in the same pull request:

```bash
pip install pip-tools     # under Python 3.12, the version CI uses
pip-compile --generate-hashes --strip-extras \
    --output-file=scripts/requirements-docs.lock scripts/requirements-docs.txt
```

A preview's page is labelled by its schema's own `title`; for 0.7.6 that reads
"FLUID 0.7.6 — Declarative Packaging Modes (preview)".

`--version` also renders a version that is not synced, if its schema is in
`schema/`. The pages for versions before 0.7.2 were rendered by earlier
releases of the renderer and are not regenerated; they are frozen, which is to
say checked by hash rather than by re-rendering.

## `generate-schema-diffs.py`

```bash
python3 generate-schema-diffs.py           # rewrite schema-diffs/
python3 generate-schema-diffs.py --check   # exit 1 if schema-diffs/ is stale
```

It compares every pair of consecutive files in `schema/`, key by key, and
writes `diff-<old>-to-<new>.md` plus `README.md`. Long values are truncated in
the output, so a diff file is a map of where to look, not a substitute for the
schema. A hand-written summary between `<!-- HUMAN-NOTE:START -->` and
`<!-- HUMAN-NOTE:END -->` in a diff file survives regeneration. The index marks
a pair whose newer version is a preview.

## The docs site

`npm run docs:build` first runs `scripts/sync-public-assets.mjs`, which copies
`schema/` and `specs/` into `docs/.vuepress/public/`, so the site serves every
schema from 0.5.7 on at the URL its `$id` names, and each HTML reference beside it. The
deploy workflow (`.github/workflows/deploy-docs.yml`) runs
`python3 generate-docs.py` with the locked renderer before that build.
