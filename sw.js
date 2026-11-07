/* 经期状态助手 Service Worker：导航请求网络优先（保证更新），其余缓存优先（保证离线可用） */
const CACHE = "cycle-v1";
const SHELL = ["./", "index.html", "manifest.webmanifest", "apple-touch-icon.png", "icon-192.png", "icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(self.clients.claim());
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  if (e.request.mode === "navigate") {
    e.respondWith(
      fetch(e.request).then(r => {
        const copy = r.clone();
        caches.open(CACHE).then(k => k.put(e.request, copy)).catch(() => {});
        return r;
      }).catch(() => caches.match(e.request).then(h => h || caches.match("./")))
    );
  } else {
    e.respondWith(
      caches.match(e.request).then(hit => hit || fetch(e.request).then(r => {
        const copy = r.clone();
        caches.open(CACHE).then(k => k.put(e.request, copy)).catch(() => {});
        return r;
      }))
    );
  }
});
