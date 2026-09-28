#!/usr/bin/env python3
"""Alt sayfalara ortak "site haritası" şeridini ekler veya günceller (altbilginin hemen üstünde).

Kullanım: python3 tools/inject_sitenav.py
Şerit, <!-- sitenav --> ... <!-- /sitenav --> işaretçileri arasında durur; betik yeniden çalıştırılınca yenilenir.
Bağlantı listesi aşağıdaki NAV içindedir; yeni sayfa eklenince buraya yazıp betiği çalıştırın.
Dil, sayfanın <html lang> özniteliğinden okunur; dil düğmesi onu değiştirdiğinde şerit kendini yeniler.
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["hazirlik.html", "islemler.html", "hatirlatici.html", "izlem.html", "sss.html", "yayinlar.html", "egitim.html",
         "sevk.html", "protokoller.html", "veri-yonetisimi.html", "veri-ve-araclar.html", "veri-sozlesme.html", "kimlik.html"]

NAV = {
    "groups": [
        {"tr": "Hastalar için", "en": "For patients", "links": [
            ["hazirlik.html", "Hazırlık planlayıcı", "Preparation planner"],
            ["islemler.html", "İşlemler", "Procedures"],
            ["hatirlatici.html", "Hatırlatıcılar", "Reminders"],
            ["izlem.html", "Uzun süreli izlem", "Long-term follow-up"],
            ["sss.html", "Sık sorulan sorular", "FAQ"]]},
        {"tr": "Bilim dalı", "en": "Division", "links": [
            ["index.html", "Ana sayfa", "Home"],
            ["index.html#arastirma", "Araştırma", "Research"],
            ["yayinlar.html", "Yayınlar", "Publications"],
            ["egitim.html", "Eğitim ve başvuru", "Training"],
            ["sevk.html", "Sevk eden hekimler", "Referring physicians"],
            ["protokoller.html", "Protokoller", "Protocols (TR)"],
            ["veri-yonetisimi.html", "Veri yönetişimi", "Data governance"],
            ["veri-ve-araclar.html", "Veri ve araçlar", "Data and tools"],
            ["kimlik.html", "Kurumsal kimlik", "Brand identity"]]}
    ]
}

SNIPPET = """<!-- sitenav -->
<style>.sitenav{border-top:1px solid var(--line);background:var(--paper-2);padding:1.4rem 0 .6rem;font-size:.86rem}.sitenav .wrap{width:min(1100px,92vw);margin:0 auto;display:grid;grid-template-columns:1fr 1.8fr;gap:.6rem 2rem}@media (max-width:820px){.sitenav .wrap{grid-template-columns:1fr}}.sitenav b{display:block;color:var(--ink-2);font-weight:500;margin-bottom:.35rem}.sitenav ul{list-style:none;margin:0 0 .8rem;padding:0;display:flex;flex-wrap:wrap;gap:.35rem}.sitenav a{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:.2rem .7rem;color:var(--ink);text-decoration:none;background:var(--paper)}.sitenav a:hover{border-color:var(--teal);color:var(--teal)}.sitenav a[aria-current="page"]{border-color:var(--teal);background:var(--teal-soft);color:var(--teal-2)}@media print{.sitenav{display:none}}</style>
<nav class="sitenav" id="sitenav" aria-label="Site haritası"><div class="wrap"></div></nav>
<script>(function(){var N=__NAV__,el=document.getElementById("sitenav"),w=el.firstElementChild,here=location.pathname.split("/").pop()||"index.html";function r(){var en=document.documentElement.lang==="en";el.setAttribute("aria-label",en?"Site map":"Site haritası");w.innerHTML=N.groups.map(function(g){return"<div><b>"+(en?g.en:g.tr)+"</b><ul>"+g.links.map(function(l){var cur=l[0]===here?' aria-current="page"':"";return'<li><a href="'+l[0]+'"'+cur+">"+(en?l[2]:l[1])+"</a></li>"}).join("")+"</ul></div>"}).join("")}r();new MutationObserver(r).observe(document.documentElement,{attributes:true,attributeFilter:["lang"]});})();</script>
<!-- /sitenav -->
"""

snippet = SNIPPET.replace("__NAV__", json.dumps(NAV, ensure_ascii=False, separators=(",", ":")))
for f in PAGES:
    path = os.path.join(ROOT, f)
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<!-- sitenav -->.*?<!-- /sitenav -->\n", "", s, flags=re.S)
    i = s.rfind("<footer")
    if i < 0:
        print("altbilgi yok, atlandı:", f)
        continue
    s = s[:i] + snippet + s[i:]
    open(path, "w", encoding="utf-8").write(s)
    print("ok", f)
