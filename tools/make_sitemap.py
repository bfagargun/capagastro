#!/usr/bin/env python3
"""sitemap.xml dosyasını üretir (sayfa başına bir adres; İngilizce sürüm hreflang ile).

Kullanım: python3 tools/make_sitemap.py [--base https://capagastro.org/]
Alan adı değişince --base ile yeniden çalıştırın. lastmod her dosyanın son git tarihinden alınır;
git yoksa dosyanın değiştirilme tarihi kullanılır. Gereksinim yok (yalnızca standart kütüphane).

Ünite içi sayfalar (protokoller.html, qr.html) ve 404.html haritaya girmez.
"""
import argparse, os, subprocess, datetime

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="https://capagastro.org/")
args = ap.parse_args()
BASE = args.base.rstrip("/") + "/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (dosya, öncelik, değişim sıklığı, İngilizce sürümü var mı)
PAGES = [
    ("index.html", "1.0", "weekly", True),
    ("hazirlik.html", "0.9", "monthly", True),
    ("islemler.html", "0.9", "monthly", True),
    ("izlem.html", "0.8", "monthly", True),
    ("sss.html", "0.8", "monthly", True),
    ("hatirlatici.html", "0.7", "monthly", True),
    ("yayinlar.html", "0.8", "weekly", True),
    ("egitim.html", "0.7", "monthly", True),
    ("sevk.html", "0.7", "monthly", True),
    ("veri-yonetisimi.html", "0.6", "yearly", True),
    ("veri-ve-araclar.html", "0.6", "monthly", True),
    ("kimlik.html", "0.5", "yearly", True),
]


def lastmod(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    ts = os.path.getmtime(os.path.join(ROOT, path))
    return datetime.date.fromtimestamp(ts).isoformat()


lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for f, prio, freq, has_en in PAGES:
    loc = BASE if f == "index.html" else BASE + f
    lines.append("  <url>")
    lines.append(f"    <loc>{loc}</loc>")
    lines.append(f"    <lastmod>{lastmod(f)}</lastmod>")
    lines.append(f"    <changefreq>{freq}</changefreq>")
    lines.append(f"    <priority>{prio}</priority>")
    if has_en:
        # Dil sürümleri aynı adreste ?lang ile sunulur; canonical Türkçe adrestir, İngilizce sürüm hreflang ile bildirilir.
        lines.append(f'    <xhtml:link rel="alternate" hreflang="tr" href="{loc}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{loc}?lang=en"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>')
    lines.append("  </url>")
lines.append("</urlset>")
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print(f"{len(PAGES)} adres yazıldı: sitemap.xml (taban {BASE})")
