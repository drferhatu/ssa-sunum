# Ayetlerin Sofrası

Kur’an-ı Kerim’de geçen yiyecekler: Ayetler, izahları ve sağlığa faydaları.
Şehit Sefer Alan Anadolu Lisesi 9/F · Peygamberimizin Hayatı dersi sunumu · 25 Kasım 2026.

- Canlı: https://drferhatu.github.io/ssa-sunum/
- Yedek PDF (internetsiz kullanım için): `ssa-sunum.pdf`

Sunumda ilerlemek için: `→` / `PageDown` / `Boşluk` ileri, `←` / `PageUp` geri, `F` tam ekran.

## Yeniden üretme

```
python scripts/fetch_ayetler.py   # ayet meali ve izahları yerel tefsir API'sinden çeker
python scripts/doldur.py          # Arapça ayetleri ve görsel künyelerini index.html'e işler
scripts/pdf_uret.sh               # ssa-sunum.pdf üretir (Chrome gerekir)
```

Ayet mealleri ve izahlar Nadiri Tefsiri’nden, görseller Wikimedia Commons’tan alınmıştır (künyeler son slaytta).
