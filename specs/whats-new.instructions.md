---
description: "Current client-side What's New modal, version key, tour priority, dynamic localized entries, layout, and update policy."
applyTo: "frontend/src/components/whats-new/WhatsNew.tsx, frontend/src/app/(app)/dashboard/page.tsx, messages/*.json"
---

# What's New

## Purpose

What's New is a client-side dashboard announcement shown once per browser/origin for a configured
content version. It has no backend or account-persisted state and is independent from the canonical
application version unless intentionally synchronized.

## Visibility

`WhatsNew.tsx` derives:

```text
fl_whats_new_seen_<WHATS_NEW_VERSION>
```

On mount it opens only when `fl_tour_done` exists and the current What's New key does not. Dismissal by
button or backdrop writes the key and hides the modal. Logout does not clear What's New keys, while it
can clear onboarding-tour state.

Consequences:

- a browser that has not completed the onboarding tour sees the tour, not What's New;
- a browser with the tour completed and an unseen content version sees What's New;
- another browser or cleared local storage can show it again for the same account;
- changing `WHATS_NEW_VERSION` makes the content eligible to appear again.

Do not claim that every existing user sees it: visibility is browser-local and requires completed-tour
state.

## Component and layout

`WhatsNew` is rendered after `OnboardingTour` on Dashboard and returns no DOM when hidden.

- Full-screen fixed blurred backdrop; backdrop click dismisses.
- Centered `max-w-md` card using `fl-*` surface and border tokens.
- Header illustration `/logo_update.png` appears on the left; title/version text appears on the right.
- Version text uses `font-code`.
- Entries use `CircleDot`, `text-sm` labels/descriptions, and theme tokens.
- Entry area is scrollable with a bounded viewport height.
- Footer contains one primary dismiss action.
- Decorative imagery has empty alt text.

## Localized data

Every root `messages/*.json` catalog contains the `whatsNew` namespace:

```json
{
  "whatsNew": {
    "title": "What's New",
    "version": "vX.Y.Z",
    "cta": "Got it",
    "entry1": {
      "label": "Feature label",
      "desc": "Short description."
    }
  }
}
```

The component reads raw messages with `useMessages()`, selects keys matching `entryN`, and sorts them
numerically. It must not probe unknown translation keys with a `useTranslations` try/catch loop because
missing keys return paths rather than throwing.

All eleven locale catalogs must contain the same entry keys and matching version label. Entry count is
variable. New content replaces old `entry*` keys rather than accumulating release history.

## Version semantics

`WHATS_NEW_VERSION` and every localized `whatsNew.version` value must match. This version identifies
the displayed content and local-storage key; it is not automatically the canonical project version.

Changing only the version while preserving entries intentionally re-announces the existing content.
Do this only with explicit maintainer approval. When announcing a release's actual changes, draft new
user-facing entries from its changelog, obtain approval, replace entries in every locale, and update the
component and localized version together.

## Update workflow

1. Decide whether the content is new or an intentional repeat.
2. Draft concise nontechnical entries from approved user-visible changes.
3. Obtain explicit approval for entry text and version behavior.
4. Replace/synchronize `entry*` keys across all locale catalogs.
5. Update `WHATS_NEW_VERSION` and all localized version labels together.
6. Keep Dashboard placement, tour priority, and dismissal semantics unchanged unless the feature itself
   is being redesigned.

No database migration, API endpoint, or backend change is required for ordinary content updates.
