"""Nadiri tefsir API'sinden (localhost:3000) yiyecek ayetlerini çeker, data/ayetler.json'a yazar."""
import json, re, sys, html, urllib.request
from pathlib import Path

BASE = "http://localhost:3000/api/ayet/{}/{}"
LISTE = [(2,57),(2,61),(2,168),(2,172),(2,261),(5,96),(5,114),(6,99),(6,141),(7,31),(12,47),(13,4),
         (16,11),(16,14),(16,66),(16,67),(16,68),(18,19),(19,25),(20,81),(21,30),(21,47),(23,19),(24,35),
         (31,16),(35,12),(36,33),(37,146),(47,15),(55,10),(55,68),(56,20),(56,28),(76,5),(76,17),(80,24),(95,1)]

def duz(h):
    h = re.sub(r"<p[^>]*>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    return html.unescape(h).strip()

out = {}
for s, a in LISTE:
    try:
        d = json.load(urllib.request.urlopen(BASE.format(s, a), timeout=10))
    except Exception as e:
        print("HATA", s, a, e); continue
    ay = d["ayet"]
    paras = re.findall(r"<p[^>]*>.*?</p>", ay["html"], flags=re.S)
    arapca = duz(paras[0]) if paras else ""
    metin = duz("".join(paras[1:]))
    out[f"{s}:{a}"] = {"sure": d["sure"]["ad"], "baslik": ay["baslik"], "bas": ay["bas"], "son": ay["son"],
                       "arapca": arapca, "metin": metin}
Path(__file__).resolve().parent.parent.joinpath("data/ayetler.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
lim = int(sys.argv[1]) if len(sys.argv) > 1 else 1100
for k, v in out.items():
    print(f"\n=== {k} | {v['sure']} {v['baslik']} ===\n{v['metin'][:lim]}")
