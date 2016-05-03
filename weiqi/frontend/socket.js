import pako from 'pako';
import store from './vuex/store';
import { server_messages } from './vuex/actions';

var socket;

export default function configWebsocket() {
    socket = new WebSocket('ws://' + window.location.host + '/api/socket');
    socket.binaryType = 'arraybuffer';

    socket.onopen = function() {
    };

    socket.onmessage = function(e) {
        var data = pako.inflate(e.data, {to: 'string'});
        var msg = JSON.parse(data);

        console.log(msg);

        var handler = server_messages[msg.method];

        if(!handler) {
            console.log("unhandled message: ", msg.method);
        } else {
            handler(store, msg.data);
        }
    };

    socket.onclose = function() {
        jQuery("#qi-disconnected").modal("show");
    };
}

export function send(topic, data) {
    var msg = JSON.stringify({'topic': topic, 'data': data});
    msg = pako.deflate(msg);
    socket.send(msg);
}

export function request(topic, data) {
}
