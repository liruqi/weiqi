import * as socket from '../socket';

function make_action(type) {
    return ({dispatch}, ...args) => dispatch(type, ...args);
}

export const server_messages = {
    'connection_data': make_action('MSG_CONNECTION_DATA'),
    'pong': make_action('MSG_PONG'),
    'room_message': make_action('MSG_ROOM_MESSAGE'),
    'room_logs': make_action('MSG_ROOM_LOGS'),
    'room_user': make_action('MSG_ROOM_USER'),
    'room_user_left': make_action('MSG_ROOM_USER_LEFT'),
    'automatch_status': make_action('MSG_AUTOMATCH_STATUS'),
    'game_started': make_action('MSG_GAME_STARTED'),
    'game_finished': make_action('MSG_GAME_FINISHED'),
    'game_data': make_action('MSG_GAME_DATA'),
    'game_update': make_action('MSG_GAME_UPDATE'),
    'game_info': make_action('MSG_GAME_INFO'),
    'user_status': make_action('MSG_USER_STATUS'),
    'load_direct_room': make_action('MSG_LOAD_DIRECT_ROOM'),
    'demo_current_node_id': make_action('MSG_DEMO_CURRENT_NODE_ID'),
    'challenges': make_action('MSG_CHALLENGES')
};

server_messages.direct_message = function({dispatch, state}, data) {
    if(data.user_id == state.auth.user.user_id || state.direct_rooms[data.user_id]) {
        dispatch('MSG_ROOM_MESSAGE', data);
    } else {
        socket.send('rooms/open_direct', {'user_id': data.user_id}, function(data) {
            dispatch('MSG_LOAD_DIRECT_ROOM', data);
        });
    }
};

export const update_route = make_action('UPDATE_ROUTE');
export const toggle_sidebar = make_action('TOGGLE_SIDEBAR');
export const update_game_time = make_action('UPDATE_GAME_TIME');
export const clear_game_update = make_action('CLEAR_GAME_UPDATE');

export function open_game({dispatch, state}, game_id) {
    var game = state.open_games[game_id];

    if(game && game.board) {
        return;
    }

    socket.send('games/open_game', {'game_id': game_id});
}

export function close_game({dispatch, state}, game_id) {
    socket.send('games/close_game', {'game_id': game_id});
    dispatch('CLOSE_GAME', game_id);
}

export function load_room_users({dispatch, state}, room_id) {
    if(!room_id || !!state.room_users[room_id]) {
        return;
    }

    socket.send('rooms/users', {'room_id': room_id}, function(data) {
        dispatch('ROOM_USERS', room_id, data.users);
    });
}

export function load_direct_room({dispatch, state}, user_id) {
    socket.send('rooms/open_direct', {'user_id': user_id}, function(data) {
        dispatch('MSG_LOAD_DIRECT_ROOM', data);
    });
}

export function close_direct_room({dispatch, state}, user_id) {
    socket.send('rooms/close_direct', {'user_id': user_id});
    dispatch('CLOSE_DIRECT_ROOM', user_id);
}

export function clear_room_update({dispatch, state}, room_id) {
    var is_direct = Object.keys(state.direct_rooms).find(function(user_id) {
        return state.direct_rooms[user_id].room_id == room_id;
    });

    if(is_direct) {
        socket.send('rooms/mark_read', {'room_id': room_id});
    }
    
    dispatch('CLEAR_ROOM_UPDATE', room_id);
}

export function create_demo({dispatch, state}, game_id) {
    socket.send('play/create_demo_from_game', {'game_id': game_id}, function(demo_id) {
        state.route.router.go({name: 'game', params: {game_id: demo_id}});
    });
}