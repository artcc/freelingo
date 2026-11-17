---
description: "Guidelines for maintaining FreeLingo's README.md: purpose, structure, deployment entry points, and update rules."
applyTo: "**/README.md"
---

# README Guidelines

## Purpose

The README is the public entry point for users, self-hosters, and contributors. It should explain what
FreeLingo is, how to start it, and where to find detailed documentation. It is not a release ledger,
implementation inventory, or exhaustive operations manual.

## Structure

Keep these sections in this order:

1. **Title, badges, and logo** — project identity and current version/runtime badges.
2. **Overview** — deployment modes, core learning flow, and major user-facing capabilities.
3. **Hosted service** — link to `freelingo.app` and distinction from AGPL self-hosting.
4. **For businesses** — deployment and commercial-licence options.
5. **Architecture** — brief system boundary with links to authoritative specs.
6. **Repository** — top-level directory tree.
7. **Stack** — concise layer-to-technology list.
8. **Quick start** — Docker Compose and Portainer paths.
9. **Operational notes** — essential provider, quota, and target-language facts.
10. **Host requirements** — Redis memory overcommit and production reverse proxy.
11. **TTS and STT** — provider selection and links to speech and Docker specs.
12. **Development, contributing, licence, and author** — project links and ownership.

## Content rules

- Keep language factual and concise.
- Keep the architecture summary short and delegate structure to `architecture.instructions.md`.
- List only top-level directories and relevant root files in the repository tree.
- Link to `https://freelingo.app` for the hosted service and to `COMMERCIAL_LICENSE.md` for commercial
  licensing.
- Cover both CLI and Portainer deployment in Quick start.
- Keep required deployment variables and host prerequisites explicit.
- Delegate CI, dependency installation, provider contracts, model matrices, voice catalogs, and full
  environment-variable reference to their dedicated files and specs.
- Keep configurable values in their configuration sources, not in the README or specifications.
  Reference variables and their owning files; document units, scope, constraints, and behavior.
  Do not duplicate default quotas, trial durations, model names, voice mappings, or operational settings.
  Preserve protocol values, supported enums, invariants, and clearly identified setup examples.
- Do not add phase/completion matrices, test counts, release history, or session-specific status.
- Do not add a separate Features section; the overview owns concise feature coverage.
- Avoid Markdown tables; use short lists that remain readable on narrow screens.

## When to update

Update the README for:

- user-facing capabilities that materially change the overview;
- supported technology or deployment changes;
- new top-level directories or relevant root files;
- version badges;
- commercial, licensing, hosted-service, or operational requirement changes;
- development or contribution entry-point changes.

Do not update it for internal refactors, files added inside existing modules, tests, implementation
counts, or spec content changes that do not affect public navigation.
