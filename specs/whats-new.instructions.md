---
description: "What's New modal specification for FreeLingo: version-aware changelog overlay shown once per version on the dashboard, following the same pattern as OnboardingTour."
applyTo: "frontend/src/**"
---

# What's New modal

## Objective

Show users a brief summary of what changed in the current version every time a new version is deployed. The modal appears automatically on the dashboard on the user's first visit after an update, then never again until the next version is released. No backend involvement — entirely client-side using localStorage, mirroring the OnboardingTour pattern.

---

## Behaviour

- **User visits dashboard and has never seen the current version's modal** — Modal appears automatically
- **User dismisses the modal (button or backdrop click)** — `localStorage` key set; modal never appears again for this version
- **New version is deployed** — Storage key changes → modal reappears for all users on next dashboard visit
- **User logs out** — Storage key is **not** cleared (unlike the tour) — no need to show it again on re-login within the same version

The key difference from OnboardingTour: the tour clears on logout (new users must see it); the What's New modal does not — a returning user who already saw v1.5.0 notes should not see them again after logging out and back in.

---

## localStorage key

```
fl_whats_new_seen_<version>
```

Example for v1.5.0:

```
fl_whats_new_seen_v1.5.0
```

The version string is defined as a constant inside the component:

```ts
const WHATS_NEW_VERSION = "v1.5.0";
const STORAGE_KEY = `fl_whats_new_seen_${WHATS_NEW_VERSION}`;
```

To ship a new release: update `WHATS_NEW_VERSION` and the matching `whatsNew.version` label in all ten translation files. Update the entries only when explicitly approved; a version-only bump preserves the existing entries.

---

## Component

**File:** `frontend/src/components/whats-new/WhatsNew.tsx`

`'use client'` component. Rendered unconditionally in `dashboard/page.tsx` immediately after `<OnboardingTour />`. Returns `null` when not visible — zero DOM output.

### Priority with OnboardingTour

Both components are rendered in the DOM at the same time. The tour takes visual priority: if `fl_tour_done` is absent (new user), the tour is visible and the What's New modal should not compete. The What's New component must check for the tour key and skip rendering if the tour is active:

```ts
useEffect(() => {
  const tourDone = localStorage.getItem("fl_tour_done");
  const seen = localStorage.getItem(STORAGE_KEY);
  if (tourDone && !seen) {
    setVisible(true);
  }
}, []);
```

This ensures:

- New user → sees tour only
- Returning user on new version → sees What's New only
- Returning user on same version → sees neither

---

## Modal structure

Single-panel layout — no step pagination. All entries for the version are shown in one scrollable list.

```
┌─────────────────────────────────────────┐
│  WHAT'S NEW — v1.5.0          [Lingu]   │
├─────────────────────────────────────────┤
│                                         │
│  ◎  FEATURE LABEL                       │
│     Short description of the feature.   │
│                                         │
│  ▣  ANOTHER FEATURE                     │
│     Short description.                  │
│                                         │
│  △  IMPROVEMENT                         │
│     Short description.                  │
│                                         │
├─────────────────────────────────────────┤
│                        [ Got it → ]     │
└─────────────────────────────────────────┘
```

### Layout details

- **Backdrop**: full-screen fixed overlay (`z-50`), semi-transparent with `backdrop-blur-sm`. Clicking it dismisses the modal.
- **Modal card**: centered, `max-w-md`, same border/surface tokens as the tour (`border-fl-border bg-fl-surface`).
- **Header**: the title uses Geist Sans with `tracking-widest uppercase text-fl-muted-2`; the version marker uses Geist Mono through `font-code`.
- **Header illustration**: title and version sit on the left; transparent `/logo_update.png` shows Lingu on the right at a fixed 85 × 85px using `next/image`, replacing the sparkle icon. The decorative image has empty alt text and stays inside the card without a background or frame. Existing modal styling, entries, and dismissal behavior are preserved.
- **Entry list**: each entry has a `CircleDot` icon, a 12px semibold sentence-case label in `text-fl-fg`, and a 14px Geist Sans description in `text-fl-muted-1` with relaxed line spacing. Rich-text emphasis uses `text-fl-fg`.
- **Divider** between header, list, and footer using `border-fl-border`.
- **Footer**: single `Got it →` button (filled `bg-fl-accent`) right-aligned.
- **Max height**: `max-h-[50vh] overflow-y-auto` on the entries container to handle long lists gracefully.

---

## Translations

Namespace: `whatsNew` in all `messages/*.json` files.

**Rule: all 10 locale files must always be updated in sync.** The supported locales are: `en`, `es`, `de`, `fr`, `it`, `nl`, `pl`, `pt`, `ro`, `ru`. No locale may be left behind. For an explicitly requested version-only bump, preserve all existing entries in every locale and update only the version labels.

Structure for each version's entries:

```json
"whatsNew": {
  "title": "What's New",
  "version": "v1.5.0",
  "cta": "Got it",
  "entry1": {
    "label": "Feature label",
    "desc": "Short description of the feature or improvement."
  },
  "entry2": {
    "label": "Another feature",
    "desc": "Short description."
  }
}
```

The number of entries is variable per version. The component reads entries dynamically using `useMessages()` from `next-intl` — it inspects the raw `whatsNew` namespace object and filters keys matching `/^entry\d+$/`, sorted numerically. **Do not use `useTranslations` in a try/catch loop to detect missing keys** — `next-intl` does not throw on missing keys; it returns the key path as a string, which would cause an infinite loop.

**When shipping approved new content: replace the existing `entry*` keys with the approved entries rather than accumulating old entries.** If the maintainer requests only a version bump, leave every entry unchanged. In either case, update the `version` key to match `WHATS_NEW_VERSION` in the component.

For v1.9.5, all ten locales preserve the four existing entries exactly: the visual-identity highlight as `entry1`, the reading-comfort and clearer-translations/website/email highlights as `entry2` and `entry3`, and the general bug-fix entry as `entry4`. `WHATS_NEW_VERSION` and every localized version label are `v1.9.5`. The existing dynamic renderer is unchanged. The dismissal key is now `fl_whats_new_seen_v1.9.5`, so a prior dismissal of an older version does not suppress this modal once onboarding is complete.

---

## Files to create / modify

- `frontend/src/components/whats-new/WhatsNew.tsx` — Create — the modal component
- `frontend/src/app/(app)/dashboard/page.tsx` — Modify — import and render `<WhatsNew />` after `<OnboardingTour />`
- `messages/en.json` (and all locale files) — Modify — add `whatsNew` namespace with current version entries

---

## Maintenance workflow (per release)

1. Bump `WHATS_NEW_VERSION` constant in `WhatsNew.tsx` to the new version string.
2. Update the `version` key across **all 10 locale files** (`en`, `es`, `de`, `fr`, `it`, `nl`, `pl`, `pt`, `ro`, `ru`) to match the component constant.
3. If new content is approved, replace the `entry*` content and remove obsolete entries. If only the version number is being bumped, preserve all entries exactly.
4. Deploy. All existing users will see the modal on their next dashboard visit.

No database migration, no backend change, no API endpoint needed.
