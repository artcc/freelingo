---
description: "Dependency security review, supported updates, reproducible manifests, validation boundaries, and unresolved upstream advisories."
applyTo: "frontend/package*.json, backend/requirements*.txt, backend/constraints*.txt, scripts/toolchain.env, scripts/bootstrap.sh, frontend/Dockerfile*, backend/Dockerfile, .github/workflows/*.yml"
---

# Dependency Updates

## Scope and authority

This specification owns the dependency review and update workflow for frontend, backend, and the
shared toolchain. Package manifests and lockfiles own exact package versions; `scripts/toolchain.env`
owns local runtime versions. Do not maintain a second version inventory here.

`AGENTS.md` owns approval requirements. A review request authorizes investigation, not installation,
package changes, application validation, container rebuilds, or publication. Obtain approval for the
proposed updates and checks before executing them.

## Review before updating

- Inspect the working tree and preserve unrelated changes. Read the affected manifests, lockfiles,
  constraints, installation scripts, and relevant domain contracts.
- Distinguish available updates, deprecation notices, and published security advisories. A newer
  version alone does not establish a vulnerability.
- Verify advisories against the exact resolved version using official package registries and
  maintainer advisories. Record the identifier, affected range, patched versions, and reference.
- Trace transitive advisories to their direct dependency. Audit totals can include several packages
  affected by the same underlying advisory; do not present them as independent vulnerabilities.
- Distinguish a vulnerable installed package from a demonstrated application exploit. Check the
  required APIs, options, callers, and runtime exposure before making impact claims.
- State the audit's scope. Package-level results do not establish the security of native libraries,
  container images, operating-system packages, or deployed versions.

For frontend reviews, use `npm audit --json`, `npm outdated --json`, and targeted `npm ls` through
`./scripts/local.sh frontend`. Audit the complete dependency graph, including tooling; an advisory's
presence in production dependencies does not by itself prove inclusion in the standalone output.
Nonzero audit/outdated exits require reading the report: distinguish reported findings from a failed
registry request or an incomplete audit.

For backend reviews, inspect all four requirements/constraints files. Query PyPI version metadata
and a vulnerability database such as OSV using exact package names and versions. Report missing
results or unresolved packages explicitly. No findings means no known applicable advisories in the
consulted sources, not proof of absence.

## Select supported fixes

- Prefer the smallest stable, officially patched update that resolves the advisory. Check release
  notes, runtime requirements, peer dependencies, and affected integrations.
- For transitive fixes, update the parent dependency or refresh the lockfile within the parent's
  declared ranges. A patch outside those ranges is not a supported resolution for that chain.
- Do not add package-manager overrides, force resolutions, use `--force` or `--legacy-peer-deps`,
  or patch installed packages to make an audit pass.
- Do not infer compatibility from similar APIs or a successful installation. Declared support is
  necessary; relevant application checks are still required.
- If no supported fix exists, leave that chain unchanged and report the advisory, dependency path,
  available upstream patch, and blocking parent range. Do not silently downgrade the parent or claim
  that the whole audit is clean.
- Keep unrelated upgrades and major-version migrations outside a security patch. Any required
  migration needs explicit scope approval and a review of its compatibility requirements.
- Treat automated upgrade suggestions as proposals. Inspect their behavior before use; do not launch
  upgrade agents, codemods, or automatic audit fixes without explicit approval.

## Apply reproducible updates

### Frontend

- Use the repository-local toolchain and the npm version pinned in `scripts/toolchain.env`.
  Update `frontend/package.json` and `frontend/package-lock.json` together.
- Preserve existing exact pins and range conventions. Keep Next.js and `eslint-config-next` on the
  same release; review bundled Next.js documentation for the installed version.
- Use targeted package updates. Review the lockfile diff for unrelated upgrades, unexpected new
  dependencies, changed sources, and platform-specific packages.
- Confirm installation from the resulting lockfile with `npm ci` when authorized. Do not disable
  required lifecycle scripts merely to obtain a passing install.
- VAD dependencies have a version/hash-checked postinstall patch. Before updating them, follow the
  patch contract in `voice-conversation.instructions.md` and inspect `frontend/scripts/patch-vad.js`
  and `frontend/scripts/copy-vad-models.js`.

### Backend and toolchain

- Keep direct runtime pins in `backend/requirements.txt`, indirect pins in
  `backend/constraints.txt`, and development pins in their corresponding `*-dev.txt` files.
- Update coupled dependencies together according to their published requirements. Ensure the
  resolved graph has exact committed pins and supports the project's Python version.
- Follow the bootstrap installation contract in `testing.instructions.md`, including binary-wheel
  availability and rejection of unpinned Python dependencies.
- Runtime or package-manager updates require coordinated changes to `scripts/toolchain.env`,
  archive checksums, Dockerfiles, CI versions, and affected cache inputs. Keep Node types on the
  selected Node major. Verify support for the deployment architectures.

## Validate in the correct environment

`testing.instructions.md` owns local checks, their commands, permissions, and failure handling.
Choose checks based on the changed dependency and its consumers, then repeat the relevant audit.
Report completed checks and remaining findings separately.

Local lint, typechecking, and unit tests use `scripts/local.sh`. Application execution and production
builds use the Docker topology documented in `docker.instructions.md`:

- Development Compose mounts the frontend and translation catalogs into the container.
- The production frontend Dockerfile copies both before building the standalone application.
- A bare host-side `npm run build` does not reproduce that filesystem layout. Do not treat its
  missing container-provided resources as evidence of a dependency regression.
- Do not copy or symlink translation catalogs into the checkout, change import paths, or modify
  Docker configuration merely to accommodate a host-side build check.
- Container builds and application checks need explicit authorization. Do not start the stack,
  recreate volumes, or invoke `run-dev.sh` as an implicit dependency validation step.

When validation fails, stop and report the exact command and error before changing code or tests.
Inspect the environment and relevant unchanged configuration before attributing the failure to the
update. An unexecuted container build remains unverified; static checks do not replace it.

## Documentation and delivery

- Identify affected specifications and obtain approval before editing them. Update current contracts
  only where dependencies change them; do not add audit logs or release narratives to specs.
- Record approved security updates in `CHANGELOG.md` under `Security`, naming the corrected behavior
  and advisory where useful. Follow `changelog.instructions.md`, including approval for unreleased
  entries, and state any unresolved chain when an entry would otherwise imply a complete fix.
- Follow `version.md` when a project-version bump is requested. What's New changes require separate
  approval; a dependency update does not authorize an announcement change.
- Summarize the actual version changes, installation and validation results, unresolved advisories,
  and any environment limitations. Do not claim deployment or complete remediation without evidence.
