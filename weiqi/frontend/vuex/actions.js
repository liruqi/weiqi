export const server_messages = {
    'connection_data': make_action('MSG_CONNECTION_DATA'),
    'pong': make_action('MSG_PONG'),
    'room_message': make_action('MSG_ROOM_MESSAGE'),
    'room_user': make_action('MSG_ROOM_USER'),
    'room_user_left': make_action('MSG_ROOM_USER_LEFT'),
    'automatch_status': make_action('MSG_AUTOMATCH_STATUS'),
    'game_started': make_action('MSG_GAME_STARTED'),
    'game_finished': make_action('MSG_GAME_FINISHED'),
    'game_data': make_action('MSG_GAME_DATA'),
    'game_update': make_action('MSG_GAME_UPDATE'),
    'load_direct_room': make_action('MSG_LOAD_DIRECT_ROOM'),
    'direct_message': make_action('MSG_DIRECT_MESSAGE'),
    'rating_update': make_action('MSG_RATING_UPDATE'),
};

export const update_route = make_action('UPDATE_ROUTE');
export const toggle_sidebar = make_action('TOGGLE_SIDEBAR');
export const update_game_time = make_action('UPDATE_GAME_TIME');
export const open_game = make_action('OPEN_GAME');
export const close_game = make_action('CLOSE_GAME');
export const load_room_users = make_action('LOAD_ROOM_USERS');
export const reload_user_avatar = make_action('RELOAD_USER_AVATAR');
export const load_direct_room = make_action('LOAD_DIRECT_ROOM');
export const clear_room_update = make_action('CLEAR_ROOM_UPDATE');
export const clear_game_update = make_action('CLEAR_GAME_UPDATE');

function make_action(type) {
    return ({dispatch}, ...args) => dispatch(type, ...args);
}