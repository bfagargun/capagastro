#!/usr/bin/env node
// img/logo*.svg dosyalarından şeffaf zeminli PNG üretir (kimlik.html indirme bağlantıları için).
// Kullanım: node tools/make_logo_png.js   (gereksinim: npm i -g playwright && npx playwright install chromium)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");
const IMG = path.join(__dirname, "..", "img");
// (dosya, hedef genişlik px, koyu önizleme zemini mi)
const JOBS = [
  ["logo", 2400], ["logo-en", 2400], ["logo-white", 2400], ["logo-mono", 2400],
  ["logo-stacked", 2000], ["logo-stacked-white", 2000],
  ["logo-mark", 1024], ["logo-mark-solid", 1024], ["logo-mark-white", 1024],
  ["sunum-kapak", 1920], ["poster-bant", 2400],
];
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [name, width] of JOBS) {
    const svg = fs.readFileSync(path.join(IMG, name + ".svg"), "utf8");
    const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
    const w = parseFloat(m[1]), h = parseFloat(m[2]);
    const scale = width / w, height = Math.round(h * scale);
    await page.setViewportSize({ width, height });
    await page.setContent(`<html><body style="margin:0;background:transparent">${svg.replace(/width="[\d.]+" height="[\d.]+"/, `width="${width}" height="${height}"`)}</body></html>`);
    await page.screenshot({ path: path.join(IMG, name + ".png"), omitBackground: true, clip: { x: 0, y: 0, width, height } });
    console.log(name + ".png", width + "x" + height);
  }
  await browser.close();
})();
