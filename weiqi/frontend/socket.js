import store from './vuex/store';
import { server_messages } from './vuex/actions';

var socket;
var message_counter = 0;
var request_handler = {};

export default function configWebsocket() {
    socket = new WebSocket('ws://' + window.location.host + '/api/socket');

    socket.onopen = function() {
    };

    socket.onmessage = function(e) {
        var data = e.data;
        var msg = JSON.parse(data);
        var handler;

        console.log(msg);

        if(msg.method == 'response') {
            handler = request_handler[msg.id];
            if(handler) {
                handler(msg.data);
                delete request_handler[msg.id];
            } else {
                console.log('got response for unknown id: ', msg.id);
            }
        } else {
            handler = server_messages[msg.method];

            if (!handler) {
                console.log("unhandled message: ", msg.method);
            } else {
                handler(store, msg.data);
            }
        }
    };

    socket.onclose = function() {
        jQuery("#qi-disconnected").modal("show");
    };
}

export function send(method, data, success) {
    message_counter += 1;
    var msg = {'method': method, 'data': data};

    if(success) {
        msg.id = message_counter;
        request_handler[msg.id] = success;
    }

    msg = JSON.stringify(msg);
    socket.send(msg);
}
