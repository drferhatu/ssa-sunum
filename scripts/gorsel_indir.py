"""Seçilen Commons görsellerini assets/img altına indirir, data/gorseller.json'a künye yazar.
Kullanım: python gorsel_indir.py <aday_kok_dizini>"""
import json, sys, io, re, time, html, urllib.request, urllib.error
from pathlib import Path
from PIL import Image

UA = {"User-Agent": "okul-sunumu-gorsel-arama/1.0 (egitim amacli)"}
SECIM = {  # hedef ad: (aday dizini, anahtar, sıra, genişlik)
 "sofra": ("aday2", "sofra2", 2, 1920), "bal": ("aday", "bal", 7, 1280), "ari": ("aday", "ari", 6, 1280),
 "hurma": ("aday2", "hurma2", 0, 1280), "hurmalik": ("aday3", "hurma3", 2, 1280),
 "zeytin": ("aday", "zeytin", 0, 1280), "zeytinagaci": ("aday", "zeytinagaci", 4, 1280),
 "incir": ("aday", "incir", 0, 1280), "uzum": ("aday2", "uzum2", 2, 1280), "nar": ("aday", "nar", 5, 1280),
 "sut": ("aday3", "sut3", 4, 1280), "balik": ("aday2", "balik2", 0, 1280), "bugday": ("aday", "bugday", 1, 1280),
 "muz": ("aday", "muz", 0, 960), "zencefil": ("aday", "zencefil", 2, 960), "mercimek": ("aday", "mercimek", 6, 960),
 "sogan": ("aday", "sogan", 1, 960),
}
kok = Path(sys.argv[1]); proje = Path(__file__).resolve().parent.parent
hedef = proje / "assets/img"; hedef.mkdir(parents=True, exist_ok=True)
kunye = {}
for ad, (dz, anahtar, i, w) in SECIM.items():
    a = json.loads((kok / dz / "adaylar.json").read_text(encoding="utf-8"))[anahtar][i]
    url = re.sub(r"/\d+px-", f"/{w}px-", a["thumb"])
    for dene in range(6):
        try:
            time.sleep(1.5)
            veri = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read(); break
        except urllib.error.HTTPError as e:
            print(ad, "HTTP", e.code); time.sleep(15 * (dene + 1))
    else:
        raise SystemExit(f"{ad} indirilemedi")
    im = Image.open(io.BytesIO(veri)).convert("RGB")
    im.save(hedef / f"{ad}.jpg", quality=84, optimize=True, progressive=True)
    sanatci = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", a["sanatci"]))).strip()[:80]
    kunye[ad] = {"baslik": a["title"].replace("File:", ""), "sanatci": sanatci, "lisans": a["lisans"], "sayfa": a["sayfa"]}
    print(ad, im.size, a["lisans"], "|", sanatci, "|", a["title"])
(proje / "data/gorseller.json").write_text(json.dumps(kunye, ensure_ascii=False, indent=1), encoding="utf-8")
