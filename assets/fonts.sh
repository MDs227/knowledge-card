#!/usr/bin/env bash
# 安裝 Iansui（芫荽）繁體手寫體 — SIL OFL 1.1，可商用
# 注意：raw.githubusercontent.com 在部分沙箱被擋（403），必須走 Releases 直連。
set -euo pipefail
DEST="${HOME}/.fonts"
mkdir -p "$DEST" "/tmp/kc-fonts"

if fc-list 2>/dev/null | grep -qi iansui; then
  echo "[fonts] Iansui 已安裝，略過"; exit 0
fi

cd /tmp/kc-fonts
echo "[fonts] 下載 Iansui …"
curl -fsSL --max-time 120 -o iansui.zip \
  "https://github.com/ButTaiwan/iansui/releases/latest/download/Iansui.zip"
unzip -o -q iansui.zip
find . -iname "Iansui*.ttf" -exec cp {} "$DEST"/ \;
find . -iname "OFL.txt" -exec cp {} "$DEST"/Iansui-OFL.txt \; 2>/dev/null || true
fc-cache -f >/dev/null 2>&1

if fc-list | grep -qi iansui; then
  echo "[fonts] OK：$(fc-list | grep -i iansui | head -1)"
else
  echo "[fonts] 失敗——將 fallback 到 Noto Sans CJK TC（手寫感會消失，請告知使用者）" >&2
  exit 1
fi
