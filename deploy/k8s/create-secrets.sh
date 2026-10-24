#!/usr/bin/env bash
# create-secrets.sh - create or reuse the FreeLingo application Secret.
# Existing values are preserved so changing this script never rotates the
# database password or invalidates refresh tokens by accident.
set -euo pipefail

NAMESPACE="${NAMESPACE:-freelingo}"
SECRET_NAME="${SECRET_NAME:-freelingo-secrets}"

kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f - >/dev/null

existing() {
  kubectl -n "${NAMESPACE}" get secret "${SECRET_NAME}" \
    -o jsonpath="{.data.$1}" 2>/dev/null | base64 -d 2>/dev/null || true
}

POSTGRES_DB="$(existing POSTGRES_DB)"
POSTGRES_USER="$(existing POSTGRES_USER)"
POSTGRES_PASSWORD="$(existing POSTGRES_PASSWORD)"
REDIS_PASSWORD="$(existing REDIS_PASSWORD)"
SECRET_KEY="$(existing SECRET_KEY)"

POSTGRES_DB="${POSTGRES_DB:-freelingo}"
POSTGRES_USER="${POSTGRES_USER:-freelingo}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-$(openssl rand -hex 24)}"
REDIS_PASSWORD="${REDIS_PASSWORD:-$(openssl rand -hex 24)}"
SECRET_KEY="${SECRET_KEY:-$(openssl rand -hex 32)}"

kubectl -n "${NAMESPACE}" create secret generic "${SECRET_NAME}" \
  --from-literal=POSTGRES_DB="${POSTGRES_DB}" \
  --from-literal=POSTGRES_USER="${POSTGRES_USER}" \
  --from-literal=POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
  --from-literal=DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}" \
  --from-literal=REDIS_PASSWORD="${REDIS_PASSWORD}" \
  --from-literal=REDIS_URL="redis://:${REDIS_PASSWORD}@redis:6379/0" \
  --from-literal=SECRET_KEY="${SECRET_KEY}" \
  --dry-run=client -o yaml | kubectl apply -f - >/dev/null

echo "Secret ${NAMESPACE}/${SECRET_NAME} is present (existing values reused where available)."
