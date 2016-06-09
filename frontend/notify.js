export function request_notify_permission() {
    Notification.requestPermission();
}

export function notify(title, body) {
    if(!("Notification" in window)) {
        return;
    }
    
    var options = {
        body: body,
        icon: '/static/favicon/apple-touch-icon-precomposed.png'
    };

    var n = new Notification(title, options);
    setTimeout(n.close.bind(n), 10000);
}
