self.addEventListener('push', function(event) {
    const data = event.data.json();
    self.registration.showNotification(data.title, {
        body: data.body,
        icon: '/static/icons/notification-icon.png', // Optional icon
        badge: '/static/icons/badge.png', // Optional badge
        data: { url: data.url } // Optional URL to open
    });
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    if (event.notification.data.url) {
        clients.openWindow(event.notification.data.url);
    }
});
