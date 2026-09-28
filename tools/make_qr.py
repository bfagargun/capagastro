#!/usr/bin/env python3
"""QR kodlarını üretir: img/qr/<ad>.png ile qr.html'nin okuduğu img/qr/list.js (ve list.json).

Kullanım: python3 tools/make_qr.py [--base https://besimagargun.com/capagastro/]
Alan adı değişince --base ile yeniden çalıştırın; kartlar ve kodlar yenilenir.
Gereksinim: pip install qrcode pillow
"""
import json, os, sys, argparse
import qrcode
from qrcode.constants import ERROR_CORRECT_Q

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="https://besimagargun.com/capagastro/")
args = ap.parse_args()
BASE = args.base.rstrip("/") + "/"

# (dosya adı, Türkçe başlık, İngilizce başlık, yol, grup)
LINKS = [
    ("hazirlik-pegdin", "Kolonoskopi hazırlığı: Pegdin", "Colonoscopy preparation: Pegdin", "hazirlik.html?s=pegdin", "planlayici"),
    ("hazirlik-xm", "Kolonoskopi hazırlığı: X-M Diet + B.T. Enema", "Colonoscopy preparation: X-M Diet + B.T. Enema", "hazirlik.html?s=xm", "planlayici"),
    ("hazirlik-pico", "Kolonoskopi hazırlığı: Picoprep / CitraFleet", "Colonoscopy preparation: Picoprep / CitraFleet", "hazirlik.html?s=pico", "planlayici"),
    ("hazirlik", "Kolonoskopi hazırlık planlayıcı (ürün seçimli)", "Colonoscopy preparation planner", "hazirlik.html", "planlayici"),
    ("islemler", "Tüm işlemler: hazırlık, işlem günü ve sonrası", "All procedures: preparation, the day and afterwards", "islemler.html", "islemler"),
    ("gastroskopi", "Gastroskopi", "Gastroscopy", "islemler.html#gastroskopi", "islemler"),
    ("kolonoskopi", "Kolonoskopi", "Colonoscopy", "islemler.html#kolonoskopi", "islemler"),
    ("ercp", "ERCP", "ERCP", "islemler.html#ercp", "islemler"),
    ("eus", "Endoskopik ultrasonografi (EUS)", "Endoscopic ultrasound (EUS)", "islemler.html#eus", "islemler"),
    ("kapsul", "Kapsül endoskopi", "Capsule endoscopy", "islemler.html#kapsul", "islemler"),
    ("enteroskopi", "Çift balon enteroskopi", "Double-balloon enteroscopy", "islemler.html#enteroskopi", "islemler"),
    ("poem", "POEM", "POEM", "islemler.html#poem", "islemler"),
    ("manometri", "Özofagus manometrisi ve impedans-pH", "Oesophageal manometry and impedance-pH", "islemler.html#manometri", "islemler"),
    ("anorektal", "Anorektal manometri", "Anorectal manometry", "islemler.html#anorektal", "islemler"),
    ("fibroscan", "FibroScan ve elastografi", "FibroScan and elastography", "islemler.html#fibroscan", "islemler"),
    ("biyopsi", "Karaciğer biyopsisi", "Liver biopsy", "islemler.html#biyopsi", "islemler"),
    ("parasentez", "Parasentez", "Paracentesis", "islemler.html#parasentez", "islemler"),
    ("bagirsak-usg", "Bağırsak ultrasonografisi", "Intestinal ultrasound", "islemler.html#bagirsak-usg", "islemler"),
    ("infuzyon", "Biyolojik tedavi ünitesi", "Biologic therapy unit", "islemler.html#infuzyon", "islemler"),
    ("peg", "PEG (beslenme tüpü)", "PEG (feeding tube)", "islemler.html#peg", "islemler"),
    ("hatirlatici", "Takip hatırlatıcıları", "Follow-up reminders", "hatirlatici.html", "diger"),
    ("izlem", "Uzun süreli izlem rehberi", "Long-term follow-up guide", "izlem.html", "diger"),
    ("site", "Bilim dalı sitesi", "Division website", "", "diger"),
]

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "qr")
os.makedirs(out_dir, exist_ok=True)
items = []
for name, tr, en, path, group in LINKS:
    url = BASE + path
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_Q, box_size=10, border=4)
    q.add_data(url)
    q.make(fit=True)
    img = q.make_image(fill_color="#0F5F66", back_color="white")
    img.save(os.path.join(out_dir, name + ".png"))
    items.append({"file": name + ".png", "tr": tr, "en": en, "url": url, "group": group})
data = {"base": BASE, "items": items}
with open(os.path.join(out_dir, "list.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
with open(os.path.join(out_dir, "list.js"), "w", encoding="utf-8") as f:
    f.write("const QR_LIST = " + json.dumps(data, ensure_ascii=False) + ";\n")
print(f"{len(items)} QR kodu yazıldı: {out_dir}")
