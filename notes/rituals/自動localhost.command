#!/bin/bash
# t-rec/notes · localhost 薄殼（接 machine/specs/02-localhost.md）
# 本檔放在 <project>/rituals/ 內
#
# ⚠️ localStorage 綁 origin。用本薄殼（127.0.0.1:9091）與從工具箱根開
#    （127.0.0.1:9090/notes/）是**同一個 origin**，資料互通；
#    但與 file:// 直開是**不同 origin**，記事不會出現。要看舊資料就固定用同一個入口。

REC_PROJECT="t-rec/notes"
REC_PORT="9091"
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
