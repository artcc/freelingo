#!/usr/bin/env bash
# bootstrap.sh - one-time FreeLingo prerequisites.
#
# Creates the namespace, generated application Secret, and TLS Secret.
# The registry pull Secret is deliberately NOT created here: run the printed
# command yourself with your registry credentials (or use
# create-registry-secret.sh).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="${NAMESPACE:-freelingo}"
REGISTRY="${REGISTRY:-local-registry:5000}"

kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f - >/dev/null

"${SCRIPT_DIR}/create-secrets.sh"
"${SCRIPT_DIR}/generate-cert.sh"

echo
if kubectl -n "${NAMESPACE}" get secret freelingo-registry >/dev/null 2>&1; then
  echo "Registry pull Secret ${NAMESPACE}/freelingo-registry already exists."
else
  cat <<EOF
Registry pull Secret is missing. Run this yourself (credentials are not stored):

  kubectl -n ${NAMESPACE} create secret docker-registry freelingo-registry \\
    --docker-server=${REGISTRY} \\
    --docker-username='<registry-user>' \\
    --docker-password='<registry-password>' \\
    --docker-email='none' \\
    --dry-run=client -o yaml | kubectl apply -f -

Or interactively:

  ${SCRIPT_DIR}/create-registry-secret.sh
EOF
fi

cat <<EOF

Next:
  1. Mirror images from a workstation with internet access:
       ${SCRIPT_DIR}/mirror-images.sh
     Optional reproducible pinning:
       ${SCRIPT_DIR}/mirror-images.sh --pin

  2. Verify node runtime trust (already configured on this cluster):
       for n in node1 node2 node3; do
         scp ${SCRIPT_DIR}/prep-node.sh \$n:/tmp/prep-node.sh
         ssh \$n sudo /tmp/prep-node.sh
       done

  3. Start or stop FreeLingo:
       ${SCRIPT_DIR}/start.sh
       ${SCRIPT_DIR}/stop.sh
EOF
