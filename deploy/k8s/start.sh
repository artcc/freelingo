#!/usr/bin/env bash
# start.sh - give FreeLingo the whole homelab and bring it up.
#
#   1. Uncordons node1-node3.
#   2. Pauses other application namespaces (recording their replica counts).
#   3. Applies the manifests and waits for every rollout.
#
# Environment:
#   NAMESPACE=freelingo
#   REGISTRY=local-registry:5000
#   PAUSE_OTHERS=true            # false: do not touch other namespaces
#   PAUSE_NAMESPACES="gpu-plane speech synanton"
#   TIMEOUT=900                  # seconds per rollout
#   APPLY=true                   # false: only scale up existing objects
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="${NAMESPACE:-freelingo}"
REGISTRY="${REGISTRY:-local-registry:5000}"
WORKERS=(node1 node2 node3)
PAUSE_OTHERS="${PAUSE_OTHERS:-true}"
PAUSE_NAMESPACES="${PAUSE_NAMESPACES:-gpu-plane speech synanton}"
TIMEOUT="${TIMEOUT:-900}"
APPLY="${APPLY:-true}"
WAIT_GPU="${WAIT_GPU:-true}"
ANNOTATION="freelingo.io/prev-replicas"

log() { printf '[start] %s\n' "$*"; }
die() { printf '[start] error: %s\n' "$*" >&2; exit 1; }

command -v kubectl >/dev/null 2>&1 || die "kubectl not found"
kubectl get ns >/dev/null 2>&1 || die "cannot reach the Kubernetes API"

log "waiting for worker nodes to be Ready"
for n in "${WORKERS[@]}"; do
  for _ in $(seq 1 120); do
    status="$(kubectl get node "$n" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}' 2>/dev/null || true)"
    [[ "${status}" == "True" ]] && break
    sleep 5
  done
  [[ "${status:-}" == "True" ]] || die "node $n did not become Ready"
  log "node $n is Ready"
done

if [[ "${WAIT_GPU}" == "true" ]]; then
  log "waiting for the NVIDIA device plugin on workers"
  for n in "${WORKERS[@]}"; do
    for _ in $(seq 1 36); do
      gpu="$(kubectl get node "$n" -o jsonpath='{.status.allocatable.nvidia\.com/gpu}' 2>/dev/null || true)"
      ready="$(kubectl -n kube-system get pods -l name=nvidia-device-plugin-ds \
        --field-selector "spec.nodeName=${n}" \
        -o jsonpath='{.items[0].status.containerStatuses[0].ready}' 2>/dev/null || true)"
      [[ -n "${gpu}" && "${gpu}" != "0" && "${ready}" == "true" ]] && break
      sleep 5
    done
    if [[ -n "${gpu}" && "${gpu}" != "0" && "${ready}" == "true" ]]; then
      log "node $n: nvidia.com/gpu=${gpu}"
    else
      log "warning: GPU plugin on $n not ready (gpu=${gpu:-?} ready=${ready:-?})"
    fi
  done
fi

for n in "${WORKERS[@]}"; do
  if kubectl get node "$n" >/dev/null 2>&1; then
    kubectl uncordon "$n" >/dev/null
    log "uncordoned $n"
  else
    log "warning: node $n not found; skipping uncordon"
  fi
done

if [[ "${PAUSE_OTHERS}" == "true" ]]; then
  for ns in ${PAUSE_NAMESPACES}; do
    kubectl get ns "$ns" >/dev/null 2>&1 || continue
    paused=0
    for kind in deployment statefulset; do
      mapfile -t names < <(kubectl -n "$ns" get "$kind" \
        -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' 2>/dev/null || true)
      for name in "${names[@]}"; do
        [[ -n "$name" ]] || continue
        prev="$(kubectl -n "$ns" get "$kind" "$name" -o jsonpath='{.spec.replicas}' 2>/dev/null || echo 0)"
        saved="$(kubectl -n "$ns" get "$kind" "$name" \
          -o jsonpath="{.metadata.annotations.freelingo\.io/prev-replicas}" 2>/dev/null || true)"
        if [[ -z "$saved" ]]; then
          kubectl -n "$ns" annotate "$kind" "$name" "${ANNOTATION}=${prev}" --overwrite >/dev/null
        fi
        kubectl -n "$ns" scale "$kind" "$name" --replicas=0 >/dev/null
        paused=$((paused + 1))
      done
    done
    log "paused ${paused} workload(s) in namespace ${ns}"
  done

  for ns in ${PAUSE_NAMESPACES}; do
    kubectl get ns "$ns" >/dev/null 2>&1 || continue
    for _ in $(seq 1 60); do
      count="$(kubectl -n "$ns" get pods --no-headers 2>/dev/null | wc -l)"
      [[ "${count}" -eq 0 ]] && break
      sleep 2
    done
    log "namespace ${ns} has no running pods"
  done
fi

kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f - >/dev/null

if ! kubectl -n "${NAMESPACE}" get secret freelingo-secrets >/dev/null 2>&1; then
  die "missing Secret ${NAMESPACE}/freelingo-secrets; run ${SCRIPT_DIR}/bootstrap.sh"
fi
if ! kubectl -n "${NAMESPACE}" get secret freelingo-tls >/dev/null 2>&1; then
  die "missing Secret ${NAMESPACE}/freelingo-tls; run ${SCRIPT_DIR}/bootstrap.sh"
fi
if ! kubectl -n "${NAMESPACE}" get secret freelingo-registry >/dev/null 2>&1; then
  cat >&2 <<EOF
[start] error: missing Secret ${NAMESPACE}/freelingo-registry.
Create it yourself with your registry credentials:

  kubectl -n ${NAMESPACE} create secret docker-registry freelingo-registry \\
    --docker-server=${REGISTRY} \\
    --docker-username='<registry-user>' \\
    --docker-password='<registry-password>' \\
    --docker-email='none' \\
    --dry-run=client -o yaml | kubectl apply -f -

Or run ${SCRIPT_DIR}/create-registry-secret.sh interactively.
EOF
  exit 1
fi

if [[ "${APPLY}" == "true" ]]; then
  kubectl apply -f "${SCRIPT_DIR}/manifests/" >/dev/null
  log "applied manifests from ${SCRIPT_DIR}/manifests"
fi

# Guardrail: no pod may reference an upstream registry at runtime.
bad="$(
  kubectl -n "${NAMESPACE}" get deploy,statefulset -o jsonpath='{range .items[*]}{range .spec.template.spec.initContainers[*]}{.image}{"\n"}{end}{range .spec.template.spec.containers[*]}{.image}{"\n"}{end}{end}' |
    grep -v "^${REGISTRY}/" || true
)"
if [[ -n "${bad}" ]]; then
  printf '[start] error: non-mirrored image reference(s) found:\n%s\n' "${bad}" >&2
  printf '[start] every image must start with %s/\n' "${REGISTRY}" >&2
  exit 1
fi
log "all workload images come from ${REGISTRY}"

for d in postgres redis backend frontend kokoro whisper llm traefik; do
  log "waiting for deployment/${d}"
  kubectl -n "${NAMESPACE}" rollout status "deployment/${d}" --timeout="${TIMEOUT}s"
done

log "FreeLingo is running"
log "  https://freelingo.local:30444 (map freelingo.local to any node IP)"
log "  https://192.168.10.31:30444"
