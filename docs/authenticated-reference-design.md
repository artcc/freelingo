# Authenticated reference design

Scope: all 24 authenticated section families, including their nested routes: admin, assessment, chat, coach, conversation, courses, dashboard, faq, feedback, flashcards, friends, games, grammar, leagues, lesson, listening, phrasebook, plan, progress, reading, review, settings, translator, vocabulary.

## Shared implementation

`frontend/src/app/(app)/nunito-local.css` imports `all-pages-reference.css` through the existing authenticated layout. Existing repository Nunito and Cairo binaries are served from `/fonts/Juba-Nunito.ttf` and `/fonts/Juba-Cairo.ttf`, prepared by `next.config.ts`. No Google Fonts or OS-installed font dependency is used. RTL prioritizes Cairo. The shared layer maps legacy duo and busuu tokens, including the previously missing blue alias, and supplies consistent shell navigation, named panels, headings, tables, inputs and controls.

Dashboard and tutor chat retain their more specific geometry in `dashboard/dashboard-layout-fix.css`. Other routes keep their own learning workflows and layouts. The screenshots are visual references, not data sources: users, friends, XP, levels, rankings and availability are not fabricated to imitate them.

## State preservation

The shared stylesheet deliberately avoids globally resetting button transforms, positioning, game card faces, dialogs, recording controls, data-correct feedback, data-movement zones, data-risk alerts and quota error colors. Completed and active UnitCard colors remain state-dependent. Disabled controls and keyboard focus remain visible.

## Validation status

All section root pages and relevant nested route styles were reviewed read-only before applying the shared contract. These changes have not been built or visually tested against a running application in this environment. A full route-specific pixel match is not established by the stylesheet alone.

## Acceptance checks before release

1. Run frontend lint, TypeScript checks, unit tests and production build.
2. Verify both local font URLs return fonts after dev and production startup. In browser computed styles, check Nunito for Latin and Cairo for Arabic, not a system fallback.
3. Open every section and nested settings/admin/course/lesson/game/social route at 1280px, 1024px, 768px and 390px, in Arabic and English.
4. Verify reading/listening initial, loading, error, exercise, result and history states; tables must scroll rather than clip.
5. Check correct/incorrect game feedback, memory flip and matching states, moving targets, disabled submissions and drawer focus trapping.
6. Check voice start/stop, microphone permission error, timeout warning, quota exceeded, streamed transcript and reduced-motion behavior.
7. Confirm payment, account deletion and logout confirmations still work and are not obscured by overlays.
