# Version

**1.8.50**

> Canonical project version. Update this file when bumping.
> Full history in [CHANGELOG.md](../CHANGELOG.md).

The voice lifecycle reliability improvement is included in the existing 1.8.50 release under `Fixed`, without a version bump or changes to the sidebar or version badge. Its 13 frontend test cases passed in the confirmed pre-push run (6.58 s), included in the 494 passed across 50 frontend files. These tests use mocks and do not validate real microphone behavior in a browser; manual validation against the remote deployment remains pending.

The same 1.8.50 release includes clearer voice status labels, static idle transcript halos, local reduced-motion support, and the Lingu role label in all ten UI locales. What's New has now been revised across all ten locales: `entry1` remains intact, the new `entry2` covers voice stability, error recovery, and visual improvements, and the former `entry2` is preserved unchanged as `entry3`. `WhatsNew.tsx`, its version constant, and its dynamic rendering and dismissal mechanism remain unchanged, so this content revision does not reopen an already-dismissed v1.8.50 modal. No new validation was run for these visual and content changes.

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
