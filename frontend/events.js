import Vue from 'vue';

var bus = new Vue();

export function add_event_listener(event, cb) {
    bus.$on(event, cb);
}

export function remove_event_listener(event, cb) {
    bus.$off(event, cb);
}

export function publish_event(event, data) {
    bus.$emit(event, data);
}