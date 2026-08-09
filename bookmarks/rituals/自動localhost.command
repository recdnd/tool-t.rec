#!/bin/bash
# t-rec/bookmarks · localhost 薄殼（接 machine/specs/02-localhost.md）
# 本檔放在 <project>/rituals/ 內
#
# ⚠️ localStorage 綁 origin。本工具原先跑在 https://exe.rec.ooo/b/，
#    搬到本機後是**全新的空間**，舊書籤不會自動出現（見 README「白屏」段）。
#    舊資料需從 exe.rec.ooo/b/ 手動匯出後重建，或接受從零開始。

REC_PROJECT="t-rec/bookmarks"
REC_PORT="9092"
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
