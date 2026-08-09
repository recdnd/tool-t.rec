#!/bin/bash
# t-rec · localhost 薄殼（接 machine/specs/02-localhost.md）
# 本檔放在 <project>/rituals/ 內
#
# 從工具箱根起 server：一個 server 同時涵蓋 /notes/ 與 /bookmarks/。
# 只想單開某個工具時走該工具自己的 rituals/。

REC_PROJECT="t-rec"
REC_PORT="9090"
# REC_LOCAL_PATH="/"
# REC_BUILD_CMD=""
# REC_SERVE_CMD=""

REC_PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

_d="$REC_PROJECT_DIR"
while [[ "$_d" != "/" && ! -d "$_d/sov/machine/lib" ]]; do _d="$(dirname "$_d")"; done
[[ -d "$_d/sov/machine/lib" ]] || _d="$(cd "$REC_PROJECT_DIR/../../DungeonsRoot" 2>/dev/null && pwd)"
MACHINE_LIB="${MACHINE_LIB:-$_d/sov/machine/lib}"

source "$MACHINE_LIB/rec-serve.sh"
rec_serve "$@"
