#!/usr/bin/env bash
# stop.sh - stop FreeLingo, or quiesce/power off the whole homelab cluster.
#
# Modes:
#   ./stop.sh                 Stop FreeLingo only, keep PVCs/Secrets, restore
#                             the namespaces paused by start.sh.
#   ./stop.sh --cluster       Stop FreeLingo and quiesce all application
#                             namespaces, then cordon + drain the workers.
#   ./stop.sh --cluster --poweroff
#                             Also power off node1-node3 and node0 over SSH.
#
# Persistent data is never deleted. PostgreSQL, Redis, avatars, audio, TTS
# previews, Secrets, and Ingress objects stay in Longhorn/etcd. Node-local
# model caches stay on the node disks.
#
# Environment:
#   NAMESPACE=freelingo
#   RESTORE_OTHERS=true          # FreeLingo-only mode
#   PAUSE_NAMESPACES="gpu-plane speech synanton"
#   CONTROL_PLANE=node0
#   WORKERS="node1 node2 node3"
set -euo pipefail

NAMESPACE="${NAMESPACE:-freelingo}"
RESTORE_OTHERS="${RESTORE_OTHERS:-true}"
PAUSE_NAMESPACES="${PAUSE_NAMESPACES:-gpu-plane speech synanton}"
CONTROL_PLANE="${CONTROL_PLANE:-node0}"
WORKERS="${WORKERS:-node1 node2 node3}"
ANNOTATION="freelingo.io/prev-replicas"

CLUSTER=false
POWEROFF=false
ASSUME_YES=false
SKIP_SNAPSHOT=false

for arg in "$@"; do
  case "$arg" in
    --cluster) CLUSTER=true ;;
    --poweroff) POWEROFF=true; CLUSTER=true ;;
    --yes) ASSUME_YES=true ;;
    --skip-snapshot) SKIP_SNAPSHOT=true ;;
    -h | --help)
      awk 'NR>1 && /^set -euo pipefail/{exit} NR>1{print}' "$0"
      exit 0
      ;;
    *)
      echo "unknown arg: $arg" >&2
      exit 2
      ;;
  esac
done

log() { printf '[stop] %s\n' "$*"; }
warn() { printf '[stop] warning: %s\n' "$*" >&2; }
die() { printf '[stop] error: %s\n' "$*" >&2; exit 1; }

command -v kubectl >/dev/null 2>&1 || die "kubectl not found"
kubectl get ns >/dev/null 2>&1 || die "cannot reach the Kubernetes API"

scale_namespace_to_zero() {
  local ns="$1" record="$2"
  kubectl get ns "$ns" >/dev/null 2>&1 || return 0
  local kind name current saved
  for kind in deployment statefulset; do
    while IFS= read -r name; do
      [[ -n "$name" ]] || continue
      current="$(kubectl -n "$ns" get "$kind" "$name" -o jsonpath='{.spec.replicas}' 2>/dev/null || echo 0)"
      if [[ "$record" == "true" ]]; then
        saved="$(kubectl -n "$ns" get "$kind" "$name" \
          -o jsonpath="{.metadata.annotations.freelingo\.io/prev-replicas}" 2>/dev/null || true)"
        if [[ -z "$saved" ]]; then
          kubectl -n "$ns" annotate "$kind" "$name" "${ANNOTATION}=${current}" --overwrite >/dev/null
        fi
      fi
      kubectl -n "$ns" scale "$kind" "$name" --replicas=0 >/dev/null
      log "scaled ${ns}/${kind}/${name} to 0"
    done < <(kubectl -n "$ns" get "$kind" -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' 2>/dev/null || true)
  done
}

wait_namespace_empty() {
  local ns="$1" timeout="${2:-180}"
  kubectl get ns "$ns" >/dev/null 2>&1 || return 0
  local deadline=$(( $(date +%s) + timeout ))
  while true; do
    local count
    count="$(kubectl -n "$ns" get pods --no-headers 2>/dev/null | wc -l)"
    [[ "$count" -eq 0 ]] && return 0
    if (( $(date +%s) > deadline )); then
      warn "${count} pod(s) still present in ${ns}; continuing"
      return 0
    fi
    sleep 2
  done
}

restore_paused_namespaces() {
  local ns kind name prev
  for ns in ${PAUSE_NAMESPACES}; do
    kubectl get ns "$ns" >/dev/null 2>&1 || continue
    local restored=0
    for kind in deployment statefulset; do
      while IFS= read -r name; do
        [[ -n "$name" ]] || continue
        prev="$(kubectl -n "$ns" get "$kind" "$name" \
          -o jsonpath="{.metadata.annotations.freelingo\.io/prev-replicas}" 2>/dev/null || true)"
        [[ -n "$prev" ]] || continue
        kubectl -n "$ns" scale "$kind" "$name" --replicas="${prev}" >/dev/null
        kubectl -n "$ns" annotate "$kind" "$name" "${ANNOTATION}-" >/dev/null
        restored=$((restored + 1))
      done < <(kubectl -n "$ns" get "$kind" -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' 2>/dev/null || true)
    done
    log "restored ${restored} workload(s) in namespace ${ns}"
  done
}

etcd_snapshot() {
  [[ "$SKIP_SNAPSHOT" == "true" ]] && return 0
  local ts
  ts="$(date +%F-%H%M%S)"
  log "saving an etcd snapshot on ${CONTROL_PLANE} (sudo may prompt)"
  ssh -t "${CONTROL_PLANE}" "sudo ETCDCTL_API=3 etcdctl snapshot save /var/backups/etcd-snapshot-${ts}.db \
    --endpoints=https://127.0.0.1:2379 \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key" ||
    warn "etcd snapshot failed or was skipped; continuing"
}

# --- FreeLingo -------------------------------------------------------------
if kubectl get ns "${NAMESPACE}" >/dev/null 2>&1; then
  log "stopping FreeLingo workloads (PVCs and Secrets are kept)"
  scale_namespace_to_zero "${NAMESPACE}" false
  wait_namespace_empty "${NAMESPACE}" 180
  log "FreeLingo pods are gone; GPU memory is released"
else
  log "namespace ${NAMESPACE} does not exist"
fi

# --- FreeLingo-only mode ---------------------------------------------------
if [[ "$CLUSTER" != "true" ]]; then
  if [[ "$RESTORE_OTHERS" == "true" ]]; then
    restore_paused_namespaces
  fi
  log "FreeLingo stopped; data volumes and Secrets were kept"
  exit 0
fi

# --- Whole-cluster quiesce -------------------------------------------------
log "quiescing application namespaces: ${PAUSE_NAMESPACES}"
for ns in ${PAUSE_NAMESPACES}; do
  scale_namespace_to_zero "$ns" true
  wait_namespace_empty "$ns" 180
done

log "cordoning workers: ${WORKERS}"
for n in ${WORKERS}; do
  kubectl cordon "$n" >/dev/null 2>&1 || warn "could not cordon $n"
done

log "draining workers"
for n in ${WORKERS}; do
  kubectl drain "$n" --ignore-daemonsets --delete-emptydir-data --force --timeout=180s ||
    warn "drain of $n finished with warnings"
done

log "workers quiesced. FreeLingo data, Secrets, etcd, and model caches were kept"

if [[ "$POWEROFF" != "true" ]]; then
  cat <<EOF

Nodes are cordoned and drained. Power them off manually, or re-run:

  $0 --cluster --poweroff

EOF
  exit 0
fi

etcd_snapshot

if [[ "$ASSUME_YES" != "true" ]]; then
  cat <<EOF

This will run 'sudo shutdown -h now' over SSH on:
  ${WORKERS} (workers), then ${CONTROL_PLANE} (control plane)

You may be prompted for the sudo password on each node.
EOF
  read -rp "Type 'yes' to continue: " reply
  [[ "$reply" == "yes" ]] || die "aborted; nodes remain quiesced, not powered off"
fi

log "powering off workers"
for n in ${WORKERS}; do
  ssh -t "$n" 'sudo shutdown -h now' || warn "could not confirm shutdown on $n"
done

log "powering off control plane ${CONTROL_PLANE}"
ssh -t "${CONTROL_PLANE}" 'sudo shutdown -h now' || warn "could not confirm shutdown on ${CONTROL_PLANE}"

log "shutdown requested on all nodes"
