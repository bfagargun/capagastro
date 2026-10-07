/* Site geçici olarak kapalı. Siteyi daha önce açmış tarayıcılarda kalan çevrimdışı kopyayı
   siler ve bu hizmet çalışanını kaldırır. Site yeniden açılınca asıl sw.js geri gelir. */
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.registration.unregister())
  );
});
