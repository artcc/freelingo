#!/usr/bin/env bash
# prep-node.sh - verify (and optionally fix) one node's access to
# local-registry:5000. Run on the node itself, usually via:
#
#   ssh node1 sudo ./prep-node.sh
#
# This cluster already resolves local-registry and trusts its CA. The script
# is idempotent and verifies that before FreeLingo starts. It only edits
# /etc/hosts or installs a CA when APPLY=1.
set -euo pipefail

REGISTRY="${REGISTRY:-local-registry:5000}"
REGISTRY_HOST="${REGISTRY%%:*}"
REGISTRY_IP="${REGISTRY_IP:-192.168.10.30}"
REGISTRY_CA="${REGISTRY_CA:-}"
APPLY="${APPLY:-0}"

fail=0

resolved="$(getent hosts "${REGISTRY_HOST}" | awk '{print $1}' | head -1 || true)"
if [[ -n "${resolved}" ]]; then
  echo "OK   ${REGISTRY_HOST} resolves to ${resolved}"
else
  echo "WARN ${REGISTRY_HOST} does not resolve on $(hostname)"
  if [[ "${APPLY}" == "1" ]]; then
    printf '%s %s\n' "${REGISTRY_IP}" "${REGISTRY_HOST}" >>/etc/hosts
    echo "     added ${REGISTRY_IP} ${REGISTRY_HOST} to /etc/hosts"
  else
    fail=1
  fi
fi

if [[ -n "${REGISTRY_CA}" && -f "${REGISTRY_CA}" ]]; then
  cp "${REGISTRY_CA}" "/usr/local/share/ca-certificates/${REGISTRY_HOST}.crt"
  update-ca-certificates >/dev/null
  echo "OK   installed ${REGISTRY_CA} into the system trust store"
elif [[ -f "/usr/local/share/ca-certificates/${REGISTRY_HOST}.crt" ]] ||
  [[ -f "/usr/local/share/ca-certificates/local-registry.crt" ]]; then
  echo "OK   ${REGISTRY_HOST} CA is present in the system trust store"
else
  echo "WARN no ${REGISTRY_HOST} CA found in /usr/local/share/ca-certificates"
  echo "     set REGISTRY_CA=/path/to/ca.crt APPLY=1 to install it"
  fail=1
fi

if grep -qs 'config_path.*certs.d' /etc/containerd/config.toml; then
  echo "OK   containerd loads registry certs from certs.d"
else
  echo "INFO containerd has no certs.d config_path; it will use the system CA"
fi

if command -v curl >/dev/null 2>&1; then
  code="$(curl -sk -o /dev/null -w '%{http_code}' "https://${REGISTRY}/v2/" || true)"
  echo "INFO https://${REGISTRY}/v2/ returned HTTP ${code} (401 is expected with auth)"
fi

exit "${fail}"
