import io from 'socket.io-client';
import store from './vuex/store';
import { server_messages } from './vuex/actions';

export default function configWebsocket() {
    var socket = io('http://' + document.domain + ':' + location.port, {
        reconnection: false
    });

    socket.on('connect', function() {
    });

    socket.on('disconnect', function() {
        jQuery("#qi-disconnected").modal("show");
    });

    Object.keys(server_messages).forEach(function(key) {
        socket.on(key, function(data) {
            if(key != 'pong') {
                console.log(key);
                console.log(data);
            }
            server_messages[key](store, data);
        });
    });
}
