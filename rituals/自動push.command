#!/bin/bash
# t-rec · push 薄殼（接 machine/specs/01-deploy.md）

REC_PROJECT="t-rec"
REC_DEPLOY_URL="https://t.rec.ooo"

REC_PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

_d="$REC_PROJECT_DIR"
while [[ "$_d" != "/" && ! -d "$_d/sov/machine/lib" ]]; do _d="$(dirname "$_d")"; done
[[ -d "$_d/sov/machine/lib" ]] || _d="$(cd "$REC_PROJECT_DIR/../../DungeonsRoot" 2>/dev/null && pwd)"
MACHINE_LIB="${MACHINE_LIB:-$_d/sov/machine/lib}"

source "$MACHINE_LIB/rec-push.sh"
rec_push "$@"
