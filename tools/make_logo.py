#!/usr/bin/env python3
"""Logo dosyalarını üretir: img/logo*.svg (yazı, yola çevrilmiş; yazı tipi kurulu olmasa da aynı görünür).

Kullanım: python3 tools/make_logo.py --fraunces <Fraunces[SOFT,WONK,opsz,wght].ttf> --publicsans <PublicSans-Regular.ttf>
Yazı tipleri (SIL Open Font License): github.com/undercasetype/Fraunces (fonts/variable/), github.com/uswds/public-sans (fonts/ttf/).
Gereksinim: pip install fonttools uharfbuzz

Üretilenler (img/): logo.svg (yatay, renkli), logo-en.svg, logo-white.svg (koyu zemin), logo-mono.svg (tek renk),
logo-stacked.svg (dikey), logo-mark.svg (yalnızca işaret, çizgi), logo-mark-solid.svg (dolu disk; favicon ile aynı).
PNG sürümleri kimlik.html sayfasındaki indirme bağlantıları için tools/make_logo_png.js ile üretilir.
"""
import argparse, os, tempfile
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import uharfbuzz as hb

ap = argparse.ArgumentParser()
ap.add_argument("--fraunces", required=True)
ap.add_argument("--publicsans", required=True)
args = ap.parse_args()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img")

TEAL, INK, INK2, PAPER = "#0F5F66", "#1B2A2F", "#4A5A5F", "#F7F5EF"
NAME = "Çapa Gastroenterohepatoloji"
SUB_TR = "İstanbul Tıp Fakültesi, İstanbul Üniversitesi"
SUB_EN = "Istanbul Faculty of Medicine, Istanbul University"

# Fraunces: sitedeki başlık ayarına yakın (wght 600, opsz 24, yumuşatma ve wonk kapalı)
vf = TTFont(args.fraunces)
static = instancer.instantiateVariableFont(vf, {"opsz": 24, "wght": 600, "SOFT": 0, "WONK": 0})
tmp = tempfile.NamedTemporaryFile(suffix=".ttf", delete=False)
static.save(tmp.name)
FONTS = {"display": tmp.name, "body": args.publicsans}


def shape(text, font_path, size):
    """Metni biçimlendirir; (yol verisi, genişlik, üst, alt) döndürür. Koordinatlar px, taban çizgisi y=0, y aşağı."""
    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob)
    font = hb.Font(face)
    upem = face.upem
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    tt = TTFont(font_path)
    glyph_set = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    scale = size / upem
    x = 0.0
    paths = []
    top, bottom = 0.0, 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        tr = (scale, 0, 0, -scale, x + pos.x_offset * scale, -pos.y_offset * scale)
        pen = SVGPathPen(glyph_set, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip(".") or "0")
        glyph_set[name].draw(TransformPen(pen, tr))
        bp = BoundsPen(glyph_set)
        glyph_set[name].draw(TransformPen(bp, tr))
        if bp.bounds:
            top = min(top, bp.bounds[1]); bottom = max(bottom, bp.bounds[3])
        d = pen.getCommands()
        if d:
            paths.append(d)
        x += pos.x_advance * scale
    return " ".join(paths), x, top, bottom


def r(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def mark(x, y, s, stroke, fill=None, solid=False):
    """40x40 kutusundaki işaret; s ölçek."""
    g = [f'<g transform="translate({r(x)} {r(y)}) scale({r(s)})">']
    if solid:
        g.append(f'<circle cx="20" cy="20" r="18" fill="{fill}"/>')
        g.append(f'<path d="M12 24c0-6 4-9 8-9s8 3 8 9-4 5-8 5-8 1-8-5z" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linejoin="round"/>')
        g.append(f'<circle cx="20" cy="21" r="2.2" fill="{stroke}"/>')
    else:
        g.append(f'<circle cx="20" cy="20" r="18" fill="none" stroke="{stroke}" stroke-width="2"/>')
        g.append(f'<path d="M12 24c0-6 4-9 8-9s8 3 8 9-4 5-8 5-8 1-8-5z" fill="none" stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>')
        g.append(f'<circle cx="20" cy="21" r="2.2" fill="{stroke}"/>')
    g.append("</g>")
    return "\n".join(g)


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {r(w)} {r(h)}" width="{r(w)}" height="{r(h)}" role="img" aria-labelledby="t">\n'
            f"<title id=\"t\">{title}</title>\n{body}\n</svg>\n")


def horizontal(sub, colors, fname, title):
    c_mark, c_name, c_sub = colors
    name_size, sub_size = 30, 12.5
    d_name, w_name, name_top, name_bottom = shape(NAME, FONTS["display"], name_size)
    d_sub, w_sub, sub_top, sub_bottom = shape(sub, FONTS["body"], sub_size)
    mark_h = 46
    gap = 13
    pad = 3
    name_base = 0.0
    sub_base = name_base + name_bottom + 9 - sub_top  # alt satır, ad satırının en alt noktasından 9 px aşağıda başlar
    text_top, text_bottom = name_base + name_top, sub_base + sub_bottom
    mark_y = (text_top + text_bottom) / 2 - mark_h / 2  # işaret, yazı bloğunun ortasına hizalı
    y0 = min(mark_y, text_top) - pad
    shift = -y0
    text_x = pad + mark_h + gap
    w = text_x + max(w_name, w_sub) + pad
    h = max(mark_y + mark_h, text_bottom) + pad + shift
    body = mark(pad, mark_y + shift, mark_h / 40, c_mark)
    body += f'\n<path fill="{c_name}" transform="translate({r(text_x)} {r(name_base + shift)})" d="{d_name}"/>'
    body += f'\n<path fill="{c_sub}" transform="translate({r(text_x)} {r(sub_base + shift)})" d="{d_sub}"/>'
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(svg(w, h, body, title))
    return round(w, 1), round(h, 1)


def stacked(sub, colors, fname, title):
    c_mark, c_name, c_sub = colors
    name_size, sub_size = 34, 13.5
    d_name, w_name, name_top, name_bottom = shape(NAME, FONTS["display"], name_size)
    d_sub, w_sub, sub_top, sub_bottom = shape(sub, FONTS["body"], sub_size)
    mark_h = 72
    pad = 4
    w = max(w_name, w_sub) + 2 * pad
    cx = w / 2
    name_base = pad + mark_h + 18 - name_top
    sub_base = name_base + name_bottom + 10 - sub_top
    h = sub_base + sub_bottom + pad
    body = mark(cx - mark_h / 2, pad, mark_h / 40, c_mark)
    body += f'\n<path fill="{c_name}" transform="translate({r(cx - w_name / 2)} {r(name_base)})" d="{d_name}"/>'
    body += f'\n<path fill="{c_sub}" transform="translate({r(cx - w_sub / 2)} {r(sub_base)})" d="{d_sub}"/>'
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(svg(w, h, body, title))
    return round(w, 1), round(h, 1)


os.makedirs(OUT, exist_ok=True)
color = (TEAL, INK, INK2)
white = (PAPER, PAPER, PAPER)
mono = (INK, INK, INK)
print("logo.svg", horizontal(SUB_TR, color, "logo.svg", "Çapa Gastroenterohepatoloji, İstanbul Tıp Fakültesi"))
print("logo-en.svg", horizontal(SUB_EN, color, "logo-en.svg", "Çapa Gastroenterohepatology, Istanbul Faculty of Medicine"))
print("logo-white.svg", horizontal(SUB_TR, white, "logo-white.svg", "Çapa Gastroenterohepatoloji (koyu zemin için)"))
print("logo-mono.svg", horizontal(SUB_TR, mono, "logo-mono.svg", "Çapa Gastroenterohepatoloji (tek renk)"))
print("logo-stacked.svg", stacked(SUB_TR, color, "logo-stacked.svg", "Çapa Gastroenterohepatoloji (dikey)"))
print("logo-stacked-white.svg", stacked(SUB_TR, white, "logo-stacked-white.svg", "Çapa Gastroenterohepatoloji (dikey, koyu zemin için)"))
open(os.path.join(OUT, "logo-mark.svg"), "w", encoding="utf-8").write(svg(40, 40, mark(0, 0, 1, TEAL), "Çapa Gastroenterohepatoloji işareti"))
open(os.path.join(OUT, "logo-mark-solid.svg"), "w", encoding="utf-8").write(svg(40, 40, mark(0, 0, 1, PAPER, TEAL, solid=True), "Çapa Gastroenterohepatoloji işareti (dolu)"))
open(os.path.join(OUT, "logo-mark-white.svg"), "w", encoding="utf-8").write(svg(40, 40, mark(0, 0, 1, PAPER), "Çapa Gastroenterohepatoloji işareti (koyu zemin için)"))


GI_ART = """<g fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" transform="translate({x} {y}) scale({s})">
<path d="M150 10 C150 60 145 90 160 120"/>
<path d="M160 120 C205 130 230 165 215 200 C200 235 150 240 125 215 C110 200 118 175 140 172"/>
<path d="M170 132 C200 145 215 172 205 195" stroke-width=".9" opacity=".55"/>
<path d="M140 172 C130 190 150 205 160 225 C175 255 150 275 135 290 C120 305 150 320 175 305 C200 290 190 260 210 250 C235 240 250 280 225 300 C205 318 175 330 160 345"/>
<path d="M60 300 C60 200 70 140 110 140 C170 140 240 130 265 150 C275 160 275 300 265 320 C255 345 230 350 200 350"/>
<path d="M78 220 h18 M78 250 h18 M78 280 h18 M250 200 h18 M250 240 h18 M250 280 h18" stroke-width=".9" opacity=".55"/>
<path d="M110 140 c10 -12 25 -14 40 -12 M175 138 c12 -14 30 -14 45 -6" stroke-width=".9" opacity=".55"/>
<circle cx="60" cy="300" r="4"/><circle cx="200" cy="350" r="4"/>
</g>"""


def cover():
    """Sunum kapağı (16:9, 1920x1080): koyu teal zemin, beyaz logo, sağda çizgi illüstrasyonu; başlık alanı boş bırakılır."""
    W, H = 1920, 1080
    lockup = open(os.path.join(OUT, "logo-white.svg"), encoding="utf-8").read()
    inner = lockup[lockup.index("</title>") + 8:lockup.rindex("</svg>")]
    body = f'<rect width="{W}" height="{H}" fill="{TEAL}"/>'
    body += f'\n<g transform="translate(120 96) scale(1.6)">{inner}</g>'
    body += "\n" + GI_ART.format(c=PAPER, x=1230, y=170, s=2.1, sw=2.2)
    body += f'\n<rect x="120" y="984" width="96" height="6" fill="{PAPER}" opacity=".85"/>'
    open(os.path.join(OUT, "sunum-kapak.svg"), "w", encoding="utf-8").write(svg(W, H, body, "Sunum kapağı şablonu"))
    # Poster üst bandı (A0 için oranlı, 8:1): sol logo, sağ illüstrasyon
    W2, H2 = 2400, 300
    body = f'<rect width="{W2}" height="{H2}" fill="{TEAL}"/>'
    body += f'\n<g transform="translate(80 92) scale(2)">{inner}</g>'
    body += "\n" + GI_ART.format(c=PAPER, x=2050, y=-20, s=.9, sw=2)
    open(os.path.join(OUT, "poster-bant.svg"), "w", encoding="utf-8").write(svg(W2, H2, body, "Poster üst bandı şablonu"))


cover()
print("sunum-kapak.svg, poster-bant.svg")
os.unlink(tmp.name)
print("bitti:", OUT)
