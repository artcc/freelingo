---
description: "Technical SEO contract: public indexing, metadata, canonical URLs, internationalization, structured data, and Search Console operations."
applyTo: "frontend/src/app/**, frontend/src/lib/seo.ts, frontend/src/middleware.ts, frontend/tests/seo.test.ts, messages/*.json"
---

# Technical SEO

## Scope and ownership

FreeLingo's public production origin is `https://freelingo.app`. Technical SEO uses the native
Next.js 16 App Router Metadata API and metadata routes. Metadata must remain consistent with visible
content and preserve authentication and privacy boundaries. `public-site.instructions.md` owns
public content and navigation; `umami.instructions.md` owns measurements.

The technical contract below defines application behavior. The operational guidance at the end
describes maintainer checks and Search Console procedures, not evidence of deployment or indexing.

- `frontend/src/lib/seo.ts` owns `SITE_URL`, `INDEXABLE_PATHS`, and `createPublicMetadata`.
- `frontend/src/app/layout.tsx` owns `metadataBase`, the title template, default robots directives,
  document language, icons, and fonts.
- `frontend/src/app/page.tsx` owns landing metadata and JSON-LD.
- Legal route-specific `layout.tsx` files own privacy and terms metadata. The existing client pages
  retain their navigation and registration-context behavior.
- Account route-specific layouts supply translated titles without altering account forms.
- `messages/*.json` owns translated metadata in the fifteen interface languages. SEO descriptions
  are separate from visible page copy.
- `frontend/src/app/sitemap.ts` and `robots.ts` publish `/sitemap.xml` and `/robots.txt`.

## Indexing policy and route inventory

The only indexable HTML pages and sitemap entries are:

- `https://freelingo.app/`: the product landing.
- `https://freelingo.app/privacy`: the privacy policy.
- `https://freelingo.app/terms`: the terms of service.

These pages explicitly emit `index, follow`. The root defaults to `noindex, follow`, with no shared
canonical or landing-specific social metadata for other pages. Indexability is opt-in, including
for future routes.

Public account utilities inherit `noindex` and are absent from the sitemap:

- `/login` and `/register`, including invitation and plan-selection variants.
- `/forgot-password`, `/reset-password`, and `/verify-email`, including token-bearing variants.

Authenticated route families and their descendants also inherit `noindex`:

- `/dashboard`, `/onboarding`, `/assessment`, and `/assessment/level-test`.
- `/plan`, `/lesson/[id]`, `/progress`, `/flashcards`, and `/flashcards/vocabulary`.
- `/chat`, `/conversation`, `/listening`, and `/reading`.
- `/games`, the Error Detective, Sentence Order, and Vocabulary Pairs catalogs, and their `[id]` pages.
- `/grammar` and `/grammar/[slug]`, `/vocabulary` and `/vocabulary/[setId]`, and `/phrasebook`.
- `/settings`, `/settings/languages`, `/settings/memories`, `/faq`, and `/feedback`.
- `/billing/success` and `/billing/canceled`.
- `/admin`, `/admin/users` and user detail, `/admin/reviews`, `/admin/feedback`, and `/admin/system`.

API, WebSocket, Umami proxy, manifest, and static-resource URLs are not content pages and do not
belong in the sitemap. Unknown pages use the existing Next.js not-found handling.

Robots rules allow HTML crawling so crawlers can observe `noindex` and existing login redirects.
They disallow `/api/` and `/ws/` and declare the absolute sitemap URL. Required JavaScript, CSS,
fonts, and images remain crawlable. Do not combine an HTML `Disallow` with a reliance on that page's
`noindex`: a blocked crawler cannot read the directive.

Robots directives are not access control. The existing middleware checks refresh-cookie presence
on its explicit route list; the app shell restores and checks the session, and backend dependencies
enforce authentication, roles, and resource ownership. SEO must not change these mechanisms.

## Metadata and canonical URLs

Each indexable page emits:

- A distinct translated title and description appropriate to its actual content.
- One absolute canonical URL using HTTPS and the production origin.
- Open Graph `website` metadata with `siteName`, matching URL, title, description, and catalog locale.
- A Twitter `summary_large_image` card with matching title and description.
- The existing `/og-image-v2.png` social image, 1200 × 630, with a brand alternative description.

Landing metadata describes structured A1–C2 learning, personalized plans, exercises, games, and
conversation with Lingu. It must not promise guaranteed outcomes or features that are unavailable.
Meta keywords are not used.

Canonical URLs omit all query strings and fragments. For example, `/privacy?from=landing` and
`/privacy?from=register&invite=...` identify `/privacy` as canonical while retaining their existing
navigation behavior. Authentication utilities do not point to the landing as a surrogate canonical.

`INDEXABLE_PATHS` is the sitemap's allowlist. Entries use absolute URLs and contain no `lastModified`
until there is a reliable, page-specific date of a significant content change. Request time, build
time, and copyright-year changes are not modification dates. `changeFrequency` and `priority` are
omitted; Google ignores them.

Future public content must explicitly define its metadata and indexability and be added to the
allowlist only when it has a stable canonical URL and genuinely public content.

## Internationalization

Interface locales are `en`, `es`, `fr`, `pt`, `de`, `it`, `pl`, `nl`, `ro`, `ru`, `tr`, `sv`, `da`,
`fi`, and `hr`. They are distinct from study-language codes.

The existing locale resolver prioritizes `NEXT_LOCALE`, then supported `Accept-Language` values,
then English. Middleware forwards `x-next-locale` for the initial server render. The browser's
locale-detection script and Settings continue to manage the existing cookies and reload behavior.
The root's `html[lang]` and translated metadata use the resolved interface locale; learned-language
examples retain `TargetLanguageText` and their own `lang` attributes.

All interface variants of a page share a single canonical URL. There are no `hreflang`,
`x-default`, or Open Graph alternate-locale claims. Cookie-selected variants are not separately
addressable language pages. Googlebot normally omits `Accept-Language`, so the default English
response is important; translating metadata does not make all fifteen variants independently
indexable.

Independent international indexing requires a separately approved architecture with stable localized
URLs, self-canonicals, reciprocal `hreflang`, an appropriate `x-default`, crawlable language links,
and migration rules. That is outside the current route and `next-intl` contract.

## Structured data

The landing includes one server-rendered JSON-LD graph:

- `WebSite`: FreeLingo's name, canonical root URL, rendered language, and an `about` reference to
  the application. This communicates the preferred site name.
- `WebApplication`: stable `#application` identity, name, localized description, URL,
  `EducationalApplication` category, `operatingSystem: Any`, and the requirement for a modern
  JavaScript-enabled browser.
- The application author remains the verified individual, Arturo Carretero Calvo, with the existing
  public author URL. An additional `Organization` is not necessary for this graph and must not be
  populated with inferred legal or business details.
- A zero-price `Offer` is present only when registration is enabled and the anonymous response
  visibly offers free signup. Its name reuses the visible CTA and its URL points to registration.
  It describes free entry, not unlimited access to paid features. No currency is asserted for the
  zero-price offer. Paid amounts and subscription periods are not inferred or duplicated in JSON-LD.

JSON serialization escapes `<` before embedding the payload in the script element. Do not insert
unescaped external text or introduce schemas unrelated to the page's visible content.

There is no `aggregateRating` or review markup. The carousel is a maximum-50 collection of approved
four- and five-star reviews with comments, not a representative aggregate of all submitted ratings.
There is no fabricated review to satisfy rich-result requirements.

Schema.org validity and Google rich-result eligibility are different. Google's software-app rich
result requires an eligible rating or review in addition to other required fields. This graph
describes the product but does not claim that eligibility. The Rich Results Test may flag that
missing requirement; do not resolve it with invented or selectively aggregated data. `WebSite`
site-name markup is checked with Schema Markup Validator and URL Inspection, not the Rich Results Test.

## Semantic and performance constraints

The landing has one H1, H2 section/footer headings, and H3 learning-step/example headings. Its main
landmark uses `display: contents` to preserve the existing layout boxes. Public legal documents use
their translated document title as H1 and the shared legal layout supplies `main`.

Core landing copy, including the Cloud/self-hosted comparison, is server-rendered independently of
animation readiness. Existing image dimensions, alternative text, reserved avatar space, and
learned-language annotations are retained. FAQ answers remain in the HTML with inactive panels hidden
and accessible button/panel relationships; no click is needed to obtain their text. Reveal sections
still depend on IntersectionObserver, and crawlers should not be assumed to interact with controls.
Changes to reveal behavior or visible content require a presentation review.

The separate English project overview in `docs/index.html` retains its own canonical URL,
`https://www.arturocarreterocalvo.com/freelingo/`. Its description and social metadata describe the
learning journey and Cloud/self-hosted options without quoting dynamic prices or trial durations.
It is not an additional route in the application's sitemap.

Geist Sans and Geist Mono retain their existing Next.js font handling. Noto Sans JP/KR/SC remain
available with the existing typography rules, without global preloads of their Latin subsets.
Three.js and Lingu's scene remain dynamically imported with the existing reduced-motion, visibility,
and cleanup behavior. No analytics dependency is needed for SEO.

Performance work should use measured evidence:

- LCP: inspect actual LCP candidates, server response time, backend config/review fetches, font
  delivery, and the hero's resources. Do not assume the canvas is the LCP element.
- INP: inspect main-thread hydration and animation work, menu and FAQ interactions, and long tasks.
- CLS: inspect image dimensions, font swaps, reserved avatar space, and asynchronous pricing/review
  presentation, including authenticated visits.

Model compression, narrower client translation payloads, changes to server fetch/streaming boundaries,
and animation scheduling require separate measurement and approval. The current social artwork is
shared across locales; replacing or translating it is a separately approved visual change.

## Operational guidance

### Validation and release responsibilities

Ask before running checks. Relevant local checks are TypeScript, ESLint, and focused
`tests/seo.test.ts`, `tests/app/landing.test.tsx`, and `tests/middleware.test.ts`. They check metadata
objects, route/crawler policy, JSON-LD output, and existing landing/session behavior using mocks.
They do not establish deployed HTML correctness, Core Web Vitals, or end-to-end authentication.

The deployment maintainer must complete production build and deployed checks:

1. Run the production frontend build in the supported deployment/CI environment.
2. Check successful public-page responses, one canonical per page, robots directives, translated
   titles/descriptions, and social metadata in the rendered HTML. Include normal and crawler requests,
   default locale, a supported locale cookie, and `Accept-Language` negotiation.
3. Check that query variants keep their navigation behavior while using clean canonicals. Confirm
   the reverse proxy/CDN neither caches one visitor's personalized response for others nor injects
   conflicting `X-Robots-Tag` headers.
4. Inspect `/sitemap.xml` for the three public URLs and `/robots.txt` for crawl access and the sitemap
   declaration. Confirm HTTPS and host normalization at ingress; canonical tags do not implement
   redirects.
5. Inspect rendered JSON-LD with Schema Markup Validator and Google's tools, applying the rich-result
   eligibility distinction above.
6. Verify account utilities remain `noindex`, authenticated routes retain their existing access
   checks, backend unauthorized requests are rejected, and unknown routes return the appropriate
   not-found response. `/reading` is included in the middleware's preliminary protected-route list;
   the authenticated shell and backend remain responsible for validating the session and access.
7. Compare responsive light/dark landing presentation and existing registration, invitation,
   legal-return, pricing, FAQ, and Lingu flows. Retain existing behavior when optimizing SEO.

### Google Search Console

1. **Verify the domain.** Add the Domain property `freelingo.app` in Search Console. Publish the exact
   DNS TXT record supplied by Google at the DNS provider, then verify. Keep the record after
   verification. Domain verification needs no tracking script or fabricated verification token.
2. **Submit the sitemap.** In Sitemaps, submit `https://freelingo.app/sitemap.xml`. Review fetch and
   parsing status and the discovered canonical URLs after deployment.
3. **Inspect URLs.** Inspect `/`, `/privacy`, and `/terms`. Use Test Live URL and inspect the rendered
   HTML, crawl availability, robots rules, and canonical. Compare the user-declared and Google-selected
   canonical once indexed. Request indexing after meaningful changes; do not submit account pages.
4. **Check indexing.** Review Page indexing for unexpected exclusions of public pages and unexpected
   inclusion of utility/private URLs. `noindex` exclusions for account pages are intended. A valid
   sitemap or indexing request does not guarantee indexing, and updates require recrawling.
5. **Review Core Web Vitals.** Check mobile and desktop reports and use PageSpeed Insights for
   diagnostics. Target field p75 LCP at most 2.5 seconds, INP at most 200 ms, and CLS at most 0.1.
   Field reports use a rolling observation window; insufficient traffic is not a passing result.
   Laboratory scores do not establish field INP or a production improvement.
6. **Track search performance.** Monitor impressions, clicks, CTR, average position, and queries.
   Compare comparable periods and filter by page, country, and device; distinguish branded and
   non-branded queries. Changes in average position alone do not establish causality.

Search Console complements the existing anonymous, self-hosted Umami setup. No Google Analytics,
account-linked tracking, or additional browser measurement script is part of this SEO contract.

## References

- [Next.js Metadata API](https://nextjs.org/docs/app/api-reference/functions/generate-metadata).
- [Google: noindex and crawl access](https://developers.google.com/search/docs/crawling-indexing/block-indexing).
- [Google: sitemap construction](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
- [Google: locale-adaptive pages](https://developers.google.com/search/docs/specialty/international/locale-adaptive-pages).
- [Google: structured data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).
- [Google: software application markup](https://developers.google.com/search/docs/appearance/structured-data/software-app).
- [Google: site names](https://developers.google.com/search/docs/appearance/site-names).
- [Google: Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals).
