export function request_notify_permission() {
    Notification.requestPermission();
}

export function notify(message) {
    if(!("Notification" in window)) {
        return;
    }
    
    var options = {
        body: message,
        icon: '/static/favicon/apple-touch-icon-precomposed.png'
    };

    var n = new Notification('weiqi.gs', options);
    setTimeout(n.close.bind(n), 10000);
}
