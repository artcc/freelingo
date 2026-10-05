# Recovery risk report: progress API and Dashboard

## Scope

This branch is an isolated recovery track. It must not be merged until the damaged `backend/app/routers/progress.py` is restored from a complete Git snapshot and the Dashboard/API contract is validated together.

## Confirmed findings

- `90e667cf37e8f5549ee16185e66a0ceb5f856699` replaced `backend/app/routers/progress.py` with a truncated file. The current file contains a `# ...` placeholder and does not contain the complete progress router.
- The last known complete progress router before the damage is `171cdf93435d6ae1078dfefe916f01d2915a1be2`.
- Dashboard commit `cc98c2b0a7d70d4c4e533444ab6f89e5d728179c` introduced a malformed closing tag, `< /h2>`, in the league card.
- Dashboard depends on `/api/progress/summary`, `/api/progress/today`, `/api/progress/history`, `/api/progress/goals`, social friends, and league data. A broken progress router can make the Dashboard appear as a frontend failure when the root cause is backend route loss.

## Risk assessment

| Risk | Severity | Mitigation before merge |
| --- | --- | --- |
| Missing progress routes | Critical | Restore the complete file from `171cdf93435d6ae1078dfefe916f01d2915a1be2`; reject any file containing truncation markers. |
| Wrong active-plan selection | High | Preserve user ownership and active-language filters; add deterministic ordering and regression coverage. |
| Dashboard JSX failure | High | Replace `< /h2>` with `</h2>` and run frontend typecheck/build. |
| Contract drift between Dashboard and API | High | Smoke-test summary, goals, history, and today endpoints with authenticated fixtures. |
| Accidental data loss | Critical | Do not run migrations, deletes, archives, or database rewrites as part of this recovery. |
| CI false confidence | Medium | Require backend tests, frontend tests, typecheck/build, and the recovery integrity checks to pass. |

## Merge gate

Do not merge this PR until the complete router restoration is committed, the Dashboard syntax is valid, CI is green, and the API smoke checks pass. The backup branch `backup/before-progress-recovery-90e667c` preserves the pre-recovery state.
