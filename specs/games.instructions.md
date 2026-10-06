---
description: "Games section, navigation catalog, empty state, and presentation boundaries."
applyTo: "frontend/src/app/(app)/games/**, frontend/src/lib/games.ts, messages/*.json"
---

# Games

## Route and access

`/games` belongs to the authenticated app layout and the middleware's protected-route list.
The shared main navigation places Games after Conversation in desktop and mobile menus.
The catalog page has no subscription restriction or Premium badge.

## Catalog and empty state

`frontend/src/lib/games.ts` exports `availableGames`, a readonly list of navigation metadata:
stable ID, `/games/` route, and title/description keys in the `games` translation namespace.
Only implemented games with working routes and translations belong in this list.

The catalog currently has no entries. When empty, the page explicitly states that no games are
available yet and offers a link to `/plan`. It shows no playable cards or inactive play controls.
A nonempty catalog renders linked cards using the existing resource-page grid pattern.

The page performs no API requests and records no attempts, XP, quota use, or lesson completion.
Navigation metadata is frontend-owned presentation data, not exercise content or authorization.

## Presentation and languages

The page uses the resource pages' `max-w-4xl` container, bordered header and surface panels,
responsive card grid, `fl-*` tokens, and existing light/dark themes. Interface text uses Geist Sans.
The title is an `h1`; the empty state and game cards use `h2` headings.

Navigation, page guidance, and empty-state text are localized in all fifteen interface catalogs.
The shared app shell retains its language selector. The empty catalog is the same for every study
language and does not load or modify a study plan.
