import pako from 'pako';
import store from './vuex/store';
import { serverMessages } from './vuex/actions';

export default function configWebsocket() {
    var sock = new WebSocket('ws://' + window.location.host + '/api/socket');
    sock.binaryType = 'arraybuffer';

    sock.onopen = function() {
    };

    sock.onmessage = function(e) {
        var data = pako.inflate(e.data, {to: 'string'});
        var msg = JSON.parse(data);

        console.log(msg);

        var handler = serverMessages[msg.method];

        if(!handler) {
            console.log("unhandled message: ", msg.method);
        } else {
            handler(store, msg.data);
        }
    };

    sock.onclose = function() {
        jQuery("#qi-disconnected").modal("show");
    };
}
