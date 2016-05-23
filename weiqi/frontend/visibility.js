var state_key, event_key, keys = {
    hidden: "visibilitychange",
    webkitHidden: "webkitvisibilitychange",
    mozHidden: "mozvisibilitychange",
    msHidden: "msvisibilitychange"
};

for (state_key in keys) {
    if (state_key in document) {
        event_key = keys[state_key];
        break;
    }
}

export function add_visibility_event_listener(cb) {
    document.addEventListener(event_key, cb);
}

export function remove_visibility_event_listener(cb) {
    document.removeEventListener(event_key, cb);
}

export function is_tab_visible() {
    return !document[state_key];
}
