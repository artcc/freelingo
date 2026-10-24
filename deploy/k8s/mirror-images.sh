#!/usr/bin/env bash
# mirror-images.sh - copy every FreeLingo image into local-registry:5000.
#
# Usage:
#   ./mirror-images.sh                       # mirror all images from images.txt
#   ./mirror-images.sh --dry-run             # print actions, change nothing
#   ./mirror-images.sh --pin                 # also rewrite manifests to digests
#   ./mirror-images.sh --use-creds           # use the runner's registry logins
#   REGISTRY=local-repository:5000 ./mirror-images.sh
#
# Upstream sources are pulled anonymously by default. This avoids stale
# Docker Hub credentials in ~/.docker/config.json turning a public pull into
# "invalid username/password". Use --use-creds only when you have a valid
# Docker Hub login (useful to avoid anonymous rate limits).
#
# Run this on a workstation with internet access and Docker or skopeo
# (skopeo preferred: it copies multi-arch manifests without a local daemon).
# The cluster nodes never pull from upstream registries at runtime.
#
# Requirements on the runner (not the cluster):
#   - skopeo OR docker
#   - network access to ghcr.io, registry-1.docker.io, local-registry:5000
#   - docker login / skopeo login to the local registry when it is auth'd
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REGISTRY="${REGISTRY:-local-registry:5000}"
IMAGES_FILE="${IMAGES_FILE:-${SCRIPT_DIR}/images.txt}"
DIGEST_FILE="${DIGEST_FILE:-${SCRIPT_DIR}/digests.lock}"
MANIFESTS_DIR="${MANIFESTS_DIR:-${SCRIPT_DIR}/manifests}"
TOOL="${TOOL:-auto}" # auto | docker | skopeo
USE_SRC_CREDS="${USE_SRC_CREDS:-false}"
DRY_RUN=0
PIN=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --pin) PIN=1 ;;
    --use-creds) USE_SRC_CREDS=true ;;
    -h | --help)
      sed -n '2,32p' "$0"
      exit 0
      ;;
    *)
      echo "unknown arg: $arg" >&2
      exit 2
      ;;
  esac
done

if [[ "$TOOL" == "auto" ]]; then
  if command -v skopeo >/dev/null 2>&1; then
    TOOL=skopeo
  elif command -v docker >/dev/null 2>&1; then
    TOOL=docker
  else
    echo "need skopeo or docker on PATH" >&2
    exit 1
  fi
fi

run() {
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

# Destination path in the local registry. Strips upstream registry hosts and
# adds library/ for Docker Hub official images, matching images.txt comments.
dst_for() {
  local src="$1" repo tag
  if [[ "$src" == *"@"* ]]; then
    repo="${src%@*}"
    tag="${src##*@}"
  else
    repo="${src%:*}"
    tag="${src##*:}"
  fi
  repo="${repo#docker.io/}"
  repo="${repo#index.docker.io/}"
  repo="${repo#registry-1.docker.io/}"
  repo="${repo#ghcr.io/}"
  repo="${repo#quay.io/}"
  if [[ "$repo" != */* ]]; then
    repo="library/${repo}"
  fi
  if [[ "$src" == *"@"* ]]; then
    echo "${REGISTRY}/${repo}@${tag}"
  else
    echo "${REGISTRY}/${repo}:${tag}"
  fi
}

mirror_one() {
  local src="$1"
  local dst
  local -a copy_flags=()
  dst="$(dst_for "$src")"
  echo "==> ${src}"
  echo "    -> ${dst}"

  local dgst="sha256:dry-run"
  if [[ $DRY_RUN -eq 0 ]]; then
    if [[ "$TOOL" == "skopeo" ]]; then
      copy_flags=(--all --retry-times 5)
      if [[ "${USE_SRC_CREDS}" == "true" ]]; then
        if [[ -n "${SRC_CREDS:-}" ]]; then
          copy_flags+=(--src-creds "${SRC_CREDS}")
        fi
      else
        copy_flags+=(--src-no-creds)
      fi
      skopeo copy "${copy_flags[@]}" "docker://${src}" "docker://${dst}"
      dgst="$(skopeo inspect --retry-times 5 --format '{{.Digest}}' "docker://${dst}")"
    else
      docker pull "${src}"
      docker tag "${src}" "${dst}"
      docker push "${dst}"
      dgst="$(docker inspect --format '{{index .RepoDigests 0}}' "${dst}" | sed 's/.*@//')"
    fi
  fi

  printf '%s\t%s\t%s\n' "${src}" "${dst}" "${dgst}" >>"${DIGEST_FILE}.tmp"
}

: >"${DIGEST_FILE}.tmp"
trap 'rm -f "${DIGEST_FILE}.tmp"' EXIT

while IFS= read -r line; do
  line="${line%%#*}"
  line="$(echo "$line" | xargs)"
  [[ -z "$line" ]] && continue
  mirror_one "$line"
done <"${IMAGES_FILE}"

sort -o "${DIGEST_FILE}.tmp" "${DIGEST_FILE}.tmp"
run mv "${DIGEST_FILE}.tmp" "${DIGEST_FILE}"
echo
echo "Wrote ${DIGEST_FILE}"

if [[ $PIN -eq 1 ]]; then
  echo
  echo "Pinning manifests to digests..."
  while IFS=$'\t' read -r src dst dgst; do
    [[ -z "$dgst" || "$dgst" == "sha256:dry-run" ]] && continue
    pinned="${dst%:*}@${dgst}"
    while IFS= read -r f; do
      [[ -n "$f" ]] || continue
      if grep -qF "${dst}@${dgst}" "$f"; then
        continue
      fi
      run sed -i "s|${dst}|${pinned}|g" "$f"
      echo "  ${f}: ${pinned}"
    done < <(grep -RIlF --include='*.yaml' --include='*.yml' "$dst" "${MANIFESTS_DIR}" || true)
  done <"${DIGEST_FILE}"
fi
