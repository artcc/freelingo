#!/bin/bash
# Shared by the local command runner and bootstrap; does not modify the caller's shell.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
source "${ROOT_DIR}/scripts/toolchain.env"
LOCAL_DIR="${ROOT_DIR}/.local"
PYTHON_HOME="${LOCAL_DIR}/python/${PYTHON_VERSION}-${PYTHON_BUILD}"
NODE_HOME="${LOCAL_DIR}/node/${NODE_VERSION}"

local_fail() {
  printf '%s\n' "$*" >&2
  exit 1
}

# These directories are disposable, but must never redirect writes outside the checkout.
for directory in "${LOCAL_DIR}" "${ROOT_DIR}/.venv" "${ROOT_DIR}/frontend/node_modules"; do
  [[ ! -L "${directory}" ]] || local_fail "Refusing symlinked directory: ${directory}"
done

# Ignore inherited package-manager settings and runtime injection paths.
while IFS= read -r variable; do
  case "${variable}" in
    PIP_*|NPM_CONFIG_*|npm_config_*|PYTHONPATH|PYTHONHOME|PYTHONUSERBASE|NODE_PATH|NODE_OPTIONS|VIRTUAL_ENV|PYTEST_ADDOPTS)
      unset "${variable}"
      ;;
  esac
done < <(compgen -v)
unset variable directory

export HOME="${LOCAL_DIR}/home"
export XDG_CACHE_HOME="${LOCAL_DIR}/cache"
export XDG_CONFIG_HOME="${LOCAL_DIR}/config"
export XDG_DATA_HOME="${LOCAL_DIR}/share"
export XDG_STATE_HOME="${LOCAL_DIR}/state"
export TMPDIR="${LOCAL_DIR}/tmp"
export TMP="${TMPDIR}" TEMP="${TMPDIR}"
export VIRTUAL_ENV="${ROOT_DIR}/.venv"
export PATH="${VIRTUAL_ENV}/bin:${NODE_HOME}/bin:${ROOT_DIR}/frontend/node_modules/.bin:/usr/bin:/bin:/usr/sbin:/sbin"
export PYTHONNOUSERSITE=1
export PIP_CONFIG_FILE=/dev/null
export PIP_REQUIRE_VIRTUALENV=true
export PIP_INDEX_URL=https://pypi.org/simple
export PIP_CACHE_DIR="${XDG_CACHE_HOME}/pip"
export PIP_DISABLE_PIP_VERSION_CHECK=1
# No implicit compiler or unpinned build-environment dependencies.
export PIP_ONLY_BINARY=:all:
export NPM_CONFIG_CACHE="${XDG_CACHE_HOME}/npm"
export NPM_CONFIG_USERCONFIG="${XDG_CONFIG_HOME}/npmrc"
export NPM_CONFIG_GLOBALCONFIG="${XDG_CONFIG_HOME}/npm-globalrc"
export NPM_CONFIG_PREFIX="${LOCAL_DIR}/npm"
export NPM_CONFIG_REGISTRY=https://registry.npmjs.org/
export NPM_CONFIG_YES=false
export NPM_CONFIG_AUDIT=false
export NPM_CONFIG_FUND=false
export NPM_CONFIG_UPDATE_NOTIFIER=false
export BLACK_CACHE_DIR="${XDG_CACHE_HOME}/black"
export RUFF_CACHE_DIR="${XDG_CACHE_HOME}/ruff"
export PYTEST_ADDOPTS="-o cache_dir=\"${XDG_CACHE_HOME}/pytest\""
export NEXT_TELEMETRY_DISABLED=1

mkdir -p "${HOME}" "${XDG_CACHE_HOME}" "${XDG_CONFIG_HOME}" "${XDG_DATA_HOME}" \
  "${XDG_STATE_HOME}" "${TMPDIR}"

require_local_runtimes() {
  [[ -x "${VIRTUAL_ENV}/bin/python" && -x "${NODE_HOME}/bin/node" ]] ||
    local_fail 'Local runtimes are missing. Run ./scripts/bootstrap.sh.'
  "${VIRTUAL_ENV}/bin/python" -c \
    'import pathlib, sys; assert sys.version.split()[0] == sys.argv[1]; assert pathlib.Path(sys.base_prefix).resolve() == pathlib.Path(sys.argv[2]).resolve()' \
    "${PYTHON_VERSION}" "${PYTHON_HOME}" ||
    local_fail 'Python does not match the local toolchain. Run ./scripts/bootstrap.sh --recreate.'
  [[ "$("${NODE_HOME}/bin/node" --version)" == "v${NODE_VERSION}" ]] ||
    local_fail 'Node does not match scripts/toolchain.env.'
  [[ "$("${NODE_HOME}/bin/node" -p 'require(process.argv[1]).version' "${NODE_HOME}/lib/node_modules/npm/package.json")" == "${NPM_VERSION}" ]] ||
    local_fail 'The bundled npm does not match scripts/toolchain.env.'
}
