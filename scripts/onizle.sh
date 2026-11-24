#!/bin/zsh
# ssa-sunum.pdf sayfalarını 2x3'lük önizleme tabakalarına çevirir. Kullanım: onizle.sh <cikti_dizini>
cd "$(dirname "$0")/.." || exit 1
O="$1"; rm -rf "$O"; mkdir -p "$O"
pdftoppm -r 68 -png ssa-sunum.pdf "$O/s"
/opt/miniconda3/envs/ferhat_ml/bin/python - "$O" <<'PY'
import sys, glob
from PIL import Image
o = sys.argv[1]; ims = [Image.open(f) for f in sorted(glob.glob(o + "/s-*.png"))]; w, h = ims[0].size
for part in range(0, len(ims), 6):
    sh = Image.new("RGB", (w * 2, h * 3), "white")
    for i, im in enumerate(ims[part:part + 6]): sh.paste(im, ((i % 2) * w, (i // 2) * h))
    sh.save(f"{o}/sheet{part // 6}.png")
print(len(ims), "sayfa", w, h)
PY
