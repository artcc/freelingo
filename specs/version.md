# Version

**1.8.55**

> Canonical project version. Update this file when bumping.
> Full history in [CHANGELOG.md](../CHANGELOG.md).

Version 1.8.55 introduces Geist Sans for the application and Latin-script learning content, selective readability adjustments, a self-hosted Geist font for the static website, and Arial/Helvetica email body text. The sidebar, README badge, and What's New version are synchronized. The initial What's New content in all ten locales contained two new readability highlights followed by the preserved general bug-fix entry. The typography review found no blocking issues. The confirmed `./scripts/pre-push.sh` run on 2026-09-11 completed successfully: auto-format, 1,019 backend tests (292.55 s, 85.56% coverage against the 70% minimum), frontend lint and TypeScript checks, and 494 frontend tests across 50 files (5.95 s). A targeted check also confirmed Tailwind font-family generation and local size overrides, compact size tokens, the static font URL/WOFF2 header and license, and all ten locale JSON files with their final bug-fix entry unchanged. Dependency deprecation warnings did not fail validation. Concurrent static-site theme/navigation edits and GitHub-link casing edits appeared after the initial typography review and are not covered by that review. The maintainer handles deployment-environment checks.

The same 1.8.55 release now also applies the approved petroleum-blue accent and subtly blue-tinted background/surface/border palette to both the application and static website. Public and authenticated pages have solid backgrounds; the dot-grid utility is removed and the PWA base color is `#0c1316`. Theme selection, layout, typography, interactions, and functional status colors are unchanged by this palette adjustment. Auxiliary subscription-button text uses full foreground opacity, and the active-language badge on admin user detail uses a lighter background tint to preserve contrast.

Palette follow-up validation on 2026-09-11 passed: generated Tailwind CSS, shared palette parity with `docs/`, unchanged non-palette tokens, and 24 representative normal/hover/badge contrast pairs at or above 4.5:1 (minimum 5.17:1 in dark mode and 4.62:1 in light mode). A parsed TypeScript comparison confirmed that the 15 modified TS/TSX files contain only the intended class/color changes; theme scripts, the authenticated shell, backend files, and all ten locale files are unchanged. The final authorized `./scripts/pre-push.sh` run passed auto-format, 1,019 backend tests (288.77 s, 85.56% coverage), frontend lint and TypeScript checks, and 494 frontend tests across 50 files (5.62 s). Dependency deprecation warnings remain non-blocking. Deployment-environment visual checks remain with the maintainer.

The subsequent approved What's New update adds the visual-identity highlight as `entry1` in all ten locales and shifts the previous `entry1`/`entry2`/`entry3` content unchanged to `entry2`/`entry3`/`entry4`. The version remains 1.8.55 and the renderer and dismissal key are unchanged. The authorized focused JSON check passed for all ten files: valid JSON, four entries in the intended order, exact preservation of the three existing entries and all unrelated translations, and the approved Spanish copy. The pre-push results above predate this content-only update; the full suites were not rerun for it.

## Sync rule

When bumping the version, update these locations in sync:

- **`specs/version.md`** — Version number above
- **`CHANGELOG.md`** — New `## [X.Y.Z]` section at top
- **`README.md`** — `version` badge: `![Version](https://img.shields.io/badge/version-X.Y.Z-brightgreen?style=flat-square)`
- **`frontend/src/app/(app)/layout.tsx`** — `vX.Y.Z` string in sidebar (desktop + mobile)
- **`frontend/src/components/whats-new/WhatsNew.tsx`** — `WHATS_NEW_VERSION` constant
- **`messages/*.json` (all 10 locales)** — Replace all `entry*` keys in the `whatsNew` namespace with the new version's entries; update the `version` key to match `WHATS_NEW_VERSION`. See `specs/whats-new.instructions.md` for the required structure.

## What's New entries — mandatory prompt

**Before updating `WhatsNew.tsx` and the `whatsNew` namespace in any locale file, always ask the user:**

> "Do you want to update the What's New entries for this version, or just bump the version number?"

- If the user wants to update the entries: proceed to update `WHATS_NEW_VERSION`, all 10 locale files, and `WhatsNew.tsx`.
- If the user only wants to bump the number: update only `specs/version.md`, `CHANGELOG.md`, and `layout.tsx`. Leave `WhatsNew.tsx` and the `whatsNew` locale keys untouched.

Never update the What's New content silently — always wait for explicit confirmation.

## What's New entries — content guidelines

When the user confirms they want to update the entries, **do not write them immediately**. First:

1. Read the corresponding `## [X.Y.Z]` section in `CHANGELOG.md` to understand what changed.
2. Draft the entries in plain, friendly language aimed at end users — no technical jargon, no code references, no internal implementation details. Focus on what the user gains or experiences, not on how it was built.
3. Present the drafted entries to the user for review and wait for approval before writing anything to `WhatsNew.tsx` or any locale file.

**Tone guidelines:**

- Write as if explaining to a non-technical user who just wants to know what improved.
- Use short, positive sentences. Highlight the benefit, not the mechanism.
- Avoid terms like: base64, endpoint, migration, StaticFiles, VAD, barge-in, JWT, Redis, CEFR (spell it out if needed), alembic, router, component, namespace, i18n.
- Good example: "Your profile photo is now stored more efficiently — pages load faster and the app uses less database space."
- Bad example: "Avatar images are no longer encoded as base64 data URIs in the PostgreSQL users.avatar TEXT column."
