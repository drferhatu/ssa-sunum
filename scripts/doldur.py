"""index.html içindeki Arapça ayet yer tutucularını (data-ayet / data-no / data-kes) ve görsel künyelerini doldurur.
Arapça metin elle yazılmaz; data/ayetler.json'daki tefsir metninden aynen alınır. Tekrar çalıştırılabilir."""
import json, re, html
from pathlib import Path

proje = Path(__file__).resolve().parent.parent
ayetler = json.loads((proje / "data/ayetler.json").read_text(encoding="utf-8"))
kunye = json.loads((proje / "data/gorseller.json").read_text(encoding="utf-8"))
TR2AR = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

def ayet_metni(anahtar, no):
    v = ayetler[anahtar]; kaynak = v["arapca"] + "\n" + v["metin"]
    isaret = "﴿" + str(no).translate(TR2AR) + "﴾"
    i = kaynak.index(isaret)
    onceki = max(kaynak.rfind("﴾", 0, i), kaynak.rfind("﴿", 0, i), kaynak.rfind("\n", 0, i))
    return kaynak[onceki + 1:i].strip(), isaret

def doldur(m):
    ozn = m.group(1)
    anahtar = re.search(r'data-ayet="([^"]+)"', ozn).group(1)
    no = re.search(r'data-no="([^"]+)"', ozn).group(1)
    kes = re.search(r'data-kes="([^"]+)"', ozn)
    metin, isaret = ayet_metni(anahtar, no)
    if kes:
        metin = metin[metin.index(kes.group(1)):]
    return f'<p{ozn}>{metin} <span class="no">{isaret}</span></p>'

p = proje / "index.html"; s = p.read_text(encoding="utf-8")
s, n = re.subn(r'<p((?=[^>]*class="ar)[^>]*data-ayet[^>]*)>.*?</p>', doldur, s, flags=re.S)
satirlar = "".join(
    f'\n          <li><a href="{html.escape(k["sayfa"])}" target="_blank" rel="noopener">{html.escape(k["baslik"][:58])}</a>'
    f' · {html.escape(k["sanatci"])} · {html.escape(k["lisans"])}</li>' for k in kunye.values())
s = re.sub(r'(<ul id="gorsel-kunye">).*?(</ul>)', lambda m: m.group(1) + satirlar + "\n        " + m.group(2), s, flags=re.S)
p.write_text(s, encoding="utf-8")
print("arapça alan:", n, "| görsel künyesi:", len(kunye))
