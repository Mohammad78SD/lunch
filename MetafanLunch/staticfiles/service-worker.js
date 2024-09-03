self.addEventListener('push', function(event) {
    const data = event.data.json();
    const options = {
        body: data.description,
        icon: '/static/images/metafan-logo.webp'
    };
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});