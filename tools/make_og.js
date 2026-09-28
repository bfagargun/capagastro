#!/usr/bin/env node
// Sayfa başına sosyal medya kartı (og:image, 1200x630) üretir: img/og-<sayfa>.png
// Kullanım: node tools/make_og.js [--fraunces <ttf>] [--publicsans <ttf>]
// Yazı tipleri verilmezse sistemdeki Georgia/Arial yedekleri kullanılır; kimlik.html'deki kaynaklar (GitHub) ile aynı dosyalar önerilir.
// Gereksinim: npm i -g playwright && npx playwright install chromium
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");
const ROOT = path.join(__dirname, "..");
const args = process.argv.slice(2);
const opt = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : ""; };
const fraunces = opt("--fraunces"), publicsans = opt("--publicsans");

// (dosya adı, üst etiket, başlık TR, başlık EN)
const CARDS = [
  ["hazirlik", "Hasta bilgilendirme", "Kolonoskopi hazırlık planlayıcı", "Colonoscopy preparation planner"],
  ["islemler", "Hasta bilgilendirme", "İşlemler ve hazırlık", "Procedures and preparation"],
  ["hatirlatici", "Hasta bilgilendirme", "Takip hatırlatıcıları", "Follow-up reminders"],
  ["izlem", "Hasta bilgilendirme", "Uzun süreli izlem rehberleri", "Long-term follow-up guides"],
  ["sss", "Hasta bilgilendirme", "Sık sorulan sorular", "Frequently asked questions"],
  ["sevk", "Meslektaşlar için", "Sevk eden hekimler için", "For referring physicians"],
  ["yayinlar", "Araştırma", "Yayınlar", "Publications"],
  ["egitim", "Bilim dalı", "Eğitim ve başvuru", "Training and applications"],
  ["veri-ve-araclar", "Araştırma grubu", "Veri setleri ve araçlar", "Data sets and tools"],
  ["veri-yonetisimi", "Araştırma grubu", "Veri yönetişimi ve sorumlu yapay zeka", "Data governance and responsible AI"],
  ["kimlik", "Bilim dalı", "Kurumsal kimlik ve basın kiti", "Brand identity and press kit"],
];

const logo = fs.readFileSync(path.join(ROOT, "img", "logo-white.svg"), "utf8");
const logoInner = logo.slice(logo.indexOf("</title>") + 8, logo.lastIndexOf("</svg>"));
const art = `<svg viewBox="0 0 320 380" style="position:absolute;right:70px;top:110px;width:330px;height:392px" fill="none" stroke="#F7F5EF" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
<path d="M150 10 C150 60 145 90 160 120"/><path d="M160 120 C205 130 230 165 215 200 C200 235 150 240 125 215 C110 200 118 175 140 172"/>
<path d="M170 132 C200 145 215 172 205 195" stroke-width=".9" opacity=".55"/>
<path d="M140 172 C130 190 150 205 160 225 C175 255 150 275 135 290 C120 305 150 320 175 305 C200 290 190 260 210 250 C235 240 250 280 225 300 C205 318 175 330 160 345"/>
<path d="M60 300 C60 200 70 140 110 140 C170 140 240 130 265 150 C275 160 275 300 265 320 C255 345 230 350 200 350"/>
<path d="M78 220 h18 M78 250 h18 M78 280 h18 M250 200 h18 M250 240 h18 M250 280 h18" stroke-width=".9" opacity=".55"/>
<path d="M110 140 c10 -12 25 -14 40 -12 M175 138 c12 -14 30 -14 45 -6" stroke-width=".9" opacity=".55"/>
<circle cx="60" cy="300" r="4"/><circle cx="200" cy="350" r="4"/></svg>`;

const fontCss = (fraunces ? `@font-face{font-family:"Fraunces";src:url("file://${fraunces}");font-weight:100 900}` : "") +
  (publicsans ? `@font-face{font-family:"Public Sans";src:url("file://${publicsans}")}` : "");

function html(kicker, tr, en) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>${fontCss}
  body{margin:0;width:1200px;height:630px;background:#0F5F66;color:#F7F5EF;font-family:"Public Sans",Arial,sans-serif;position:relative;overflow:hidden}
  .logo{position:absolute;left:84px;top:64px}
  .kicker{position:absolute;left:84px;top:190px;font-size:24px;letter-spacing:.02em;opacity:.85;font-style:italic;font-family:"Fraunces",Georgia,serif}
  .title{position:absolute;left:84px;top:236px;width:720px;font-family:"Fraunces",Georgia,serif;font-weight:300;font-variation-settings:"opsz" 144,"wght" 300;font-size:66px;line-height:1.08;letter-spacing:-.01em}
  .en{position:absolute;left:84px;bottom:118px;width:720px;font-size:28px;opacity:.9}
  .url{position:absolute;left:84px;bottom:56px;font-size:22px;opacity:.75}
  .bar{position:absolute;left:84px;bottom:100px;width:96px;height:5px;background:#F7F5EF;opacity:.85}
  </style></head><body>
  <svg class="logo" viewBox="0 0 481.2 57.9" width="722" height="87" style="overflow:visible">${logoInner}</svg>
  ${art}
  <div class="kicker">${kicker}</div><div class="title">${tr}</div><div class="bar"></div><div class="en">${en}</div><div class="url">besimagargun.com/capagastro</div>
  </body></html>`;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  const os = require("os");
  const tmp = path.join(os.tmpdir(), "capagastro-og.html");
  for (const [name, kicker, tr, en] of CARDS) {
    fs.writeFileSync(tmp, html(kicker, tr, en));
    await page.goto("file://" + tmp, { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    await page.screenshot({ path: path.join(ROOT, "img", `og-${name}.png`), clip: { x: 0, y: 0, width: 1200, height: 630 } });
    console.log(`og-${name}.png`);
  }
  await browser.close();
  try { fs.unlinkSync(tmp); } catch (e) {}
})();
