// SafeFarm Myanmar - Service Worker
const CACHE_NAME = 'safefarm-v1';
const STREAMLIT_URL = 'http://localhost:8501';

// Static assets to cache
const STATIC_ASSETS = [
  './',
  './index.html',
  './offline.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing SafeFarm service worker...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - handle requests
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle Streamlit server requests
  if (url.hostname === 'localhost' && url.port === '8501') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // If server is available, clone and cache the response
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          // Server is offline - try to serve from cache or show offline page
          return caches.match(request).then((cachedResponse) => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // Return offline page for navigation requests
            if (request.mode === 'navigate') {
              return caches.match('./offline.html');
            }
            return new Response('Offline', { status: 503 });
        })
        })
    );
    return;
  }

  // Handle static assets (PWA files)
  event.respondWith(
    caches.match(request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(request).then((response) => {
          // Cache new static assets
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, responseClone);
            });
          }
          return response;
        });
      })
      .catch(() => {
        // Return offline page for navigation requests
        if (request.mode === 'navigate') {
          return caches.match('./offline.html');
        }
        return new Response('Offline', { status: 503 });
      })
  );
});

// Check if Streamlit server is available
self.addEventListener('message', (event) => {
  if (event.data === 'check-server') {
    fetch(STREAMLIT_URL, { mode: 'no-cors' })
      .then(() => {
        event.source.postMessage({ serverStatus: 'online' });
      })
      .catch(() => {
        event.source.postMessage({ serverStatus: 'offline' });
      });
  }
});
