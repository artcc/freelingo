#!/usr/bin/env bash
# stop-k8s.sh - convenience wrapper: quiesce the cluster, optionally power off.
#
#   ./stop-k8s.sh                 quiesce FreeLingo + app namespaces, cordon/drain
#   ./stop-k8s.sh --poweroff      also power off node1-node3 and node0
#   ./stop-k8s.sh --poweroff --yes
#
# Persistent data is kept. See stop.sh for the full behavior.
set -euo pipefail
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/stop.sh" --cluster "$@"
