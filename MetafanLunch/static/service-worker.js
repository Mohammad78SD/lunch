// self.addEventListener('push', function (event) {
//   const data = event.data.json();
//   const options = {
//     body: data.description,
//     icon: '/static/images/metafan-logo.webp'
//   };
//   event.waitUntil(
//     self.registration.showNotification(data.title, options)
//   );
// });

var staticCacheName = 'MetafanPanel-v1';

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function (cache) {
      return cache.addAll([
        '',
      ]);
    })
  );
});

self.addEventListener('fetch', function (event) {
  var requestUrl = new URL(event.request.url);
  if (requestUrl.origin === location.origin) {
    if ((requestUrl.pathname === '/')) {
      event.respondWith(caches.match(''));
      return;
    }
  }
  event.respondWith(
    caches.match(event.request).then(function (response) {
      return response || fetch(event.request);
    })
  );
});