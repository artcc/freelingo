#!/usr/bin/env bash
# create-registry-secret.sh - create the imagePullSecret for local-registry:5000.
# Run this yourself with registry credentials; nothing is written to disk.
#
# Usage:
#   REGISTRY_USER=... REGISTRY_PASSWORD=... ./create-registry-secret.sh
#   ./create-registry-secret.sh          # prompts
#
# Every FreeLingo pod references this Secret as freelingo-registry.
set -euo pipefail

NAMESPACE="${NAMESPACE:-freelingo}"
SECRET_NAME="${SECRET_NAME:-freelingo-registry}"
REGISTRY_HOST="${REGISTRY_HOST:-local-registry:5000}"

if [[ -z "${REGISTRY_USER:-}" ]]; then
  read -rp "Registry username: " REGISTRY_USER
fi
if [[ -z "${REGISTRY_PASSWORD:-}" ]]; then
  read -rsp "Registry password: " REGISTRY_PASSWORD
  echo
fi

kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f - >/dev/null

kubectl -n "${NAMESPACE}" create secret docker-registry "${SECRET_NAME}" \
  --docker-server="${REGISTRY_HOST}" \
  --docker-username="${REGISTRY_USER}" \
  --docker-password="${REGISTRY_PASSWORD}" \
  --docker-email="${REGISTRY_EMAIL:-none}" \
  --dry-run=client -o yaml | kubectl apply -f - >/dev/null

unset REGISTRY_PASSWORD

echo "Secret ${NAMESPACE}/${SECRET_NAME} created/updated for ${REGISTRY_HOST}."
