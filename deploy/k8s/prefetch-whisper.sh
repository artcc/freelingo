#!/usr/bin/env bash
# prefetch-whisper.sh - seed the faster-whisper model cache on a node.
#
# The cluster has no internet egress at runtime. This script downloads the
# model on the workstation (Docker required), copies it through a temporary
# Pod to the node's hostPath, and restarts the offline whisper Deployment.
#
# Usage:
#   ./prefetch-whisper.sh                 # download and copy if not cached
#   FORCE=1 ./prefetch-whisper.sh         # re-download the snapshot
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="${NAMESPACE:-freelingo}"
NODE="${WHISPER_NODE:-node2}"
MODEL="${WHISPER_MODEL:-large-v3-turbo}"
REPO="${WHISPER_REPO:-mobiuslabsgmbh/faster-whisper-large-v3-turbo}"
HOST_PATH="${WHISPER_HOST_PATH:-/opt/freelingo/whisper}"
CACHE_DIR="${WHISPER_CACHE_DIR:-/tmp/freelingo-whisper-cache}"
COPY_POD="whisper-cache-copy"
FORCE="${FORCE:-0}"

command -v docker >/dev/null 2>&1 || {
  echo "docker is required on this workstation" >&2
  exit 1
}

cleanup() {
  kubectl -n "${NAMESPACE}" delete pod "${COPY_POD}" --ignore-not-found >/dev/null 2>&1 || true
}
trap cleanup EXIT

mkdir -p "${CACHE_DIR}"

if [[ "${FORCE}" == "1" || ! -d "${CACHE_DIR}/models--${REPO//\//--}" ]]; then
  echo "Downloading ${REPO} into ${CACHE_DIR} ..."
  docker run --rm -v "${CACHE_DIR}:/cache" python:3.12-slim sh -c \
    "pip install -q --no-cache-dir huggingface_hub && \
     python -c \"from huggingface_hub import snapshot_download; print(snapshot_download('${REPO}', cache_dir='/cache'))\""
  # The container runs as root; make the cache readable by the copy Pod.
  docker run --rm -v "${CACHE_DIR}:/cache" python:3.12-slim chmod -R a+rX /cache
else
  echo "Using cached snapshot in ${CACHE_DIR}"
fi

kubectl -n "${NAMESPACE}" delete pod "${COPY_POD}" --ignore-not-found >/dev/null 2>&1 || true
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: ${COPY_POD}
  namespace: ${NAMESPACE}
spec:
  nodeName: ${NODE}
  restartPolicy: Never
  imagePullSecrets:
    - name: freelingo-registry
  containers:
    - name: copy
      image: local-registry:5000/library/postgres:16-alpine
      imagePullPolicy: IfNotPresent
      command: ["sh", "-c", "sleep 3600"]
      volumeMounts:
        - name: cache
          mountPath: /models
  volumes:
    - name: cache
      hostPath:
        path: ${HOST_PATH}
        type: DirectoryOrCreate
EOF

kubectl -n "${NAMESPACE}" wait --for=condition=Ready "pod/${COPY_POD}" --timeout=180s
echo "Copying cache to ${NODE}:${HOST_PATH} ..."
tar -C "${CACHE_DIR}" -cf - . | kubectl -n "${NAMESPACE}" exec -i "${COPY_POD}" -- tar -xf - -C /models

echo "Restarting whisper with the offline cache..."
kubectl -n "${NAMESPACE}" apply -f "${SCRIPT_DIR}/manifests/41-whisper.yaml" >/dev/null
kubectl -n "${NAMESPACE}" rollout restart deployment/whisper >/dev/null
kubectl -n "${NAMESPACE}" rollout status deployment/whisper --timeout=600s

echo "Whisper model ${MODEL} is available on ${NODE}."
