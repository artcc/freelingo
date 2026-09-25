# Version

**1.9.25**

This is the canonical current development version. Its publication state and date belong to
`CHANGELOG.md`; the canonical value may therefore correspond to a changelog section marked
`Unreleased`.

## Rules

- Use Semantic Versioning.
- Keep release history only in `CHANGELOG.md`.
- A version bump is a coordinated documentation and product-label change, not a validation record.

## Required synchronization

When bumping the canonical version, update:

- `specs/version.md`.
- The top version heading in `CHANGELOG.md`.
- The README version badge.
- The current-version line in `AGENTS.md`.
- Desktop and mobile sidebar labels in `frontend/src/app/(app)/layout.tsx`.

## What's New

`WHATS_NEW_VERSION` and `messages/*.json` `whatsNew.version` must match each other, but they need not be
bumped merely because the canonical project version changes. They identify the client announcement
content and storage key.

Before changing them, confirm whether the maintainer wants new entries or intentionally wants to show
the existing entries again under a new key. New content must replace old `entry*` keys consistently in
all fifteen locale catalogs. See `whats-new.instructions.md`.
