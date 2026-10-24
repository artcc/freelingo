#!/usr/bin/env bash
# generate-cert.sh - create the self-signed TLS Secret used by the Ingress.
# The certificate covers freelingo.local and the cluster node addresses, so
# both https://freelingo.local:30444 and https://<node-ip>:30444 work.
set -euo pipefail

NAMESPACE="${NAMESPACE:-freelingo}"
SECRET_NAME="${SECRET_NAME:-freelingo-tls}"
SAN_DNS="${SAN_DNS:-freelingo.local}"
# Both cluster networks. Node3's 192.168.18.x address is .167, not .33.
SAN_IPS="${SAN_IPS:-192.168.10.30 192.168.10.31 192.168.10.32 192.168.10.33 192.168.18.30 192.168.18.31 192.168.18.32 192.168.18.33}"
FORCE=0

for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    -h | --help)
      sed -n '2,8p' "$0"
      exit 0
      ;;
    *)
      echo "unknown arg: $arg" >&2
      exit 2
      ;;
  esac
done

kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f - >/dev/null

if kubectl -n "${NAMESPACE}" get secret "${SECRET_NAME}" >/dev/null 2>&1 && [[ $FORCE -eq 0 ]]; then
  echo "Secret ${NAMESPACE}/${SECRET_NAME} already exists; use --force to replace it."
  exit 0
fi

tmp="$(mktemp -d)"
trap 'rm -rf "${tmp}"' EXIT

san="DNS:${SAN_DNS}"
for ip in ${SAN_IPS}; do
  san="${san},IP:${ip}"
done

openssl req -x509 -nodes -newkey rsa:2048 -days 825 \
  -keyout "${tmp}/tls.key" \
  -out "${tmp}/tls.crt" \
  -subj "/CN=${SAN_DNS}" \
  -addext "subjectAltName=${san}" \
  >/dev/null 2>&1

kubectl -n "${NAMESPACE}" create secret tls "${SECRET_NAME}" \
  --cert="${tmp}/tls.crt" \
  --key="${tmp}/tls.key" \
  --dry-run=client -o yaml | kubectl apply -f - >/dev/null

echo "Secret ${NAMESPACE}/${SECRET_NAME} created."
