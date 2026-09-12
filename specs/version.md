# Version

**1.9.5**

> Canonical project version. Update this file when bumping.
> Full history in [CHANGELOG.md](../CHANGELOG.md).

## Versioning rules

- Use semantic versioning (`MAJOR.MINOR.PATCH`).
- Keep release history in `CHANGELOG.md`. Specifications define the current structure, behavior, and general rules, not change-by-change narratives or validation logs.

## Sync rule

When bumping the version, update these locations in sync:

- **`specs/version.md`** — Version number above
- **`CHANGELOG.md`** — New `## [X.Y.Z]` section at top
- **`README.md`** — `version` badge: `![Version](https://img.shields.io/badge/version-X.Y.Z-brightgreen?style=flat-square)`
- **`AGENTS.md`** — Current project version reference
- **`frontend/src/app/(app)/layout.tsx`** — `vX.Y.Z` string in sidebar (desktop + mobile)
- **`frontend/src/components/whats-new/WhatsNew.tsx`** — `WHATS_NEW_VERSION` constant
- **`messages/*.json` (all 10 locales)** — Update `whatsNew.version` to match `WHATS_NEW_VERSION`. Replace the `entry*` content only when explicitly approved; a version-only bump preserves every existing entry. See `specs/whats-new.instructions.md` for the required structure.

## What's New policy

- Before modifying the modal or its translations, confirm whether the user wants new entries or only a version bump.
- A version-only bump updates the component constant and all ten localized version labels while preserving every entry. Keep the modal on an older version only when explicitly requested.
- For new entries, use the release's changelog as the source, draft concise user-facing copy without technical jargon, and obtain approval before writing it to the locale files.
- Follow [the modal specification](whats-new.instructions.md) for structure and dismissal behavior.