---
description: "Public landing and static project site: content structure, deployment distinctions, navigation, localization, and accessible presentation."
applyTo: "frontend/src/app/page.tsx, frontend/src/components/{LanguageBubbles.tsx,ui/landing-faq.tsx,ui/landing-nav.tsx,billing/**}, docs/**, messages/*.json"
---

# Public Site

## Scope and ownership

This specification owns the public landing's content and navigation and the separate static project
overview. `seo.instructions.md` owns metadata, canonical URLs, indexing, and structured data;
`platform.instructions.md` owns registration and session restoration;
`subscriptions-freemium.instructions.md` owns pricing, trials, checkout, and access policy.
Shared visual, avatar, and media components belong to `architecture-frontend.instructions.md`.

## Landing structure

`frontend/src/app/page.tsx` is server-rendered. Its hero introduces the study plan, practice and voice
conversation with Lingu. The `#features` anchor leads to an ordered three-step learning journey:
level assessment and a structured A1–C2 curriculum, comprehension/vocabulary practice and the three
available games, then speaking with Lingu. The steps connect horizontally on desktop and vertically
on mobile without additional animation or client-side state. Game names reuse the `games`
translation namespace.

The static written English correction example accompanies an explanation of voice practice started
from a completed lesson, whose content and answered exercises can inform Lingu's conversation. It
uses `TargetLanguageText` with `en-GB`, localized labels, and no simulated controls or API requests.
Spaced repetition, XP and streaks are supplementary copy rather than a separate feature grid.
The hero uses one animated Lingu in `LanguageBubbles`.
Language greetings surround Lingu in a wide elliptical orbit from the small-screen breakpoint;
on narrower viewports they wrap into spaced rows below the avatar. The hero reserves the orbit's
width, and Lingu and the greetings appear together when the avatar is ready. Orbit offsets use
rounded CSS custom properties and centered margin positioning so server and browser markup agree
without relying on serialized `calc()` expressions. Floating animations respect reduced motion.

## Cloud and self-hosting

A short hero line links to `#modalities`, whose two cards precede pricing:

- FreeLingo Cloud describes managed hosting, updates and AI/voice within plan limits. Its link goes
  explicitly to `https://freelingo.app/login`, independently of the current instance's registration
  or session state.
- Self-hosting identifies AGPL-3.0 software, operator-owned maintenance, and infrastructure/provider
  costs. Its installation link goes to the repository's `#quick-start`.

The comparison distinguishes the current installation's main action from the official Cloud link and
states that accounts and progress are installation-specific. Stripe availability is not evidence that
an installation is the official Cloud service. The cards render without reveal gating.

## Entry actions and configuration

Hero and end-of-journey CTAs share the same destination: `/dashboard` when a refresh cookie is present,
`/register` for anonymous visitors when registration is open, otherwise `/login`. Cookie presence
selects navigation; it does not establish a valid authenticated session.

The landing revalidates `/api/config` hourly and passes `allowRegistration` to pricing. Registration
form gating, invitation preservation through legal pages, and backend validation are defined in
`platform.instructions.md`.

Anonymous signup copy invites visitors to start learning free. With Stripe enabled, both signup CTAs
clarify that registration needs no card. The public `freemium_trial_enabled` flag determines whether
copy describes initial Premium access followed by limited free access or limited free access directly.
It does not promise a fixed signup-trial duration: public config omits `FREEMIUM_TRIAL_DAYS`.
That period is independent of the optional Stripe subscription trial; a missing Stripe trial duration
defaults to zero on the landing. Trial eligibility and checkout behavior remain defined by the billing
specification. Reviews use the publication contract in `reviews.instructions.md`.

## FAQ, localization, and accessibility

`LandingFAQ` uses `landing.faq`, separately from the authenticated `faq` catalog. Its six questions
cover deployment modes, free signup versus the card-based Premium trial, self-hosting requirements,
storage and external processing, study languages, and the learning journey. Answers remain in the
rendered HTML, with inactive panels hidden; buttons expose `aria-expanded`, `aria-controls`, and
labelled answer regions. Measurement behavior belongs to `umami.instructions.md`.
The study-language answer interpolates the shared localized language list defined in
`architecture-frontend.instructions.md`, rather than maintaining a separate list in each translation.

Landing copy uses `next-intl` in all interface catalogs. The learning-journey and deployment-comparison
content renders without reveal gating; CTA transitions respect reduced motion and retain visible
keyboard focus. Metadata must remain consistent with the visible content under the SEO contract.

## Static project overview

`docs/index.html` is a separate English project site, not another application route. It presents a
general overview, feature cards, deployment comparison, and open-source/licensing section. It shares
the landing's Cloud/self-hosted terminology, learning journey, and operational distinctions without
duplicating dynamic prices or trial durations. Its CTAs lead to FreeLingo Cloud and the repository
installation guide.

Its CSS preserves the solid blue-tinted theme and language orbit, compact hero spacing, visible
keyboard focus, and reduced-motion support. Its canonical URL is defined in `seo.instructions.md`.
