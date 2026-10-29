# Development

## Local validation environment

Local work uses backend tests/static checks and frontend lint, typecheck and unit tests. Backend
tests use in-memory SQLite and mocked services. Docker and a running application are not required;
deployment checks belong to the maintainer. Container configuration is documented in
`specs/docker.instructions.md`.

The supported hosts are macOS and glibc-based Linux on arm64 or x86_64. Bootstrap needs the OS utilities
Bash, curl, tar and a SHA-256 utility (`shasum` or `sha256sum`), plus network access. Python, Node,
npm, pip and project libraries are installed inside this checkout. No Homebrew installation or global
package-manager setup is needed.

## Setup

From the repository root:

```bash
./scripts/bootstrap.sh
```

`scripts/toolchain.env` pins Python 3.14.9, Node 26.13.0 LTS, bundled npm 11.20.0 and pip 26.2.2. Bootstrap
downloads standalone CPython from `astral-sh/python-build-standalone` and Node from `nodejs.org`,
verifying their archives against committed SHA-256 checksums before extraction.

Generated directories are ignored by Git:

- `.local/python/` and `.local/node/`: versioned, self-contained language runtimes.
- `.local/cache/`, `.local/tmp/`, `.local/home/`, `.local/config/`, `.local/share/`, and `.local/state/`:
  downloads, package/tool caches, temporary files and process-local user directories.
- `.venv/`: Python environment based on the repository's standalone interpreter.
- `frontend/node_modules/`: frontend dependencies installed with `npm ci`.

Python installation uses `backend/requirements-dev.txt`, which includes runtime requirements and
the pinned Ruff/Black tools. `constraints.txt` and `constraints-dev.txt` pin indirect dependencies.
Bootstrap rejects an unpinned resolved dependency and requires binary wheels, avoiding implicit
compiler installations and unpinned build dependencies. The frontend uses the committed npm lockfile.

## Running commands

Use the command runner from the repository root:

```bash
# Targeted backend tests; disable the aggregate coverage threshold for focused runs
./scripts/local.sh backend python -m pytest tests/test_auth.py -v --no-cov

# Frontend tests and static checks
./scripts/local.sh frontend npm run test:run
./scripts/local.sh frontend npm run lint
./scripts/local.sh frontend ./node_modules/.bin/tsc --noEmit

# Canonical formatting and full pre-push validation, when explicitly requested
./scripts/format.sh
./scripts/pre-push.sh
```

`scripts/local.sh` accepts `root`, `backend` or `frontend` as its working directory, followed by a
command and its arguments. It verifies the local runtimes and uses a project-only toolchain PATH plus
basic OS utilities. It isolates HOME, XDG directories, temporary files and package-manager settings
for the child process. The calling shell's configuration is unchanged.

Format and pre-push scripts use the same environment. They invoke installed tools directly, so missing
tools fail instead of being downloaded by `npx`. Pre-push does not install dependencies; bootstrap is
the explicit installation step. Running bare system `python`, `npm` or `npx` bypasses this isolation.

Ask before launching tests, checks or formatters. Stop on a test failure and obtain approval before
changing code or tests. See `specs/testing.instructions.md` for validation boundaries.

## Recreating and updating

If the generated directories are deleted, rerun `./scripts/bootstrap.sh`. To replace an existing,
broken or outdated virtual environment and reinstall frontend dependencies:

```bash
./scripts/bootstrap.sh --recreate
```

This removes `.venv` and recreates it from the local interpreter; `npm ci` recreates `node_modules`.
Cached downloads and runtimes are reused. The generated folders contain no authoritative project
configuration and should not hold secrets or user data. After moving the checkout, recreate the
environment because virtualenv scripts contain absolute paths.

Review dependency updates in the committed requirements, constraints and npm lockfile. Runtime
updates require matching versions and archive checksums in `scripts/toolchain.env`; npm must match
the selected Node archive's bundled version. Keep exact Python, Node, npm and pip versions aligned
with CI and images. Use the local npm 11.20.0 when intentionally regenerating the frontend lockfile.
