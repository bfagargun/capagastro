#!/usr/bin/env node
// index.html içindeki <!--pre:ad--> ... <!--/pre:ad--> statik kopyalarını, sayfayı tarayıcıda çizdirip yeniler.
// Kullanım: node tools/prerender.js   (gereksinim: npm i -g playwright && npx playwright install chromium)
// Veri blokları (TEAM, ALUMNI, PROJECTS, PUBS_ALL, COLLAB, FACTS) değişince çalıştırın; JavaScript çalıştırmayan
// okuyucular ve arama motorları bu kopyaları görür.
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");
const FILE = path.join(__dirname, "..", "index.html");
const IDS = ["facts", "pi-pubs", "projects", "team", "collab", "alumni", "pubs"];
(async () => {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ locale: "tr-TR" })).newPage();
  // Dış görseller (AVESİS fotoğrafları) yüklenemezse sayfa baş harflere düşer; statik kopyaya bu düşmüş hali yazmamak için görselleri 1x1 PNG ile karşılarız.
  const PNG = Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=", "base64");
  await page.route(/^https?:\/\//, r => r.request().resourceType() === "image" ? r.fulfill({ contentType: "image/png", body: PNG }) : r.abort());
  await page.goto("file://" + FILE, { waitUntil: "load" });
  await page.waitForTimeout(800);
  const html = await page.evaluate(ids => Object.fromEntries(ids.map(id => [id, (document.getElementById(id) || { innerHTML: null }).innerHTML])), IDS);
  await browser.close();
  let s = fs.readFileSync(FILE, "utf8"), changed = 0;
  for (const id of IDS) {
    if (html[id] == null) { console.log("bulunamadı:", id); continue; }
    const open = `<!--pre:${id}-->`, close = `<!--/pre:${id}-->`;
    const a = s.indexOf(open), b = s.indexOf(close);
    if (a < 0 || b < 0) { console.log("işaret yok:", id); continue; }
    const inner = html[id].replace(open, "").replace(close, "");
    const next = s.slice(0, a + open.length) + inner + s.slice(b);
    if (next !== s) { changed++; s = next; console.log("yenilendi:", id); } else console.log("aynı:", id);
  }
  fs.writeFileSync(FILE, s);
  console.log(changed + " blok değişti.");
})();
