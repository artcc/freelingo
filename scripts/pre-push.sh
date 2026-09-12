#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

source "${ROOT_DIR}/.venv/bin/activate"

python -m pip install --quiet pip==26.2.1
python -m pip install --quiet -r "${ROOT_DIR}/backend/requirements.txt"

"${ROOT_DIR}/scripts/format.sh"

pushd "${ROOT_DIR}/backend" >/dev/null
pytest -v
popd >/dev/null

pushd "${ROOT_DIR}/frontend" >/dev/null
npm run lint
npx tsc --noEmit
npm run test:run
popd >/dev/null
