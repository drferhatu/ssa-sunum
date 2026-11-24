#!/bin/zsh
# index.html'i Chrome ile 16:9 (1440x810) sayfalı PDF'e çevirir -> ssa-sunum.pdf
cd "$(dirname "$0")/.." || exit 1
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-pdf-header-footer --virtual-time-budget=15000 --run-all-compositor-stages-before-draw \
  --print-to-pdf="$PWD/ssa-sunum.pdf" "file://$PWD/index.html" 2>/dev/null
ls -la ssa-sunum.pdf
