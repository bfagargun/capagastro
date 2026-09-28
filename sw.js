/* Çapa Gastroenterohepatoloji: çevrimdışı destek.
   Gezinmelerde ağ öncelikli (sayfa güncelse hemen görünür), ağ yoksa önbellek, o da yoksa cevrimdisi.html.
   Aynı kaynaktan diğer dosyalarda önce önbellek, arkada yenileme. Başka kaynaklar (yazı tipleri, OpenAlex) dokunulmaz.
   Sayfa içerikleri değiştiğinde VERSION değiştirmek gerekmez; eski önbellekleri temizlemek için değiştirin. */
const VERSION = "2026-09-28a";
const CACHE = "capagastro-" + VERSION;
const PRECACHE = ["./", "./index.html", "./hazirlik.html", "./islemler.html", "./hatirlatici.html", "./izlem.html", "./cevrimdisi.html", "./pubs.js", "./img/icon-192.png", "./manifest.webmanifest"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("capagastro-") && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (req.mode === "navigate") {
    e.respondWith(fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || caches.match("./cevrimdisi.html"))));
    return;
  }
  e.respondWith(caches.match(req).then(cached => {
    const net = fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    }).catch(() => cached);
    return cached || net;
  }));
});
