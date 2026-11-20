#!/usr/bin/env python3
"""Sitenin hızlı denetimi (commit öncesi): python3 tools/check.py [dosya...]

Denetlenenler, her HTML dosyası için:
- uzun/kısa tire (– —) ve şapkalı a (â) yok (site yazım kuralı)
- HTML etiket dengesi
- satır içi <script> bloklarının sözdizimi (node ile) ve JSON-LD bloklarının geçerliliği
- yerel bağlantıların (href/src) var olan dosyalara gitmesi
- noindex ve canonical varlığı (yayın öncesi hatırlatma olarak yalnızca bildirilir)
Ayrıca sw.js, manifest.webmanifest ve sitemap.xml denetlenir. Hata varsa çıkış kodu 1.
Gereksinim: node (script sözdizimi için; yoksa o adım atlanır).
"""
import os, re, sys, json, glob, subprocess, shutil
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
problems = []


def err(f, msg):
    problems.append(f"{f}: {msg}")


class Balance(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"</{tag}> satır {self.getpos()[0]} beklenmedik (açık: {[t for t, _ in self.stack[-3:]]})")


def check_html(path):
    f = os.path.relpath(path, ROOT)
    s = open(path, encoding="utf-8").read()
    for m in re.finditer(r"[–—âÂ]", s):
        line = s.count("\n", 0, m.start()) + 1
        err(f, f"yasak karakter {m.group()!r} satır {line}")
    p = Balance()
    p.feed(s)
    for e in p.errors[:5]:
        err(f, "etiket dengesi: " + e)
    if p.stack:
        err(f, "kapanmamış etiketler: " + str([t for t, _ in p.stack[:5]]))
    node = shutil.which("node")
    for i, m in enumerate(re.finditer(r"<script([^>]*)>([\s\S]*?)</script>", s), 1):
        attrs, body = m.group(1), m.group(2)
        if "src=" in attrs:
            continue
        if "ld+json" in attrs:
            try:
                json.loads(body)
            except Exception as e:
                err(f, f"JSON-LD geçersiz: {e}")
            continue
        if node:
            r = subprocess.run([node, "-e", "new Function(require('fs').readFileSync(0,'utf8'))"], input=body, text=True, capture_output=True)
            if r.returncode:
                err(f, f"script #{i} sözdizimi: {r.stderr.strip().splitlines()[-1][:120]}")
    # Bağlantılar: script blokları dışındaki (statik) href/src değerleri; şablon ifadeleri atlanır
    static = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", s)
    for m in re.finditer(r'\b(?:href|src)="([^"#?]+)[^"]*"', static):
        h = m.group(1)
        if re.match(r"^(https?:|mailto:|tel:|data:|javascript:|//)", h) or h.startswith("/") or "$" in h or "'" in h:
            continue
        if not os.path.exists(os.path.join(os.path.dirname(path), h)):
            err(f, f"yerel bağlantı yok: {h}")
    if 'name="robots"' in s and "noindex" in s:
        notes.append(f"{f}: noindex (taslak)")
    if f not in ("404.html", "cevrimdisi.html", "qr.html") and 'rel="canonical"' not in s:
        err(f, "canonical yok")


notes = []
files = [os.path.join(ROOT, a) for a in sys.argv[1:]] or sorted(glob.glob(os.path.join(ROOT, "*.html")))
for path in files:
    check_html(path)
for extra in ["sw.js", "manifest.webmanifest", "sitemap.xml", "img/qr/list.js"]:
    path = os.path.join(ROOT, extra)
    if not os.path.exists(path):
        continue
    s = open(path, encoding="utf-8").read()
    if extra.endswith(".webmanifest"):
        try:
            json.loads(s)
        except Exception as e:
            err(extra, f"JSON geçersiz: {e}")
    elif extra.endswith(".xml"):
        try:
            import xml.dom.minidom as md
            md.parseString(s)
        except Exception as e:
            err(extra, f"XML geçersiz: {e}")
    elif shutil.which("node"):
        r = subprocess.run(["node", "--check", path], capture_output=True, text=True)
        if r.returncode:
            err(extra, "sözdizimi: " + r.stderr.strip().splitlines()[-1][:120])
    if extra == "sw.js":
        for m in re.finditer(r'"\./([^"]+)"', s):
            if not os.path.exists(os.path.join(ROOT, m.group(1))):
                err(extra, f"önbellek listesinde olmayan dosya: {m.group(1)}")

for n in notes:
    print("not:", n)
if problems:
    print("\n".join("HATA " + p for p in problems))
    print(f"\n{len(problems)} sorun.")
    sys.exit(1)
print(f"{len(files)} HTML dosyası ve ek dosyalar temiz.")
