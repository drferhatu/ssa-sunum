"""Wikimedia Commons'ta her yiyecek için aday görselleri arar, küçük önizlemeleri indirir ve kontak tabakası üretir.
Kullanım: python gorsel_aday.py <cikti_dizini>"""
import json, sys, io, time, urllib.request, urllib.parse, urllib.error
from pathlib import Path
from PIL import Image, ImageDraw

UA = {"User-Agent": "okul-sunumu-gorsel-arama/1.0 (egitim amacli)"}
API = "https://commons.wikimedia.org/w/api.php"
ARAMALAR = {
 "bal": ["honeycomb honey", "honey jar dipper"], "hurma": ["dates fruit Phoenix dactylifera", "medjool dates"],
 "zeytin": ["olives branch Olea europaea", "olive oil olives"], "incir": ["figs fruit Ficus carica"],
 "uzum": ["grapes bunch vine"], "nar": ["pomegranate fruit open"], "sut": ["glass of milk"],
 "balik": ["fresh fish market", "grilled fish dish"], "bugday": ["wheat ears field", "wheat grains"],
 "sofra": ["fruit still life table", "mediterranean food table"], "muz": ["bananas bunch"],
 "zencefil": ["ginger root"], "mercimek": ["lentils"], "sogan": ["onions"], "ari": ["honey bee flower"],
 "zeytinagaci": ["old olive tree"], "hurmaagaci": ["date palm fruit tree"],
}
def api(**p):
    p.update(format="json")
    r = urllib.request.Request(API + "?" + urllib.parse.urlencode(p), headers=UA)
    return json.load(ac(r))

def ac(r):
    for dene in range(6):
        try:
            time.sleep(1.2)
            return urllib.request.urlopen(r, timeout=30)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(15 * (dene + 1))
    raise SystemExit("429: istek siniri asilamadi")

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
if len(sys.argv) > 2:  # istege bagli: {"ad": ["sorgu", ...]} bicimli JSON dosyasi
    ARAMALAR = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
meta = {}
for ad, sorgular in ARAMALAR.items():
    adaylar = []
    for q in sorgular:
        for kat in ['incategory:"Quality images"', 'incategory:"Featured pictures on Wikimedia Commons"', '']:
            if kat == '' and len(adaylar) >= 5: continue
            d = api(action="query", generator="search", gsrsearch=f"{q} filetype:bitmap {kat}", gsrnamespace=6,
                    gsrlimit=8, prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=420)
            for pg in (d.get("query", {}).get("pages", {}) or {}).values():
                ii = pg["imageinfo"][0]; em = ii.get("extmetadata", {})
                if ii["width"] < 1600 or pg["title"] in [a["title"] for a in adaylar]: continue
                adaylar.append({"title": pg["title"], "thumb": ii["thumburl"], "w": ii["width"], "h": ii["height"],
                                "lisans": em.get("LicenseShortName", {}).get("value", "?"),
                                "sanatci": em.get("Artist", {}).get("value", "?"), "sayfa": ii["descriptionurl"]})
    adaylar = adaylar[:10]; meta[ad] = adaylar
    sheet = Image.new("RGB", (5 * 430, 2 * 330), "white"); dr = ImageDraw.Draw(sheet)
    for i, a in enumerate(adaylar):
        try:
            im = Image.open(io.BytesIO(ac(urllib.request.Request(a["thumb"], headers=UA)).read())).convert("RGB")
        except Exception as e:
            print("indirilemedi", a["title"], e); continue
        im.thumbnail((420, 290)); x, y = (i % 5) * 430 + 5, (i // 5) * 330 + 5
        sheet.paste(im, (x, y)); dr.text((x, y + 295), f"{i} {a['lisans']} {a['w']}x{a['h']}", fill="black")
    sheet.save(out / f"{ad}.jpg", quality=80); print(ad, len(adaylar))
(out / "adaylar.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
